from itertools import zip_longest
from pathlib import Path
from typing import Dict, Any

import aiohttp_jinja2
import jinja2
from aiohttp import web
from guitarpractice.exercises import get_exercise, list_exercises
from guitarpractice.formatters import to_vextab

from exercises import fretboard_diagrams, note_finder, note_finder_variations

router = web.RouteTableDef()


@router.get('/')
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> Dict[str, Any]:
    exercises = list_exercises().get('exercises')
    note_finders = note_finder_variations()

    return {
        'exercises': exercises,
        'note_finders': note_finders,
    }


@router.get('/exercise/{exercise_id}/{variation}/')
@aiohttp_jinja2.template("exercise.html")
async def exercise_view(request: web.Request) -> Dict[str, Any]:
    exercise_id = request.match_info['exercise_id']
    variation = request.match_info['variation']

    exercise = get_exercise(exercise_id, variation)
    diagrams = fretboard_diagrams(exercise)
    diagram_labels = []

    if exercise.shape_labels:
        diagram_labels = [
            shape.name
            for shape in exercise.shapes
        ]

    diagrams = [
        {'shape': shape, 'label': label}
        for shape, label in zip_longest(diagrams, diagram_labels)
    ]

    context = {
        'tab': to_vextab(exercise),
        'diagrams': diagrams,
    }

    return context


@router.get('/note-finder/')
@aiohttp_jinja2.template("note_finder.html")
async def note_finder_view(request: web.Request) -> Dict[str, Any]:
    strings = request.query.get('strings', '6').split(',')
    speed = request.query.get('speed', 'slow')

    interval_map = {
        'slow': 3000,
        'medium': 2000,
        'fast': 1500,
    }

    return {
        'notes': note_finder(strings),
        'speed': interval_map[speed],
    }


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
