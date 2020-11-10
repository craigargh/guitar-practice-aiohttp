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
        lowest_fret = min(position.fret for position in positions if position)
        highest_fret = max(position.fret for position in positions if position)
        min_fret = max(0, lowest_fret - 1)
        max_fret = highest_fret + 1

        if max_fret - min_fret < 5:
            max_fret = min_fret + 5

        bg_color = '#e7e7e7'
        color = '#606060'

        height = 350
        if max_fret - min_fret > 6:
            height = 500

        style = {
            'marker': {
                'color': color,
                'border_color': color,
            },
            'string': {
                'color': color,
            },
            'inlays': {
                'color': color,
            },
            'fret': {
                'color': color,
            },
            'nut': {
                'color': color,
            },
            'drawing': {
                'background_color': bg_color,
                'font_color': color,
                'height': height,
            },
        }

        fb = fretboard.Fretboard(frets=(min_fret, max_fret), style=style)

        for position in positions:
            if position is None:
                continue

            if position.highlighted:
                styling = {'color': bg_color}
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

    static_dir = str(Path(__file__).parent / "static")
    app.add_routes([web.static('/static', static_dir)])
    router.static('/static', static_dir)

    return app


web.run_app(init_app())
