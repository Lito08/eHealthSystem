Follow this command:
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate

To create superadmin for initial database setup:
python manage.py createsuperuser

To run the server:
python manage.py runserver

To handle static files:
python manage.py collectstatic --noinput
