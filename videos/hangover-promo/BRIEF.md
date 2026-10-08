---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Hangover é o Strava da sua noite"
destination: shorts-tiktok-reels
aspect: 1080x1920
language: pt-BR
audience: jovens adultos (18+) que saem à noite com amigos
length: 20s
angle: product-walkthrough
voice: kokoro-pm_alex
---

## Intent

Vídeo de apresentação de 20 segundos do app HANGOVER ("O Strava da sua noite"), com narração e
música. Pedido do usuário: "utilize esse plugin para criar o vídeo de apresentação do aplicativo
hangover, quero que tenha duração de 20 segundos" · "quero narração e música".
Roteiro escolhido: "A noite em 20s" — começar a noite → foto/IA → Zeca ao vivo → figurinha pro Stories.

## Assets

- assets/screens/*.jpg — telas reais do app (build web local, noites de exemplo do próprio app)
- assets/sticker.png — figurinha PNG transparente exportada pelo botão BAIXAR PNG do app
- assets/mascots/*.png — Zeca, Paçoca e Nina com fundo transparente, capturados do app
- assets/fonts/ — Bellyvia Bold (logo), Unbounded, Geist e Geist Mono (as fontes do app)
- assets/audio/narration-mix.m4a — narração Kokoro pm_alex (pt-BR) + trilha 120 BPM sintetizada, já mixadas

## Customizations

- Narração local (Kokoro pm_alex): a ElevenLabs recusou a geração (plano gratuito bloqueado) e a
  HeyGen não está logada; o usuário escolheu a voz local.
- Trilha própria a 120 BPM (host audio), com impactos em 2,0 s (logo) e 14,0 s (tela final).

## Notes

- Seguir os princípios do app: não incentivar beber mais; "Se beber, não dirija" e 18+ na tela final.
- Identidade: fundo #09090A, texto #F4F4EF, destaque laranja #FC5200 (tokens.ts), cards raio 28.
- Rede bloqueia cdn.jsdelivr.net: GSAP vai local em assets/vendor/gsap.min.js.
