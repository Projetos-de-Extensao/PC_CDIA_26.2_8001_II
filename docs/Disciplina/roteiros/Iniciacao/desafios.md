# Desafios de Arquitetura de Nuvem

Os desafios para os grupos devem ser formulados focando na **tomada de decisão arquitetural** e na **justificativa técnica** de cada escolha. Abaixo, apresento a formulação detalhada dos desafios, começando pelo Case 1.

### **Case 1: Fintech – "FastPay Instantâneo"**

**Desafio Detalhado:** O grupo deverá projetar a infraestrutura para uma startup de pagamentos que enfrenta problemas de latência e quedas frequentes em sua API.

*   **O Problema:** A arquitetura atual não suporta o crescimento acelerado e apresenta latência média de 200ms, o que é inaceitável para pagamentos em tempo real.

*   **Requisitos Técnicos:**

    *   **Performance:** Garantir latência **abaixo de 50ms** para 90% das transações.
    *   **Disponibilidade:** SLA de **99,99%** (aproximadamente 52 min de downtime/ano).
    *   **Segurança:** Conformidade estrita com **PCI-DSS** para dados de cartões e **LGPD**.

*   **Restrição Financeira:** O orçamento total é de **US\$ 2.000,00/mês**.

*   **Serviços Sugeridos para o DAS:** O grupo deve justificar o uso de instâncias EC2, RDS Multi-AZ para o PostgreSQL, ElastiCache (Redis) para reduzir a latência e KMS para criptografia.

### **Case 2: E-commerce – "Black Friday Ready"**

**Desafio Detalhado:** O grupo atuará como uma consultoria para uma loja virtual experiente que precisa escalar sua operação em 10x durante picos de tráfego, sem explodir os custos.

*   **O Problema:** O sistema atual é rígido e caro; o cliente quer pagar apenas pelo que usa (elasticidade) e otimizar gastos em períodos de baixa demanda.

*   **Requisitos Técnicos:**

    *   **Escalabilidade:** Implementação de **Auto Scaling** e **Load Balancer** para lidar com o aumento súbito de usuários.
    *   **Eficiência:** Uso de **S3** para entrega de mídia/arquivos estáticos para aliviar os servidores de aplicação.

*   **Objetivo de Cloud:** Reduzir o custo operacional mensal comparado ao modelo atual on-premises ou em nuvem mal configurada.

### **Case 3: GovTech – "Portal Cidadão Seguro"**
**Desafio Detalhado:** Planejar a infraestrutura de uma plataforma pública que lida com dados sensíveis de milhões de cidadãos, onde o risco de vazamento deve ser minimizado ao máximo.

*   **O Problema:** A plataforma é alvo constante de tentativas de invasão e precisa de auditoria completa de cada ação realizada.

*   **Requisitos Técnicos:**

    *   **Segurança Máxima:** Implementação de uma **VPC** altamente isolada, com uso rigoroso de **Security Groups** (stateful) e **NACLs** (stateless).
    *   **Governança:** Controle granular de acesso via **IAM** e monitoramento de logs centralizados no **CloudWatch**.

*   **Compliance:** Conformidade total com a **LGPD** e trilhas de auditoria para todos os acessos a dados sensíveis.

### **Case 4: HealthTech – "Vitalis Health"**

**Desafio Detalhado:** Desenvolver o projeto para um sistema de monitoramento remoto de pacientes crônicos, integrando dados de dispositivos wearables com dashboards médicos.

*   **O Problema:** Hospitais não conseguem monitorar pacientes em tempo real de forma confiável e os dados precisam estar disponíveis 24/7 para emergências.

*   **Requisitos Técnicos:**

    *   **Resiliência:** O sistema não pode parar; exige-se uma estratégia de **Backup** com RPO de 15 min e RTO de 1 hora.
    *   **Integração:** Capacidade de processar dados vindos de wearables e armazená-los de forma segura.

*   **Conformidade:** Seguir normas internacionais de saúde (como HIPAA) e nacionais (LGPD), garantindo criptografia em repouso e em trânsito.

### **Case 5: EdTech – "EducaStream Global"**

**Desafio Detalhado:** O grupo atuará no planejamento da infraestrutura de uma startup de ensino a distância (EAD) em rápido crescimento que atende a milhões de alunos ativos. O principal foco do projeto é viabilizar a entrega eficiente de conteúdos de mídia e videoaulas.

*   **O Problema:** A plataforma armazena e distribui milhares de videoaulas pesadas. A entrega de conteúdo sem uma rede de distribuição geográfica consome excessivamente os recursos computacionais dos servidores de aplicação, resultando em travamentos constantes nos horários de pico (como noites e finais de semana) e gerando cobranças exorbitantes de tráfego de saída de dados (Data Transfer Out).

*   **Requisitos Técnicos:**

    *   **Performance:** Baixa latência e carregamento rápido para o player de vídeo, independentemente da localização do usuário no país.
    *   **Escalabilidade:** Capacidade de absorver picos massivos e sazonais de tráfego durante lançamentos de grandes cursos ou períodos de exames escolares.
    *   **Segurança:** Mecanismos de controle de acesso aos recursos de mídia para impedir downloads piratas de cursos pagos.

*   **Restrição Financeira:** Perfil de startup com orçamento altamente restrito e necessidade de **custo otimizado**, com limite de **US\$ 1.000,00/mês**.

*   **Serviços Sugeridos para o DAS:** Utilização de buckets **Amazon S3** para hospedar os arquivos estáticos e de mídia, integrados com o **Amazon CloudFront (CDN)** para cache global de conteúdo. A API de gerenciamento acadêmico e controle de progresso deve rodar em instâncias **EC2** com **Auto Scaling** conectadas a um banco de dados relacional **RDS (PostgreSQL)** gerenciado.

### **Case 6: AgTech – "Lavoura Inteligente"**

**Desafio Detalhado:** O grupo projetará a arquitetura para uma plataforma de análise de dados agrícolas alimentada por sensores IoT (Internet das Coisas) distribuídos por lavouras conectadas de grande extensão.

*   **O Problema:** Milhares de sensores enviam telemetria detalhada de umidade do solo, acidez, temperatura e clima de minuto em minuto. O banco de dados relacional tradicional atual não suporta a alta concorrência de escritas simultâneas de séries temporais, gerando lentidão extrema no banco e atrasos de até horas na emissão de alertas automáticos e críticos de irrigação aos produtores.

*   **Requisitos Técnicos:**

    *   **Processamento e Ingestão:** Ingestão massiva de dados com processamento analítico e geração de insights em **tempo real**.
    *   **Escalabilidade de Escrita:** A estrutura de armazenamento precisa escalar horizontalmente para acomodar as leituras e gravações contínuas de bilhões de registros de sensores sem perda de dados.
    *   **Visualização:** Fornecer dados limpos e consolidados para que a aplicação web renderize painéis interativos para agrônomos de campo.

*   **Restrição Financeira:** Empresa consolidada no setor do agronegócio, com orçamento razoável de até **US\$ 1.500,00/mês**.

*   **Serviços Sugeridos para o DAS:** Uso de banco de dados NoSQL **Amazon DynamoDB** para persistência altamente escalável dos dados brutos e de telemetria. Processamento serverless orientado a eventos usando **AWS Lambda** e **API Gateway** para coleta e sanitização de payloads de sensores, e o **Amazon S3** para guardar arquivos históricos e consolidados de safras passadas.

