import random
import json

all_duration = [0.25, 0.5, 1, 2, 4]

with open('chordproglib.json','r') as rdata:
    chordproglib = json.load(rdata)
    rdata.close()
    
# FUNCTION TO GENERATE A CHORD PROGRESSION BASED ON THE KEY SIGNATURE AND NUMBER OF BARS
def genchord(scaletype: str, scalechords: list, barnum: float):
    if random.random() <= 0.5 and str(barnum) in chordproglib[scaletype].keys():
        prog = random.choice(chordproglib[scaletype][str(barnum)])
        prog = [scalechords[x] for x in prog]
    else:
        prog = random.choices(scalechords, k = barnum - 1)
        prog.insert(0, scalechords[0])

    return prog

# FUNCTION TO GENERATE A LIST OF RIFF BASED ON A CHORD PROGRESSION
def genriff(prog: list, timesig: list):
    limit = 0
    time = 0
    riff = []
    for i in range(len(prog)):                  # Iterate through each chord in the progression
        limit += 4 * timesig[0] / timesig[1]    # Duration of 1 chord in quarter notes
        available_duration = [x for x in all_duration if x <= limit - time]
        note = [
                prog[i][1],
                random.choice([3, 4, 5]),
                random.choice(available_duration)
                ]
        riff.append([note])
        time += note[2]

        while time < limit: 
            available_duration = [x for x in all_duration if x <= limit - time]
            note = [
                random.choice([x for x in prog[i] if str(x).isdigit()]),
                random.choice([3, 4, 5]),
                random.choice(available_duration)
                ]
            riff[i].append(note)
            time += note[2]

    return riff
            
