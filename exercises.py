import random

import fretboard


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


def note_finder(strings, qty, sharps):
    note_choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G',]
    if sharps:
        note_choices.extend(['A#', 'C#', 'D#', 'F#', 'G#'])

    notes = []
    prev_note = None

    for _ in range(qty):
        chosen_note = random.choice(note_choices)
        while chosen_note == prev_note:
            chosen_note = random.choice(note_choices)

        notes.append({'note': chosen_note, 'string': random.choice(strings)})

        prev_note = chosen_note

    return notes


def note_finder_variations():
    return [
        {'name': 'String 6', 'query_string': '6'},
        {'name': 'String 5', 'query_string': '5'},
        {'name': 'String 4', 'query_string': '4'},
        {'name': 'String 3', 'query_string': '3'},
        {'name': 'String 2', 'query_string': '2'},
        {'name': 'String 1', 'query_string': '1'},
        {'name': 'Lower Strings', 'query_string': '6,5,4'},
        {'name': 'Upper Strings', 'query_string': '3,2,1'},
        {'name': 'All Strings', 'query_string': '6,5,4,3,2,1'},
    ]
