from itertools import zip_longest
from pathlib import Path
from typing import Dict, Any

import aiohttp_jinja2
import jinja2
from aiohttp import web
from guitarpractice.exercises import get_exercise, list_exercises
from guitarpractice.formatters import to_vextab

from exercises import fretboard_diagrams, note_finder, note_finder_variations, note_on_each_string

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
    duration = request.query.get('mins', '2')
    sharps = request.query.get('sharps', 'false')

    interval_map = {
        'slowest': 10000,
        'slow': 5000,
        'medium': 3000,
        'fast': 2000,
        'fastest': 1500,
    }
    tick_speed = interval_map[speed]
    duration_ms = (int(duration)) * 60000
    qty = int(duration_ms / tick_speed) + 1

    include_sharps = sharps != 'false'

    return {
        'notes': note_finder(strings, qty, include_sharps),
        'speed': tick_speed,
        'duration': duration_ms,
    }


@router.get('/note-on-each-string/')
@aiohttp_jinja2.template("note_on_each_string.html")
async def note_on_each_string_view(request: web.Request) -> Dict[str, Any]:
    sharps = request.query.get('sharps', 'false')
    include_sharps = sharps != 'false'

    notes = note_on_each_string(include_sharps)
    return {
        'notes': notes,
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
