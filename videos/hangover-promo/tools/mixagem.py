import json, numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt
SR = 44100
music, sr = sf.read('music.wav'); assert sr == SR
N = len(music)
STARTS = [0.25, 1.80, 3.50, 8.15, 11.15, 14.30, 16.80]
voice = np.zeros(N)
spans = []
for i, at in enumerate(STARTS):
    v, vsr = sf.read(f'out/pm_alex_{i}.wav')
    v = resample_poly(v, 147, 80)  # 24k -> 44.1k
    v = sosfilt(butter(2, 90, 'high', fs=SR, output='sos'), v)
    a = int(at * SR); b = min(N, a + len(v))
    voice[a:b] += v[: b - a]
    spans.append({'line': i, 'start': at, 'end': round(at + len(v) / SR, 3)})
# compressão leve e nível da voz
voice = np.tanh(voice / np.max(np.abs(voice)) * 1.6) * 0.8
# envelope da voz -> ducking da música
env = np.abs(voice)
win = int(0.05 * SR)
env = np.convolve(env, np.ones(win) / win, mode='same')
env = env / env.max()
gate = np.clip(env * 6, 0, 1)
# suaviza ataque/release (~120 ms)
sm = int(0.12 * SR)
gate = np.convolve(gate, np.ones(sm) / sm, mode='same')
duck = 1 - 0.62 * np.clip(gate, 0, 1)
mixed = music * duck[:, None] * 0.75 + voice[:, None] * 0.95
mixed /= np.max(np.abs(mixed)) / 0.95
sf.write('voice.wav', voice.astype(np.float32), SR, subtype='PCM_16')
sf.write('mix.wav', mixed.astype(np.float32), SR, subtype='PCM_16')
json.dump(spans, open('spans.json', 'w'), indent=1)
print(json.dumps(spans))
