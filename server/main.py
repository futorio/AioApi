import asyncio

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
            'coerce': int,
            'required': True,
        },
        'lost_arg': {
            'type': 'float',
            'coerce': float,
            'required': False,
        },
    }
    validator = Validator(args_schema)
    if not validator.validate(dict(request.query)):
        raise HTTPUnprocessableEntity(text=str(validator.errors))

    bar_count: int = validator.document.get('bar_count')
    sleep_time: float = validator.document.get('lost_arg')

    await asyncio.sleep(sleep_time)
    return Response(text='bar'*bar_count)


app = web.Application()
app.add_routes([web.get('/', hello_handler)])
web.run_app(app)
