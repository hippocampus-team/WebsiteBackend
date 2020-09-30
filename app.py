import os

import yandexwebdav
from aiohttp import web

FOLDER = '/hippocampus/'
CARDS = FOLDER + 'cards.txt'
BIOS = FOLDER + 'bios.txt'
TEAM_BIO = FOLDER + 'teambio.txt'
CONTACTS = FOLDER + 'contacts.txt'

conf = yandexwebdav.Config({
    "user": os.environ.get('YANDEX_LOGIN'),
    "password": os.environ.get('YANDEX_PASSWORD')
})


async def get_cards(request):
    response = ''
    while True:
        try:
            response = conf.download(CARDS).decode('utf-8')
            return web.Response(text=response, headers={
                "Access-Control-Allow-Origin": "*"
            })
        except yandexwebdav.ConnectionException as e:
            print('ConnectionException: ' + str(e.code))


app = web.Application()
app.router.add_get('/cards', get_cards())
web.run_app(app, port=os.getenv('PORT', 8080))
