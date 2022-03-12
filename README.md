# Random Song Generator
A program to randomly generate songs with chords and notes as midi files.

## Data Structure
### Chord
A Chord is a list containing the following elements in the same order:
- Chord type (ex: '', 'm', 'm7'...): **str**
- Root note of chord (in pitch class): **int**
- Other notes (in pitch class), with each notes being another item in the list: **int**
	> Example: F minor triad - ['m', 5, 8, 0]

### Note
A note is a list containing the following elements in the same order: 
- Pitch class (0 to 11): **int**
- Octave number (with 4 being the middle C): **int**
- Note duration in quarter notes: **float**
	> Example: A3 half note - [9, 3, 2]

### Prog (progression)
A prog (short for progression) is a list containing chords that make up a music progressions.
	> Example: C G Am F progression - [['', 0, 4, 7], ['', 7, 11, 2], ['m', 9, 0, 4], ['', 5, 9, 0]]

### Riff
A riff is a list containing smaller lists notes. Each smaller lists correspond to a chord (containing notes in that chord), and the whole riff correspond to a progression.
	> Example: [
	> [[0, 5, 0.25], [0, 5, 0.25], [4, 4, 1], [0, 5, 0.25], [0, 4, 2], [4, 5, 0.25]],
	> [[7, 4, 4]],
	> [[9, 4, 0.5], [4, 5, 0.5], [9, 5, 1], [9, 4, 1], [9, 5, 0.5], [0, 3, 0.25], [0, 4, 0.25]],
	> [[5, 3, 2], [0, 3, 0.25], [9, 3, 0.25], [5, 5, 0.5], [5, 3, 0.25], [5, 4, 0.5], [9, 5, 0.25]]
	> ]