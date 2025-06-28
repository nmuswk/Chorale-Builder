from music21 import converter, note, chord, stream

def extract_voices(score):
    # Assume score.parts[0] = upper staff (Soprano + Alto)
    # and score.parts[1] = lower staff (Tenor + Bass)
    upper = score.parts[0].flat.getElementsByClass(note.Note)
    lower = score.parts[1].flat.getElementsByClass(note.Note)

    # Divide evenly: alternating between soprano/alto and tenor/bass
    soprano = upper[::2]
    alto = upper[1::2]
    tenor = lower[::2]
    bass = lower[1::2]

    return soprano, alto, tenor, bass

def check_spacing(s, a, t, b):
    errors = []

    for i, (sNote, aNote, tNote, bNote) in enumerate(zip(s, a, t, b)):
        if abs(sNote.pitch.midi - aNote.pitch.midi) > 12:
            errors.append(f"Measure {i+1}: Soprano and Alto more than an octave apart")
        if abs(aNote.pitch.midi - tNote.pitch.midi) > 12:
            errors.append(f"Measure {i+1}: Alto and Tenor more than an octave apart")
    return errors

def check_voice_crossing(s, a, t, b):
    errors = []
    for i, (sNote, aNote, tNote, bNote) in enumerate(zip(s, a, t, b)):
        if aNote.pitch > sNote.pitch:
            errors.append(f"Measure {i+1}: Alto crosses above Soprano")
        if tNote.pitch > aNote.pitch:
            errors.append(f"Measure {i+1}: Tenor crosses above Alto")
        if bNote.pitch > tNote.pitch:
            errors.append(f"Measure {i+1}: Bass crosses above Tenor")
    return errors

def check_parallel_intervals(part1, part2, interval_name="P5"):
    from music21 import interval
    errors = []
    for i in range(len(part1)-1):
        int1 = interval.Interval(part1[i], part2[i])
        int2 = interval.Interval(part1[i+1], part2[i+1])
        if int1.simpleName == interval_name and int2.simpleName == interval_name:
            errors.append(f"Parallel {interval_name} between measures {i+1} and {i+2}")
    return errors

def validate_chorale(xml_path="chorale_output.xml"):
    score = converter.parse(xml_path)
    soprano, alto, tenor, bass = extract_voices(score)

    errors = []
    errors += check_spacing(soprano, alto, tenor, bass)
    errors += check_voice_crossing(soprano, alto, tenor, bass)
    errors += check_parallel_intervals(soprano, bass, "P5")
    errors += check_parallel_intervals(tenor, bass, "P5")
    errors += check_parallel_intervals(soprano, bass, "P8")
    errors += check_parallel_intervals(tenor, bass, "P8")

    if errors:
        print("❌ Errors found:")
        for e in errors:
            print("  -", e)
        exit(1)
    else:
        print("✅ Chorale passed all checks.")

if __name__ == "__main__":
    validate_chorale()
