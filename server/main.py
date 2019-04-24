from aiohttp.web import (Request, Response,
                         HTTPForbidden, HTTPUnprocessableEntity)
from aiohttp import web
from aiohttp.web import middleware

from cerberus import Validator

routes = web.RouteTableDef()


@middleware
async def authentication(request: Request, handler) -> Response:
    if request.headers.get('auth') is None:
        raise HTTPForbidden()

    return await handler(request)


@routes.get('/')
async def hello_handler(request: Request) -> Response:
    args_schema: dict = {
        'bar_count': {
            'type': 'integer',
            'required': True,
        },
        'lost_arg': {
            'type': 'string',
            'required': False,
        },
    }
    validator = Validator()
    if not validator.validare(request.query, args_schema):
        raise HTTPUnprocessableEntity()

    return Response(text='bar')


app = web.Application(middlewares=[authentication])
app.add_routes([web.get('/', hello_handler)])
web.run_app(app)
