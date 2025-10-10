from vercel_wsgi import handle
from itsgomel.wsgi import application

def handler(event, context):
    return handle(event, context, application)
