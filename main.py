'''
Author: Kyle Yang
Creation Date: November 18
Last Modified: December 30
Project Description: Plays music. Letters represent pitches in the melody.
Beats, motifs, and chords in the music are randomly generated using rules.
Each of the letters that fall down have a random size, color, and centerX.
Instructions: Click the screen to play music. Click pause to pause the music.
Click restart to restart the music. Click volume to change volume on and off.
Credits: None
Updates: None
Rubric Items:
    Beat Class: Line 75
    Beat Pattern 1: Line 156, Line 158
    Beat Pattern 2: Line 157, Line 159
    Beat Rules: Line 120
    Motif Class: Line 167
    Motif Transformation: Line 217
    Melody Rules: Line 173
    Chord Class: Line 311
    Harmonize a note: Line 340
    Chord Transition Rules: Line 348, Line 350
    Art Randomness: Lines 385-387
    Art Rule 1: Line 385
    Art Rule 2: Line 386
    Art Rule 3: Line 387
    Play/Pause: Line 359
    Restart: Line 362
    Volume: Line 365
'''

# main
def main():
    motif.initializeRules()
    beat.createDrumPattern()
    motif.createMelody()
    rootsList = [ ]
    for note in motif.melody.notes:
        rootsList.append(note.pitch)
    chord.createChords(rootsList)

# constants
app.beatsPerMinute = 100

# globals
app.background = 'skyBlue'

# classes
class GUI(object):
    # GUI Class
    def play(self, shouldLoop, shouldRestart):
        # Plays the chord.
        for sequencer in self.sequencers:
            sequencer.play(loop=shouldLoop, restart=shouldRestart)

    def pause(self):
        # Pauses the chord.
        for sequencer in self.sequencers:
            sequencer.pause()
    
    def volume(self):
        # Turns off or turns on the volume of the chord.
        for sequencer in self.sequencers:
            if sequencer.volume == 0:
                sequencer.volume = 0.6
            else:
                sequencer.volume = 0

class Rule(object):
    # Rule Class
    def __init__(self, degrees, probability):
        self.degrees = degrees
        self.probability = probability

class Beat(GUI):
    # Beat Class
    def __init__(self):
        self.kick = Sequencer(tuple(), instrument='kick-drum', name='kick')
        self.snare = Sequencer(tuple(), instrument='snare-drum', name='snare')
        self.sequencers = [self.kick, self.snare]
    
    def createList(self, val, numVal):
        # Creates a list with multiple of the same value.
        lst = [ ]
        for i in range(numVal):
            lst.append(val)
        return lst
    
    def copyList(self, listToCopy, startIndex, endIndex):
        # Copies part of a list from startIndex to endIndex.
        newList = [ ]
        for index in range(startIndex, endIndex):
            newList.append(listToCopy[index])
        return newList
    
    def substituteBeads(self, bracelet, index):
        # Writes code to complete Step 5, then returns two lists: a new bracelet list,
        # and a new unusedBeads list.
        # Moves all elements in the bracelet after the index to the empty unusedBeads.
        newBracelet = self.copyList(bracelet, 0, index)
        newUnusedBeads = self.copyList(bracelet, index, len(bracelet))
        return newBracelet, newUnusedBeads
    
    def addBeads(self, bracelet, unusedBeads):
        # This function performs steps 3 and 4 of the algorithm. They are:
        # 3. Starts an index at 0.
        # 4. Until the unusedBeads list is empty:
        #      Removes an element and adds it to the element at the index in bracelet.
        #      Updates the index.
        index = 0
        while (unusedBeads != [ ]):
            prevVal = bracelet[index]
            newRemainder = unusedBeads.pop()
            bracelet[index] = bracelet[index] + newRemainder
            index = (index + 1) % len(bracelet)
    
        # Performs step 5.
        return self.substituteBeads(bracelet, index)
    
    def generateRhythm(self, numBeats, numRests, offset):
        # Creates the bracelet and unusedBeads lists and fills them with 'X' and '.'s.
        bracelet = self.createList('X', numBeats)
        unusedBeads = self.createList('.', numRests)
        
        # Loops until all rests are evenly distributed among the beats.
        while ((len(bracelet) > 1) and (len(unusedBeads) > 1)):
            bracelet, unusedBeads = self.addBeads(bracelet, unusedBeads)
        rhythm = ''
        for c in bracelet:
            rhythm += c
        for c in unusedBeads:
            rhythm += c
        offsetRhythm = ''
        for i in range(len(rhythm)):
            if (i < offset):
                offsetRhythm += '.'
            else:
                offsetRhythm += rhythm[i - offset]
        return offsetRhythm
    
    def decodePattern(self, pattern, beatNote, restNote):
        # Converts the 'X' and '.'s to beats and rests.
        notes = [ ]
        for character in pattern:
            if (character == 'X'):
                notes.append(beatNote)
            else:
                notes.append(restNote)
        return tuple(notes)
    
    def createDrumPattern(self):
        # Creates the beat pattern for the rhythm.
        beat1 = Note('C', 3, 1/10, velocity=1)
        beat2 = Note('C', 3, 1/10, velocity=1)
        rest = Note(None, 1, 1/10, velocity=0)
        kickPattern1 = self.generateRhythm(randrange(5,10), randrange(20,30), 0)
        kickPattern2 = self.generateRhythm(randrange(5,10), randrange(5,10), 0)
        snarePattern1 = self.generateRhythm(4, 28, 2)
        snarePattern2 = self.generateRhythm(2, 14, 3)
        kickPattern = (kickPattern1 + kickPattern2 + kickPattern1 + kickPattern2 +
                       kickPattern1 + kickPattern2 + kickPattern2)
        snarePattern = (snarePattern1 + snarePattern2 + snarePattern1 +
                        snarePattern2 + snarePattern1 + snarePattern2 + snarePattern2)
        self.kick.notes = self.decodePattern(kickPattern, beat1, rest)
        self.snare.notes = self.decodePattern(snarePattern, beat2, rest)

class Motif(GUI):
    # Motif Class
    def __init__(self):
        self.melody = Sequencer(tuple(), instrument='organ', name='melody')
        self.sequencers = [self.melody]
    
    def initializeRules(self):
        # Creates a list of rules and adds them to app.rules.
        commonRules = [ [ 1, 1 ], [ -1, -1 ], [ 2, -1 ], [ -2, 1 ] ]
        uncommonRules = [ [ 2, 2 ], [ -2, -2 ], [ 3, 1 ], [ -1, -3 ] ]
        rareRules = [ [ 6, -1 ], [ -6, 1 ], [ 7, -7 ] ]
        for rule in commonRules:
            app.rules.append(Rule(rule, 100))
        for rule in uncommonRules:
            app.rules.append(Rule(rule, 75))
        for rule in rareRules:
            app.rules.append(Rule(rule, 50))
    
    def getNextRule(self):
        # Gets a random rule from app.rules as the next rule.
        nextRule = choice(app.rules)
        chance = randrange(0, 100)
        while (nextRule.probability < chance):
            nextRule = choice(app.rules)
        return nextRule
    
    def generateMotif(self, numNotes):
        # Creates a motif or list of degrees using rules.
        motifDegrees = [ ]
        while (len(motifDegrees) < numNotes):
            rule = self.getNextRule()
            for degree in rule.degrees:
                if (len(motifDegrees) < numNotes):
                    motifDegrees.append(degree)
        return motifDegrees
    
    def createMelodyFromMotif(self, motif, scale, index):
        # Creates a melody using the motif, scale, and index.
        notes = [ ]
        scaleNotes = app.scales[scale]
        prevNote = scaleNotes[index]
        prevNote.scaleIndex = index
        for degree in motif:
            scaleIndex = (degree + prevNote.scaleIndex) % len(scaleNotes)
            note = scaleNotes[scaleIndex]
            note.scaleIndex = scaleIndex
            notes.append(note)
            prevNote = note
        return tuple(notes)
    
    def generateTransformation(self, transformation, scale, motif):
        # Transforms the motif into a sequential, inverted, or retrograde pattern.
        if (transformation == 'normal'):
            notes = self.createMelodyFromMotif(motif, scale, 0)
        elif (transformation == 'sequential'):
            notes = self.createMelodyFromMotif(motif, scale, 2)
        elif (transformation == 'inverted'):
            invertedMotif = [ ]
            for degree in motif:
                invertedMotif.append(degree * -1)
            notes = self.createMelodyFromMotif(invertedMotif, scale, 0)
        elif (transformation == 'retrograde'):
            normalNotes = self.createMelodyFromMotif(motif, scale, 0)
            retrogradeNotes = [ ]
            for noteIndex in range(len(normalNotes) - 1, -1, -1):
                retrogradeNotes.append(normalNotes[noteIndex])
            notes = tuple(retrogradeNotes)
        if (transformation == 'sequential-inverted'):
            invertedMotif = [ ]
            for degree in motif:
                invertedMotif.append(degree * -1)
            notes = self.createMelodyFromMotif(invertedMotif, scale, 3)
        return notes

    def createMelody(self):
        # Creates the melody for the music.
        rest = Note(None, 1, 1/10, velocity=0)
        scale1 = choice([ 'C Major', 'G Major' ])
        if (scale1 == 'C Major'):
            scale2 = 'G Major'
        else:
            scale2 = 'C Major'
        motif1 = self.generateMotif(10)
        motif2 = self.generateMotif(20)
    
        # verse
        notes1 = self.generateTransformation('normal', scale1, motif1)
        notes2 = self.generateTransformation('sequential', scale1, motif1)
    
        # chorus
        notes3 = self.generateTransformation('inverted', scale1, motif2)
        notes4 = self.generateTransformation('retrograde', scale1, motif2)
    
        # bridge
        notes5 = self.generateTransformation('sequential-inverted', scale1, motif1)
        notes6 = self.generateTransformation('sequential-inverted', scale2, motif1)
    
        # verse 1
        notes = [ ]
        for i in range(2):
            for note in notes1:
                notes.append(note)
        notes.pop()
        notes.append(rest)
    
        # chorus
        for note in notes3:
            notes.append(note)
        notes.pop()
        notes.append(rest)
    
        # verse 2
        for i in range(2):
            for note in notes1:
                notes.append(note)
        for i in range(2):
            for note in notes2:
                notes.append(note)
        notes.pop()
        notes.append(rest)
    
        # chorus
        for note in notes3:
            notes.append(note)
        notes.pop()
        notes.append(rest)
    
        # bridge
        for i in range(2):
            for note in notes5:
                notes.append(note)
        for i in range(2):
            for note in notes6:
                notes.append(note)
        notes.pop()
        notes.append(rest)
    
        # final chorus
        for note in notes3:
            notes.append(note)
        for note in notes4:
            notes.append(note)
        self.melody.notes = tuple(notes)

class Chord(GUI):
    # Chord Class
    def __init__(self, numSequencers):
        self.sequencers = [ ]
        for i in range(numSequencers):
            self.sequencers.append(Sequencer(tuple([ ]), instrument='wave'))
    
    def addNote(self, sequencer, newNote):
        # Adds a note to the sequencer.
        currentNotes = list(sequencer.notes)
        currentNotes.append(newNote)
        sequencer.notes = tuple(currentNotes)
    
    def addChords(self, chordsList):
        # Adds chords for the sequencers.
        for chord in chordsList:
            rootNote = Note(chord[0], 3, 1/10)
            for index in range(len(self.sequencers)):
                sequencer = self.sequencers[index]
                if (index == 0):
                    self.addNote(sequencer, rootNote)
                elif (index < len(chord)):
                    semitone = chord[index]
                    newNote = rootNote.getNote(semitone)
                    newNote.velocity = 0.3
                    self.addNote(sequencer, newNote)
                else:
                    self.addNote(sequencer, Note(None, 3, rootNote.duration))

    def createChords(self, rootsList):
        # Creates a list of chord semitones that .addChords can use to create Note
        # instances at random to its sequencers. The first chord is a major chord,
        # then minor, then diminished, then major seventh. Chords picked randomly.
        # chordsList is a list of root pitch, smallSemitone, bigSemitone sublists.
        chordsList = [ ]
        for root in rootsList:
            if rootsList.index(root) % 2 == 0:
                chordsList.append(choice([(root,4,7),(root,3,7)]))
            else:
                chordsList.append(choice([(root,3,6),(root,4,7,10)]))
        self.addChords(chordsList)

beat = Beat()
motif = Motif()
chord = Chord(4)

# groups
letters = Group()
pause = Group(
                Rect(30,350,60,30),
                Label('Pause',60,365,fill='white',size=15))
restart = Group(
                Rect(100,350,60,30),
                Label('Restart',130,365,fill='white',size=15))
volume = Group(
                Rect(170,350,60,30),
                Label('Volume',200,365,fill='white',size=15))

# lists
app.rules = [ ]

# dictionaries
app.scales = {
    'C Major': [ Note('C', 4, 1/10), Note('D', 4, 1/10), Note('E', 4, 1/10),
                Note('F', 4, 1/10), Note('G', 4, 1/10), Note('A', 4, 1/10),
                Note('B', 4, 1/10), Note('C', 5, 1/10) ],
    'G Major': [ Note('G', 4, 1/10), Note('A', 4, 1/10), Note('B', 4, 1/10),
                Note('C', 5, 1/10), Note('D', 5, 1/10), Note('E', 5, 1/10),
                Note('F#', 5, 1/10), Note('G', 5, 1/10) ]
    }

# functions
def makeLetter(pitch):
    # Makes a letter with a random size, color, and centerX.
    size = randrange(10,30)
    color = choice(['red','green','blue'])
    centerX = randrange(100,300)
    letter = Label(pitch,centerX,0,size=size,fill=color,bold=True)
    letters.add(letter)

# onMousePress
def onMousePress(mouseX,mouseY):
    if volume.hits(mouseX,mouseY):
        beat.volume()
        motif.volume()
        chord.volume()
    elif restart.hits(mouseX,mouseY):
        beat.play(True,True)
        motif.play(True,True)
        chord.play(True,True)
    elif pause.hits(mouseX,mouseY):
        beat.pause()
        motif.pause()
        chord.pause()
    else:
        beat.play(True,False)
        motif.play(True,False)
        chord.play(True,False)

# onSignal
def onSignal(noteSignals):
    if noteSignals[0][1] == 'kick':
        if app.background == 'skyBlue':
            app.background = 'darkRed'
        else:
            app.background = 'skyBlue'
    for signal in noteSignals:
        if signal[1] == 'melody':
            if signal[0].pitch != None:
                makeLetter(signal[0].pitch)

# onStep
def onStep():
    for letter in letters:
        if letter.centerY > 400:
            letters.remove(letter)
        else:
            letter.centerY += 10

main()
