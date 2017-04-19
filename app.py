#!/usr/bin/env python3

import aiohttp_jinja2
import aioredis
import jinja2
import os

from aiohttp import web
from datetime import datetime
from subconscious.model import RedisModel, Column
from uuid import uuid4


# For simplicity all of this is in one file
# Typically, you'd pull a lot of this out into models.py, views.py and perhaps even forms.py


class Paste(RedisModel):
    uuid = Column(type=str, primary_key=True)
    created_at = Column(type=str, required=True, sort=True)
    title = Column(type=str, required=True)
    body = Column(type=str, required=True)


@aiohttp_jinja2.template('index.jinja2')
async def index(request):
    # TODO: add LIMIT to subconscious
    recent_pastes = [paste async for paste in Paste.all(db=request.app['db'], order_by='-created_at')]
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
        return {'paste_obj': paste_obj.as_dict()}
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
                created_at=str(datetime.utcnow().isoformat()),
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
    # flush the DB (not very production safe):
    app['db'].flushdb()
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
