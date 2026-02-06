$env:PYTHONPATH = (Resolve-Path "..").Path
python -m app.seed_db
