from aiohttp.web import Request, Response, HTTPForbidden
from aiohttp import web
from aiohttp.web import middleware

routes = web.RouteTableDef()


@middleware
async def authentication(request: Request, handler) -> Response:
    if request.headers.get('auth') is None:
        raise HTTPForbidden

    return await handler(request)

@routes.get('/')
async def hello_handler(request: Request) -> Response:
    return Response(text='bar')

app = web.Application()
app.add_routes([web.get('/', hello_handler)])
web.run_app(app)