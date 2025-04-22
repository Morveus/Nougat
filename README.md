⚠️ **WARNING: This project is currently a work in progress. Features may be incomplete or subject to change.** ⚠️
⚠️ I'm working in English but have some shitty habits of mixing fr/en ; i18n is not up to date at all ⚠️


# Game Collection Manager

A Django-based web application for managing your game collection.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see your game collection! 

Other commands:
```bash
# Compile translations
python manage.py compilemessages

# Generate translations
python manage.py makemessages -l fr  # For French
python manage.py makemessages -l en  # For English
```


