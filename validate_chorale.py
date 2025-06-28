from music21 import converter, interval, pitch, note

voice_ranges = {
    'S': ('C4', 'G5'),
    'A': ('F3', 'D5'),
    'T': ('C3', 'G4'),
    'B': ('E2', 'C4')
}

def extract_voices(score):
    soprano = score.parts[0].getElementsByClass('Voice')[0]
    alto = score.parts[0].getElementsByClass('Voice')[1]
    tenor = score.parts[1].getElementsByClass('Voice')[0]
    bass = score.parts[1].getElementsByClass('Voice')[1]
    return {'S': soprano, 'A': alto, 'T': tenor, 'B': bass}

def spacing_and_crossing(voices):
    errors = []
    pairs = [('S', 'A'), ('A', 'T'), ('T', 'B')]
    for i in range(len(voices['S'])):
        for v1, v2 in pairs:
            n1, n2 = voices[v1][i], voices[v2][i]
            if n1.isNote and n2.isNote:
                iv = interval.Interval(n1, n2)
                if iv.semitones < 0:
                    errors.append(f"Voice crossing: {v1} below {v2} at note {i}")
                if v1 in ['S', 'A'] and iv.semitones > 12:
                    errors.append(f"Spacing too wide between {v1}-{v2} at note {i}")
    return errors

def parallels(voices):
    errors = []
    def check(v1, v2, label):
        for i in range(len(voices[v1])-1):
            n1a, n1b = voices[v1][i], voices[v2][i]
            n2a, n2b = voices[v1][i+1], voices[v2][i+1]
            if all(n.isNote for n in [n1a, n1b, n2a, n2b]):
                iv1 = interval.Interval(n1a, n1b)
                iv2 = interval.Interval(n2a, n2b)
                if iv1.simpleName in ['P5', 'P8'] and iv1.simpleName == iv2.simpleName:
                    errors.append(f"Parallel {iv1.simpleName} in {label} at notes {i}-{i+1}")
    for v1, v2 in [('S', 'B'), ('A', 'B'), ('T', 'B'), ('S', 'A'), ('S', 'T')]:
        check(v1, v2, f"{v1}-{v2}")
    return errors

def unresolved_sevenths(voices):
    errors = []
    for i in range(len(voices['S'])-1):
        for part in voices:
            n1 = voices[part][i]
            n2 = voices[part][i+1]
            if all(n.isNote for n in [n1, n2]):
                if n1.name == 'G' and n2.name != 'F':
                    errors.append(f"Unresolved 7th (G) in {part} at note {i}")
    return errors

def leading_tone_resolution(voices):
    errors = []
    for i in range(len(voices['S'])-1):
        for part in ['S', 'A']:
            n1 = voices[part][i]
            n2 = voices[part][i+1]
            if all(n.isNote for n in [n1, n2]):
                if n1.name == 'C#' and n2.name != 'D':
                    errors.append(f"Leading tone (C#) in {part} at note {i} does not resolve to D")
    return errors

def range_check(voices):
    errors = []
    for part, notes in voices.items():
        lo = pitch.Pitch(voice_ranges[part][0])
        hi = pitch.Pitch(voice_ranges[part][1])
        for i, n in enumerate(notes):
            if n.isNote and not (lo <= n.pitch <= hi):
                errors.append(f"{part} out of range at note {i}: {n.nameWithOctave}")
    return errors

def hidden_intervals(voices):
    errors = []
    for i in range(len(voices['S']) - 1):
        s1, s2 = voices['S'][i], voices['S'][i+1]
        b1, b2 = voices['B'][i], voices['B'][i+1]
        if all(n.isNote for n in [s1, s2, b1, b2]):
            iv1 = interval.Interval(s1, s2)
            iv2 = interval.Interval(b1, b2)
            soprano_leaps = iv1.semitones > 2
            if soprano_leaps and iv1.direction == iv2.direction:
                final_iv = interval.Interval(s2, b2).simpleName
                if final_iv in ['P5', 'P8']:
                    errors.append(f"Hidden {final_iv} between S-B at notes {i}-{i+1}")
    return errors

def cadence_check(voices):
    errors = []
    # Final two notes in S
    if len(voices['S']) >= 2:
        last, penult = voices['S'][-1], voices['S'][-2]
        if last.isNote and penult.isNote:
            if penult.name == 'A' and last.name == 'D':
                errors.append("Soprano leaps 5-1 at cadence (A to D)")
    return errors

def validate_chorale(filename='chorale_output.xml'):
    score = converter.parse(filename)
    voices = extract_voices(score)

    checks = [
        spacing_and_crossing,
        parallels,
        unresolved_sevenths,
        leading_tone_resolution,
        range_check,
        hidden_intervals,
        cadence_check
    ]

    all_errors = []
    for check in checks:
        all_errors.extend(check(voices))

    if all_errors:
        print("❌ Errors found:")
        for err in all_errors:
            print("  -", err)
        exit(1)
    else:
        print("✅ Chorale passed all checks.")

if __name__ == "__main__":
    validate_chorale()
