from music21 import stream, note, metadata, key, meter, clef

def build_chorale(title="D Minor Chorale Example", output_name="chorale_output.xml"):
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = title
    score.metadata.composer = "Stephen"

    key_sig = key.Key("d")
    time_sig = meter.TimeSignature("4/4")

    upper = stream.Part(id='UpperStaff')
    lower = stream.Part(id='LowerStaff')
    upper.append(clef.TrebleClef())
    lower.append(clef.BassClef())

    for part in [upper, lower]:
        part.append(key_sig)
        part.append(time_sig)

    # Create voices
    soprano = stream.Voice(id='Soprano')
    alto = stream.Voice(id='Alto')
    tenor = stream.Voice(id='Tenor')
    bass = stream.Voice(id='Bass')

    def add_chord(s, a, t, b, dur=2):
        soprano.append(note.Note(s, quarterLength=dur))
        alto.append(note.Note(a, quarterLength=dur))
        tenor.append(note.Note(t, quarterLength=dur))
        bass.append(note.Note(b, quarterLength=dur))

    # Chord progression: i - ii65 - V7 - VI - iv - V7 - i
    add_chord("D5", "A4", "F3", "D3")        # i
    add_chord("F4", "D4", "G3", "E3")        # ii65 (E G Bb D)
    add_chord("E4", "C#4", "G3", "A2")       # V7 (A C# E G)
    add_chord("F4", "D4", "D3", "Bb2")       # VI (Bb D F)
    add_chord("D5", "G4", "Bb3", "G2")       # iv (G Bb D)
    add_chord("E4", "C#4", "G3", "A2")       # V7 again
    add_chord("D5", "A4", "F3", "D3", 4)     # i - whole notes

    upper.append(soprano)
    upper.append(alto)
    lower.append(tenor)
    lower.append(bass)

    score.insert(0, upper)
    score.insert(0, lower)

    score.write('musicxml', fp=output_name)

if __name__ == "__main__":
    build_chorale()
