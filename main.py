from pathlib import Path
from typing import Dict, Any

import aiohttp_jinja2
import jinja2
from aiohttp import web
from guitarpractice.exercises.rhythm_sixteenth_notes import rhythm_sixteenth_notes
from guitarpractice.formatters import to_vextab

router = web.RouteTableDef()


@router.get('/exercise')
@aiohttp_jinja2.template("exercise.html")
async def greet_user(request: web.Request) -> Dict[str, Any]:
    exercise = rhythm_sixteenth_notes(level=1)

    context = {
        'notes': to_vextab(exercise)
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
