vytvorenie vyrtualneho prostredia: 
 - python -m venv .venv
aktivovanie vyrtualneho prostredia:
 - windows: .\.venv\bin\activate
 - macos: source .venv/bin/activate
 - linux: source .venv/bin/activate

nainstalovat potrebne kniznice:
 - pip install -r requirements.txt

spustit server:
 - gunicorn -w 4 -t 100 app:app
