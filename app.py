import os

import yandexwebdav
from aiohttp import web

FOLDER = u'/hippocampus/'
conf = yandexwebdav.Config({
    "user": os.environ.get('YANDEX_LOGIN'),
    "password": os.environ.get('YANDEX_PASSWORD')
})


async def get_json(request):
    files = conf.list(FOLDER)
    response = ''
    jsons = list()
    for file in files:
        if len(file.keys()):
            jsons.append(conf.download(list(file.keys())[0]).decode('utf-8'))
    for j in jsons:
        response += j + '\n'
    return web.Response(text=response)


app = web.Application()
app.router.add_get('/cards', get_json)
web.run_app(app, port=os.getenv('PORT', 8080))
