# **Case de Exemplo: Logística & IoT – "SwiftTrack IoT"**

**Desafio Detalhado:** O grupo atuará no planejamento da infraestrutura de nuvem híbrida (IaaS e Serverless) para uma empresa de logística expressa (*last-mile*) que realiza o monitoramento e rastreamento de entregas urbanas em tempo real. A equipe de arquitetura deve estruturar o ecossistema para suportar tanto a plataforma de telemetria dos veículos quanto o sistema administrativo de faturamento e rotas.

*   **O Problema:** A infraestrutura legada não consegue lidar com a alta concorrência de conexões simultâneas enviadas pelos rastreadores GPS de milhares de veículos em trânsito. O fluxo incessante de escritas de telemetria causa gargalos e travamento na API administrativa central, impedindo que os operadores acessem os relatórios de faturamento nos horários de pico e atrasando a confirmação das entregas para os clientes finais.
*   **Requisitos Técnicos:**
    *   **Processamento de Telemetria:** Capacidade de ingerir e persistir dados de geolocalização e telemetria em **tempo real** sem afetar o desempenho do sistema de gestão.
    *   **Disponibilidade:** SLA global de **99,95%** de uptime para a API de faturamento e painéis administrativos.
    *   **Segurança e Privacidade:** Criptografia de dados sensíveis de motoristas e clientes em repouso e em trânsito para conformidade com a **LGPD**, além de isolamento completo das credenciais de banco de dados.
    *   **Automação:** Fluxo de deploy automatizado a fim de eliminar processos manuais e reduzir a indisponibilidade durante atualizações de versão em produção.
*   **Restrição Financeira:** Orçamento operacional máximo estipulado em **US\$ 1.500,00/mês**.
*   **Serviços Sugeridos para o DAS:** 
    *   A API administrativa centralizada desenvolvida em Python com **Django REST Framework** rodando em instâncias **Amazon EC2** configuradas com Gunicorn e Nginx.
    *   Banco de dados relacional **Amazon RDS (PostgreSQL)** em arquitetura de alta disponibilidade **Multi-AZ** para garantir a persistência segura de dados transacionais.
    *   Mecanismo de recepção serverless usando **Amazon API Gateway** e **AWS Lambda** para processar as mensagens dos dispositivos IoT rapidamente e com baixo custo.
    *   Banco de dados NoSQL **Amazon DynamoDB** para o armazenamento altamente escalável das coordenadas GPS e histórico de rotas.
    *   **Amazon S3** acoplado ao **Amazon CloudFront (CDN)** para o armazenamento e entrega otimizada de mídias estáticas (como imagens digitalizadas de comprovantes de entrega).
    *   Gestão automatizada de segredos via **AWS Secrets Manager** para proteger as credenciais do banco de dados.
    *   Uso de **AWS CodePipeline** para automatizar o ciclo de integração e entrega contínua (CI/CD) a partir do repositório Git.


Ele foi planejado estrategicamente como o **exemplo ideal para a disciplina** porque integra, em uma única arquitetura híbrida e realista, **100% do conteúdo programático e das ferramentas previstas na ementa e no cronograma**:

*   A API administrativa centralizada em **Django REST Framework** rodando em **Amazon EC2** (com Nginx/Gunicorn).
*   Persistência relacional com **Amazon RDS (PostgreSQL)** em Multi-AZ para dados de negócios transacionais (faturamento, clientes, rotas).
*   Ingestão serverless de alta concorrência usando **AWS Lambda** e **Amazon API Gateway**.
*   Banco de dados NoSQL **Amazon DynamoDB** para armazenar as séries temporais de GPS dos veículos logísticos.
*   Arquivos estáticos e mídias no **Amazon S3** integrados ao **Amazon CloudFront (CDN)**.
*   Automação com pipeline de CI/CD via **AWS CodePipeline**.

---

### O Documento de Visão Completo 

Este arquivo foi detalhado de ponta a ponta seguindo o padrão oficial do RUP/UP para a fase de *Inception*, estruturado da seguinte forma:

1.  **Introdução:** Define o propósito do projeto, delimita seu escopo técnico/funcional e esclarece terminologias cruciais da nuvem (VPC, RDS, DynamoDB, SLA, RTO/RPO).
2.  **Posicionamento de Mercado:** Descreve as dores reais do setor de logística (*last-mile*) sob uma tabela de problema/impacto estruturada, contrastando a solução moderna contra arquiteturas legadas e on-premises.
3.  **Mapeamento de Stakeholders:** Identifica as expectativas exatas de Gestores Logísticos, Diretores Financeiros (CFOs), Profissionais de Segurança (CISOs) e do próprio Corpo Docente de TI.
4.  **Visão Geral da Solução:** Apresenta a perspectiva híbrida (Django + ingestão orientada a eventos serverless) e as principais dependências do ecossistema.
5.  **Recursos do Produto (Arquitetura AWS):** Fornece uma tabela robusta que mapeia cada recurso tecnológico (VPC, EC2, RDS, S3, DynamoDB, API Gateway, Lambda, Secrets Manager, CloudWatch e CodePipeline) com o seu respectivo papel e sua **justificativa técnica detalhada** conectada ao negócio.
6.  **Restrições do Projeto:** Estabelece limites realistas de orçamento (máximo de US\$ 1.500,00/mês), prazo acadêmico (20 semanas), stack tecnológico obrigatório, segurança corporativa (criptografia de dados em trânsito e repouso de dados sensíveis para conformidade com a **LGPD**) e restrição de pessoal.
7.  **Atributos de Qualidade (SLA e SLO):** Especifica metas mensuráveis de **Disponibilidade** (SLA global de 99,95% via Multi-AZ), **Performance** (latência menor que 80ms para ingestão), **Segurança** (KMS para repouso e HTTPS/TLS para trânsito), **Continuidade de Negócio** (RPO de 15 minutos e RTO de 1 hora via Point-In-Time Recovery) e **Custo-eficiência** (dimensionamento automático via Auto Scaling).
8.  **Histórico de Versões:** Bloco de controle documental para o ciclo de vida do projeto.

