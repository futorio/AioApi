import traceback
import asyncio

import aiohttp

from aiohttp.web import (Request, Response,
                         HTTPUnauthorized, HTTPUnprocessableEntity,
                         HTTPBadRequest,)
from aiohttp import web
from aiohttp.web import middleware

from cerberus import Validator


AUTH_URL: str = 'http://auth.pressindex.int/v2/auth/signin'
token_storage: set = set()


async def get_auth_token(data: bytes) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(AUTH_URL, data=data) as response:
            response_data = await response.json()
            if 'access_token' in response_data:
                return response_data['access_token']
            else:
                raise HTTPBadRequest()


def token_is_valid(token: str) -> bool:
    """Заглушка валидации токена"""
    return token in token_storage


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
    auth_token = request.headers.get('auth')

    if request.path == '/auth' or token_is_valid(auth_token):
        return await handler(request)
    else:
        raise HTTPUnauthorized()


async def get_token_handler(request: Request) -> str:
    if request.can_read_body:
        post_body = await request.read()
    else:
        raise HTTPBadRequest()

    auth_token = await get_auth_token(post_body)
    token_storage.add(auth_token)
    return auth_token


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
    app.add_routes([web.get('/', handler),
                    web.post('/auth', get_token_handler)])
    web.run_app(app)


if __name__ == '__main__':
    main()
