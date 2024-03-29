from itertools import zip_longest
from pathlib import Path
from typing import Dict, Any

import aiohttp_jinja2
import jinja2
from aiohttp import web
from guitarpractice.exercises import get_exercise, list_exercises
from guitarpractice.formatters import to_vextab
from guitarpractice.shapes.chord import list_movable_chord_shapes, list_open_chords

from exercises import fretboard_diagrams, note_finder, note_finder_variations, note_on_each_string, make_diagram
from diatonic_chords import list_chord_shapes, build_tone_chords

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
    flats = request.query.get('flats', 'false')

    include_sharps = sharps != 'false'
    include_flats = flats != 'false'

    notes = note_on_each_string(include_sharps, include_flats)
    return {
        'notes': notes,
    }


@router.get('/diatonic-chords/')
@aiohttp_jinja2.template("diatonic_chords.html")
async def diatonic_chords_view(request: web.Request) -> Dict[str, Any]:
    key = request.query.get('key', 'C')
    scale = request.query.get('scale', 'major')
    shape_notes = request.query.get('shape-notes', 'false')

    if 'sharp' in key:
        key = key.replace('sharp', '#')

    shape_notes = shape_notes != 'false'

    intervals = [
        'I',
        'II',
        'III',
        'IV',
        'V',
        'VI',
        'VII',
    ]

    table = [[''] + intervals]

    for tonality, chords in build_tone_chords(key, scale).items():
        if len(chords.keys()) == 0:
            continue

        row = [tonality]

        for interval in intervals:
            chord = chords.get(interval, "-")
            row.append(chord)

        table.append(row)

    open_shape_names = list_chord_shapes(key, scale, True)

    chord_shapes = {}
    for open_shape_name in open_shape_names:
        split_index = 2 if '#' in open_shape_name else 1
        note_name = open_shape_name[:split_index]
        tonality = open_shape_name[split_index:]

        diagrams = [
            make_diagram(movable_shape)
            for movable_shape in list_open_chords(note_name, tonality)
        ]

        if chord_shapes.get(tonality) is None:
            chord_shapes[tonality] = []

        chord_shapes[tonality].extend(diagrams)

    movable_shape_names = list_chord_shapes(key, scale, False)

    for shape_name in movable_shape_names:
        diagrams = [
            make_diagram(movable_shape)
            for movable_shape in list_movable_chord_shapes(shape_name)
        ]
        chord_shapes[shape_name].extend(diagrams)

    return {
        'table': table,
        'chord_shapes': chord_shapes
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
