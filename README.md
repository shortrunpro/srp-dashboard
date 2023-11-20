# srp-dashboard

*** Starting Django ***
* source ./venv/bin/activate - starts virtual environment
* python manage.py runserver - start django server
*** URL *** http://127.0.0.1:8000/ ***
*** Admin URL *** http://127.0.0.1:8000/admin ***
*** End Starting Django ***

*** Create App ***
* python manage.py startapp <appname>
* Go to djangoTest folder and add new app to settings.py
* Add model information in model.py along with url info and templates if needed
* python manage.py makemigrations <appname>
* python manage.py migrate <appname>
* Any changes to the model will require the make migrations calls 
*** End Create App ***


