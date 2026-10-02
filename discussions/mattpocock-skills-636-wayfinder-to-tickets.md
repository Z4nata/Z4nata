# Wayfinder to tickets (mattpocock/skills#636)

- **Fonte:** https://github.com/mattpocock/skills/discussions/636
- **Categoria:** Q&A
- **Baixado em:** 2026-10-02

---

## Pergunta original

**@Ravikc** em 21 jul 2026

Lets say I started a wayfinder session, it created many grilling issues, I resolved all of them in seperate sessions. now the map issues has no open sub-issues.

Now how do I go from here to tickets?

i. Should I run /to-spec and then /to-tickets in the original wayfinder session?
ii. Or can I run /to-spec in a new session by just pointing it to the map issue url?
iii. something else?

---

## Resposta

**@gladtail** em 22 jul 2026

I suppose that just run /to-spec in a new session by just pointing it to the map issue url. Here is what aihero.dev says:

> "Once all the tickets are closed, all of that information gets saved onto the map with the original tickets as primary sources. You can then take this map and turn it into a spec the regular way."

https://www.aihero.dev/skills/skills-changelog-v1-1-wayfinder-to-spec-to-tickets-grilling-improvements#after-wayfinder-completes

---

## Resumo (pt-BR)

Depois que todas as sub-issues de grilling do mapa do wayfinder forem fechadas, abra uma **sessão nova** e rode `/to-spec` apontando para a URL da issue do mapa. Em seguida rode `/to-tickets` a partir da spec gerada. Não precisa voltar à sessão original do wayfinder: o mapa já guarda as decisões, com as issues originais como fontes primárias.
