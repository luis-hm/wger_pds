# Trabalho Final PDS 2026.2 — Wger (Treinamento + Nutrição)

Equipe: Letícia, Luis, Mylena, Pedro e Samira.

Esta pasta explica o que foi feito no trabalho final, como executar os dois projetos e o que
muda entre eles.

| Arquivo | Conteúdo |
|---|---|
| [COMO_EXECUTAR.md](COMO_EXECUTAR.md) | Instalação, execução lado a lado, roteiro da demo e testes |
| [PADROES.md](PADROES.md) | Builder e Prototype: problema, código antes/depois, diagramas, GRASP e SOLID |
| [seed_demo.py](seed_demo.py) | Cria a mesma rotina de demonstração nos dois projetos |
| [img/](img/) | Primeira página dos PDFs gerados antes e depois |

## Os dois projetos

```
wger/
├── wger-fork/   ANTES: o wger que selecionamos na Parte 1, só com o recorte do escopo
├── wger-pds/    DEPOIS: o mesmo fork com os padrões Builder e Prototype aplicados
└── docs/        esta documentação
```

* **wger-fork** é um fork do [wger](https://github.com/wger-project/wger) (commit upstream `aebe882`).
  Os módulos do escopo (treino em `manager`, `nutrition` e o catálogo de `exercises`) estão
  **sem alteração**. Os módulos fora do escopo (medidas, peso, galeria, troféus, academias e
  calculadoras de IMC e calorias) saíram do menu. Ver `wger-fork/FORK_PDS.md`.
* **wger-pds** foi criado com `git clone` do wger-fork e tem **um commit a mais**, com os padrões.
  Por isso `git diff HEAD~1` dentro do `wger-pds` mostra exatamente o que mudou.

## Padrões aplicados

| Padrão GoF | Onde | Problema que resolve |
|---|---|---|
| **Builder** | `wger/manager/pdf_builder.py`, usado por `wger/manager/views/pdf.py` | Duas views de PDF (`workout_log` e `workout_view`) de ~70 linhas quase idênticas, cada uma montando o reportlab na mão |
| **Prototype** | `wger/manager/models/prototype.py`, usado por Routine, Day, Slot, SlotEntry, configs e Label | A view `copy_routine` reconstruía a rotina por fora, com 4 laços aninhados e 10 chamadas manuais a `copy_config`, e **esquecia de copiar os labels** |

Extra: GRASP (Information Expert, Creator, Pure Fabrication, High Cohesion, Low Coupling,
Polymorphism) e SOLID (SRP, OCP, LSP). Detalhes e trechos de código em [PADROES.md](PADROES.md).

## O sistema tem front?

Sim, em duas partes:

1. **Front React** (`@wger-project/react-components`). Ele vem do npm já compilado em
   `node_modules` e é servido pelo Django. São as telas de dashboard, rotinas e nutrição. É ali
   que ficam os botões **Copiar rotina** e **PDF**, que chamam as rotas Django
   `/routine/<id>/copy`, `/routine/<id>/pdf/log` e `/routine/<id>/pdf/table`. Essas rotas são
   justamente as views que refatoramos.
2. **Templates Django**: o menu superior (`navigation.html`), login, preferências e o próprio
   PDF gerado.

O código-fonte do React **não foi alterado**, porque ele é um projeto separado publicado no npm.
A diferença aparece no front pelo resultado das rotas refatoradas:

| Onde aparece | ANTES (wger-fork, :8000) | DEPOIS (wger-pds, :8001) |
|---|---|---|
| Copiar rotina | A cópia perde o label "Semana de deload" | A cópia mantém o label |
| PDF da rotina (log e tabela) | Título e dias | Título, **período da rotina** (ex.: 19.11.2026 – 14.01.2027) e dias |
| Menu (os dois projetos) | Sem medidas, peso, galeria, troféus, academias e calculadoras | Igual |

Isso foi conferido com os dois servidores rodando. Após clicar em copiar, a API
`/api/v2/routine/2/date-sequence-display/`, que alimenta a tela da rotina no React, devolve
`[]` labels no ANTES e `['Semana de deload']` no DEPOIS. As imagens dos PDFs estão em [img/](img/).

## Diferenças de código (wger-pds em relação ao wger-fork)

```
 wger/manager/models/prototype.py        |  39 +++  (novo: classe Prototype)
 wger/manager/pdf_builder.py             | 153 +++  (novo: Builder, 2 ConcreteBuilders, Director)
 wger/manager/views/pdf.py               | 165 +---  (views passam a só tratar a requisição)
 wger/manager/views/routine.py           |  67 +--  (copy_routine vira routine.clone(...))
 wger/manager/models/routine.py          |  25 +-   (clone e clone_children)
 wger/manager/models/day.py, slot.py, slot_entry.py, label.py, abstract_config.py  (herdam Prototype)
 wger/manager/tests/test_copy_routine.py |  17 +    (novo teste: cópia leva os labels)
 wger/manager/tests/test_pdf_builder.py  |  27 +    (novo teste: ordem dos passos do Director)
 wger/manager/tests/test_pdf.py          |   2 +-   (o Paragraph mudou de módulo)
```

Não houve mudança de banco: `makemigrations --check` não detecta alterações. A suíte do
`manager` passa inteira, com 394 testes, incluindo os 2 novos.

## Fora do que foi feito

* **Nutrição.** Os padrões foram aplicados só no treino, que é o recorte das apresentações.
  O mesmo Director poderia montar o PDF do plano alimentar (`nutrition/views/plan.py`,
  `export_pdf`), e o mesmo Prototype poderia copiar o plano (`copy`). Fica como trabalho futuro.
* **Strategy nas operações de progressão.** Está citado como trabalho futuro no roteiro da apresentação.

