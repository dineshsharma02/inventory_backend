import jwt 
from datetime import datetime,timedelta
from django.conf import settings


def get_access_token(payload,days):
    token = jwt.encode({"exp":datetime.now()+timedelta(days = days),**payload}),
    settings.secret_key