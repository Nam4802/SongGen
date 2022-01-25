from midiutil import MIDIFile

# FUNCTION TO ADD A CHORD TO MIDI TRACK
def addChordMidi(midiobj, track: int, channel: int, chord: list, timesig: list, starttime: float):
    for i in range(timesig[0]):                     # Loop to add each time a chord is played according to the number of notes in bar
        for j in range(1, len(chord)):              # Loop to add notes of the current chord
                if j == 1:
                    tracker = 0
                elif (chord[j] - chord[j - 1]) < 0: # Increase pitch if the pitch class of current note is smaller than the previous note
                    tracker += 12
                midiobj.addNote(track, channel, chord[j] + 48 + tracker, starttime, duration = 4 / timesig[1], volume = 70)
        starttime += 4 / timesig[1]                 # starttime is in quarter notes

# FUNCTION TO ADD A RIFF TO MIDI TRACK
def addRiffMidi(midiobj, track: int, channel: int, riff: list, starttime: float):
    for note in riff:
        midinote = note[0] + 12 * (note[1] + 1)
        duration = note[2]
        midiobj.addNote(track, channel, midinote, starttime, duration, volume = 100)
        starttime += duration