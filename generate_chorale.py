from music21 import stream, note, metadata, key, meter, clef

def build_chorale(title, chords, output_name="chorale_output.xml", key_sig="d", time_sig="4/4"):
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = title
    score.metadata.composer = "Stephen"

    key_obj = key.Key(key_sig)
    time_obj = meter.TimeSignature(time_sig)

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
        # i (D minor): D - A - F - D
        ("D5", "A4", "F3", "D3"),
        # ii65 (E half-dim7 in 1st inv): F - D - Bb - G
        ("F4", "D4", "Bb3", "G2"),
        # V7 (A7): E - C# - G - A
        ("E5", "C#4", "G3", "A2"),
        # VI (Bb major): F - D - Bb - Bb
        ("F4", "D4", "Bb3", "Bb2"),
        # iv (G minor): G - D - Bb - G
        ("G4", "D4", "Bb3", "G2"),
        # V7 again (A7): E - C# - G - A
        ("E5", "C#4", "G3", "A2"),
        # i (D minor), whole notes: D - A - F - D
        ("D5", "A4", "F3", "D3", 4),
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
    return output_name

build_chorale("D Minor Chorale Example", [])
