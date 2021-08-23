# server.py
import re
import json
import aiohttp_autoreload
import aiohttp_cors
import aiohttp_debugtoolbar

from aiohttp_remotes import AllowedHosts, BasicAuth, Secure, setup
from aiohttp_debugtoolbar import toolbar_middleware_factory
from aiohttp import web

from aspiredb.core.api import routes #, setup_file_writer
from aspiredb.core.zen import zen_now


# ------- config ------------
debug = True  # O
port = 22090
host = "0.0.0.0"

# -----------  Application -------------
app = web.Application()
aiohttp_debugtoolbar.setup(app)

app.add_routes(routes)


async def resources(request):
    return web.Response(text=f"{[ resource for resource in app.router.resources()]}")


app.router.add_get("/resource", resources)

# Configure default CORS settings.
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    },
)

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)


async def app_factory(app):
    app = app
    #await setup_file_writer()
    await setup(
        app, AllowedHosts(allowed_hosts=("*",))
    )  # , BasicAuth("user", "password", "realm"))

    return app

def serve():
    if debug:
        print("Reloading....")
        aiohttp_autoreload.start()
    web.run_app(app_factory(app), host=host, port=port)


if __name__ == "__main__":
    serve()
    