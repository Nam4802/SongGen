import json

basechordlib = {
    'dchordtype': {
        'major': ['', 0, 4, 7],
        'minor': ['m', 0, 3, 7],
        'diminished': ['dim', 0, 3, 6],
        'major7th': ['maj7', 0, 4, 7, 11],
        'minor7th': ['m7', 0, 3, 7, 10],
        'dominant7th': ['7', 0, 4, 7, 10],
        'diminished7th': ['dim7', 0, 3, 6, 9],
        'halfdiminished7th': ['dim7b5', 0, 3, 6, 10]
        },
    'dscaletype': {
        'majscale': {
            'ctypeofscale': [
                ['', 0, 4, 7],          # I
                ['m', 2, 5, 9],         # ii
                ['m', 4, 7, 11],        # iii
                ['', 5, 9, 0],          # IV
                ['', 7, 11, 2],         # V
                ['m', 9, 0, 4],         # vi
                ['dim', 11, 2, 5],      # viidim
                ['maj7', 0, 4, 7, 11],  # Imaj7
                ['m7', 2, 5, 9, 0],     # iim7
                ['m7', 4, 7, 11, 2],    # iiim7
                ['maj7', 5, 9, 0, 4],   # IVmaj7
                ['7', 7, 11, 2, 5],     # V7
                ['m7', 9, 0, 4, 7],     # vim7
                ['dim7b5', 11, 2, 5, 9] # viidim7b5
                ],
            'scalenotes': [0, 2, 4, 5, 7, 9, 11]
            },
        'minscale': {
            'ctypeofscale': [
                ['m', 0, 3, 7],         # i
                ['dim', 2, 5, 8],       # iidim
                ['', 3, 7, 10],         # bIII
                ['m', 5, 8, 0],         # iv
                ['m', 7, 10, 2],        # v
                ['', 8, 0, 3],          # bVI
                ['', 10, 2, 5],         # bVII
                ['m7', 0, 3, 7, 10],    # im7
                ['dim7b5', 2, 5, 8, 0], # iidim7b5
                ['maj7', 3, 7, 10, 2],  # bIIImaj7
                ['m7', 5, 8, 0, 3],     # ivm7
                ['m7', 7, 10, 2, 5],    # vm7
                ['maj7', 8, 0, 3, 7],   # bVImaj7
                ['7', 10, 2, 5, 8]      # bVII7
                ],
            'scalenotes': [0, 2, 3, 5, 7, 8, 10]
            }
        }
    }

basechordproglib = {
    'majscale': {
        '4': [
            [0, 3, 4, 4], # I-IV-V-V
            [0, 4, 5, 3], # I-V-vi-IV
            [0, 3, 4, 3], # I-IV-V-IV
            [0, 5, 3, 4]  # I-vi-IV-V
            ],
        '8': [
            [0, 4, 3, 3, 0, 4, 0, 4], # I-V-IV-IV-I-V-I-V (eight bar blues)
            [0, 4, 5, 2, 3, 0, 3, 4], # I-V-vi-iii-IV-I-IV-V (canon)
            ]
        },
    'minscale': {
        '4': [
            [0, 3, 4, 4], # i-iv-v-v
            [0, 5, 2, 6], # i-bVI-bIII-bVII
            [0, 3, 2, 5], # i-iv-bIII-bVI
            [0, 3, 5, 4]  # i-iv-bVI-v
            ]
        }
    }

# FUNCTION TO RESET THE CHORDPROGLIB AND CHORDLIB WITH THE DATA IN THIS MODULE
def resetlib():
    with open('chordlib.json','w') as wdata:
            json.dump(basechordlib, wdata, indent = 4, sort_keys = True)
            wdata.close()

    with open('chordproglib.json','w') as wdata:
            json.dump(basechordproglib, wdata, indent = 4, sort_keys = True)
            wdata.close()

# FUNCTION TO ADD CUSTOM CHORD TO ALL SCALETYPE LIBRARY (Chord format = ["prefix", notes1, notes2, ...])
def addtoall(chord):
    with open('chordlib.json','r') as rdata:                            # Data initiation
        chordlib = json.load(rdata)
        rdata.close()

    test = chord[1:]            # Chord to be added with prefix removed (test chord)
    for scaletype in chordlib['dscaletype'].values():                   # Loop to go through all scale types
        for notes in scaletype['scalenotes']:                           # Loop to go through all notes (offset) in a scale type
            testofnote = []
            for i in test:                                              # Loop to add the note offset to all notes of the testing chord
                i = i + notes
                testofnote.append(i%12)
            if set(testofnote).issubset(scaletype['scalenotes']):       # Check if all the notes in the current testing chord belongs to scale
                testofnote.insert(0,chord[0])
                scaletype['ctypeofscale'].append(testofnote)
    
    with open('chordlib.json','w') as wdata:
        json.dump(chordlib, wdata, indent = 4, sort_keys = True)
        wdata.close()

# FUNCTION TO ADD CUSTOM CHORD TO 1 SCALETYPE LIBRARY
def addtoscale(chord, scaletype):                                       # scaletype should be something like chordlib['dscaletype']['majscale' or 'minscale']
    with open('chordlib.json','r') as rdata:                            # Data initiation
        chordlib = json.load(rdata)
        rdata.close()

    tc = chord[1:]
    for notes in scaletype['scalenotes']:
        tcofnote = []
        for i in tc:
            i = i + notes
            tcofnote.append(i%12)
        if set(tcofnote).issubset(scaletype['scalenotes']):
            tcofnote.insert(0,chord[0])
            scaletype['ctypeofscale'].append(tcofnote)

    chordlib['dscaletype'] = dscaletype
    chordlib['dchordtype'] = dchordtype

    with open('chordlib.json','w') as wdata:
        json.dump(chordlib, wdata, indent = 4, sort_keys = True)
        wdata.close()