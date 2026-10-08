"""Trilha de 20 s a 120 BPM (lá menor) para o vídeo do Hangover.

Grade: 1 tempo = 0,5 s, 1 compasso = 2 s.
  0-2   intro (pad abrindo, hats, riser)      -> impacto em 2,0 (logo)
  2-12  groove completo
  12-14 build sem bumbo (caixa acelerando)    -> impacto em 14,0 (tela final)
  14-18 groove completo
  18-20 acorde final soando e fade
"""
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
DUR = 20.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(7)


def t_arr(sec):
    return np.arange(int(sec * SR)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, f, 'low', fs=SR, output='sos'), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def place(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def saw(f, t, phase=0.0):
    return 2 * ((f * t + phase) % 1.0) - 1


# ---------- instrumentos ----------
def kick():
    t = t_arr(0.45)
    f = 46 + 120 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 6.5)
    click = hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 400) * 0.25
    return np.tanh((body + click) * 1.6)


def clap():
    t = t_arr(0.25)
    n = rng.standard_normal(len(t))
    env = np.zeros_like(t)
    for d in (0.0, 0.011, 0.022):
        env += np.where(t >= d, np.exp(-(t - d) * 60), 0)
    env += np.exp(-t * 14) * 0.5
    return bp(n, 900, 4200) * env * 0.9


def hat(open_=False):
    t = t_arr(0.22 if open_ else 0.06)
    n = rng.standard_normal(len(t))
    return hp(n, 7000, 4) * np.exp(-t * (16 if open_ else 90)) * (0.35 if open_ else 0.28)


def supersaw(notes, dur, cutoff, detune=0.12, voices=5):
    t = t_arr(dur)
    left = np.zeros_like(t)
    right = np.zeros_like(t)
    for n in notes:
        f0 = midi(n)
        for v in range(voices):
            cents = (v - (voices - 1) / 2) * detune * 100 / (voices - 1)
            f = f0 * 2 ** (cents / 1200)
            s = saw(f, t, rng.random())
            pan = v / (voices - 1)
            left += s * (1 - pan)
            right += s * pan
    norm = len(notes) * voices / 2
    return lp(left / norm, cutoff), lp(right / norm, cutoff)


def impact():
    t = t_arr(1.6)
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-t * 8)) * t) * np.exp(-t * 2.8)
    noise = lp(rng.standard_normal(len(t)), 3500) * np.exp(-t * 5) * 0.35
    return np.tanh((boom + noise) * 1.4)


def riser(dur):
    t = t_arr(dur)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(t)
    # varredura em blocos (filtro subindo)
    blocks = 24
    size = len(t) // blocks
    for b in range(blocks):
        fc = 400 * (9000 / 400) ** (b / (blocks - 1))
        seg = n[b * size:(b + 1) * size]
        out[b * size:(b + 1) * size] = bp(seg, fc * 0.7, min(fc * 1.4, 20000))
    return out * (t / dur) ** 2 * 0.5


def reverb_ir(sec=1.4):
    t = t_arr(sec)
    l = rng.standard_normal(len(t)) * np.exp(-t * 4.2)
    r = rng.standard_normal(len(t)) * np.exp(-t * 4.2)
    return lp(l, 6000) * 0.05, lp(r, 6000) * 0.05


# ---------- harmonia ----------
# Am7 | Fmaj7 | Cmaj7 | G  (um acorde por compasso)
CHORDS = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 55, 59, 64], [55, 59, 62, 67]]
ROOTS = [45, 41, 48, 43]


def bar_of(t):
    return int(t // 2.0)


drums = np.zeros(N)
bass = np.zeros(N)
stabL = np.zeros(N)
stabR = np.zeros(N)
padL = np.zeros(N)
padR = np.zeros(N)
fxL = np.zeros(N)
fxR = np.zeros(N)

K, C, CH, OH = kick(), clap(), hat(), hat(True)

kick_times = []
for b in range(40):  # 40 tempos
    at = b * BEAT
    full = (2.0 <= at < 12.0) or (14.0 <= at < 18.0)
    if full:
        place(drums, K, at, 0.95)
        kick_times.append(at)
        if b % 2 == 1:
            place(drums, C, at, 0.55)
        place(drums, OH, at + BEAT / 2, 0.6)
    # hats de 16 no intro, no groove e no build
    if at < 18.0:
        for s in range(4):
            g = 0.35 if at < 2.0 else 0.5
            place(drums, CH, at + s * BEAT / 4, g * (1.0 if s % 2 == 0 else 0.6))

# caixa acelerando no build (12-14) e no fim do intro (1-2)
for start, end in ((1.0, 2.0), (12.0, 14.0)):
    t = start
    while t < end - 1e-6:
        prog = (t - start) / (end - start)
        step = BEAT / 2 if prog < 0.5 else (BEAT / 4 if prog < 0.85 else BEAT / 8)
        place(drums, C, t, 0.15 + 0.4 * prog)
        t += step

# baixo: colcheias no contratempo, com a fundamental do acorde
for b in range(40):
    at = b * BEAT
    if not ((2.0 <= at < 12.0) or (14.0 <= at < 18.0)):
        continue
    root = ROOTS[bar_of(at) % 4]
    for off, oct_ in ((BEAT / 2, 0), (BEAT * 0.75, 12 if b % 4 == 3 else 0)):
        t = t_arr(0.2)
        f = midi(root + oct_)
        tone = saw(f, t) * 0.5 + np.sin(2 * np.pi * f / 2 * t) * 0.8
        env = np.minimum(1, t * 300) * np.exp(-t * 9)
        place(bass, lp(tone * env, 380), at + off, 0.55)

# stabs sincopados (posições em semicolcheias dentro do compasso)
STAB_POS = [0, 3, 6, 10, 12]
for bar in range(10):
    t0 = bar * 2.0
    if not ((2.0 <= t0 < 12.0) or (14.0 <= t0 < 18.0)):
        continue
    notes = [n + 12 for n in CHORDS[bar % 4]]
    for p in STAB_POS:
        l, r = supersaw(notes, 0.3, 2600)
        env = np.minimum(1, t_arr(0.3) * 500) * np.exp(-t_arr(0.3) * 14)
        place(stabL, l * env, t0 + p * BEAT / 4, 0.32)
        place(stabR, r * env, t0 + p * BEAT / 4, 0.32)

# pad contínuo (abre o filtro no intro)
for bar in range(10):
    t0 = bar * 2.0
    l, r = supersaw(CHORDS[bar % 4], 2.05, 1400 if t0 >= 2 else 700, detune=0.2)
    env = np.minimum(1, t_arr(2.05) * 8) * np.minimum(1, (2.05 - t_arr(2.05)) * 20)
    g = 0.22 if t0 < 18 else 0.0
    place(padL, l * env, t0, g)
    place(padR, r * env, t0, g)

# bombeamento do pad pelo bumbo (sidechain)
duck = np.ones(N)
for kt in kick_times:
    i = int(kt * SR)
    seg = t_arr(0.4)
    curve = 1 - 0.75 * np.exp(-seg * 9)
    j = min(N, i + len(seg))
    duck[i:j] = np.minimum(duck[i:j], curve[: j - i])
padL *= duck
padR *= duck

# efeitos: riser antes dos impactos, impactos, acorde final
R1, R2 = riser(1.0), riser(2.0)
place(fxL, R1, 1.0, 0.8); place(fxR, R1, 1.0, 0.8)
place(fxL, R2, 12.0, 0.8); place(fxR, R2, 12.0, 0.8)
IMP = impact()
for at in (2.0, 14.0):
    place(fxL, IMP, at, 0.9); place(fxR, IMP, at, 0.9)
# acorde final em 18,0
l, r = supersaw([n + 12 for n in CHORDS[0]] + [45 + 12], 2.0, 3000, detune=0.18)
env = np.minimum(1, t_arr(2.0) * 400) * np.exp(-t_arr(2.0) * 2.2)
place(fxL, l * env, 18.0, 0.5); place(fxR, r * env, 18.0, 0.5)
place(fxL, IMP * 0.8, 18.0); place(fxR, IMP * 0.8, 18.0)
place(drums, K, 18.0, 0.9)

# reverb nos stabs, palmas e efeitos
irL, irR = reverb_ir()
wetL = fftconvolve(stabL + fxL * 0.5 + drums * 0.15, irL)[:N]
wetR = fftconvolve(stabR + fxR * 0.5 + drums * 0.15, irR)[:N]

L = drums + bass + stabL + padL + fxL + wetL
R = drums + bass + stabR + padR + fxR + wetR
mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 0.9)
# fade final
fade = np.ones(N)
fi = int(19.0 * SR)
fade[fi:] = np.linspace(1, 0, N - fi) ** 1.5
mix *= fade[:, None]
mix /= np.max(np.abs(mix)) / 0.89
sf.write('music.wav', mix.astype(np.float32), SR, subtype='PCM_16')
print('ok', mix.shape)
