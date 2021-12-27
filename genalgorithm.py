import random

chordproglib = {
    'majscale': {       # scalechords order: I, IV, V, ii, iii, vi, Imaj7, IVmaj7, ii7, iii7, vi7, V7
        '4': [
            [0, 1, 2, 2], # I-IV-V-V
            [0, 2, 5, 1], # I-V-vi-IV
            [0, 1, 2, 1], # I-IV-V-IV
            [0, 5, 1, 2]  # I-vi-IV-V
            ],
        '8': [
            [0, 2, 1, 1, 0, 2, 0, 2], # I-V-IV-IV-I-V-I-V (eight bar blues)
            [0, 2, 5, 4, 1, 0, 1, 2], # I-V-vi-iii-IV-I-IV-V (canon)
            ]
        },
    'minscale': {       # scalechords order: bIII, bVI, bVII, i, iv, v, bIIImaj7, bVImaj7, im7, ivm7, vm7, bVII7 (no iidim)
        '4': [
            [3, 4, 5, 5], # i-iv-v-v
            [3, 1, 0, 2], # i-bVI-bIII-bVII
            [3, 3, 0, 1], # i-iv-bIII-bVI
            [3, 4, 1, 5]  # i-iv-bVI-v
            ]
        }
    }

def genchord(prog, scaletype, scalechords, barnum):
    if random.random() <= 0.5 and str(barnum) in chordproglib[scaletype].keys():
        prog = random.choice(chordproglib[scaletype][str(barnum)])
        prog = [scalechords[x] for x in prog]
    else:
        prog = random.choices(scalechords, k = barnum - 1)
        if scaletype == 'majscale':
            prog.insert(0, scalechords[0])
        elif scaletype == 'minscale':
            prog.insert(0, scalechords[3])
            
