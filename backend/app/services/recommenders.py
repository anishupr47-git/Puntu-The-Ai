from typing import Any
from sqlalchemy.orm import Session
from ..models import Song, Movie


def list_songs(db: Session) -> list[Song]:
    return db.query(Song).order_by(Song.id.asc()).all()


def list_movies(db: Session) -> list[Movie]:
    return db.query(Movie).order_by(Movie.id.asc()).all()


def _song_to_dict(song: Song) -> dict[str, Any]:
    return {
        'id': song.code,
        'title': song.title,
        'artist': song.artist,
        'mood': song.mood,
        'energy': song.energy,
        'genre': song.genre,
        'era': song.era,
        'tags': song.tags,
    }


def _movie_to_dict(movie: Movie) -> dict[str, Any]:
    return {
        'id': movie.code,
        'title': movie.title,
        'year': movie.year,
        'mood': movie.mood,
        'energy': movie.energy,
        'genre': movie.genre,
        'era': movie.era,
        'tags': movie.tags,
        'synopsis': movie.synopsis,
    }


def _score_item(item: dict[str, Any], prefs: dict[str, str]) -> int:
    score = 0
    for key in ['mood', 'energy', 'genre', 'era']:
        if prefs.get(key) and item.get(key) == prefs[key]:
            score += 2
    if prefs.get('tag'):
        if prefs['tag'] in item.get('tags', []):
            score += 1
    return score


def _extract_prefs(message: str) -> dict[str, str]:
    text = message.lower()
    moods = ['calm', 'focused', 'uplifted', 'energized', 'romantic', 'moody', 'dreamy', 'melancholy', 'happy', 'reflective', 'intense', 'tense']
    energy = ['low', 'medium', 'high']
    genres = ['synthwave', 'ambient', 'indie', 'chillhop', 'electronic', 'soul', 'pop', 'folk', 'lofi', 'house', 'postrock', 'altpop', 'rnb', 'piano', 'electronica', 'rock', 'drama', 'thriller', 'fantasy', 'sci-fi', 'crime', 'comedy', 'action', 'adventure', 'mystery', 'romance']
    eras = ['2000s', '2010s', '2020s']

    prefs: dict[str, str] = {}
    for mood in moods:
        if mood in text:
            prefs['mood'] = mood
            break
    for e in energy:
        if f'{e} energy' in text or f'{e}-energy' in text:
            prefs['energy'] = e
            break
    for g in genres:
        if g in text:
            prefs['genre'] = g
            break
    for era in eras:
        if era in text:
            prefs['era'] = era
            break
    for tag in [
        'night','neon','coastal','heist','memory','drive','cinematic','cozy','noir','study','rain','sunrise','late',
        'focus','pulse','soft','city','forest','ocean','desert','mountain','vintage','future','analog','glow','storm',
        'amber','silver','midnight','dawn','horizon','static','signal','bloom','quiet','run','spark','shadow','breeze',
        'echo','drift','road','bridge','harbor','glass','sky','roadtrip','isolation','family','community','river',
        'gallery','racing','travel','dream','mystery','survival','rebirth','time','letters','fog','underground','chase',
        'secret','lighthouse'
    ]:
        if tag in text:
            prefs['tag'] = tag
            break
    return prefs


def recommend_songs(db: Session, message: str, limit: int = 5) -> list[dict[str, Any]]:
    prefs = _extract_prefs(message)
    songs = list_songs(db)
    scored = sorted(songs, key=lambda item: _score_item(_song_to_dict(item), prefs), reverse=True)
    return [_song_to_dict(song) for song in scored[:limit]]


def recommend_movies(db: Session, message: str, limit: int = 5) -> list[dict[str, Any]]:
    prefs = _extract_prefs(message)
    movies = list_movies(db)
    scored = sorted(movies, key=lambda item: _score_item(_movie_to_dict(item), prefs), reverse=True)
    return [_movie_to_dict(movie) for movie in scored[:limit]]
