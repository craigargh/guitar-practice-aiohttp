from pathlib import Path
from typing import Dict, Any

import aiohttp_jinja2
import fretboard
import jinja2
from aiohttp import web
from guitarpractice.exercises import get_exercise, list_exercises
from guitarpractice.formatters import to_vextab

router = web.RouteTableDef()


@router.get('/')
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> Dict[str, Any]:
    exercises = list_exercises().get('exercises')

    return {'exercises': exercises}


@router.get('/exercise/{exercise_id}/{variation}/')
@aiohttp_jinja2.template("exercise.html")
async def exercise_view(request: web.Request) -> Dict[str, Any]:
    exercise_id = request.match_info['exercise_id']
    variation = request.match_info['variation']

    exercise = get_exercise(exercise_id, variation)
    diagrams = fretboard_diagrams(exercise)

    context = {
        'tab': to_vextab(exercise),
        'diagrams': diagrams,
    }

    return context


def fretboard_diagrams(exercise):
    diagrams = []

    for shape in exercise.shapes:
        positions = shape.positions
        lowest_fret = min(position.fret for position in positions)
        highest_fret = max(position.fret for position in positions)
        min_fret = max(0, lowest_fret - 1)
        max_fret = highest_fret + 1 if min_fret > 0 else 3

        fb = fretboard.Fretboard(frets=(min_fret, max_fret), style={'marker': {'color': 'darkslategray'}})

        for position in positions:
            if position.highlighted:
                styling = {'color': 'white'}
            else:
                styling = {}

            string = 6 - position.string
            fb.add_marker(string=string, fret=position.fret, **styling)

        diagram_svg = str(fb.render().getvalue()).replace('<?xml version="1.0" encoding="utf-8" ?>', '')
        diagrams.append(diagram_svg)

    return diagrams


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(router)
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(Path(__file__).parent / "templates"))
    )

    return app


web.run_app(init_app())
