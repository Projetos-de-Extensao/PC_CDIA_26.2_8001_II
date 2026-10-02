# Documento de Visão (v1.0)

## SBrT PhotoMatch — Recuperação de Fotos por Reconhecimento Facial

**Projeto:** Desafio de Arquitetura de Nuvem — Case 2 (E-commerce "Black Friday Ready", adaptado)
**Data:** 04/09/2026
**Status:** Versão inicial

---

### 1. Introdução

#### 1.1 Propósito

Definir a visão de escopo e a arquitetura AWS para o **SBrT PhotoMatch**, aplicação web que permite a participantes do SBrT2026 encontrarem, por meio de uma selfie, as fotos em que aparecem no acervo fotográfico oficial do SBrT2025 (1.427 imagens, 3.344 rostos já indexados). O sistema foi validado academicamente no artigo *"Designing a Face Recognition System for Event Photography"* (SBrT2026) e será demonstrado ao vivo durante o evento (29/09 a 02/10/2026), com acesso via QR Code no pôster.

#### 1.2 Escopo

1. Aplicação web simples (upload de selfie → lista de fotos correspondentes).
2. API de busca: embedding da selfie (dlib ResNet, 128-d) + comparação por distância euclidiana contra o acervo já pré-indexado.
3. Armazenamento do acervo de imagens do SBrT2025 e entrega das fotos correspondentes ao usuário.
4. Infraestrutura elástica dimensionada para um pico de acesso concentrado em 4 dias (duração do evento), com custo mínimo fora dessa janela.

Fora do escopo: reprocessamento do acervo (embeddings já gerados na fase de pesquisa), autenticação de usuários, armazenamento permanente de selfies.

#### 1.3 Definições, Acrônimos e Abreviações

- **Embedding:** vetor numérico que representa um rosto para comparação de similaridade.
- **τ (threshold):** distância euclidiana máxima para considerar uma correspondência (0,60, definido no artigo).
- **S3, EC2, ALB, ASG:** serviços AWS (armazenamento de objetos, servidor virtual, load balancer, auto scaling group).
- **LGPD:** Lei Geral de Proteção de Dados.

#### 1.4 Referências

- Vasconcelos et al., "Designing a Face Recognition System for Event Photography," SBrT 2026.
- Desafio "Case 2: E-commerce – Black Friday Ready", disciplina Big Data e Cloud Computing.
- Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018).

---

### 2. Posicionamento

#### 2.1 Oportunidade de Negócio

Participantes de eventos técnicos raramente recebem, ou demoram a receber, as fotos em que aparecem. O SBrT PhotoMatch demonstra, em produção e ao vivo, uma forma automática de resolver isso, servindo também como validação prática do artigo aceito no SBrT2026.

#### 2.2 Descrição do Problema

| | |
|---|---|
| **O problema de...** | Buscar manualmente fotos próprias em um acervo de mais de mil imagens de um evento. |
| **Afeta...** | Participantes do SBrT2025 que também estarão no SBrT2026. |
| **Cujo impacto é...** | Perda de tempo, fotos nunca recuperadas, baixa visibilidade do trabalho de pesquisa apresentado. |
| **Uma solução bem-sucedida incluiria...** | Um site simples, disponível durante o evento, que devolve os resultados em poucos segundos, mesmo com vários acessos simultâneos na sala do pôster. |

#### 2.3 Posicionamento do Produto

Para participantes do SBrT já fotografados em edições anteriores, o SBrT PhotoMatch é uma demonstração funcional que devolve fotos correspondentes a uma selfie em segundos, sem cadastro. Diferente de uma galeria estática ou busca manual, usa reconhecimento facial validado cientificamente no artigo de origem.

---

### 3. Descrição dos Stakeholders e Usuários

| **Stakeholder** | **Necessidade Primária** | **Expectativa na Nuvem (AWS)** |
|---|---|---|
| Participantes do evento (usuários finais) | Encontrar as próprias fotos rapidamente | Resposta em poucos segundos, mesmo com fila de acesso no horário do pôster |
| Nicholas (autor/responsável) | Demonstração estável durante os 4 dias do evento, sem custo relevante fora dessa janela | Infraestrutura que escala durante o evento e volta ao mínimo depois |
| Professor/avaliador da disciplina | Validar a decisão arquitetural do desafio de Cloud | DAS justificado tecnicamente, conectado ao Case 2 |

---

### 4. Visão Geral do Produto/Solução

#### 4.1 Perspectiva do Produto

Aplicação web leve (frontend simples + API), hospedada na AWS. O acervo de fotos e os embeddings do SBrT2025 já existem (gerados durante a pesquisa) e são apenas consultados em tempo real — não há reprocessamento do acervo em produção.

#### 4.2 Funcionalidades Principais

- Upload de selfie pelo navegador (mobile-friendly, para uso a partir do QR Code).
- Geração do embedding da selfie e comparação com o acervo indexado.
- Retorno das fotos com distância abaixo de τ = 0,60, ordenadas por similaridade.

#### 4.3 Suposições e Dependências

- **Suposição:** o volume de acesso é proporcional ao público presencial do evento (dezenas a poucas centenas de acessos concentrados, não milhares).
- **Dependência:** biblioteca `face_recognition` (dlib), já usada e validada no artigo.

---

### 5. Recursos do Produto (Arquitetura AWS)

| **Serviço AWS** | **Papel na Arquitetura** | **Justificativa Técnica** |
|---|---|---|
| Amazon EC2 (ou Lambda, a decidir na fase de elaboração) | Servidor da API de matching | Executa o embedding da selfie e a varredura no acervo; carga leve por requisição, mas variável ao longo do dia do evento |
| Auto Scaling Group + Application Load Balancer | Absorver o pico de acesso durante o evento | Replica o padrão do Case 2: tráfego concentrado em janela curta (4 dias), sem previsão exata do volume simultâneo na sala do pôster |
| Amazon S3 | Armazenamento do acervo de 1.427 fotos do SBrT2025 e entrega dos resultados | Evita que o servidor de aplicação sirva arquivos de imagem diretamente; custo baixo, leitura via URL pré-assinada |
| Amazon CloudWatch | Monitoramento básico | Acompanhar CPU/latência da API durante o evento e confirmar que o Auto Scaling reage a tempo |
| AWS Budgets | Controle de custo | Alerta se o gasto ultrapassar o orçamento pessoal do projeto |

---

### 6. Restrições do Projeto

- **Orçamentária:** custo pago pelo próprio autor; meta de até **US$ 20–30 no mês do evento**, tendendo a zero fora dessa janela.
- **Prazo:** sistema em produção até 29/09/2026 (início do SBrT2026).
- **Tecnológica:** reaproveitar o pipeline já validado (`face_recognition`/dlib, τ = 0,60); acervo e embeddings do SBrT2025 já prontos.
- **Segurança e Privacidade:** selfies enviadas pelos usuários não podem ser retidas após a busca; as fotos do acervo já são material de fotografia profissional do evento, não coletado para fins biométricos (conforme registrado no artigo).
- **Pessoal:** projeto solo (Nicholas).

---

### 7. Atributos de Qualidade (SLA e SLO)

- **Disponibilidade:** sem SLA formal — meta informal de disponibilidade durante o horário do evento (09h–18h, 29/09 a 02/10/2026).
- **Performance:** resposta da busca em até ~5s por requisição (embedding + varredura em 3.344 embeddings é uma operação leve).
- **Segurança:** tráfego apenas via HTTPS; selfie descartada logo após o processamento da requisição.
- **Custo-eficiência:** Auto Scaling reduzido ao mínimo (idealmente zero/near-zero) fora da janela do evento.

---

### 8. Aprovação e Histórico de Versões

| **Versão** | **Data** | **Descrição da Alteração** | **Autor(es)** |
|---|---|---|---|
| 1.0 | 04/09/2026 | Elaboração inicial do Documento de Visão | Nicholas Borges de Vasconcelos |
