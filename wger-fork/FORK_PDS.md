# Fork PDS 2026.2 — recorte Treinamento + Nutrição (ANTES)

Fork do [wger](https://github.com/wger-project/wger) (commit upstream `aebe882`, licença AGPL v3),
reduzido ao escopo definido na Parte 1 do trabalho. **Código dos módulos do escopo sem alteração**:
este é o estado "ANTES" usado na apresentação. O estado "DEPOIS" (com os padrões GoF) fica no
projeto `wger-pds`.

## No escopo

| Módulo | Pasta | O que entra |
|---|---|---|
| Treinamento | `wger/manager` | Routine, Day, Slot, SlotEntry, configs (sets, reps, peso, descanso, RIR), WorkoutSession, WorkoutLog, PDF da rotina, cópia de rotina |
| Nutrição | `wger/nutrition` | NutritionPlan, Meal, MealItem, Ingredient, LogItem |
| Catálogo de exercícios | `wger/exercises` | Exercise, categoria, equipamento, músculo (usado pelo CU08) |

## Fora do escopo (removido da interface)

Medidas corporais, peso corporal, galeria, troféus, academias (gym), calculadoras de IMC e de
calorias. Os itens foram retirados do menu (`wger/core/templates/navigation.html`).

Os apps `gym`, `measurements`, `weight`, `gallery`, `trophies` e `mailer` continuam instalados
apenas como **dependência técnica**: migrations do `core` dependem deles (ex.: `UserProfile.gym`
é FK para `gym.Gym`, e a migration `core/0027` depende de `gallery/0001`), e o `NutritionPlan`
usa o peso corporal no cálculo de g/kg. Apagá-los quebraria o esquema do banco.

## Rodar

Ver `../docs/COMO_EXECUTAR.md`.
