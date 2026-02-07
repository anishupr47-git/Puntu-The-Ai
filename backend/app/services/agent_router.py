import re
from typing import Any, Optional
from sqlalchemy.orm import Session
from .ollama import OllamaClient
from .recommenders import recommend_songs, recommend_movies
from .football import predict_match, available_teams


ollama = OllamaClient()

SKILLS = {
    'general_chat',
    'decision_helper',
    'study_planner',
    'hygiene_routine',
    'meal_planner',
    'sleep_schedule',
    'fitness_plan',
    'song_recommender',
    'song_writer',
    'movie_suggester',
    'football_predictor',
}

KEYWORDS = {
    'decision_helper': ['decide', 'decision', 'option', 'options', 'choice', 'vs', 'versus'],
    'study_planner': ['study', 'exam', 'revision', 'learn'],
    'hygiene_routine': ['hygiene', 'skincare', 'shower', 'routine'],
    'meal_planner': ['meal', 'food', 'diet', 'nutrition', 'lunch', 'dinner'],
    'sleep_schedule': ['sleep', 'bedtime', 'wake'],
    'fitness_plan': ['fitness', 'workout', 'gym', 'training', 'run'],
    'song_recommender': ['song', 'music', 'playlist'],
    'song_writer': ['lyrics', 'songwriter', 'verse', 'chorus'],
    'movie_suggester': ['movie', 'film', 'cinema'],
    'football_predictor': ['football', 'soccer', 'match', 'score'],
}


def route_skill(message: Optional[str], explicit_skill: Optional[str], mode: Optional[str]) -> str:
    if explicit_skill in SKILLS:
        return explicit_skill

    if mode:
        mode = mode.lower()
        if mode == 'decide':
            return 'decision_helper'
        if mode == 'plan':
            if message:
                msg = message.lower()
                if 'sleep' in msg:
                    return 'sleep_schedule'
                if 'meal' in msg or 'food' in msg:
                    return 'meal_planner'
                if 'fitness' in msg or 'workout' in msg:
                    return 'fitness_plan'
            return 'study_planner'
        if mode == 'create':
            return 'song_writer'
        if mode == 'ask':
            return 'general_chat'

    text = (message or '').lower()
    for skill, words in KEYWORDS.items():
        if any(w in text for w in words):
            return skill

    return 'general_chat'


def _extract_options(message: str) -> list[str]:
    for sep in [' vs ', ' versus ', ' or ']:
        if sep in message.lower():
            parts = [p.strip() for p in re.split(sep, message, flags=re.IGNORECASE) if p.strip()]
            if len(parts) >= 2:
                return parts[:3]
    return []


def _extract_time(message: str) -> Optional[str]:
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', message, re.IGNORECASE)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    meridiem = match.group(3).lower()
    if meridiem == 'pm' and hour != 12:
        hour += 12
    if meridiem == 'am' and hour == 12:
        hour = 0
    return f'{hour:02d}:{minute:02d}'


def _format_minutes(total_minutes: int) -> str:
    hours = (total_minutes // 60) % 24
    minutes = total_minutes % 60
    return f'{hours:02d}:{minutes:02d}'


async def handle_skill(
    skill: str,
    message: str,
    context: Optional[dict[str, Any]] = None,
    db: Optional[Session] = None,
) -> Any:
    context = context or {}

    if skill == 'decision_helper':
        options = _extract_options(message)
        if not options:
            return {
                'clarifying_questions': [
                    'What options are you choosing between?',
                    'Which criteria matter most (cost, time, impact, enjoyment)?',
                    'Are there any hard constraints or deadlines?'
                ],
                'recommendation': None,
                'plan': []
            }
        choice = options[0]
        return {
            'clarifying_questions': [],
            'recommendation': {
                'choice': choice,
                'why': [
                    'It aligns with the most common constraints (time and effort).',
                    'It keeps optionality for follow-up decisions.'
                ],
                'tradeoffs': [
                    f'You may delay exploring {options[1]} if priorities shift.'
                ]
            },
            'plan': [
                'Confirm the top two criteria you care about.',
                f'Run a 30-minute test or preview for {choice}.',
                'Commit to the option that feels best after the trial.'
            ]
        }

    if skill == 'study_planner':
        return {
            'goal': 'Build a balanced study rhythm with focus blocks and recovery.',
            'schedule': [
                {'day': 'Mon', 'focus': 'Deep work block', 'duration_min': 90},
                {'day': 'Tue', 'focus': 'Practice problems', 'duration_min': 75},
                {'day': 'Wed', 'focus': 'Recall + flashcards', 'duration_min': 60},
                {'day': 'Thu', 'focus': 'Mixed review', 'duration_min': 75},
                {'day': 'Fri', 'focus': 'Mock session', 'duration_min': 90},
            ],
            'tips': [
                'Finish each session with a 5-minute recap note.',
                'Rotate topics to avoid fatigue.'
            ]
        }

    if skill == 'hygiene_routine':
        return {
            'morning': ['Hydrate', 'Gentle cleanse', 'Moisturize', 'SPF'],
            'night': ['Cleanse', 'Exfoliate 2x/week', 'Hydrating serum', 'Moisturizer'],
            'notes': 'Keep routines simple and consistent for two weeks before changing products.'
        }

    if skill == 'meal_planner':
        return {
            'breakfast': 'Greek yogurt, berries, and oats',
            'lunch': 'Grilled chicken quinoa bowl with greens',
            'dinner': 'Salmon, roasted vegetables, and sweet potato',
            'snacks': ['Nuts', 'Fruit', 'Hummus + carrots'],
        }

    if skill == 'sleep_schedule':
        wake_time = _extract_time(message) or '07:00'
        hours, minutes = map(int, wake_time.split(':'))
        wake_minutes = hours * 60 + minutes
        bedtime_minutes = (wake_minutes - 8 * 60) % (24 * 60)
        return {
            'target_wake_time': wake_time,
            'target_bed_time': _format_minutes(bedtime_minutes),
            'wind_down': ['Dim lights 60 minutes before bed', 'No caffeine after 2pm', 'Short journal to clear thoughts'],
            'consistency': 'Keep the same schedule within 45 minutes even on weekends.'
        }

    if skill == 'fitness_plan':
        return {
            'plan': [
                {'day': 'Day 1', 'focus': 'Full body strength', 'notes': 'Squat, push, pull, core'},
                {'day': 'Day 2', 'focus': 'Zone 2 cardio', 'notes': '30-40 minutes steady pace'},
                {'day': 'Day 3', 'focus': 'Mobility + accessories', 'notes': 'Hips, shoulders, back'}
            ],
            'recovery': ['8k steps daily', 'Protein with each meal', 'Sleep 7-8 hours']
        }

    if skill == 'song_recommender':
        if db is None:
            raise ValueError('Database session required for song recommendations.')
        return recommend_songs(db, message)

    if skill == 'movie_suggester':
        if db is None:
            raise ValueError('Database session required for movie suggestions.')
        return recommend_movies(db, message)

    if skill == 'football_predictor':
        if db is None:
            raise ValueError('Database session required for football predictions.')
        text = message.lower()
        teams = available_teams(db)
        found = []
        for team in teams:
            idx = text.find(team.lower())
            if idx != -1:
                found.append((idx, team))
        if len(found) >= 2:
            found.sort(key=lambda item: item[0])
            return predict_match(db, found[0][1], found[1][1])
        return {
            'guardrail': 'Please provide a home and away team.',
            'available_teams': teams
        }

    if skill == 'song_writer':
        system = 'You are a songwriter. Write concise lyrics with a verse, pre-chorus, and chorus. Keep it original and emotive.'
        return await ollama.generate(prompt=message, system=system, temperature=0.8)

    if skill == 'general_chat':
        system = 'You are PUNTU, a playful, confident AI assistant. Be concise, helpful, and upbeat.'
        return await ollama.generate(prompt=message, system=system, temperature=0.6)

    return await ollama.generate(prompt=message, system='You are a helpful assistant.', temperature=0.6)
