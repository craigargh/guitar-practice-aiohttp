from pathlib import Path
from typing import Dict, Any

import aiohttp_jinja2
import jinja2
from aiohttp import web
from guitarpractice.exercises import get_exercise
from guitarpractice.formatters import to_vextab

router = web.RouteTableDef()


@router.get('/exercise/{exercise_id}/{variation}')
@aiohttp_jinja2.template("exercise.html")
async def exercise_view(request: web.Request) -> Dict[str, Any]:
    exercise_id = request.match_info['exercise_id']
    variation = request.match_info['variation']

    exercise = get_exercise(exercise_id, variation)

    context = {
        'tab': to_vextab(exercise)
    }

    return context


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(Path(__file__).parent / "templates"))
    )

    return app


web.run_app(init_app())
