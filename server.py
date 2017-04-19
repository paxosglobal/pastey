import asyncio
import aiohttp_jinja2
import aioredis
import jinja2
import os

from aiohttp import web
from subconscious.model import RedisModel, Column
from uuid import uuid4


# For simplicity all of this is in one file
# Typically, you'd pull a lot of this out into models.py, views.py and perhaps even forms.py


class Paste(RedisModel):
    uuid = Column(type=str, primary_key=True)
    title = Column(type=str, required=True)
    body = Column(type=str, required=True)


@aiohttp_jinja2.template('index.jinja2')
async def index(request):
    cnt, recent_pastes = 0, []
    # TODO: better syntax for async generator?
    # TODO: get most recent Pasteys only
    async for paste in Paste.all(db=request.app['db']):
        recent_pastes.append(paste)
        cnt += 1
        if cnt > 5:
            # TODO: add LIMIT to subconscious
            break
    return {'recent_pastes': recent_pastes}


@aiohttp_jinja2.template('get_paste.jinja2')
async def get_paste(request):
    uuid = request.match_info.get('uuid')
    if not uuid:
        return {}
    paste_obj = await Paste.get_object_or_none(
        db=request.app['db'],
        uuid=uuid,
    )

    if paste_obj:
        # Render the page
        return {
            'title': paste_obj.title,
            'body': paste_obj.body,
        }
    else:
        # Redirect to homepage
        return web.HTTPFound('/')


@aiohttp_jinja2.template('save_paste.jinja2')
async def save_paste(request):
    post_data = await request.post()
    if post_data:
        title = post_data.get('title')
        body = post_data.get('body', '')
        if title:
            paste_obj = Paste(
                uuid=str(uuid4()),
                title=title,
                body=body,
            )
            await paste_obj.save(request.app['db'])
            # redirect to paste page
            return web.HTTPFound('/pastes/{}'.format(paste_obj.uuid))
        else:
            # TODO: show error msg
            pass

    return {}


async def init_app(app):
    app['db'] = await aioredis.create_redis(
        address=(
            os.getenv('REDIS_HOST', 'redis'),
            int(os.getenv('REDIS_PORT', 6379))
        ),
        db=int(os.getenv('REDIS_DB', 1)),
        loop=None,
        encoding='utf-8',
    )
    return app


def create_app():
    app = web.Application()
    app.on_startup.append(init_app)
    app.router.add_get('/', index)
    app.router.add_route('*', '/pastes', save_paste)
    app.router.add_get('/pastes/{uuid}', get_paste)
    templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates_dir))
    return app


if __name__ == '__main__':
    # For basic invocation: $ python server.py
    loop = asyncio.get_event_loop()
    app = create_app(loop=loop)
    web.run_app(
        app,
        host=os.getenv('PASTEY_HOST', '0.0.0.0'),
        port=int(os.getenv('PASTEY_PORT', 5000)),
    )
else:
    # This is where you'd create the app via gunicorn: $ ./entrypoint.sh
    pass
