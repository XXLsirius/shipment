- django server

Set environment variable
	REDIS_OM_URL
	redis://@192.168.140.211:6379
unzip shipment-django.zip
Extract to shipment-django folder.
cd shipment-django
python -m venv .venv
Open command prompt in main folder.
.venv\Scripts\activate.bat
python manage.py runserver
- front-end
npm run dev
Finally connect to the site on port 8000.