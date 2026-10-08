# Instruções para o Claude

## Criação de vídeo: sempre com HyperFrames

Use o [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen) para criar ou editar
qualquer vídeo: animação, motion graphic, promo, explainer, vídeo com legendas, overlays,
vídeo a partir de música, de PR ou de site, e apresentação animada. Só use outra ferramenta
quando o pedido citar essa ferramenta.

- Comece sempre pela skill `/hyperframes`. Ela é o roteador: faz o briefing, escolhe o
  fluxo de criação e indica as skills de domínio (`/hyperframes-core`, `/hyperframes-animation`,
  `/media-use` etc.).
- Siga o ciclo do próprio HyperFrames: compor em HTML, `lint` e `check`, preview e render com
  `npx hyperframes`.
- Geradores de mídia por IA (imagem, vídeo, voz, música) servem para produzir os assets. O
  vídeo final é montado e renderizado no HyperFrames.

## Skills instaladas

As 21 skills publicadas do HyperFrames estão em `.claude/skills/`, copiadas do commit
`0c76e52` de `heygen-com/hyperframes` (CLI v0.8.140). Licença: Apache-2.0
(`.claude/skills/LICENSE-hyperframes`).

Para atualizar, substitua as pastas pela versão mais recente:

```bash
git clone --depth 1 https://github.com/heygen-com/hyperframes /tmp/hyperframes
for s in /tmp/hyperframes/skills/*/; do rm -rf ".claude/skills/$(basename "$s")"; cp -r "$s" .claude/skills/; done
```
