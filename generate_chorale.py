from music21 import stream, note, metadata, key, meter, clef

def build_chorale(output_name="chorale_output.xml"):
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "D Minor Chorale (Final)"
    score.metadata.composer = "Stephen"

    k = key.Key("d")
    ts = meter.TimeSignature("4/4")

    # Create and configure parts
    upper = stream.Part(id="UpperStaff")
    lower = stream.Part(id="LowerStaff")
    for p, cl in [(upper, clef.TrebleClef()), (lower, clef.BassClef())]:
        p.append(cl)
        p.append(k)
        p.append(ts)

    # Define voices
    soprano = stream.Voice(id="Soprano")
    alto    = stream.Voice(id="Alto")
    tenor   = stream.Voice(id="Tenor")
    bass    = stream.Voice(id="Bass")

    # Helper to add chords
    def add_chord(s, a, t, b, dur=2):
        soprano.append(note.Note(s, quarterLength=dur))
        alto.append(note.Note(a, quarterLength=dur))
        tenor.append(note.Note(t, quarterLength=dur))
        bass.append(note.Note(b, quarterLength=dur))

    # Add the chord progression
    add_chord("D5", "F4", "D4", "D3")        # i
    add_chord("E5", "G4", "Bb3", "D3")       # ii65
    add_chord("A4", "C#4", "E3", "G2")       # V7
    add_chord("Bb4", "D4", "F3", "Bb2")      # VI
    add_chord("G4", "Bb3", "D3", "G2")       # iv
    add_chord("A4", "C#4", "E3", "G2")       # V7
    add_chord("D5", "F4", "A3", "D3", 4)     # final i

    # Attach voices to parts
    upper.append(soprano)
    upper.append(alto)
    lower.append(tenor)
    lower.append(bass)

    # Add parts to score
    score.insert(0, upper)
    score.insert(0, lower)

    # Export
    score.write('musicxml', fp=output_name)
    print(f"Written {output_name}")

if __name__ == "__main__":
    build_chorale()
