# Hero of the Water v5.0 — Prototipo Figma
## Passo a passo para montar e publicar no Lovable

---

### O QUE VOCE VAI PRECISAR
- Conta no Figma (gratuita: figma.com)
- Os 7 arquivos PNG da pasta `figma_screens/`
- Conta no Lovable (lovable.dev)

---

### PASSO 1 — Criar o projeto no Figma

1. Abra o Figma (pelo navegador ou app)
2. Clique em **"+ New design file"**
3. Renomeie o arquivo para: **Hero of the Water — Prototype**
   (clique duas vezes no nome la em cima pra renomear)

---

### PASSO 2 — Importar as telas

1. Abra a pasta `figma_screens/` no seu computador
2. Selecione os 7 arquivos PNG:
   - 01_Dificuldade.png
   - 02_Menu_Principal.png
   - 03_Instrucoes.png
   - 04_Selecao_Fases.png
   - 05_Gameplay_Fase1.png
   - 06_Vitoria.png
   - 07_Derrota.png
3. Arraste todos de uma vez pro canvas do Figma
4. As 7 imagens vao aparecer empilhadas. Organize elas lado a lado
   com um espaco entre cada uma (tipo uma fileira)

---

### PASSO 3 — Transformar cada imagem em Frame

Para CADA uma das 7 imagens, faca:

1. Clique na imagem pra selecionar
2. No painel da direita, anote o tamanho (deve ser 960 x 640)
3. Aperte **Ctrl+Alt+G** (isso coloca a imagem dentro de um Frame)
4. No painel da esquerda, renomeie o Frame:
   - `01 - Dificuldade`
   - `02 - Menu Principal`
   - `03 - Instrucoes`
   - `04 - Selecao de Fases`
   - `05 - Gameplay`
   - `06 - Vitoria`
   - `07 - Derrota`

Resultado: 7 Frames nomeados, cada um com sua tela dentro.

---

### PASSO 4 — Criar os botoes clicaveis (hotspots)

Agora voce vai colocar areas invisiveis sobre os botoes pra tornar
o prototipo navegavel. Para cada hotspot:

1. Selecione a ferramenta **Rectangle** (R)
2. Desenhe um retangulo em cima do botao
3. No painel da direita, mude o **Fill** (preenchimento) para
   opacidade 0% (totalmente transparente) — ou remova o fill
4. Repita para todos os botoes listados abaixo

**TELA 01 - Dificuldade (3 hotspots):**
- 1 retangulo sobre o botao FACIL
- 1 retangulo sobre o botao MEDIA
- 1 retangulo sobre o botao DIFICIL

**TELA 02 - Menu Principal (2 hotspots):**
- 1 retangulo sobre o botao JOGAR
- 1 retangulo sobre o botao INSTRUCOES

**TELA 03 - Instrucoes (1 hotspot):**
- 1 retangulo sobre o botao VOLTAR

**TELA 04 - Selecao de Fases (4 hotspots):**
- 1 retangulo sobre o card da Fase 1
- 1 retangulo sobre o card da Fase 2
- 1 retangulo sobre o card da Fase 3
- 1 retangulo sobre o botao VOLTAR

**TELA 05 - Gameplay (2 hotspots):**
- 1 retangulo na metade direita da tela (simula "ganhou")
- 1 retangulo na metade esquerda da tela (simula "perdeu")

**TELA 06 - Vitoria (1 hotspot):**
- 1 retangulo sobre o botao PROXIMA FASE

**TELA 07 - Derrota (1 hotspot):**
- 1 retangulo sobre o botao RECOMECAR

---

### PASSO 5 — Conectar a navegacao (Prototype)

1. Clique na aba **"Prototype"** no painel da direita (ao lado de Design)
2. Agora, para CADA hotspot, faca:
   a) Clique no retangulo transparente
   b) Vai aparecer um circulo azul na borda do retangulo
   c) Arraste esse circulo ate o Frame de destino (a setinha azul conecta)
   d) Na janelinha que aparece, configure:
      - Trigger: **On click**
      - Action: **Navigate to**
      - Animation: **Dissolve**
      - Duration: **300ms**

**Mapa de conexoes (de onde -> pra onde):**

| Tela | Botao | Vai pra |
|------|-------|---------|
| 01 Dificuldade | FACIL | 02 Menu Principal |
| 01 Dificuldade | MEDIA | 02 Menu Principal |
| 01 Dificuldade | DIFICIL | 02 Menu Principal |
| 02 Menu Principal | JOGAR | 04 Selecao de Fases |
| 02 Menu Principal | INSTRUCOES | 03 Instrucoes |
| 03 Instrucoes | VOLTAR | 02 Menu Principal |
| 04 Selecao de Fases | Fase 1 | 05 Gameplay |
| 04 Selecao de Fases | Fase 2 | 05 Gameplay |
| 04 Selecao de Fases | Fase 3 | 05 Gameplay |
| 04 Selecao de Fases | VOLTAR | 02 Menu Principal |
| 05 Gameplay | Lado direito | 06 Vitoria |
| 05 Gameplay | Lado esquerdo | 07 Derrota |
| 06 Vitoria | PROXIMA FASE | 05 Gameplay |
| 07 Derrota | RECOMECAR | 04 Selecao de Fases |

---

### PASSO 6 — Configurar o ponto de inicio

1. Ainda na aba **Prototype**
2. Clique no Frame **"01 - Dificuldade"**
3. No painel da direita, em **Flow starting point**, clique em **"+"**
4. Agora esse frame e a primeira tela quando alguem abre o prototipo

---

### PASSO 7 — Testar o prototipo

1. Clique no botao **"Play"** (triangulo) no canto superior direito do Figma
2. O prototipo abre numa nova aba
3. Teste clicando nos botoes — voce deve navegar entre as telas
4. Se algum botao nao funciona, volte e confira se o hotspot esta
   conectado ao frame certo

---

### PASSO 8 — Publicar no Lovable

1. No Figma, copie o link do prototipo:
   - Clique em **Share** (canto superior direito)
   - Em **"Link to prototype"**, clique **Copy link**
   - Garanta que a permissao esta em **"Anyone with the link"** > **"can view"**

2. No Lovable:
   - Abra o mural do projeto
   - Adicione um novo elemento/embed
   - Cole o link do prototipo do Figma
   - O prototipo interativo vai aparecer no mural
   - Quem acessar o mural consegue navegar entre as telas clicando

---

### RESUMO DAS 7 TELAS

| # | Tela | O que mostra |
|---|------|-------------|
| 1 | Dificuldade | 3 botoes: Facil, Media, Dificil |
| 2 | Menu Principal | Titulo do jogo + Samuel + JOGAR/INSTRUCOES |
| 3 | Instrucoes | Controles, objetivo, sistema de estrelas |
| 4 | Selecao de Fases | 5 cards de fases com estrelas e progresso |
| 5 | Gameplay | Cena do jogo: rio, Samuel, lixo, predios |
| 6 | Vitoria | Missao Concluida + estrelas + pontuacao |
| 7 | Derrota | Missao Falha + botao recomecar |

---

### FLUXO VISUAL

```
DIFICULDADE --> MENU PRINCIPAL --> SELECAO DE FASES --> GAMEPLAY
                    |                   |                  |
                    v                   v                  |-----> VITORIA
                INSTRUCOES          (VOLTAR pro Menu)      |
                    |                                      |-----> DERROTA
                    v                                                |
                (VOLTAR pro Menu)                          (RECOMECAR)
                                                               |
                                                               v
                                                        SELECAO DE FASES
```

---

### PALETA DE CORES (se precisar recriar algo)

| Cor | Codigo | Onde usa |
|-----|--------|---------|
| Azul ceu | #5B9BD5 | Fundo do ceu |
| Azul agua | #2277AA | Rio |
| Verde | #4CAF50 | Grama e botoes |
| Marrom | #8B6914 | Chao |
| Amarelo | #FFD700 | Estrelas |
| Vermelho | #C0392B | Botao derrota |
| Escuro | #1A1A2E | Fundo tela derrota |

---

Hero of the Water v5.0 — ODS 6: Agua Limpa e Saneamento
Equipe ADS 2026: Filipe - Andre - Julio - Joao - Edmilson
