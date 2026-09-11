Excelente solicitação! Vamos estruturar os artefatos do RUP/UP para cada semana da disciplina **Projeto de Cloud**, alinhando-os com as atividades propostas. Isso criará um fluxo lógico de documentação que culminará no **Documento de Arquitetura de Software (DAS)** completo.

---

## ESTRUTURA DE DOCUMENTOS RUP/UP PARA PROJETO DE CLOUD

### Disciplina: Projeto de Cloud (140h) - 20 Semanas

---

### FASES DO RUP/UP E SEUS FLUXOS DE TRABALHO

| **Fase RUP** | **Semanas** | **Fluxos de Trabalho (Disciplinas RUP)** |
| :--- | :--- | :--- |
| **Inception (Concepção)** | 1 - 2 | Modelagem de Negócios, Requisitos, Análise Preliminar |
| **Elaboration (Elaboração)** | 3 - 8 | Requisitos, Análise e Design, Arquitetura, Ambiente |
| **Construction (Construção)** | 10 - 15 | Implementação, Teste, Implantação (Planejada) |
| **Transition (Transição)** | 16 - 18 | Implantação (Validação), Gerenciamento de Mudanças |

---

### MAPEAMENTO SEMANAL DE DOCUMENTOS E ATIVIDADES

| **Semana** | **Fase RUP** | **Atividade** | **Documento RUP/UP** | **Descrição do Artefato** |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Inception** | Apresentação da disciplina. Revisão dos serviços AWS. Definição do caso de uso. | **Documento de Visão** | Versão inicial: descreve o problema, os stakeholders, as necessidades do negócio e a visão geral da solução. Inclui o case de negócio (ex: fintech, e-commerce, saúde). |
| **2** | **Inception** | Levantamento de Requisitos Não-Funcionais. Definição de SLAs, SLOs e métricas. | **Documento de Requisitos Suplementares** | Foco em requisitos não-funcionais: desempenho (TPS, latência), disponibilidade (99,9%), segurança, usabilidade, manutenibilidade. Inclui SLAs e SLOs. |
| **3** | **Elaboration** | **Workshop 1:** Projeto de VPC e Rede. | **Modelo de Casos de Uso (Arquitetural)** | Diagrama de Casos de Uso de infraestrutura: "Configurar Rede", "Estabelecer Conectividade", "Gerenciar Tráfego". Descreve atores (Admin, DevOps) e fluxos. |
| **4** | **Elaboration** | **Workshop 2:** Segurança e Controle de Acesso. | **Modelo de Análise (Pacotes/Subsistemas)** | Estrutura de pacotes de segurança: IAM, Network Security, Data Security. Define responsabilidades de cada componente de segurança. |
| **5** | **Elaboration** | **Workshop 3:** Dimensionamento de Banco de Dados (RDS). | **Modelo de Análise (Classes de Análise)** | Classes de análise para o banco de dados: `DatabaseInstance`, `ReadReplica`, `BackupPolicy`. Descreve responsabilidades e relacionamentos. |
| **6** | **Elaboration** | **Workshop 4:** Dimensionamento de Computação (EC2). | **Modelo de Análise (Classes de Análise)** | Classes para computação: `ComputeInstance`, `AutoScalingGroup`, `LoadBalancer`. Detalha configurações de escalabilidade. |
| **7** | **Elaboration** | **Workshop 5:** Dimensionamento de Armazenamento (S3). | **Modelo de Análise (Classes de Análise)** | Classes para armazenamento: `StorageBucket`, `LifecyclePolicy`, `ReplicationRule`. Define políticas de lifecycle e versionamento. |
| **8** | **Elaboration** | Consolidação da Arquitetura. | **Modelo de Design (Diagramas de Sequência/Comunicação)** | Diagramas de sequência para fluxos críticos: "Usuário faz requisição → API → Banco → Resposta". Demonstra interações entre componentes. |
| **9** | - | **AVALIAÇÃO 1 (P1)** | - | Prova sobre Arquitetura AWS, Dimensionamento e Well-Architected. |
| **10** | **Construction** | **Workshop 6:** Estratégias de Deploy (Blue-Green, Canary). | **Modelo de Design (Diagramas de Atividades)** | Fluxograma do pipeline de CI/CD. Diagramas de atividades mostrando o fluxo de deploy: Build → Test → Deploy → Validation → Rollback. |
| **11** | **Construction** | **Workshop 7:** Gerenciamento de Configurações e Segredos. | **Modelo de Design (Diagramas de Componentes)** | Diagramas de componentes mostrando integração com Secrets Manager e Parameter Store. Interfaces para acesso a configurações. |
| **12** | **Construction** | **Workshop 8:** Planejamento de Backup e Disaster Recovery. | **Plano de Gerenciamento de Configuração e Mudanças** | Inclui estratégias de backup (snapshots, replicação) e mudanças (rollback procedures). Define RPO/RTO. |
| **13** | **Construction** | **Workshop 9:** Estimativa de Custos e Otimização. | **Modelo de Implantação (Diagramas de Deploy)** | Diagramas de deployment mostrando distribuição geográfica, Multi-AZ, regiões. Inclui a infraestrutura de produção e DR. |
| **14** | **Construction** | **Workshop 10:** Monitoramento e Observabilidade. | **Modelo de Teste (Plano de Teste)** | Plano de teste para validação pós-deploy. Inclui testes de performance, stress, segurança e métricas de observabilidade. |
| **15** | **Construction** | Consolidação do Plano de Implantação. | **Documento de Arquitetura de Software (DAS) - Versão Preliminar** | Compilação de todos os artefatos anteriores: diagramas, cálculos, justificativas, estimativas. |
| **16** | **Transition** | **Simulação Prática:** Deploy em sandbox AWS. | **Relatório de Teste (Avaliação de Teste)** | Relatório detalhado da simulação: o que foi testado, resultados obtidos, comparação com estimativas (custo x real, performance x esperada). |
| **17** | **Transition** | Ajustes finos nos artefatos. | **Documento de Arquitetura de Software (DAS) - Versão Final** | Versão revisada com base nos resultados da simulação. Inclui lições aprendidas e recomendações. |
| **18** | **Transition** | **AVALIAÇÃO 2 (P2):** Defesa oral. | **Documento de Arquitetura de Software (DAS) Completo + Apresentação** | DAS final consolidado + apresentação de defesa do projeto (20 min). |
| **19** | - | **AVALIAÇÃO SUPLEMENTAR (PS)** | - | Prova de reposição. |
| **20** | - | Encerramento. Feedback. | **Documento de Avaliação Pós-Implantação** | Feedback final sobre o processo e recomendações para projetos futuros. |

---

### DESCRIÇÃO DETALHADA DOS PRINCIPAIS ARTEfATOS RUP/UP

#### 1. Documento de Visão (Semana 1)

**Estrutura do Documento:**

| **Seção** | **Descrição** |
| :--- | :--- |
| 1. Introdução | Propósito, escopo, definições, referências. |
| 2. Posicionamento | Oportunidade de negócio, descrição do problema, posicionamento do produto. |
| 3. Descrição dos Stakeholders e Usuários | Perfis de usuários (Desenvolvedor, DevOps, Analista de Dados, etc.), necessidades. |
| 4. Visão Geral do Produto | Perspectiva do produto, funcionalidades principais, suposições e dependências. |
| 5. Recursos do Produto | Lista de funcionalidades (ex: API REST, Autenticação, Armazenamento de Dados). |
| 6. Restrições | Orçamento, prazo, tecnologia, conformidade (LGPD). |

**Exemplo Prático:**

> *"O projeto visa implantar uma API de análise de dados financeiros para uma fintech, garantindo alta disponibilidade (99,95%), baixa latência (< 100ms) e conformidade com a LGPD, com custo operacional estimado em R$ 5.000/mês."*

---

#### 2. Documento de Requisitos Suplementares (Semana 2)

**Estrutura do Documento:**

| **Seção** | **Descrição** |
| :--- | :--- |
| 1. Requisitos de Desempenho | Throughput (req/s), tempo de resposta, capacidade de usuários simultâneos. |
| 2. Requisitos de Confiabilidade | Disponibilidade (SLA), MTBF, MTTR, RPO, RTO. |
| 3. Requisitos de Segurança | Autenticação, autorização, criptografia (em trânsito e repouso), auditoria. |
| 4. Requisitos de Usabilidade | Interfaces de monitoramento, dashboards, alertas. |
| 5. Requisitos de Manutenibilidade | Facilidade de deploy, rollback, atualizações. |
| 6. Requisitos de Operação | Monitoramento, logging, backup, recovery. |

**Exemplo Prático:**

> *"A API deve suportar 1.000 requisições por segundo com latência média de 80ms, disponibilidade de 99,95%, RPO de 15 minutos e RTO de 1 hora."*

---

#### 3. Modelo de Casos de Uso (Semana 3)

**Estrutura dos Casos de Uso:**

| **Elemento** | **Descrição** |
| :--- | :--- |
| **Atores** | Admin, DevOps, Cliente, Sistema. |
| **Casos de Uso** | "Configurar Infraestrutura", "Implantar Nova Versão", "Monitorar Sistema", "Recuperar de Falha". |
| **Pré-condições** | O que deve estar disponível antes. |
| **Pós-condições** | O que muda após a execução. |
| **Fluxo Principal** | Passos normais do caso de uso. |
| **Fluxos Alternativos** | Exceções e caminhos alternativos. |

**Diagrama de Casos de Uso (Exemplo):**
@startuml
top to bottom direction

actor "Administrador" as Admin
actor "DevOps" as DevOps
actor "Cliente" as Cliente
actor "Sistema" as Sistema

rectangle "API Financeira" {
  usecase "Configurar Infraestrutura" as UC1
  usecase "Implantar Nova Versão" as UC2
  usecase "Monitorar Sistema" as UC3
  usecase "Recuperar de Falha" as UC4
}

Admin --> UC1
DevOps --> UC2
Cliente --> UC3
Sistema --> UC4

UC1 --> UC2 : Executa
UC2 --> UC3 : Gera logs
UC3 --> UC4 : Detecta falha
@enduml

---

#### 4. Modelo de Análise (Semanas 4-7)

**Classes de Análise (Exemplo - RDS):**

| **Classe** | **Responsabilidades** | **Atributos** |
| :--- | :--- | :--- |
| `DatabaseInstance` | Gerenciar instância RDS | engine, instanceClass, storageSize, multiAZ, backupRetention |
| `ReadReplica` | Gerenciar réplicas de leitura | sourceInstance, region, replicationLag |
| `BackupPolicy` | Gerenciar políticas de backup | frequency, retentionDays, snapshotWindow |
| `ParameterGroup` | Gerenciar parâmetros do banco | parameters: Map<String, String>, family |

---

#### 5. Modelo de Design (Semanas 10-13)

**Diagrama de Sequência - Deploy Blue-Green:**

```
Usuário       Pipeline        Green Env      Blue Env      Load Balancer
  |              |                |              |                |
  |--Trigger--->|                |              |                |
  |              |--Build------->|              |                |
  |              |                |              |                |
  |              |--Test-------->|              |                |
  |              |                |              |                |
  |              |--Deploy Green>|              |                |
  |              |                |              |                |
  |              |--Health Check>|              |                |
  |              |<----OK--------|              |                |
  |              |                |              |                |
  |              |--Switch LB--->|              |               *|
  |              |                |              |                |
  |              |                |              |--Rollback--->|
  |              |                |              |                |
```

---

#### 6. Documento de Arquitetura de Software (DAS) - Semanas 15 e 17

**Estrutura Completa do DAS:**

| **Seção** | **Conteúdo** |
| :--- | :--- |
| 1. Introdução | Propósito, escopo, referências, visão geral do documento. |
| 2. Visão Geral da Arquitetura | Decisões arquiteturais (serviços AWS), restrições, princípios de design. |
| 3. Modelo de Dados | Diagrama Entidade-Relacionamento, esquemas de banco, índices. |
| 4. Modelo de Componentes | Diagrama de componentes, interfaces, serviços (API, Auth, Storage). |
| 5. Modelo de Implantação | Diagrama de deployment (VPC, sub-redes, AZs, regiões), configurações de rede. |
| 6. Modelo de Segurança | IAM, Security Groups, criptografia, compliance (LGPD). |
| 7. Modelo de Desempenho | Dimensionamento (EC2, RDS, S3), justificativas técnicas, cálculos. |
| 8. Modelo de Deploy | Estratégias (Blue-Green, Canary), CI/CD, rollback procedures. |
| 9. Modelo de Continuidade | Backup, DR (RPO/RTO), estratégias de recuperação. |
| 10. Modelo de Custos | AWS Pricing Calculator, TCO, otimizações (Savings Plans, Spot). |
| 11. Modelo de Monitoramento | CloudWatch, dashboards, alarmes, métricas críticas. |
| 12. Relatório de Validação | Resultados da simulação, comparações teórico vs prático, lições aprendidas. |
| 13. Anexos | Diagramas (VPC, Sequência, Atividades), planilhas, referências. |

---

#### 7. Relatório de Teste / Simulação (Semana 16)

**Estrutura do Relatório:**

| **Seção** | **Descrição** |
| :--- | :--- |
| 1. Objetivo | Validar o planejamento com a prática. |
| 2. Cenários Testados | Deploy da API em sandbox, testes de performance, segurança. |
| 3. Métricas Coletadas | Custo real, latência, throughput, tempo de deploy, tempo de recovery. |
| 4. Comparação | Planejado (estimativas) vs Executado (real). |
| 5. Análise de Discrepâncias | O que deu diferente do esperado e por quê. |
| 6. Lições Aprendidas | O que poderia ser melhorado no planejamento. |
| 7. Recomendações | Sugestões para projetos futuros. |

---

### FLUXO DE TRABALHO E INTEGRAÇÃO DOS ARTEFATOS

```
Documento de Visão (Semana 1)
        ↓
Requisitos Suplementares (Semana 2)
        ↓
Casos de Uso (Semana 3)
        ↓
Modelo de Análise (Semanas 3-7)
        ↓
Modelo de Design (Semanas 8-14)
        ↓
DAS - Versão Preliminar (Semana 15)
        ↓
Simulação / Validação (Semana 16)
        ↓
DAS - Versão Final (Semana 17)
        ↓
Apresentação / Defesa (Semana 18)
```

---

### RESUMO DOS ENTREGÁVEIS POR SEMANA

| **Semana** | **Entregável Principal** | **Formato** |
| :--- | :--- | :--- |
| 1 | Documento de Visão (v1) | Documento Word/Google Docs |
| 2 | Documento de Requisitos Suplementares | Documento Word/Google Docs |
| 3 | Diagrama de Casos de Uso | Draw.io / Lucidchart |
| 4 | Pacotes de Análise (Segurança) | Draw.io / Lucidchart |
| 5 | Classes de Análise (RDS) | Draw.io / Lucidchart |
| 6 | Classes de Análise (EC2) | Draw.io / Lucidchart |
| 7 | Classes de Análise (S3) | Draw.io / Lucidchart |
| 8 | Diagramas de Sequência | Draw.io / Lucidchart |
| 9 | AVALIAÇÃO 1 | Prova Individual |
| 10 | Diagramas de Atividades (Deploy) | Draw.io / Lucidchart |
| 11 | Diagramas de Componentes | Draw.io / Lucidchart |
| 12 | Plano de Backup e DR | Documento Word/Google Docs |
| 13 | Diagramas de Deploy | Draw.io / Lucidchart |
| 14 | Plano de Teste | Documento Word/Google Docs |
| 15 | DAS - Versão Preliminar | Documento Completo |
| 16 | Relatório de Simulação | Documento Word/Google Docs |
| 17 | DAS - Versão Final | Documento Completo |
| 18 | AVALIAÇÃO 2 | DAS + Apresentação Oral |
| 19 | AVALIAÇÃO SUPLEMENTAR | Prova |
| 20 | Documento de Encerramento | Relatório Final |

---

### EXEMPLO PRÁTICO DE CONTEÚDO PARA O DAS

**Seção 5.3 - Dimensionamento do RDS (Cálculo)**

> **Cenário:** API com 1.000 requisições/segundo, cada requisição gera 2 queries SQL.
> - Total de queries: 2.000 qps (queries por segundo).
> - Tempo médio de execução: 10ms.
> - IOPS necessários: 2.000 qps × 10ms = 20 IOPS.
> - Base de dados: 100 GB, crescimento de 10 GB/mês.
>
> **Escolha:** `db.t3.medium` (6 GB RAM, 2 vCPUs, suporte a 1.000 conexões).
> - IOPS provisionados: 100 (baseline), com capacidade de burst para 3.000 IOPS.
> - Storage: 100 GB SSD (gp3).
> - Multi-AZ: Habilitado (RPO = 0, failover automático).
> - Read Replicas: 1 réplica em outra AZ para distribuição de carga.
>
> **Custo Estimado (AWS Pricing Calculator - US East):**
> - RDS: $0.086/hora × 24 × 30 = $61,92/mês.
> - Storage: 100 GB × $0.10/GB = $10,00/mês.
> - Total: ~$71,92/mês (~R$ 350,00/mês).
>
> **Justificativa:** A instância t3.medium oferece o melhor custo-benefício para a carga esperada, com folga para picos de demanda, enquanto o Multi-AZ garante a disponibilidade de 99,95% exigida pelo SLA.

---

Essa estrutura garante que cada semana da disciplina **Projeto de Cloud** produza um artefato RUP/UP específico, construindo gradativamente o DAS completo. A integração com a disciplina **Big Data e Cloud Computing** acontece naturalmente, pois os artefatos de planejamento (Projeto de Cloud) são baseados na experiência prática da construção (Big Data e Cloud Computing).