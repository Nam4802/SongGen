import json
import random

sname = {'majscale':'Major scale', 'minscale':'Minor scale'}
chartopc = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11}
pctochar = {0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'}

rdata = open('data.json','r')
data = json.load(rdata)
rdata.close()

dchordtype = data['dchordtype']
dscaletype = data['dscaletype']

# FUNCTION TO ADD CUSTOM CHORD TO ALL SCALETYPE LIBRARY (Chord format = ["prefix", notes1, notes2, ...])
def addtoall(chord):
    test = chord[1:]            # Chord to be added with prefix removed (test chord)
    for sdata in dscaletype.values():                                   # Loop to go through all scale types
        for notes in sdata['scalenotes']:                               # Loop to go through all notes (offset) in a scale type
            testofnote = []
            for i in test:                                              # Loop to add the note offset to all notes of the testing chord
                i = i + notes
                testofnote.append(i%12)
            if set(testofnote).issubset(sdata['scalenotes']):           # Check if all the notes in the current testing chord belongs to scale
                testofnote.insert(0,chord[0])
                sdata['ctypeofscale'].append(testofnote)
    
    data['dscaletype'] = dscaletype                                     # Saving back to data.json
    data['dchordtype'] = dchordtype

    with open('data.json','w') as wdata:
        json.dump(data,wdata, indent = 4, sort_keys = True)
        wdata.close()

# FUNCTION TO ADD CUSTOM CHORD TO 1 SCALETYPE LIBRARY
def addtoscale(chord,sdata):
    tc = chord[1:]
    for notes in sdata['scalenotes']:
        tcofnote = []
        for i in tc:
            i = i + notes
            tcofnote.append(i%12)
        if set(tcofnote).issubset(sdata['scalenotes']):
            tcofnote.insert(0,chord[0])
            sdata['ctypeofscale'].append(tcofnote)

    data['dscaletype'] = dscaletype
    data['dchordtype'] = dchordtype

    with open('data.json','w') as wdata:
        json.dump(data,wdata, indent = 4, sort_keys = True)
        wdata.close()

class ChordProg:
    def __init__(self, scaletype, root='C', barnum=4):
        self.scaletype = scaletype
        self.barnum = barnum
        self.root = root
        self.scale = root + ' ' + sname[scaletype]
        self.rootoffset = chartopc[root]          # Difference between the selected root and C
        self.scalenotes = dscaletype[scaletype]['scalenotes']
        self.scalechords = dscaletype[scaletype]['ctypeofscale']

        for i in range(len(self.scalenotes)):                           # Change notes by adding the root offset to get new notes of the scale
            self.scalenotes[i] = (self.scalenotes[i] + self.rootoffset)%12
        for i in range(len(self.scalechords)):                          # Change notes in the chords of the scale type to get according chords
            for j in range(1,len(self.scalechords[i])):
                self.scalechords[i][j] = (self.scalechords[i][j] + self.rootoffset)%12
        self.prog = random.sample(self.scalechords,self.barnum)         # Generate a random progression equal the number of bars

    def regenprog(self):
        self.prog = random.sample(self.scalechords,self.barnum)

    def printprog(self):
        print('Your progression is:', end = ' ')
        for chord in self.prog:
            print(pctochar[chord[1]] + chord[0], end= ' ')
        print()

    @classmethod
    def getprog(cls):
        return cls(
            input('Enter "majscale"/"minscale": '),
            input('Root note: '),
            int(input('Number of bar in progression: '))
            )

class Song:
    def __init__(self, scaletype, root='C', vbarnum=8, pbarnum=4, cbarnum=4, timesig=[4,4], bpm=120):
        self.scaletype = scaletype
        self.vbarnum = vbarnum
        self.pbarnum = pbarnum
        self.cbarnum = cbarnum
        self.timesig = timesig
        self.bpm = bpm
        self.root = root
        self.scale = root + ' ' + sname[scaletype]
        self.rootoffset = chartopc[root]
        self.scalenotes = dscaletype[scaletype]['scalenotes']
        self.scalechords = dscaletype[scaletype]['ctypeofscale']
        
        for i in range(len(self.scalenotes)):
            self.scalenotes[i] = (self.scalenotes[i] + self.rootoffset)%12
        for i in range(len(self.scalechords)):
            for j in range(1,len(self.scalechords[i])):
                self.scalechords[i][j] = (self.scalechords[i][j] + self.rootoffset)%12
        
        self.prog = {
            'verse':random.sample(self.scalechords, self.vbarnum),
            'prechorus':random.sample(self.scalechords, self.pbarnum),
            'chorus':random.sample(self.scalechords, self.cbarnum)
            }
        
    def regenprog(self):
        self.prog = {
            'verse':random.sample(self.scalechords, self.vbarnum),
            'pre-chorus':random.sample(self.scalechords, self.pbarnum),
            'chorus':random.sample(self.scalechords, self.cbarnum)
            }

    def printprog(self):
        print('Your progression is:')
        for progname in self.prog:
            print('   ' + progname.capitalize() + ':')
            for chord in self.prog[progname]:
                print('   ' + pctochar[chord[1]] + chord[0], end = '')
            print()
        print()

    @classmethod
    def getsong(cls):
        return cls(
            input('Enter "majscale"/"minscale": '),
            input('Root note: '),
            int(input('Number of bar in verse progression: ')),
            int(input('Number of bar in pre-chorus progression: ')),
            int(input('Number of bar in chorus progression: ')),
            [int(x) for x in input('Time signature (ex: 4 4): ').split()],
            int(input('BPM of the song: '))
            )