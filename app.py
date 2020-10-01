import os

import yandexwebdav
from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized

FOLDER = '/hippocampus/'
TRIES = 2
docs = {
    '/cards': FOLDER + 'cards.txt',
    '/bios': FOLDER + 'bios.txt',
    '/teambio': FOLDER + 'teambio.txt',
    '/contacts': FOLDER + 'contacts.txt'
}

config = yandexwebdav.Config({
    "user": os.environ.get('YANDEX_LOGIN'),
    "password": os.environ.get('YANDEX_PASSWORD')
})


async def get_json(request):
    for i in range(TRIES):
        try:
            response = config.download(docs[request.path]).decode('utf-8')
            return web.Response(text=response, headers={
                "Access-Control-Allow-Origin": "*"
            })
        except yandexwebdav.ConnectionException as e:
            print('ConnectionException: ' + str(e.code))
        except AttributeError:
            print('AttributeError')
    return HTTPUnauthorized()


def set_routes():
    for path in docs.keys():
        app.router.add_get(path, get_json)


app = web.Application()
set_routes()
web.run_app(app, port=os.getenv('PORT', 8080))
