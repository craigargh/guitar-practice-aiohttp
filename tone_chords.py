# Notes
# suspended chords https://www.youtube.com/watch?v=qu49nYaBfdM
# augmented chords https://www.youtube.com/watch?v=wNWDjhDo2Ak
# minor maj7 chords https://www.youtube.com/watch?v=Zr5hjIECFlk
# shell chords https://www.youtube.com/watch?v=tDhc2PEXLyw
# All math rock chords https://www.youtube.com/watch?v=8E-Ajb7ABdE

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
    'add9': {
        'I': 'add9',
        'II': 'madd9',
        'III': 'mb9',
        'IV': 'add9',
        'V': 'add9',
        'VI': 'madd9',
        'VII': 'dimb9',
    },
    'add11': {
        'II': 'madd11',
        'III': 'madd11',
        'VI': 'madd11',
    },
    'ninth': {
        'I': 'maj9',
        'II': 'min9',
        'III': 'min7b9',
        'IV': 'maj9',
        'V': '9',
        'VI': 'min9',
        'VII': 'm7b5b9',
    },
    'eleventh': {
        'II': 'min11',
        'III': 'm7(11)',
        'VI': 'min11',
    },
    '13th': {
        'I': 'maj13',
        'II': 'min13',
        'IV': 'maj7(13)',
        'V': '13',
    },
    '7sus4': {
        'II': '7sus4',
        'III': '7sus4',
        'V': '7sus4',
        'VI': '7sus4',
    },
    'sixth': {
        'I': '6',
        'II': 'min6',
        'III': 'minb6',
        'IV': '6',
        'V': '6',
        'VI': 'minb6',
    },
    '6/9': {
        'I': '6/9',
        'II': 'min6/9',
        'IV': '6/9',
        'V': '6/9',
    },
    'sus2/4': {
        'I': 'sus4add9',
        'II': 'sus4add9',
        'V': 'sus4add9',
        'VI': 'sus4add9',
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
