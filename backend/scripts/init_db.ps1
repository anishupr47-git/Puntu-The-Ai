$env:PYTHONPATH = (Resolve-Path "..").Path
python -m app.init_db
