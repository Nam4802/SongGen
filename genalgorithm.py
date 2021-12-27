import random
import json

with open('chordproglib.json','r') as rdata:
    chordproglib = json.load(rdata)
    rdata.close()

def genchord(prog, scaletype, scalechords, barnum):
    if random.random() <= 0.5 and str(barnum) in chordproglib[scaletype].keys():
        prog = random.choice(chordproglib[scaletype][str(barnum)])
        prog = [scalechords[x] for x in prog]
    else:
        prog = random.choices(scalechords, k = barnum - 1)
        prog.insert(0, scalechords[0])
            
