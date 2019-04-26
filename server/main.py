import traceback
import asyncio

from aiohttp.web import (Request, Response,
                         HTTPUnauthorized, HTTPUnprocessableEntity, )
from aiohttp import web
from aiohttp.web import middleware

from cerberus import Validator


@middleware
async def response_middleware(request: Request, handler) -> Response:
    message: dict = {'success': True, 'result': None, 'error': None}
    status_code = 200
    try:
        message['result'] = await handler(request)
    except Exception:
        traceback_message = traceback.format_exc()

        status_code = 500
        message['success'] = False
        message['error'] = traceback_message
    finally:
        return web.json_response(message, status=status_code)


@middleware
async def auth_middleware(request: Request, handler) -> str:
    if request.headers.get('auth') is None:
        raise HTTPUnauthorized()

    return await handler(request)


async def handler(request: Request) -> str:
    args_schema: dict = {
        'foo': {'type': 'integer', 'coerce': int, 'required': True, },
        'bar': {'type': 'float', 'coerce': float, 'required': False,
                'default': 0.0, },
    }
    validator = Validator(args_schema)
    if not validator.validate(dict(request.query)):
        raise HTTPUnprocessableEntity()

    await asyncio.sleep(1.0)
    return 'bar'


def main() -> None:
    app = web.Application(middlewares=[response_middleware, auth_middleware])
    app.add_routes([web.get('/', handler)])
    web.run_app(app)


if __name__ == '__main__':
    main()
