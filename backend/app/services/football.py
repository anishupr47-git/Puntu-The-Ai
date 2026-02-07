import math
from typing import Any
from collections import defaultdict
from sqlalchemy.orm import Session
from ..models import Club, NationalTeam, FootballMatch


def _load_matches(db: Session) -> list[dict[str, Any]]:
    rows = db.query(FootballMatch).all()
    return [
        {
            'season': row.season,
            'league': row.league,
            'date': row.date.isoformat(),
            'home_team': row.home_team,
            'away_team': row.away_team,
            'home_goals': row.home_goals,
            'away_goals': row.away_goals,
        }
        for row in rows
    ]


def list_clubs(db: Session) -> list[dict[str, Any]]:
    rows = db.query(Club).all()
    grouped = defaultdict(lambda: {'league': None, 'country': None, 'season': None, 'teams': []})
    for row in rows:
        key = (row.league, row.country, row.season)
        entry = grouped[key]
        entry['league'] = row.league
        entry['country'] = row.country
        entry['season'] = row.season
        entry['teams'].append(row.team)
    return [
        {
            'league': entry['league'],
            'country': entry['country'],
            'season': entry['season'],
            'teams': sorted(entry['teams']),
        }
        for entry in grouped.values()
    ]


def list_national_teams(db: Session) -> list[dict[str, Any]]:
    rows = db.query(NationalTeam).all()
    grouped = defaultdict(list)
    for row in rows:
        grouped[row.confederation].append(row.team)
    return [
        {'confederation': confed, 'teams': sorted(teams)}
        for confed, teams in grouped.items()
    ]


def all_club_teams(db: Session) -> list[str]:
    rows = db.query(Club.team).all()
    return sorted({row[0] for row in rows})


def all_national_teams(db: Session) -> list[str]:
    rows = db.query(NationalTeam.team).all()
    return sorted({row[0] for row in rows})


def _poisson(k: int, lam: float) -> float:
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)


def available_teams(db: Session) -> list[str]:
    teams = set()
    club_rows = db.query(Club.team).all()
    national_rows = db.query(NationalTeam.team).all()
    teams.update({row[0] for row in club_rows})
    teams.update({row[0] for row in national_rows})
    matches = _load_matches(db)
    for m in matches:
        teams.add(m['home_team'])
        teams.add(m['away_team'])
    return sorted(teams)


def predict_match(db: Session, home_team: str, away_team: str) -> dict[str, Any]:
    matches = _load_matches(db)
    if len(matches) < 10:
        return {
            'guardrail': 'Dataset is too small for stable predictions.',
            'available_teams': available_teams(db),
        }

    teams = available_teams(db)

    home_goals = [int(m['home_goals']) for m in matches]
    away_goals = [int(m['away_goals']) for m in matches]
    league_home_avg = sum(home_goals) / len(home_goals)
    league_away_avg = sum(away_goals) / len(away_goals)

    stats: dict[str, dict[str, float]] = {t: {'home_scored': 0, 'home_conceded': 0, 'away_scored': 0, 'away_conceded': 0, 'home_matches': 0, 'away_matches': 0} for t in teams}

    for m in matches:
        h = m['home_team']
        a = m['away_team']
        hg = int(m['home_goals'])
        ag = int(m['away_goals'])
        stats[h]['home_scored'] += hg
        stats[h]['home_conceded'] += ag
        stats[h]['home_matches'] += 1
        stats[a]['away_scored'] += ag
        stats[a]['away_conceded'] += hg
        stats[a]['away_matches'] += 1

    def _avg(team: str, key: str, match_key: str) -> float:
        matches_count = stats[team][match_key]
        return stats[team][key] / matches_count if matches_count else 0.0

    guardrails = []
    if home_team not in teams or away_team not in teams:
        guardrails.append('No historical team data found. Using league-average priors.')

    home_attack = (_avg(home_team, 'home_scored', 'home_matches') / league_home_avg) if home_team in teams else 1.0
    home_defense = (_avg(home_team, 'home_conceded', 'home_matches') / league_away_avg) if home_team in teams else 1.0
    away_attack = (_avg(away_team, 'away_scored', 'away_matches') / league_away_avg) if away_team in teams else 1.0
    away_defense = (_avg(away_team, 'away_conceded', 'away_matches') / league_home_avg) if away_team in teams else 1.0

    home_xg = league_home_avg * home_attack * away_defense
    away_xg = league_away_avg * away_attack * home_defense

    scorelines = []
    max_goals = 5
    win = draw = lose = 0.0
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = _poisson(h, home_xg) * _poisson(a, away_xg)
            scorelines.append({'score': f'{h}-{a}', 'probability': p})
            if h > a:
                win += p
            elif h == a:
                draw += p
            else:
                lose += p

    top_scores = sorted(scorelines, key=lambda x: x['probability'], reverse=True)[:5]
    return {
        'home_team': home_team,
        'away_team': away_team,
        'home_xg': round(home_xg, 2),
        'away_xg': round(away_xg, 2),
        'outcome_probabilities': {
            'home_win': round(win, 3),
            'draw': round(draw, 3),
            'away_win': round(lose, 3),
        },
        'top_scorelines': [
            {'score': s['score'], 'probability': round(s['probability'], 3)} for s in top_scores
        ],
        'guardrails': 'Poisson baseline. Use as directional guidance only.' + (
            f" {' '.join(guardrails)}" if guardrails else ''
        )
    }
