import json
import random
import time
from core import Song

# Dictionaries for printing
sname = {'majscale':'Major scale', 'minscale':'Minor scale'}
chartopc = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11}
pctochar = {0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'}

# Get scaletype & chordtype data
with open('chordlib.json','r') as rdata:
    chordlib = json.load(rdata)
    rdata.close()

dchordtype = chordlib['dchordtype']
dscaletype = chordlib['dscaletype']

# Input & Output
def generateprog():
    print('Please enter your parameters to generate a new progression!')
    print('***********************************************************')
    time.sleep(1)
    x = ChordProg.getprog()
    print('***********************************************************')
    time.sleep(1)
    x.printprog()

def generatesong():
    print('Please enter your parameters to generate a new song!')
    print('***********************************************************')
    time.sleep(1)
    x = Song.getsong()
    print('***********************************************************')
    time.sleep(1)
    x.printprog()

generatesong()




