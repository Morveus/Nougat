⚠️ **WARNING: This project is currently a work in progress. Features may be incomplete or subject to change.** ⚠️

# ![favicon-32x32](https://github.com/user-attachments/assets/debe8331-52dd-4c74-bdff-aa69ba67db62) Nougat
A Django-based web application for managing your LAN Party games collection.

Deploy, add your games, have people filter by platform, max players...

![image](https://github.com/user-attachments/assets/7e05e1b6-f880-4dd0-862d-420d9fe63897)

I've intentionally added support for non-LAN games to for sharing titles that may be solo or retrogaming. You can filter by LAN/non-LAN :)

![image](https://github.com/user-attachments/assets/ff8a7b57-df05-4988-8d2a-67300589185b)


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

## Docker

1. Build the Docker image:
```bash
docker build -t gamecollection .
```

2. Run the Docker container:
```bash
docker run -d -p 8000:8000 gamecollection \
    -v $(pwd)/database:/app/database \
    -v $(pwd)/media:/app/media \
    -e CSRF_TRUSTED_ORIGINS=https://games.morve.us,http://games.morve.us \
    -e DJANGO_SUPERUSER_USERNAME=admin \
    -e DJANGO_SUPERUSER_EMAIL=admin@admin.com \
    -e DJANGO_SUPERUSER_PASSWORD=admin
```

3. Access the application at http://localhost:8000/


