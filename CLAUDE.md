# Instruções para o Claude

## Criação de vídeo

Todo vídeo é renderizado e exportado com o [HyperFrames](https://github.com/heygen-com/hyperframes)
(HeyGen): animação, motion graphic, promo, explainer, vídeo com legendas, overlays, vídeo a partir
de música, de PR ou de site, e apresentação animada. Só use outra ferramenta quando o pedido citar
essa ferramenta.

Para criar, escolha a skill assim:

1. **O pedido é um formato do Motion Graphics Skill Pack** → use a skill dele. Ela traz as regras
   de estilo e de marca, e exporta com HyperFrames.

   | Pedido | Skill |
   | --- | --- |
   | Configurar a marca para animação | `brand-intake` |
   | Escrever um briefing ou um prompt de animação | `motion-brief-writer`, `motion-prompt-writer`, `reference-to-motion` |
   | Vídeo de lançamento de produto, curso ou oferta | `launch-video` |
   | Lançamento no estilo Apple (barra de menu, notch, widgets) | `apple-launch-film` |
   | Explainer documental no estilo Vox | `vox-explainer` |
   | Gráfico animado com números reais | `animated-chart` |
   | Marco de seguidores, assinantes ou receita | `milestone-reveal` |
   | Um dos 16 efeitos de interface, dados ou tipografia | `motion-effects` |
   | Abertura cinematográfica em 3D | `title-sequence-3d` |
   | Mesmo briefing em três IAs, lado a lado | `model-showdown` |
   | Promo de newsletter | `newsletter-promo` |
   | Capa de newsletter como GIF em loop | `loop-cover` |
   | Converter um vídeo para Reel ou TikTok (1080 x 1920) | `reel-export` |

2. **Qualquer outro pedido de vídeo** → comece pela skill `/hyperframes`. Ela é o roteador: faz o
   briefing, escolhe o fluxo de criação e indica as skills de domínio (`/hyperframes-core`,
   `/hyperframes-animation`, `/media-use` etc.).

- Se `brand.md` e `MOTION.md` existirem no projeto, leia os dois antes de animar.
- Siga o ciclo do HyperFrames: compor em HTML, `lint` e `check`, preview e render com
  `npx hyperframes`.
- Geradores de mídia por IA (imagem, vídeo, voz, música) servem para produzir os assets. O
  vídeo final é montado e renderizado no HyperFrames.

## Skills instaladas

Tudo fica em `.claude/skills/`:

- **HyperFrames:** as 21 skills publicadas de `heygen-com/hyperframes`, do commit `0c76e52`
  (CLI v0.8.140). Licença Apache-2.0 (`.claude/skills/LICENSE-hyperframes`).
- **Motion Graphics Skill Pack:** as 15 skills de `charlie947/motion-graphics-skills`, do commit
  `229022e`. Licença MIT (`.claude/skills/LICENSE-motion-graphics-skills`).

Para atualizar, substitua as pastas pela versão mais recente:

```bash
git clone --depth 1 https://github.com/heygen-com/hyperframes /tmp/hyperframes
git clone --depth 1 https://github.com/charlie947/motion-graphics-skills /tmp/motion-graphics-skills
for s in /tmp/hyperframes/skills/*/ /tmp/motion-graphics-skills/skills/*/; do
  rm -rf ".claude/skills/$(basename "$s")"; cp -r "$s" .claude/skills/
done
```
