# DOCUMENTO DE REQUISITOS SUPLEMENTARES (v1.0)

## XXXX

**Projeto:** Projeto de Cloud - Fase de Inception  
**Data:** 27/08/2026  
**Status:** Versão inicial para validação arquitetural

---

## 1. Propósito e escopo

Este documento define os requisitos não-funcionais, os objetivos de nível de serviço (SLOs), o acordo de nível de serviço (SLA) e as condições operacionais da plataforma SwiftTrack IoT.

O escopo inclui:

- 
-
-


Não fazem parte deste documento a implementação do código da aplicação, o desenho detalhado da VPC ou a contratação de serviços externos de geocodificação.

## 2. Contexto e restrições

| Item | Premissa ou restrição |
|---|---|
| Escala inicial |  |
| Frequência de telemetria |  |
| Pico de ingestão |  |
| Stack obrigatória |  |
| Equipe |  |
| Orçamento |  |
| Regulamentação |  |
| Crescimento esperado | |

## 3. Definições e indicadores

- **SLA:** compromisso formal de nível de serviço com o cliente.
- **SLO:** objetivo mensurável que orienta o serviço.
- **SLI:** indicador observado para verificar um SLO.
- **p95:** valor abaixo do qual estão 95% das medições.
- **RPO:** máximo de dados que podem ser perdidos após uma falha.
- **RTO:** tempo máximo para restaurar o serviço.
- **MTTR:** tempo médio para reparar ou restaurar o serviço.

## 4. Requisitos de desempenho e capacidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-PER-01 |  |
| RNF-PER-02 |  |
| RNF-PER-03 |  |
| RNF-PER-04 |  |
| RNF-CAP-01 |  |
| RNF-CAP-02 |  |

**Medição:** CloudWatch, métricas do API Gateway e testes de carga controlados. As medições devem registrar percentis, taxa de erro, throughput e cenário utilizado.

## 5. Requisitos de disponibilidade e confiabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-CON-01 |  |  |
| RNF-CON-02 |  |  |
| RNF-CON-03 |  |  |
| RNF-CON-04 |  |  |
| RNF-CON-05 |  |  |
| RNF-CON-06 | | |

**Diretriz:** utilizar, quando compatível com o orçamento...

## 6. Requisitos de segurança e privacidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-SEG-01 |  |  |
| RNF-SEG-02 |  |  |
| RNF-SEG-03 |  |  |
| RNF-SEG-04 |  |  |
| RNF-SEG-05 | |  |
| RNF-SEG-06 |  |  |
| RNF-SEG-07 |  |  |

## 7. Requisitos de operação e observabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-OPS-01 |  |  |
| RNF-OPS-02 |  |  |
| RNF-OPS-03 |  |  |
| RNF-OPS-04 |  | |
| RNF-OPS-05 |  |  |
| RNF-OPS-06 |  |  |

## 8. Requisitos de manutenibilidade e entrega

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-MAN-01 | | |
| RNF-MAN-02 | | |
| RNF-MAN-03 | | |
| RNF-MAN-04 || |
| RNF-MAN-05 | | |

## 9. Requisitos de usabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-USA-01 | | |
| RNF-USA-02 | | |
| RNF-USA-03 | | |

## 10. Requisitos de custo

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-CUS-01 || |
| RNF-CUS-02 | | |
| RNF-CUS-03 | | |
| RNF-CUS-04 | | |

**Trade-off obrigatório:** disponibilidade, desempenho e segurança não devem ser aprovados sem registrar o impacto correspondente no orçamento.

## 11. SLA e responsabilidades

O SLA inicial da API de faturamento e gestão estabelece **99,95% de disponibilidade mensal**, medido por chamadas sintéticas HTTPS a partir de uma região de referência. Manutenções comunicadas com antecedência e dentro da janela aprovada não entram no cálculo, conforme contrato definitivo.

| Responsável | Obrigações principais |
|---|---|
| AWS | |
| SwiftTrack | |
| Equipe de projeto | |

Descumprimentos devem gerar registro de incidente, análise de causa e plano de ação. Penalidades ou créditos comerciais serão definidos no contrato do serviço e não são assumidos como requisito técnico deste documento.

## 12. Dependências, riscos e decisões pendentes

| Item | Impacto | Tratamento |
|---|---|---|
| Custo real de Multi-AZ e observabilidade | Pode exceder US$ 1.500/mês | Validar no AWS Pricing Calculator antes do desenho final. |
| || |
| || |
| || |
| || |

## 13. Critérios de aprovação

O documento será considerado aprovado quando:

1. todos os requisitos críticos tiverem métrica e critério de aceitação;
2. a arquitetura proposta demonstrar atendimento aos requisitos de desempenho e disponibilidade;
3. o custo estimado estiver dentro do orçamento ou possuir exceção formal aprovada;
4. o plano de segurança e LGPD for revisado pelo responsável de segurança;
5. os testes de carga, backup, restore e rollback estiverem planejados.

## 14. Histórico de versões

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 27/08/2026 | Criação do Documento de Requisitos Suplementares para o case SwiftTrack IoT. | Equipe do projeto |

