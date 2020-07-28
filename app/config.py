import boto3

db = boto3.resource('dynamodb')

DEBUG = True

SECRET_KEY = 'aqwrgsrtkj65476riqw34tare'

from datetime import timedelta

REMEMBER_COOKIE_DURATION = timedelta(days=30)

