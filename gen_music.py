"""Generate all chiptune music WAV files for Hero of the Water."""
import os, math, wave, struct

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
NOTE_FREQS = {
    'C3':130.81,'D3':146.83,'E3':164.81,'F3':174.61,'G3':196.00,
    'A3':220.00,'B3':246.94,'C4':261.63,'D4':293.66,'E4':329.63,
    'F4':349.23,'G4':392.00,'A4':440.00,'B4':493.88,'C5':523.25,
    'D5':587.33,'E5':659.25,'F5':698.46,'G5':783.99,'A5':880.00,
    'Bb3':233.08,'Eb4':311.13,'Ab3':207.65,'Bb4':466.16,
    'F#4':369.99,'G#4':415.30,'Db4':277.18,'Gb4':369.99,'R':0,
}

def sq(freq, dur, sr=22050, vol=0.3):
    s = []
    p = sr / freq if freq > 0 else sr
    for i in range(int(sr * dur)):
        if freq <= 0:
            s.append(0)
        else:
            s.append(vol if (i % int(p)) < int(p / 2) else -vol)
    return s

def sn(freq, dur, sr=22050, vol=0.2):
    s = []
    for i in range(int(sr * dur)):
        if freq <= 0:
            s.append(0)
        else:
            s.append(vol * math.sin(2 * math.pi * freq * i / sr))
    return s

def mx(t1, t2):
    l = max(len(t1), len(t2))
    return [max(-1.0, min(1.0, (t1[i] if i < len(t1) else 0) + (t2[i] if i < len(t2) else 0))) for i in range(l)]

def ww(fn, samples, sr=22050):
    fp = os.path.join(GAME_DIR, fn)
    with wave.open(fp, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        buf = bytearray(len(samples) * 4)
        for i, s in enumerate(samples):
            v = int(max(-32767, min(32767, s * 32767)))
            struct.pack_into('<hh', buf, i * 4, v, v)
        wf.writeframes(bytes(buf))
    print(f"  {fn}: {os.path.getsize(fp)} bytes")

def melody(notes, dur, sr=22050, vol=0.25):
    s = []
    fd = int(sr * 0.01)
    for n in notes:
        f = NOTE_FREQS.get(n, 0)
        t = sq(f, dur, sr, vol)
        for i in range(min(fd, len(t))):
            t[i] *= i / fd
        for i in range(min(fd, len(t))):
            t[len(t) - 1 - i] *= i / fd
        s.extend(t)
    return s

def bass(notes, dur, sr=22050, vol=0.15):
    s = []
    for n in notes:
        f = NOTE_FREQS.get(n, 0)
        s.extend(sn(f, dur, sr, vol))
    return s

# Menu: dreamy, welcoming
print("Menu...")
m = ['C4','R','E4','G4','R','C5','R','R','G4','R','E4','R','C4','R','R','R',
     'F4','R','A4','C5','R','A4','R','R','G4','R','F4','E4','R','R','C4','R',
     'C4','R','G4','R','E4','R','C5','R','E5','R','C5','R','G4','E4','C4','R']
b = ['C3','C3','C3','C3','E3','E3','E3','E3','G3','G3','G3','G3','C3','C3','C3','C3',
     'F3','F3','F3','F3','A3','A3','A3','A3','G3','G3','G3','G3','E3','E3','C3','C3',
     'C3','C3','G3','G3','E3','E3','C3','C3','F3','F3','A3','A3','G3','G3','C3','C3']
ww('music_menu.wav', mx(melody(m, 0.35, vol=0.18), bass(b, 0.35, vol=0.10)))

# Phase 1: calm, pentatonic nature
print("Phase 1...")
m = ['C4','D4','E4','G4','A4','G4','E4','D4','C4','E4','G4','A4','C5','A4','G4','E4',
     'G4','A4','C5','D5','C5','A4','G4','E4','D4','E4','G4','A4','G4','E4','D4','C4',
     'E4','G4','A4','C5','R','A4','G4','E4','D4','C4','D4','E4','G4','E4','D4','C4']
b = ['C3','C3','C3','C3','G3','G3','G3','G3','A3','A3','A3','A3','E3','E3','E3','E3',
     'G3','G3','G3','G3','D3','D3','D3','D3','C3','C3','C3','C3','G3','G3','C3','C3',
     'A3','A3','E3','E3','G3','G3','C3','C3','D3','D3','E3','E3','G3','G3','C3','C3']
ww('music_phase1.wav', mx(melody(m, 0.30, vol=0.18), bass(b, 0.30, vol=0.11)))

# Phase 2: tense, urban, D minor
print("Phase 2...")
m = ['D4','R','F4','R','A4','Bb4','A4','F4','D4','E4','F4','A4','Bb4','A4','R','D4',
     'F4','G4','Bb4','A4','F4','D4','R','E4','F4','A4','D5','Bb4','A4','F4','E4','D4',
     'D4','F4','A4','Bb4','R','A4','G4','F4','E4','D4','F4','A4','Bb4','A4','D4','R']
b = ['D3','D3','D3','D3','F3','F3','A3','A3','Bb3','Bb3','A3','A3','D3','D3','D3','D3',
     'G3','G3','Bb3','Bb3','F3','F3','D3','D3','A3','A3','D3','D3','Bb3','Bb3','A3','A3',
     'D3','D3','F3','F3','Bb3','Bb3','A3','A3','G3','G3','Bb3','Bb3','D3','D3','D3','D3']
ww('music_phase2.wav', mx(melody(m, 0.20, vol=0.25), bass(b, 0.20, vol=0.16)))

# Phase 3: warm, emotional, F major
print("Phase 3...")
m = ['F4','R','A4','R','C5','R','F5','R','R','C5','R','A4','R','F4','R','R',
     'G4','R','Bb4','R','D5','R','F5','R','R','D5','R','Bb4','R','G4','R','R',
     'A4','R','C5','R','F5','R','R','C5','Bb4','R','A4','R','F4','R','R','R']
b = ['F3','F3','F3','F3','A3','A3','A3','A3','C3','C3','C3','C3','F3','F3','F3','F3',
     'G3','G3','G3','G3','Bb3','Bb3','Bb3','Bb3','D3','D3','D3','D3','G3','G3','G3','G3',
     'A3','A3','A3','A3','F3','F3','F3','F3','Bb3','Bb3','A3','A3','F3','F3','F3','F3']
ww('music_phase3.wav', mx(melody(m, 0.38, vol=0.20), bass(b, 0.38, vol=0.12)))

# Phase 4: mechanical, A minor
print("Phase 4...")
m = ['A4','C5','A4','C5','E5','C5','E5','C5','A4','C5','A4','C5','B4','A4','B4','A4',
     'E4','A4','E4','A4','C5','A4','C5','A4','D5','C5','D5','C5','B4','A4','B4','A4',
     'A4','E4','A4','E4','C5','B4','C5','B4','A4','C5','A4','E4','A4','E4','A4','R']
b = ['A3','A3','A3','A3','E3','E3','E3','E3','A3','A3','A3','A3','E3','E3','E3','E3',
     'C3','C3','C3','C3','A3','A3','A3','A3','D3','D3','D3','D3','E3','E3','E3','E3',
     'A3','A3','E3','E3','A3','A3','E3','E3','A3','A3','A3','A3','E3','E3','A3','A3']
ww('music_phase4.wav', mx(melody(m, 0.22, vol=0.23), bass(b, 0.22, vol=0.15)))

# Phase 5: epic, intense, E minor
print("Phase 5...")
m = ['E4','B4','E5','G5','E5','B4','G4','E4','F#4','A4','D5','E5','G5','E5','D5','A4',
     'E4','G4','B4','E5','G5','B4','E5','G5','A4','D5','E5','G5','A5','G5','E5','D5',
     'B4','E5','G5','E5','B4','G4','E4','B4','E5','G5','A5','G5','E5','B4','G4','E4']
b = ['E3','E3','E3','E3','B3','B3','B3','B3','F3','F3','A3','A3','D3','D3','D3','D3',
     'E3','E3','G3','G3','B3','B3','E3','E3','A3','A3','D3','D3','E3','E3','G3','G3',
     'B3','B3','E3','E3','B3','B3','E3','E3','A3','A3','B3','B3','E3','E3','E3','E3']
ww('music_phase5.wav', mx(melody(m, 0.18, vol=0.28), bass(b, 0.18, vol=0.17)))

print("TODAS as musicas geradas!")
