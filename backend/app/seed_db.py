import csv
import json
import os
from datetime import datetime
from pathlib import Path
from .core.database import SessionLocal
from .models import Song, Movie, Club, NationalTeam, FootballMatch


DATA_DIR = Path(__file__).resolve().parents[0] / 'data'


def seed_songs(db):
    if db.query(Song).count() > 0 and os.getenv('SEED_FORCE') != '1':
        return
    if os.getenv('SEED_FORCE') == '1':
        db.query(Song).delete()
    with open(DATA_DIR / 'songs.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)
    objects = [
        Song(
            code=item['id'],
            title=item['title'],
            artist=item['artist'],
            mood=item['mood'],
            energy=item['energy'],
            genre=item['genre'],
            era=item['era'],
            tags=item['tags'],
        )
        for item in songs
    ]
    db.bulk_save_objects(objects)
    db.commit()


def seed_movies(db):
    if db.query(Movie).count() > 0 and os.getenv('SEED_FORCE') != '1':
        return
    if os.getenv('SEED_FORCE') == '1':
        db.query(Movie).delete()
    with open(DATA_DIR / 'movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)
    objects = [
        Movie(
            code=item['id'],
            title=item['title'],
            year=item['year'],
            mood=item['mood'],
            energy=item['energy'],
            genre=item['genre'],
            era=item['era'],
            tags=item['tags'],
            synopsis=item['synopsis'],
        )
        for item in movies
    ]
    db.bulk_save_objects(objects)
    db.commit()


def seed_clubs(db):
    if db.query(Club).count() > 0 and os.getenv('SEED_FORCE') != '1':
        return
    if os.getenv('SEED_FORCE') == '1':
        db.query(Club).delete()
    with open(DATA_DIR / 'clubs.json', 'r', encoding='utf-8') as f:
        leagues = json.load(f)
    objects = []
    for league in leagues:
        for team in league['teams']:
            objects.append(
                Club(
                    league=league['league'],
                    country=league['country'],
                    season=league['season'],
                    team=team,
                )
            )
    db.bulk_save_objects(objects)
    db.commit()


def seed_national_teams(db):
    if db.query(NationalTeam).count() > 0 and os.getenv('SEED_FORCE') != '1':
        return
    if os.getenv('SEED_FORCE') == '1':
        db.query(NationalTeam).delete()
    with open(DATA_DIR / 'national_teams.json', 'r', encoding='utf-8') as f:
        confeds = json.load(f)
    objects = []
    for confed in confeds:
        for team in confed['teams']:
            objects.append(
                NationalTeam(
                    confederation=confed['confederation'],
                    team=team,
                )
            )
    db.bulk_save_objects(objects)
    db.commit()


def seed_matches(db):
    if db.query(FootballMatch).count() > 0 and os.getenv('SEED_FORCE') != '1':
        return
    if os.getenv('SEED_FORCE') == '1':
        db.query(FootballMatch).delete()
    with open(DATA_DIR / 'football.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        objects = []
        for row in reader:
            objects.append(
                FootballMatch(
                    season=row['season'],
                    league=row['league'],
                    date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                    home_team=row['home_team'],
                    away_team=row['away_team'],
                    home_goals=int(row['home_goals']),
                    away_goals=int(row['away_goals']),
                )
            )
    db.bulk_save_objects(objects)
    db.commit()


def seed_all():
    db = SessionLocal()
    try:
        seed_songs(db)
        seed_movies(db)
        seed_clubs(db)
        seed_national_teams(db)
        seed_matches(db)
    finally:
        db.close()


if __name__ == '__main__':
    seed_all()
