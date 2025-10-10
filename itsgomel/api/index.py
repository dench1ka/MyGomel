# api/index.py
from itsgomel.wsgi import application

def handler(event, context):
    from mangum import Mangum  # если используешь ASGI
    asgi_handler = Mangum(application)
    return asgi_handler(event, context)
