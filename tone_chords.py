# Notes
# suspended chords https://www.youtube.com/watch?v=qu49nYaBfdM
# augmented chords https://www.youtube.com/watch?v=wNWDjhDo2Ak
# minor maj7 chords https://www.youtube.com/watch?v=Zr5hjIECFlk
# shell chords https://www.youtube.com/watch?v=tDhc2PEXLyw
from itertools import cycle

tone_chords = {
    'major': {
        'I': 'maj',
        'II': 'min',
        'III': 'min',
        'IV': 'maj',
        'V': 'maj',
        'VI': 'min',
        'VII': 'dim',
    },
    'seventh': {
        'I': 'maj7',
        'II': 'min7',
        'III': 'min7',
        'IV': 'maj7',
        'V': '7',
        'VI': 'min7',
        'VII': 'min7b5',
    },
    'ninth': {
        'I': 'maj9',
        'II': 'min9',
        'IV': '7b9',
        'V': '9',
        'VI': 'min9',
    },
    'add9': {
        'I': 'add9',
        'II': 'madd9',
        'III': 'mb9',
        'IV': 'add9',
        'V': 'add9',
        'VI': 'madd9',
        'VII': 'dimb9',
    },
    'sus2': {
        'I': 'sus2',
        'II': 'sus2',
        'IV': 'sus2',
        'V': 'sus2',
        'VI': 'sus2',
    },
    'sus4': {
        'I': 'sus4',
        'II': 'sus4',
        'III': 'sus4',
        'V': 'sus4',
        'VI': 'sus4',
    },
    'sixth': {
        'I': '6',
        'II': 'm6',
        'III': 'minb6',
        'IV': '6',
        'V': '6',
        'VI': 'minb6',
    },
}

scale_steps = {
    'major': [
        'root',
        'major2',
        'major3',
        'perfect4',
        'perfect5',
        'major6',
        'major7',
    ]
}

interval_offsets = {
    'root': 0,
    'major2': 2,
    'major3': 4,
    'perfect4': 5,
    'perfect5': 7,
    'major6': 9,
    'major7': 11,
}

all_notes = [
    'A',
    'A#',
    'B',
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    'F#',
    'G',
    'G#',
]


def build_tone_chords(key, scale):
    intervals = [
        'I',
        'II',
        'III',
        'IV',
        'V',
        'VI',
        'VII',
    ]
    notes = scale_notes(key, scale)

    key_tone_chords = {}

    for tonality, values in tone_chords.items():
        key_tone_chords[tonality] = {}

        for note, interval in zip(notes, intervals):
            chord = values.get(interval)

            if chord is None:
                continue

            note_chord = note + chord
            key_tone_chords[tonality][interval] = note_chord

    return key_tone_chords


def list_chord_shapes(key, scale, shape_notes):
    chords = []

    tone_chord_source = build_tone_chords(key, scale) if shape_notes else tone_chords

    for degrees in tone_chord_source.values():
        for chord in degrees.values():
            if chord in chords:
                continue
            chords.append(chord)

    return chords


def scale_notes(key, scale):
    scale = scale_steps[scale]
    steps = [interval_offsets[interval] for interval in scale]

    root_offset = all_notes.index(key)

    notes_cycle = all_notes + all_notes
    note_names = [
        notes_cycle[root_offset + step]
        for step in steps
    ]

    return note_names
