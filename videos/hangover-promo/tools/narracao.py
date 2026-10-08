import sys, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
LINES = [
 "Começou a noite?",
 "Abre o Hangover.",
 "Tira uma foto da bebida, e a inteligência artificial estima o tipo e o volume.",
 "O Zeca acompanha sua noite, ao vivo.",
 "No fim, o resumo vira figurinha pro Stories.",
 "Hangover: o Strava da sua noite.",
 "Se beber, não dirija.",
]
FIX = {"tʃˈipw": "tʃˈipʊ", "ˌɐ̃ŋɡovˈer": "xˈɛŋɡowveɾ", "ˌɐ̃ŋɡovˈeɾ": "xˈɛŋɡowveɾ", "stˌoɾˈiys": "stˈɔɾis", "strˈavæ": "istɾˈavɐ"}
voice = sys.argv[1]; speed = float(sys.argv[2])
for i, t in enumerate(LINES):
    ph = k.tokenizer.phonemize(t, 'pt-br')
    for a, b in FIX.items(): ph = ph.replace(a, b)
    samples, sr = k.create(ph, voice=voice, speed=speed, is_phonemes=True)
    sf.write(f"out/{voice}_{i}.wav", samples, sr)
    print(i, round(len(samples)/sr, 2), ph)
