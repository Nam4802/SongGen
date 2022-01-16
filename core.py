import json
import random
import math
from midiutil import MIDIFile
import genalgorithm

sname = {'majscale':'Major scale', 'minscale':'Minor scale'}
chartopc = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11}
pctochar = {0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'}

with open('chordlib.json','r') as rdata:
    chordlib = json.load(rdata)
    rdata.close()

dchordtype = chordlib['dchordtype']
dscaletype = chordlib['dscaletype']

# NOTE ON DATA TYPE: 
# A chord is a list in the following format: ["prefix", notes1, notes2, ...]
# Where the prefix is the chord type: '' = Major, 'm' = Minor, '7' = Major 7th...

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
    
    chordlib['dscaletype'] = dscaletype                                 # Saving back to data.json
    chordlib['dchordtype'] = dchordtype

    with open('chordlib.json','w') as wdata:
        json.dump(chordlib, wdata, indent = 4, sort_keys = True)
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

    chordlib['dscaletype'] = dscaletype
    chordlib['dchordtype'] = dchordtype

    with open('chordlib.json','w') as wdata:
        json.dump(chordlib, wdata, indent = 4, sort_keys = True)
        wdata.close()
        
# FUNCTION TO ADD A CHORD TO MIDI TRACK
def addChordMidi(midiobj, track: int, channel: int, chord: list, timesig: list, starttime: float):
    for i in range(timesig[0]):                     # Loop to add each time a chord is played according to the number of notes in bar
        for j in range(1, len(chord)):              # Loop to add notes of the current chord
                if j == 1:
                    tracker = 0
                elif (chord[j] - chord[j - 1]) < 0: # Increase pitch if the pitch class of current note is smaller than the previous note
                    tracker += 12
                midiobj.addNote(track, channel, chord[j] + 48 + tracker, starttime, duration = 4 / timesig[1], volume = 100)
        starttime += 4 / timesig[1]                 # starttime is in quarter notes

# FUNCTION TO ADD A RIFF TO MIDI TRACK
def addRiffMidi(midiobj, track: int, channel: int, riff: list, starttime: float):
    for note in riff:
        midinote = note[0] + 12 * (note[1] + 1)
        duration = note[2]
        midiobj.addNote(track, channel, midinote, starttime, duration, volume = 100)
        starttime += duration

class Song:         # Default song structure: verse - verse - chorus - verse - verse - chorus - bridge - solo - chorus - chorus
    def __init__(self, scaletype, root='C', vbarnum=4, cbarnum=4, bbarnum=4, timesig=[4,4], bpm=120):
        self.scaletype = scaletype
        self.vbarnum = vbarnum
        self.cbarnum = cbarnum
        self.bbarnum = bbarnum
        self.timesig = timesig
        self.bpm = bpm
        self.root = root
        self.scale = root + ' ' + sname[scaletype]
        self.rootoffset = chartopc[root]
        self.scalenotes = dscaletype[scaletype]['scalenotes']
        self.scalechords = dscaletype[scaletype]['ctypeofscale']

        # CHANGE DEFAULT SCALE NOTES & CHORDS TO THE CURRENT KEY'S
        for i in range(len(self.scalenotes)):
            self.scalenotes[i] = (self.scalenotes[i] + self.rootoffset)%12
        for i in range(len(self.scalechords)):
            for j in range(1,len(self.scalechords[i])):
                self.scalechords[i][j] = (self.scalechords[i][j] + self.rootoffset)%12
        
        # INITIATE MIDI FILE OBJECT
        self.midi = MIDIFile(2)
        self.midi.addTempo(0, 0, bpm)
        self.midi.addTempo(1, 0, bpm)
        self.midi.addTimeSignature(0, 0, timesig[0], int(math.log2(timesig[1])), 24)
        self.midi.addTimeSignature(1, 0, timesig[0], int(math.log2(timesig[1])), 24)

        # GENERATION OF THE SONG
        self.genrythm()
        self.genlead()
        self.gensong()
        
    # INSTANCE METHOD DECLARATION
    
    # Function to generate the chord progressions for the whole song
    def genrythm(self):
        self.rythm = {
            'verse': genalgorithm.genchord(self.scaletype, self.scalechords, self.vbarnum),
            'chorus': genalgorithm.genchord(self.scaletype, self.scalechords, self.cbarnum),
            'bridge': genalgorithm.genchord(self.scaletype, self.scalechords, self.bbarnum)
            }

    # Function to generate the notes, riffs and solos for the whole song
    def genlead(self):
        self.lead = {'solo': genalgorithm.genriff(self.prog['chorus'], self.timesig)}

    # Function to generate the midi file based on the specified song structure
    #   Verse: 0
    #   Chorus: 1
    #   Bridge: 2
    #   Solo: 3
    def gensong(self, pattern = 0):
        if pattern == 0:
            pattern = [0, 0, 1, 0, 0, 1, 2, 3, 1, 1]    # Default pattern
        starttime_rythm = 0
        starttime_lead = 0
        for x in pattern:
            if x == 0:
                for chord in self.rythm['verse']:
                    addChordMidi(self.midi, 0, 0, chord, self.timesig, starttime_rythm)
                    starttime_rythm += 4 * self.timesig[0] / self.timesig[1]
            elif x == 1:
                for chord in self.rythm['chorus']:
                        addChordMidi(self.midi, 0, 0, chord, self.timesig, starttime_rythm)
                        starttime_rythm += 4 * self.timesig[0] / self.timesig[1]
            elif x == 2:
                for chord in self.rythm['bridge']:
                    addChordMidi(self.midi, 0, 0, chord, self.timesig, starttime_rythm)
                    starttime_rythm += 4 * self.timesig[0] / self.timesig[1]
            elif x == 3:
                starttime_lead = starttime_rythm
                for riff in self.lead['solo']:
                    addRiffMidi(self.midi, 1, 0, riff, starttime_lead)
                    starttime_lead += 4 * self.timesig[0] / self.timesig[1]
                for chord in self.rythm['chorus']:
                        addChordMidi(self.midi, 0, 0, chord, self.timesig, starttime_rythm)
                        starttime_rythm += 4 * self.timesig[0] / self.timesig[1]
        with open('midifile.midi', 'wb') as output:
            self.midi.writeFile(output)

    # Function to print the progression (chords) of each part of the song
    def printprog(self):
        print('Your progression is:')
        for progname in self.rythm:
            print('   ' + progname.capitalize() + ':')
            for chord in self.rythm[progname]:
                print('   ' + pctochar[chord[1]] + chord[0], end = '')
            print()
        print()

    # INPUT METHOD
    @classmethod
    def getsong(cls):
        while True:
            scaletype = input('Enter "majscale"/"minscale": ')
            if scaletype not in sname:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                break
        while True:
            root = input('Root note: ')
            if root not in chartopc:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                break
        while True:
            try:
                vbarnum = int(input('Number of bar in verse progression: '))
            except ValueError:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                vbarnum = abs(vbarnum)
                break
        while True:
            try:
                cbarnum = int(input('Number of bar in chorus progression: '))
            except ValueError:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                cbarnum = abs(cbarnum)
                break
        while True:
            try:
                bbarnum = int(input('Number of bar in bridge progression: '))
            except ValueError:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                bbarnum = abs(bbarnum)
                break
        while True:
            try:
                timesig = [int(x) for x in input('Time signature (ex: 4 4): ').split()]
            except ValueError:
                print('This is not what I asked for. Please try again.')
                continue
            if len(timesig) != 2 and len(timesig) != 0:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                timesig =  [abs(x) for x in timesig]
                break
        while True:
            try:
                bpm = int(input('BPM of the song: '))
            except ValueError:
                print('This is not what I asked for. Please try again.')
                continue
            else:
                bpm = abs(bpm)
                break
        
        return cls(scaletype, root, vbarnum, cbarnum, bbarnum, timesig, bpm)
