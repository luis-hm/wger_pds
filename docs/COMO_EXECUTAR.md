# Como executar os dois projetos

Os dois projetos rodam ao mesmo tempo, em portas diferentes, cada um com o seu banco SQLite
(`<projeto>/db/database.sqlite`). Assim dá para mostrar o ANTES e o DEPOIS lado a lado.

| Projeto | Papel | Porta |
|---|---|---|
| `wger-fork` | ANTES | http://localhost:8000 |
| `wger-pds` | DEPOIS | http://localhost:8001 |

Login: usuário **admin**, senha **adminadmin**.

## Pré-requisitos

* Python 3.12+ e [uv](https://docs.astral.sh/uv/)
* Node.js 18+ e npm

## Primeira instalação

Os comandos abaixo valem para cada projeto. Rode dentro de `wger-fork` e depois dentro de `wger-pds`.

```bash
uv sync --group dev                       # dependências Python (.venv)
npm install                               # front React compilado e bibliotecas JS
npx --yes sass@1.83.0 wger/core/static/scss/main.scss wger/core/static/bootstrap-compiled.css
mkdir -p db
uv run wger bootstrap --settings-path settings.local_dev --no-process-static
uv run python manage.py shell --settings=settings.local_dev < ../docs/seed_demo.py
```

* `bootstrap` cria o banco, roda as migrations, carrega exercícios e idiomas e cria o usuário admin.
* `seed_demo.py` cria a rotina **"Treino ABC"**, com 3 dias, 6 exercícios, séries, repetições,
  carga, descanso e RIR, além do label **"Semana de deload"**. Rodar de novo recria a rotina sem duplicar.
* O `sass` é chamado pelo `npx` porque não vem nas dependências do projeto. Sem ele, o
  bootstrap padrão falha no passo de CSS.

## Rodar

Em dois terminais:

```bash
cd wger-fork && uv run python manage.py runserver 8000 --settings=settings.local_dev
cd wger-pds  && uv run python manage.py runserver 8001 --settings=settings.local_dev
```

## Roteiro da demonstração

Abra os dois em abas lado a lado e faça os mesmos passos em cada um.

### 1. Escopo (os dois projetos)
Abra o menu **Training** e o menu **Nutrition**. Medidas, galeria, troféus, peso corporal e
calculadoras não aparecem mais.

### 2. Builder: PDF da rotina
1. Vá em **Training → Routines → Treino ABC**.
2. Baixe o PDF de log e o PDF de tabela. As URLs diretas são `/en/routine/1/pdf/log` e `/en/routine/1/pdf/table`.
3. **ANTES:** o PDF tem título e dias.
   **DEPOIS:** aparece também o período da rotina abaixo do título.
   O conteúdo das tabelas é o mesmo, então a refatoração não mudou o resultado.
4. Mostre o código: `wger-fork/wger/manager/views/pdf.py` (duas funções quase iguais) e
   `wger-pds/wger/manager/views/pdf.py` (3 linhas por view) junto com `wger-pds/wger/manager/pdf_builder.py`.

### 3. Prototype: copiar rotina
1. Na rotina **Treino ABC**, use **Copiar**. A URL direta é `/en/routine/1/copy`.
2. Abra a cópia, que é a rotina 2.
3. **ANTES:** a cópia não tem o label "Semana de deload".
   **DEPOIS:** a cópia tem o label. Dias, exercícios e configurações são copiados nos dois.
4. Mostre o código: `wger-fork/wger/manager/views/routine.py` (laços aninhados) e
   `wger-pds/wger/manager/views/routine.py` (`routine.clone(user=request.user)`).

Para ver o label sem o front, use a API que a tela da rotina consome (logado no navegador):
`/api/v2/routine/2/date-sequence-display/`.

Para repetir a demo do zero, rode o `seed_demo.py` de novo.

## Testes

```bash
cd wger-pds
DJANGO_SETTINGS_MODULE=settings.ci uv run ./manage.py test wger.manager --parallel auto
```

Testes que cobrem os padrões:

* `test_copy_routine.py`: cópia completa, rotina vazia, rollback em caso de erro, permissões e
  o teste novo `test_copy_routine_copies_labels`.
* `test_pdf.py`: os dois PDFs, o acesso de outros usuários e o escape de texto do usuário.
* `test_pdf_builder.py` (novo): o Director chama os passos na ordem certa.

Rodando os mesmos testes antigos no `wger-fork`, eles também passam. O comportamento foi
preservado e o que mudou foram só as duas melhorias descritas.

## Ver a diferença de código

```bash
cd wger-pds
git log --oneline          # fork + 1 commit com os padrões
git diff HEAD~1 --stat
git diff HEAD~1 -- wger/manager/views/
```

## Publicar no GitHub (não foi feito)

1. No GitHub, faça **Fork** de https://github.com/wger-project/wger, ou crie um repositório vazio.
2. Envie cada projeto como uma branch do mesmo repositório:

```bash
cd wger-fork && git remote add origin <url-do-repo> && git push origin main:antes
cd ../wger-pds && git remote add origin <url-do-repo> && git push origin main:depois
```

Assim a comparação `antes...depois` no GitHub mostra o diff dos padrões.
