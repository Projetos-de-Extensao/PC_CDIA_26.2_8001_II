# PROJETO DE CLOUD - FASE DE INCEPTION
#### LEVANTAMENTO DE REQUISITOS NÃO-FUNCIONAIS, SLAs, SLOs E DOCUMENTO DE REQUISITOS SUPLEMENTARES
### CASE "SWIFTTRACK IOT" COMO EXEMPLO CENTRAL

---

## 1. OBJETIVOS DA SEMANA

### 1.1. Objetivo Geral
Capacitar os alunos a identificar, documentar e quantificar requisitos não-funcionais para projetos de infraestrutura em nuvem, traduzindo necessidades de negócio em métricas técnicas (SLAs, SLOs) que guiarão todo o projeto de arquitetura, utilizando o case "SwiftTrack IoT" como referência prática.

### 1.2. Objetivos Específicos
- Compreender a diferença entre requisitos funcionais e não-funcionais.
- Identificar e classificar requisitos não-funcionais críticos para projetos em nuvem.
- Definir SLAs (Service Level Agreements) e SLOs (Service Level Objectives) mensuráveis.
- Estabelecer métricas de desempenho, disponibilidade, segurança, usabilidade e manutenibilidade.
- Elaborar a versão inicial do Documento de Requisitos Suplementares.
- Aplicar os conceitos ao case "SwiftTrack IoT".

---

## 2. ESTRUTURA DA AULA 

| **Horário** | **Atividade** | **Duração** | **Tipo** |
| :--- | :--- | :--- | :--- |
| 09:00 - 09:15 | Abertura: Conexão com a Semana Anterior | 15 min | Expositiva/Interativa |
| 09:15 - 10:00 | Teoria: Requisitos Não-Funcionais no Contexto de Nuvem | 45 min | Expositiva com Exemplos |
| 10:00 - 10:45 | SLAs, SLOs e Métricas: O que, Por que e Como Definir | 45 min | Expositiva + Estudo de Caso |
| 10:45 - 11:00 | Intervalo | 15 min | - |
| 11:00 - 11:40 | Exercício Prático: Definição de SLAs/SLOs para o Case SwiftTrack | 40 min | Hands-on em Grupo |
| 11:40 - 12:15 | Preenchimento do Documento de Requisitos Suplementares | 35 min | Hands-on Guiado |
| 12:15 - 12:45 | Apresentação dos Resultados e Discussão | 30 min | Pitch e Feedback |
| 12:45 - 13:00 | Encerramento, Dúvidas e Orientações para Entrega | 15 min | Sessão Final |

---

## 3. DESENVOLVIMENTO DETALHADO

---

### 3.1. ABERTURA: CONEXÃO COM A SEMANA ANTERIOR 

**Tema:** "Da Visão à Métrica - O Case SwiftTrack IoT"

#### 3.1.1. Revisão Rápida - "O que ficou da Semana 1?" 

**Dinâmica:** Os alunos recebem o **Documento de Visão do SwiftTrack IoT** (disponível no material de apoio) e respondem rapidamente:

1. **"Qual o problema central da SwiftTrack?"**
2. **"Quem são os principais stakeholders?"**
3. **"Qual a principal restrição do projeto?"**

**Respostas Esperadas:**
1. Infraestrutura legada não suporta alta concorrência de conexões IoT.
2. Gestores logísticos, CFO, CISO, equipe de TI.
3. Orçamento de US$ 1.500/mês.

**Objetivo:** Mostrar como o Documento de Visão se conecta diretamente aos requisitos não-funcionais.

#### 3.1.2. Contextualização do Tema - "O Desafio da SwiftTrack" 

**Slide de Abertura:**

```
+------------------------------------------------------+
|   DA VISÃO ÀS MÉTRICAS - SWIFTTRACK IOT              |
+------------------------------------------------------+
|                                                       |
|   Documento de Visão (Semana 1):                      |
|   "Implantar infraestrutura híbrida para telemetria   |
|    de 10.000 veículos em tempo real."                |
|                                                       |
|              ↓ (O que isso significa?)                |
|                                                       |
|   Documento de Requisitos Suplementares (Semana 2):   |
|   - Ingestão de 5.000 eventos/segundo                |
|   - Latência < 80ms para telemetria                  |
|   - Disponibilidade: 99,95% para API                 |
|   - RPO: 15 min, RTO: 1 hora                         |
|   - Custo: < US$ 1.500/mês                           |
|                                                       |
+------------------------------------------------------+
```

**Momento Interativo:**
> *"Observem o Documento de Visão da SwiftTrack. O que está escrito lá que vocês acham que precisa ser 'traduzido' em números para a arquitetura?"*

**Respostas Esperadas:**
- "Processamento em tempo real" → Latência, throughput.
- "Alta concorrência de conexões" → Escalabilidade, TPS.
- "Sem afetar o sistema de gestão" → Isolamento, disponibilidade.
- "Conformidade com LGPD" → Criptografia, segurança.
- "Orçamento US$ 1.500" → Custo.

---

### 3.2. TEORIA: REQUISITOS NÃO-FUNCIONAIS NO CONTEXTO DE NUVEM

**Tema:** "O que a SwiftTrack realmente precisa?"

#### 3.2.1. Conceitos Fundamentais

| **Conceito** | **Definição** | **Exemplo (SwiftTrack)** |
| :--- | :--- | :--- |
| **Requisitos Funcionais** | O que o sistema **faz**. Funcionalidades, comportamentos. | "A API deve processar dados de GPS dos veículos." |
| **Requisitos Não-Funcionais** | Como o sistema **é**. Atributos de qualidade, restrições. | "A API deve processar 5.000 eventos/segundo com latência < 80ms." |

**Metáfora Ilustrativa com a SwiftTrack:**

```
+------------------------------------------------------+
|    REQUISITOS FUNCIONAIS (O QUE)                      |
+------------------------------------------------------+
|    A SwiftTrack precisa:                              |
|    - Ingerir dados de GPS dos veículos               |
|    - Armazenar histórico de rotas                     |
|    - Gerar faturas para clientes                      |
|    - Exibir dashboards para operadores               |
+------------------------------------------------------+

+------------------------------------------------------+
|    REQUISITOS NÃO-FUNCIONAIS (COMO)                  |
+------------------------------------------------------+
|    A SwiftTrack precisa que a ingestão seja:          |
|    - Rápida (< 80ms de latência)                     |
|    - Confiável (99,95% de disponibilidade)           |
|    - Segura (criptografada, LGPD)                    |
|    - Escalável (10.000 veículos)                     |
|    - Econômica (US$ 1.500/mês)                       |
+------------------------------------------------------+
```

#### 3.2.2. Categorias de Requisitos Não-Funcionais Aplicadas à SwiftTrack

| **Categoria** | **O que é?** | **Exemplo na SwiftTrack** | **Como Medir?** |
| :--- | :--- | :--- | :--- |
| **Desempenho** | Velocidade e capacidade. | Ingestão de 5.000 eventos/segundo; Latência < 80ms. | TPS, ms, MB/s. |
| **Disponibilidade** | Tempo operacional. | API de faturamento com 99,95% de uptime. | %, minutos/ano. |
| **Confiabilidade** | Operação sem falhas. | RPO 15 min, RTO 1 hora. | Minutos, horas. |
| **Segurança** | Proteção de dados. | Criptografia AES-256; Conformidade LGPD. | Algoritmos, padrões. |
| **Usabilidade** | Facilidade de uso. | Dashboards intuitivos para operadores. | NPS, tempo de treinamento. |
| **Manutenibilidade** | Facilidade de manutenção. | Deploy automatizado via CodePipeline; Logs centralizados. | Tempo de deploy, cobertura de logs. |
| **Escalabilidade** | Capacidade de crescer. | Suporte a 10.000 veículos + crescimento de 20%/ano. | Número de instâncias, tempo de auto scaling. |
| **Custo** | Recursos financeiros. | Orçamento máximo US$ 1.500/mês. | $/hora, $/mês, $/transação. |

**Exemplo Prático - SwiftTrack:**

| **Categoria** | **Requisito** | **Métrica** |
| :--- | :--- | :--- |
| Desempenho | Ingestão de dados de GPS. | 5.000 eventos/segundo, latência < 80ms. |
| Disponibilidade | API de faturamento. | 99,95% de uptime mensal. |
| Segurança | Dados de motoristas/clientes. | Criptografia AES-256, LGPD. |
| Custo | Todos os serviços AWS. | < US$ 1.500/mês. |

#### 3.2.3. Como Identificar Requisitos Não-Funcionais?

**Perguntas Guia para Levantamento (Aplicadas à SwiftTrack):**

| **Pergunta** | **Requisito Não-Funcional Identificado** | **Resposta no Case** |
| :--- | :--- | :--- |
| "Quantos veículos serão monitorados?" | Desempenho, Escalabilidade. | 10.000 veículos, crescimento 20%/ano. |
| "Qual a janela de tempo para processar os dados?" | Desempenho, Latência. | Tempo real (< 80ms). |
| "O sistema pode ficar fora do ar?" | Disponibilidade. | 99,95% (API de faturamento). |
| "Qual o orçamento disponível?" | Custo. | US$ 1.500/mês. |
| "Quais regulamentações se aplicam?" | Segurança, Compliance. | LGPD (dados pessoais). |
| "Quem vai operar o sistema?" | Manutenibilidade, Usabilidade. | Equipe de TI interna. |
| "Como vamos saber se o sistema está saudável?" | Monitoramento. | CloudWatch com métricas customizadas. |

**Técnica: "Os 5 Porquês" - Aplicado à SwiftTrack:**

> *"Por que precisamos de alta disponibilidade?"*
> *→ "Porque se o sistema de faturamento cair, não emitimos notas fiscais."*
> *→ "Por que isso é grave?"*
> *→ "Porque clientes não recebem comprovantes e atrasamos pagamentos."*
> *→ "Qual o impacto financeiro de 1 hora de downtime?"*
> *→ "Cerca de US$ 10.000 em faturas não processadas."*
> *→ "Então qual disponibilidade precisamos?"*
> *→ "99,95% para perder no máximo US$ 500/ano."*

**Atividade Rápida:** Em duplas, os alunos aplicam a técnica dos "5 Porquês" para um dos requisitos da SwiftTrack (ex: "segurança de dados de motoristas") e identificam 3 requisitos não-funcionais.

---

### 3.3. SLAs, SLOs E MÉTRICAS: O QUE, POR QUE E COMO DEFINIR (45 min)

**Tema:** "Transformando o 'quanto' em 'como' - O Caso SwiftTrack"

#### 3.3.1. Conceitos Fundamentais com Exemplos da SwiftTrack (15 min)

| **Conceito** | **Definição** | **Exemplo (SwiftTrack)** |
| :--- | :--- | :--- |
| **SLA (Service Level Agreement)** | Acordo formal entre provedor e cliente sobre o nível de serviço esperado. | "Disponibilidade de 99,95% para API de faturamento com crédito de 10% se descumprido." |
| **SLO (Service Level Objective)** | Objetivo mensurável que compõe um SLA. | "Latência p95 < 80ms para ingestão" ou "Uptime > 99,95%." |
| **SLI (Service Level Indicator)** | Métrica real que indica se o SLO está sendo cumprido. | "Latência p95 medida = 65ms" ou "Uptime calculado = 99,97%." |

**Analogia com a SwiftTrack:**

```
+------------------------------------------------------+
|   SWIFTTRACK É UMA OPERAÇÃO DE LOGÍSTICA              |
+------------------------------------------------------+
|                                                       |
|   SLA: "A entrega deve chegar ao cliente em até       |
|        2 horas após a coleta."                        |
|   SLO: "Chegar em 1 hora e 30 minutos ou menos."     |
|   SLI: "A entrega chegou em 1 hora e 20 minutos."    |
|                                                       |
|   Se falharmos o SLO (1h45), ainda estamos dentro    |
|   do SLA (2h). Se falharmos o SLA, o cliente recebe  |
|   um desconto.                                       |
+------------------------------------------------------+
```

#### 3.3.2. Estrutura de um SLA - Aplicada à SwiftTrack 

| **Componente** | **Descrição** | **Exemplo (SwiftTrack)** |
| :--- | :--- | :--- |
| **Serviço** | O que está sendo entregue. | API de Faturamento e Gestão. |
| **Métrica** | O que será medido. | Disponibilidade, latência. |
| **Objetivo** | O valor alvo. | 99,95% de disponibilidade, latência < 80ms. |
| **Janela de Medição** | Período de avaliação. | Mensal (30 dias). |
| **Exceções** | O que não é contabilizado. | Manutenção programada (máx 2h/mês), ataques DDoS. |
| **Penalidades** | O que acontece se falhar. | Crédito de 10% na fatura mensal. |
| **Responsabilidades** | Quem é responsável por quê. | AWS (infraestrutura) vs Empresa (código/config). |

**Exemplo de SLA para a SwiftTrack:**

```
+------------------------------------------------------+
|  SLA - API DE FATURAMENTO SWIFTTRACK                 |
+------------------------------------------------------+
|                                                       |
|  Serviço: API REST de faturamento e gestão.          |
|  Métrica: Disponibilidade.                           |
|  Objetivo: 99,95% de uptime mensal.                 |
|  Janela: 30 dias corridos.                          |
|  Exceções: Manutenção programada (máx 2h/mês).      |
|  Penalidade: 10% de crédito na fatura se < 99,95%.  |
|  Responsabilidades:                                  |
|    - AWS: EC2, RDS, S3, DynamoDB.                   |
|    - SwiftTrack: Código, configuração, monitoramento.|
|                                                       |
+------------------------------------------------------+
```

#### 3.3.3. SLOs Detalhados por Categoria - SwiftTrack 

**Desempenho:**

| **SLO** | **Descrição** | **Métrica** | **Justificativa** |
| :--- | :--- | :--- | :--- |
| Latência de Ingestão | Tempo para processar eventos IoT. | p95 < 80ms | Experiência do motorista em tempo real. |
| Throughput de Ingestão | Capacidade de processamento. | > 5.000 eventos/segundo | Pico de 10.000 veículos. |
| Latência da API | Tempo de resposta para dashboards. | p95 < 200ms | Usabilidade dos operadores. |

**Disponibilidade e Confiabilidade:**

| **SLO** | **Descrição** | **Métrica** | **Justificativa** |
| :--- | :--- | :--- | :--- |
| Uptime (API) | API administrativa disponível. | 99,95% (~22 min/mês downtime) | Faturamento contínuo. |
| Uptime (Ingestão) | Telemetria disponível. | 99,9% (~43 min/mês downtime) | Tolerância maior para dados de rastreamento. |
| RPO | Dados perdidos permitidos. | < 15 minutos | Recuperação de dados críticos. |
| RTO | Tempo de recuperação. | < 1 hora | Continuidade de negócio. |

**Segurança:**

| **SLO** | **Descrição** | **Métrica** | **Justificativa** |
| :--- | :--- | :--- | :--- |
| Criptografia em Repouso | Dados armazenados seguros. | AES-256 | LGPD, dados sensíveis. |
| Criptografia em Trânsito | Dados transmitidos seguros. | TLS 1.3 | LGPD, dados sensíveis. |
| Rotação de Chaves | Chaves criptográficas renovadas. | A cada 90 dias | Boas práticas de segurança. |
| Logs de Auditoria | Rastreabilidade de acessos. | 100% das transações | Conformidade. |

**Manutenibilidade:**

| **SLO** | **Descrição** | **Métrica** | **Justificativa** |
| :--- | :--- | :--- | :--- |
| Tempo de Deploy | Nova versão em produção. | < 10 minutos | Agilidade, CI/CD. |
| Tempo de Rollback | Reversão de versão. | < 5 minutos | Resposta a incidentes. |
| Cobertura de Logs | Logs disponíveis para depuração. | 100% das requisições | Observabilidade. |

**Custo:**

| **SLO** | **Descrição** | **Métrica** | **Justificativa** |
| :--- | :--- | :--- | :--- |
| Custo Total | Orçamento operacional. | < US$ 1.500/mês | Restrição financeira. |
| Custo por Requisição | Custo unitário de ingestão. | < US$ 0,001 | Escalabilidade financeira. |

#### 3.3.4. Estudo de Caso - "O que aconteceu com a concorrente?"

**Cenário:**
> *Uma concorrente da SwiftTrack definiu "alta disponibilidade" como requisito, mas não quantificou. Em um dia de pico (Black Friday), o sistema de telemetria ficou 4 horas offline. O custo estimado: US$ 40.000 em multas contratuais + US$ 100.000 em perda de clientes.*

**Pergunta para a Turma:**
> *"Como um SLA/SLO poderia ter evitado isso?"*

**Resposta Esperada:**
- Definir SLO de 99,95% de disponibilidade para telemetria.
- Planejar arquitetura Multi-AZ com DynamoDB global.
- Estabelecer monitoramento com CloudWatch e alarmes.
- Realizar testes de carga antes do pico.

**Lições Aprendidas:**
> *"Requisitos vagos custam dinheiro. Requisitos mensuráveis salvam dinheiro."*

---

### 3.4. EXERCÍCIO PRÁTICO: DEFINIÇÃO DE SLAs/SLOs PARA O CASE SWIFTTRACK

**Tema:** "Seu Case, Suas Métricas"

#### 3.4.1. Instruções e Template 

**Template Entregue aos Alunos:**

| **Categoria** | **SLO** | **Métrica** | **Justificativa** | **Risco se não cumprido** | **Serviço AWS Envolvido** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Desempenho** | | | | | |
| **Disponibilidade** | | | | | |
| **Segurança** | | | | | |
| **Manutenibilidade** | | | | | |
| **Custo** | | | | | |

**Instruções:**
1. Baseado no Documento de Visão da SwiftTrack, cada grupo define **pelo menos 2 SLOs por categoria**.
2. Para cada SLO, deve haver:
   - Métrica clara (ex: p95, %, minutos).
   - Justificativa (ex: "SLA do concorrente", "expectativa do mercado", "norma regulatória").
   - Risco identificado (ex: "Perda de clientes", "Multa regulatória").
   - Serviço AWS que será usado para atingir o SLO.

#### 3.4.2. Atividade em Grupo 

**Exemplo de Preenchimento - SwiftTrack:**

| **Categoria** | **SLO** | **Métrica** | **Justificativa** | **Risco se não cumprido** | **Serviço AWS** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Desempenho** | Latência de ingestão < 80ms | p95 do tempo de processamento | Motoristas precisam de rastreamento em tempo real. | Motoristas perdem confiança no sistema. | Lambda, API Gateway, DynamoDB. |
| | Throughput > 5.000 eventos/s | Eventos por segundo | Pico de 10.000 veículos simultâneos. | Fila de eventos, atraso no rastreamento. | DynamoDB, Lambda. |
| **Disponibilidade** | Uptime API > 99,95% | Minutos de downtime/mês | Faturamento contínuo para clientes. | Multas contratuais, perda de receita. | RDS Multi-AZ, EC2 Auto Scaling. |
| | Uptime ingestão > 99,9% | Minutos de downtime/mês | Rastreamento tolera pequenas falhas. | Perda de dados de rastreamento. | Lambda, DynamoDB. |
| | RTO < 1 hora | Minutos para recuperar | Continuidade de negócio. | Paralisação das operações. | RDS Multi-AZ, DynamoDB. |
| | RPO < 15 minutos | Minutos de dados perdidos | Recuperação de dados críticos. | Perda de faturas e rotas. | RDS PITR, DynamoDB backups. |
| **Segurança** | Dados criptografados em repouso | AES-256 | LGPD, dados sensíveis de motoristas. | Multas, processos, perda de reputação. | RDS (KMS), S3 (KMS), DynamoDB. |
| | Dados criptografados em trânsito | TLS 1.3 | LGPD, dados sensíveis. | Multas, interceptação de dados. | API Gateway, CloudFront. |
| | Rotação de chaves | A cada 90 dias | Boas práticas de segurança. | Chaves comprometidas. | Secrets Manager, KMS. |
| **Manutenibilidade** | Deploy < 10 min | Minutos para novo deploy | Agilidade para correções e features. | Lentidão para lançamentos. | CodePipeline, CodeBuild. |
| | Rollback < 5 min | Minutos para reverter | Minimizar impacto de falhas. | Prolongamento de problemas. | CodeDeploy. |
| | Cobertura de logs | % de requisições logadas | Observabilidade para depuração. | Dificuldade em diagnosticar problemas. | CloudWatch Logs. |
| **Custo** | Custo total < US$ 1.500/mês | Dólares mensais | Orçamento aprovado. | Projeto inviável. | Todos os serviços. |
| | Custo por evento < US$ 0,001 | Dólares por evento | Escalabilidade financeira. | Margem de lucro reduzida. | Lambda, DynamoDB, API Gateway. |

**Material de Apoio:**
- Tabela de referência de disponibilidade.
- Referência de padrões de segurança.
- Lista de serviços AWS e seus custos médios.
- **Documento de Visão da SwiftTrack** (disponível para consulta).

#### 3.4.3. Revisão e Validação 

**Dinâmica:** Cada grupo troca sua tabela com outro grupo. O grupo revisor verifica:

| **Critério** | **Verificado?** | **Comentário** |
| :--- | :--- | :--- |
| Os SLOs são mensuráveis? | | |
| Há justificativas claras ligadas ao negócio? | | |
| Os riscos estão bem identificados? | | |
| Os SLOs são realistas com o orçamento? | | |
| Há conflitos entre SLOs? (ex: custo vs disponibilidade) | | |
| Os serviços AWS sugeridos são adequados? | | |

**Exemplo de Conflito (SwiftTrack):**
- SLO de disponibilidade 99,95% (requer RDS Multi-AZ) → Custo aumenta.
- SLO de custo < US$ 1.500/mês → Pode não comportar Multi-AZ.
- **Solução:** Justificar trade-off no Documento de Requisitos Suplementares.

---

### 3.5. PREENCHIMENTO DO DOCUMENTO DE REQUISITOS SUPLEMENTARES

**Tema:** "Documentando a SwiftTrack para o Futuro"

#### 3.5.1. Apresentação do Template (5 min)

**Template do Documento de Requisitos Suplementares:**

---

**DOCUMENTO DE REQUISITOS SUPLEMENTARES - SWIFTTRACK IOT**

| **Seção** | **Descrição** |
| :--- | :--- |
| **1. Introdução** | Propósito, escopo, definições, referências. |
| **2. Requisitos de Desempenho** | Throughput, latência, tempo de resposta, capacidade. |
| **3. Requisitos de Confiabilidade** | Disponibilidade, MTBF, MTTR, RPO, RTO. |
| **4. Requisitos de Segurança** | Autenticação, autorização, criptografia, auditoria. |
| **5. Requisitos de Usabilidade** | Interfaces, dashboards, documentação, treinamento. |
| **6. Requisitos de Manutenibilidade** | Deploy, rollback, monitoramento, logs, testes. |
| **7. Requisitos de Operação** | Backup, recovery, gestão de incidentes. |
| **8. Requisitos de Custo** | Orçamento, otimização, previsibilidade. |
| **9. Aprovação** | Assinaturas, versões, histórico. |

---

#### 3.5.2. Preenchimento Guiado - Seção por Seção 

**Passo 1: Introdução (2 min)**

| **Campo** | **Exemplo (SwiftTrack)** |
| :--- | :--- |
| Propósito | Definir os requisitos não-funcionais para a implantação da plataforma de telemetria SwiftTrack na AWS. |
| Escopo | API Django REST (EC2), RDS PostgreSQL, DynamoDB, S3, Lambda, API Gateway, CodePipeline. |
| Definições | TPS, Latência, RPO, RTO, LGPD, IoT, Telemetria, Last-mile. |
| Referências | AWS Well-Architected, LGPD, Documento de Visão SwiftTrack v1.0. |

**Passo 2: Requisitos de Desempenho (4 min)**

| **Requisito** | **Descrição** | **Métrica** |
| :--- | :--- | :--- |
| Throughput de Ingestão | Capacidade de processamento de eventos IoT. | > 5.000 eventos/segundo (pico: 10.000). |
| Latência de Ingestão | Tempo para processar cada evento. | p95 < 80ms. |
| Latência da API | Tempo de resposta para dashboards administrativos. | p95 < 200ms. |
| Tempo de Carregamento | Tempo para carregar dashboards. | < 3 segundos. |

**Passo 3: Requisitos de Confiabilidade **

| **Requisito** | **Descrição** | **Métrica** |
| :--- | :--- | :--- |
| Disponibilidade (API) | API de faturamento e gestão operacional. | 99,95% de uptime mensal. |
| Disponibilidade (Ingestão) | Pipeline de telemetria operacional. | 99,9% de uptime mensal. |
| RPO | Dados perdidos permitidos. | < 15 minutos. |
| RTO | Tempo de recuperação. | < 1 hora. |
| MTBF | Tempo médio entre falhas. | > 720 horas. |
| MTTR | Tempo médio de reparo. | < 30 minutos. |

**Passo 4: Requisitos de Segurança**

| **Requisito** | **Descrição** |
| :--- | :--- |
| Autenticação | Obrigatório MFA para admin, JWT para API. |
| Autorização | RBAC (Admin, Operador, Auditor). |
| Criptografia (repouso) | AES-256 para RDS, S3, DynamoDB, backups. |
| Criptografia (trânsito) | TLS 1.3 para toda comunicação externa. |
| Auditoria | Logs de todas as transações e acessos administrativos. |
| Compliance | LGPD (dados pessoais de motoristas e clientes). |
| Isolamento | Credenciais de banco de dados no Secrets Manager. |

**Passo 5: Requisitos de Usabilidade **

| **Requisito** | **Descrição** |
| :--- | :--- |
| Dashboards | Monitoramento do status da API, latência, TPS. |
| Documentação | Documentação interativa (Swagger/OpenAPI) para API. |
| Alertas | Alertas claros para incidentes (email, SMS, Slack). |
| Treinamento | Capacitação da equipe de operação. |

**Passo 6: Requisitos de Manutenibilidade **

| **Requisito** | **Descrição** | **Métrica** |
| :--- | :--- | :--- |
| Deploy automatizado | CI/CD via CodePipeline. | < 10 minutos. |
| Rollback rápido | Reversão para versão estável. | < 5 minutos. |
| Monitoramento | CloudWatch com métricas customizadas. | 100% de cobertura. |
| Logs | Logs centralizados e pesquisáveis. | 100% das requisições. |

**Passo 7: Requisitos de Operação **

| **Requisito** | **Descrição** |
| :--- | :--- |
| Backup | Backup diário do RDS com retenção de 30 dias; Snapshots do DynamoDB. |
| Recovery | Procedimento documentado e testado de recuperação. |
| Gestão de Incidentes | Plano de resposta a incidentes (P1, P2, P3). |
| Manutenção Programada | Janela de manutenção de 2h/mês (fora do horário comercial). |

**Passo 8: Requisitos de Custo **

| **Requisito** | **Descrição** | **Métrica** |
| :--- | :--- | :--- |
| Orçamento | Custos operacionais totais. | < US$ 1.500/mês. |
| Otimização | Uso de Spot Instances para workloads não-críticas. | Economia de 20-30%. |
| Previsibilidade | Custo previsível com variação < 10%. | > 90% de previsibilidade. |

#### 3.5.3. Checklist de Verificação 

| **Item** | **Verificado?** | **Observação** |
| :--- | :--- | :--- |
| Todos os SLOs têm métricas mensuráveis? | | |
| Há justificativas para cada requisito? | | |
| Os conflitos entre requisitos estão documentados? | | |
| Os requisitos são realistas com o orçamento? | | |
| Há conexão com o Documento de Visão? | | |
| Os serviços AWS sugeridos estão alinhados? | | |

---

### 3.6. APRESENTAÇÃO DOS RESULTADOS E DISCUSSÃO 

**Tema:** "Defendendo Suas Métricas para a SwiftTrack"

#### 3.6.1. Estrutura da Apresentação

| **Seção** | **Duração** | **Conteúdo** |
| :--- | :--- | :--- |
| **1. Overview** | 30s | "Somos o Grupo X e nosso case é SwiftTrack IoT." |
| **2. Principais SLOs** | 1.5min | Os 3 SLOs mais críticos e por quê. |
| **3. Trade-offs** | 1.5min | "Sacrificamos X para conseguir Y por causa de Z." |
| **4. Pergunta para Turma** | 30s | "O que vocês acham do nosso trade-off?" |

#### 3.6.2. Dinâmica de Participação - "Banca Examinadora"

**Durante as apresentações,** os outros grupos atuam como **banca examinadora** e preenchem:

| **Grupo** | **SLO Mais Crítico** | **Trade-off Destacado** | **Pergunta para o Grupo** |
| :--- | :--- | :--- | :--- |
| Grupo 1 | | | |
| Grupo 2 | | | |
| ... | | | |

**Perguntas para Estimular Discussão:**

1. *"Esse SLO de 99,95% é realista com o orçamento de US$ 1.500?"*
2. *"Como vocês garantiriam o RPO de 15 minutos com o DynamoDB?"*
3. *"Qual SLO vocês flexibilizariam se o orçamento fosse reduzido para US$ 1.000?"*
4. *"Como vocês mediriam a latência de ingestão < 80ms na prática?"*
5. *"O que vocês fariam para proteger os dados de motoristas contra vazamentos?"*

---

### 3.7. ENCERRAMENTO, DÚVIDAS E ORIENTAÇÕES PARA ENTREGA 

**Tema:** "Próximos Passos"

#### 3.7.1. Recap dos Aprendizados

**Dinâmica:** Em um quadro virtual (Miro), alunos escrevem:

1. **