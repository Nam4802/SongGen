import random
import json

with open('chordproglib.json','r') as rdata:
    chordproglib = json.load(rdata)
    rdata.close()

with open('notelib.json', 'r') as rdata:
    notelib = json.load(rdata)
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
        availduration = [x for x in notelib['duration'] if x <= limit - time]
        availdurationweight = [notelib['durationweight'][x] for x in range(len(availduration))]
        note = [
                int(prog[i][1]),
                int(random.choices(notelib['octave'], notelib['octaveweight'])[0]),
                float(random.choices(availduration, availdurationweight)[0])
                ]
        riff.append([note])
        time += note[2]

        while time < limit: 
            availduration = [x for x in notelib['duration'] if x <= limit - time]
            availdurationweight = [notelib['durationweight'][x] for x in range(len(availduration))]
            note = [
                int(random.choice([x for x in prog[i] if str(x).isdigit()])),
                int(random.choices(notelib['octave'], notelib['octaveweight'])[0]),
                float(random.choices(availduration, availdurationweight)[0])
                ]
            riff[i].append(note)
            time += note[2]

    return riff
            
