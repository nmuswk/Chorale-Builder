from music21 import stream, note, metadata, key, meter, clef
#trigger build
def build_chorale(output_name="chorale_output.xml"):
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "D Minor Chorale Example"
    score.metadata.composer = "Stephen"

    key_obj = key.Key("d")
    time_obj = meter.TimeSignature("4/4")

    upper = stream.Part(id='UpperStaff')
    lower = stream.Part(id='LowerStaff')
    upper.append(clef.TrebleClef())
    lower.append(clef.BassClef())
    for part in [upper, lower]:
        part.append(key_obj)
        part.append(time_obj)

    soprano = stream.Voice(id='Soprano')
    alto = stream.Voice(id='Alto')
    tenor = stream.Voice(id='Tenor')
    bass = stream.Voice(id='Bass')

    def add_chord(sop, alt, ten, bas, durs=2):
        notes = [(soprano, sop), (alto, alt), (tenor, ten), (bass, bas)]
        if isinstance(durs, int): durs = [durs] * 4
        for (v, p), dur in zip(notes, durs):
            if str(p).lower() == 'rest':
                v.append(note.Rest(quarterLength=dur))
            else:
                v.append(note.Note(p, quarterLength=dur))

    chords = [
        ("D5", "F4", "D4", "D3"),       # i
        ("D4", "E4", "Bb3", "G2"),     # ii65
        ("G4", "C#4", "E3", "A2"),     # V7
        ("F4", "D4", "F3", "Bb2"),     # VI
        ("A4", "Bb3", "D3", "G2"),     # iv
        ("F4", "C#4", "E3", "A2"),     # V7
        ("D5", "F4", "A3", "D3", 4),   # i
    ]

    for chord in chords:
        add_chord(*chord)

    upper.append(soprano)
    upper.append(alto)
    lower.append(tenor)
    lower.append(bass)
    score.insert(0, upper)
    score.insert(0, lower)

    score.write('musicxml', fp=output_name)
    print(f"Chorale written to {output_name}")

if __name__ == "__main__":
    build_chorale()
