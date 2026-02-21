# App de Anotação Judicial (DV/IC)

Aplicação Streamlit para anotação manual por juízes, com foco em simplicidade de uso, fluxo vertical e persistência em Google Sheets.

## Funcionalidades implementadas
- Interface integral em português de Portugal, com linguagem formal.
- Login interno por `username/password` (sem email).
- Atribuição automática de ramo:
  - `J_DV_*` -> Violência Doméstica (DV)
  - `J_IC_*` -> Incumprimento Contratual (IC)
  - sem prefixo -> atribuição pseudoaleatória fixa por hash do `username`
- Workflow vertical:
  1. Leitura do caso (website por `iFrame`)
  2. Escolha da classe de desfecho
  3. Indicação de confiança
  4. Justificação opcional
  5. Gravação manual / autosave
- Fallback de visualização:
  - prioridade: `iFrame` com URL original
  - fallback: `texto_integral_completo`
- Navegação livre entre casos:
  - `Anterior` / `Seguinte`
  - seleção direta por slider
- Progresso explícito (`x/50` e percentagem), com indicador visual de casos.
- Gravação:
  - botão manual `Gravar progresso`
  - autosave a cada 60 segundos (se houver alterações pendentes)
- Bloqueio final:
  - botão explícito `Concluir e bloquear anotação` após 100%
  - estado persistente em aba técnica `estado`

## Estrutura
```text
judge_data_anotation_app/
  app.py
  models.py
  ui.py
  styles.css
  requirements.txt
  services/
    auth.py
    assignment.py
    data_loader.py
    persistence.py
    progress.py
  credentials/
    juizes.exemplo.json
  .streamlit/
    secrets.toml
```

## Dados utilizados
Localização dos datasets:
- `../data/processed_data/gold_test/dv_gold_test_full.csv`
- `../data/processed_data/gold_test/boc_gold_test_full.csv`

Colunas usadas em runtime:
- `url`
- `n_processo`
- `texto_integral_completo`

`texto_integral_sem_decisao` não é usado pela aplicação.

## Modelo de persistência (Google Sheets)
Existem **2 ficheiros** de Google Sheets: um para DV e outro para IC.

Cada ficheiro contém:
- aba `decisao` (matriz `n_processo` x `juiz`)
- aba `confianca` (matriz `n_processo` x `juiz`)
- aba `justificacao` (matriz `n_processo` x `juiz`)
- aba `estado` com:
  - `username`
  - `ramo`
  - `finalizado`
  - `finalizado_em`
  - `ultima_gravacao_em`

Nota:
- A app tenta atualizar a aba e, se não existir, tenta criá-la automaticamente.

## Configuração local
1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Criar/configurar `.streamlit/secrets.toml` com:
- ligações Google Sheets (`gsheets_dv` e `gsheets_ic`, ou nomes custom com `gsheets_connection_dv` / `gsheets_connection_ic`)
- credenciais da service account Google

3. Configurar credenciais de login dos juízes:
- copiar `credentials/juizes.exemplo.json` para `credentials/juizes.json`
- ajustar utilizadores e palavras-passe
- manter `credentials/juizes.json` fora de controlo de versão (`.gitignore`)

4. Executar:
```bash
streamlit run app.py
```

## Deploy no Streamlit Cloud
Modelo recomendado para este caso:
- app pública
- controlo de acesso feito por login interno na app

Passos:
1. Publicar este diretório no repositório.
2. No painel da app no Streamlit Cloud, configurar `Secrets` com conteúdo equivalente ao `secrets.toml`.
3. Definir credenciais de login:
  - recomendado: `credentials_json` em `Secrets`
  - alternativa: `auth_credentials` em `Secrets`
4. Validar:
  - login
  - leitura por iFrame e fallback de texto
  - gravação manual/autosave
  - bloqueio final

## Formatos de credenciais suportados
- Recomendado (simples): `{ "J_DV_01": { "password": "1234" } }`
- Também suportado: `{ "J_DV_01": "1234" }`
- Compatibilidade antiga: `{ "J_DV_01": { "salt": "...", "password_hash": "..." } }`

## Notas de segurança
- Em ambiente de produção, evitar passwords em texto simples.
- Preferir hash+sal por utilizador.
- Não commitar:
  - `.streamlit/secrets.toml`
  - `credentials/juizes.json`

