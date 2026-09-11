# Documento de Visão (v1.0) 
## Case de Exemplo: SwiftTrack IoT
### Projeto de Cloud - Fase de Inception

### 1. Introdução
Este documento descreve as necessidades de negócio, restrições e requisitos de infraestrutura da plataforma SwiftTrack IoT, além de guiar o planejamento arquitetural da solução na nuvem AWS.

#### 1.1. Propósito
Definir a visão de escopo e arquitetura lógica/física para a implantação da plataforma **SwiftTrack IoT** na infraestrutura de nuvem AWS, demonstrando a viabilidade de uma arquitetura resiliente, de alta performance e custo otimizado para o monitoramento de frotas logísticas em tempo real.

#### 1.2. Escopo
O escopo deste projeto de cloud engloba os seguintes componentes e serviços AWS:
1. **Portal Administrativo e API Transacional:** Desenvolvido em Python com Django REST Framework para cadastros de frotas, motoristas, roteirização e emissão de relatórios consolidados.
2. **Pipeline Serverless de Ingestão de IoT:** Endpoint HTTP leve para receber ping de telemetria e dados de GPS de milhares de dispositivos a cada 10 segundos de forma assíncrona.
3. **Persistência de Dados Híbrida:** Armazenamento relacional para as operações de negócio e NoSQL para o histórico contínuo de rastreamento (séries temporais).
4. **Infraestrutura de Rede e Segurança:** Isolamento lógico dos servidores de aplicação e banco de dados, firewall rígido e gerenciamento seguro de variáveis de ambiente.
5. **Automação CI/CD:** Pipeline de integração e entrega contínua para garantir atualizações automáticas e seguras no servidor de produção.

#### 1.3. Definições, Acrônimos e Abreviações
* **API:** Application Programming Interface
* **VPC:** Virtual Private Cloud (Rede Virtual Privada)
* **RDS:** Relational Database Service (Banco de Dados Relacional Gerenciado)
* **NoSQL:** Not Only SQL (Banco de Dados Não Relacional)
* **IoT:** Internet of Things (Internet das Coisas)
* **SLA:** Service Level Agreement (Acordo de Nível de Serviço)
* **RPO:** Recovery Point Objective (Objetivo de Ponto de Recuperação)
* **RTO:** Recovery Time Objective (Objetivo de Tempo de Recuperação)
* **IaC:** Infrastructure as Code (Infraestrutura como Código)

#### 1.4. Referências
* AWS Well-Architected Framework (Pillars of Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability).
* Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018).
* Plano de Ensino da Disciplina: Big Data e Cloud Computing (5º Período).

---

### 2. Posicionamento

#### 2.1. Oportunidade de Negócio
O mercado de logística e e-commerce de última milha (last-mile) exige precisão cirúrgica na previsão de entrega. Startups e médias empresas de transporte não possuem capital para investir em pesados datacenters físicos locais capazes de lidar com a volumetria e a oscilação de dados gerada por rastreadores GPS de frotas em movimento. Oferecer uma plataforma escalável em modelo SaaS, que pague apenas pelo uso e forneça dashboards em tempo real para as transportadoras, representa uma oportunidade de capturar um mercado logístico em expansão anual de 18%.

#### 2.2. Descrição do Problema

| **O problema de...** | Lentidão sistêmica, perda ocasional de pacotes de GPS de caminhões em rota e quedas completas do portal administrativo durante o horário comercial (alto volume de acessos). |
| :--- | :--- |
| **Afeta...** | Despachantes logísticos, motoristas parceiros e, em última instância, os clientes finais das transportadoras que não conseguem ver o status real das encomendas. |
| **Cujo impacto é...** | Reclamações de atraso não previsíveis, multas contratuais por descumprimento de SLAs de entrega, perda de confiança da marca e fadiga operacional do time de suporte ao cliente. |
| **Uma solução bem-sucedida incluiria...** | Uma arquitetura desacoplada na AWS que separe o fluxo de alta frequência de escrita (sinais de GPS) do fluxo administrativo transacional, garantindo que o portal de gerenciamento não caia mesmo sob um tsunami de dados de sensores. |

#### 2.3. Posicionamento do Produto
Para transportadoras brasileiras de médio e grande porte, a **SwiftTrack IoT** é uma solução inteligente de rastreamento de carga que provê telemetria em tempo real com latência inferior a 100ms e SLA de disponibilidade de 99,99%. Diferente das plataformas tradicionais on-premises (caras e inflexíveis) ou de arquiteturas legadas que utilizam bancos relacionais para gravar registros de log de IoT e degradam performance sob carga, nossa solução combina o poder escalável de microsserviços serverless na AWS com armazenamento híbrido otimizado por propósito.

---

### 3. Descrição dos Stakeholders e Usuários

| **Stakeholder (Perfil)** | **Necessidade Primária** | **Expectativa na Nuvem (AWS)** |
| :--- | :--- | :--- |
| **Gestores Logísticos (Despachantes)** | Monitorar frotas em tempo real no mapa e disparar alertas automáticos se uma rota for violada. | Painel ágil que carregue o histórico de rotas instantaneamente, sem atrasos visuais ou travamentos. |
| **Equipe Acadêmica/Professores (TI)** | Validar a qualidade técnica do projeto de infraestrutura proposto pelos estudantes. | Solução 100% justificada à luz do AWS Well-Architected Framework, documentada de forma clara no DAS. |
| **Diretores Financeiros (CFO/SaaS)** | Manter o custo operacional da nuvem dentro do orçamento restrito para maximizar a margem operacional. | Configuração com orçamentos previsíveis, alertas de faturamento e uso de recursos otimizados (dimensionamento correto). |
| **Profissionais de Segurança (CISO)** | Garantir que dados de tráfego, rotas sensíveis e segredos comerciais estejam protegidos e em conformidade com as leis nacionais. | Criptografia integral de dados, rastreabilidade de acessos e rede blindada contra ameaças externas. |

---

### 4. Visão Geral do Produto/Solução

#### 4.1. Perspectiva do Produto
A SwiftTrack IoT operará como um ecossistema nativo na nuvem AWS de formato híbrido. A aplicação principal em Django REST Framework servirá os canais web e mobile administrativos (via protocolo HTTPS). Em paralelo, um fluxo de ingestão Serverless autônomo receberá dados de sensores de IoT via chamadas de baixo payload enviadas pelos rastreadores embarcados nos veículos logísticos.

#### 4.2. Funcionalidades Principais
* **Portal de Administração Operacional:** Gestão de clientes, frotas, ordens de serviço e emissão de notas fiscais digitais.
* **Ingestão Contínua de Telemetria:** Processador assíncrono de telemetria GPS (latitude, longitude, velocidade, ignição, temperatura do baú de carga).
* **Painel do Mapa de Rastreamento:** Atualização dinâmica em mapa geográfico do posicionamento dos veículos da frota.
* **Sistema de Alertas:** Notificações em tempo real caso ocorram anormalidades na telemetria (ex: quebra de limite de velocidade ou desvio de temperatura em caminhão de carga fria).

#### 4.3. Suposições e Dependências
* **Suposições:** Dispositivos rastreadores possuem conectividade à rede móvel 4G/5G para enviar dados de GPS; a equipe do projeto tem proficiência prática em configurar a infraestrutura por meio do Console AWS e práticas de IaC.
* **Dependências:** Integrações com APIs externas de Geocodificação Reversa (ex: Google Maps API) para traduzir coordenadas lat/long em nomes de ruas nos relatórios administrativos.

---

### 5. Recursos do Produto (Arquitetura AWS)

Para implementar a visão proposta de forma ideal e cobrindo os módulos do roteiro de ensino, a arquitetura AWS foi desenhada com as seguintes ferramentas fundamentais:

| **Serviço AWS** | **Papel na Arquitetura** | **Justificativa Técnica (Por que usar?)** |
| :--- | :--- | :--- |
| **Amazon VPC** | Isolamento de Rede e Firewalls | Configurar sub-redes públicas (para o Load Balancer e API Gateway) e privadas (para EC2 e RDS). Security Groups atuando como firewall de instâncias (stateful) e NACLs como firewall de sub-redes (stateless) para restringir o tráfego apenas nas portas necessárias (80/443 e 5432). |
| **Amazon EC2** | Servidor de Aplicação Web (Portal) | Instância (ex: t3.medium) para hospedar a API administrativa em Django REST rodando sob Gunicorn e Nginx como proxy reverso, integrada ao Auto Scaling Group. |
| **Amazon RDS (PostgreSQL)** | Banco de Dados Relacional Central | Persistência de dados transacionais complexos (usuários, perfis de frotas, notas fiscais, faturamento) que necessitam de transações ACID. Configurado em Multi-AZ para garantir alta disponibilidade e failover automático em caso de desastre. |
| **Amazon DynamoDB** | Banco NoSQL de Telemetria | Armazenamento de alta velocidade de escrita em escala para o histórico temporal contínuo dos pings de GPS enviados a cada 10s. Fornece escalabilidade horizontal nativa sem perdas de desempenho e custos previsíveis por capacidade de leitura/gravação. |
| **AWS Lambda + API Gateway** | Pipeline Serverless de Ingestão | O API Gateway expõe uma rota REST pública simples para as frotas postarem JSONs de telemetria. O AWS Lambda processa, sanitiza e escreve o dado no DynamoDB de maneira serverless, escalando de zero a milhares de conexões em segundos sem onerar os servidores EC2. |
| **Amazon S3 + CloudFront** | Armazenamento e CDN de Estáticos | S3 para guardar de forma barata fotos dos canhotos de entrega assinados digitalmente pelos clientes. O CloudFront (CDN) cacheará os dados de mapas e ativos estáticos da interface administrativa do front-end, eliminando o tráfego direto de leitura para as instâncias EC2. |
| **AWS CodePipeline + CodeBuild** | Automação e Pipeline CI/CD | Pipeline automatizado que dispara testes unitários no GitHub e atualiza a aplicação de forma automatizada na EC2, mitigando erros manuais de deploy. |
| **Amazon CloudWatch** | Observabilidade e Alertas | Coleta e consolidação de métricas operacionais (CPU da EC2, IOPS do RDS, latência do API Gateway) e geração de logs consolidados para auditoria operacional. |
| **AWS Secrets Manager** | Gerenciamento Seguro de Credenciais | Centralização segura de segredos de produção como chaves de API externas e credenciais de conexão do banco RDS, injetadas dinamicamente na aplicação para evitar senhas expostas no código-fonte. |

---

### 6. Restrições do Projeto

* **Orçamentária:** O orçamento operacional total para hospedagem do protótipo funcional e simulação está fixado em no máximo **US$ 1.500,00 por mês**.
* **Prazo:** O cronograma acadêmico impõe uma restrição de **20 semanas** para conclusão de todas as fases, desde a Incepção, Elaboração, até a Construção e Defesa Oral final na transição.
* **Tecnológica:** A aplicação web principal deve obrigatoriamente utilizar **Django REST Framework** em Python. Todo o deploy produtivo deve ser feito exclusivamente dentro de uma conta sandbox da **AWS** aplicando serviços gerenciados.
* **Segurança e Compliance:** Em atendimento às normas de privacidade nacionais, nenhum dado de localização histórico de motoristas ou dados de identificação pessoal (CPF, dados cadastrais) pode ser trafegado sem criptografia em trânsito e em repouso. O sistema deve atender às exigências básicas da **LGPD**.
* **Pessoal:** O time é composto por um grupo fixo de **4 arquitetos/desenvolvedores** dividindo papéis de desenvolvimento backend e administração de infraestrutura (DevOps).

---

### 7. Atributos de Qualidade (SLAs E SLOs)

* **Disponibilidade:** A plataforma administrativa e o endpoint de ingestão devem manter um SLA global de uptime de **99,95% de disponibilidade** (aproximadamente 4,3 horas de indisponibilidade permitidas por ano). Isso é alcançado usando sub-redes distribuídas em pelo menos 2 Zonas de Disponibilidade (Multi-AZ), instâncias EC2 sob Auto Scaling e RDS Multi-AZ.
* **Performance (Latência):** O endpoint de ingestão Serverless deve responder com latência inferior a **80ms para 95% das escritas** (p95). A leitura de dashboards do portal operacional pelo usuário deve carregar em menos de 150ms usando o caching eficiente do Amazon S3, DynamoDB Query e CloudFront.
* **Segurança (Criptografia):** Todas as comunicações públicas devem ser feitas exclusivamente sob protocolo criptografado **HTTPS/TLS (porta 443)**. Os dados confidenciais armazenados no RDS e no DynamoDB devem ser criptografados em repouso usando o AWS KMS com chaves gerenciadas pela AWS.
* **Continuidade de Negócio (Backup & DR):**
  * **RPO (Recovery Point Objective):** Máximo de **15 minutos** de perda de dados transacionais, alcançado através de rotinas automáticas de backups diários e point-in-time recovery habilitados no Amazon RDS e DynamoDB.
  * **RTO (Recovery Time Objective):** Tempo máximo de recuperação total de indisponibilidade sistêmica catastrófica em menos de **1 hora**, auxiliado pelo uso de infraestrutura configurada sob templates ou scripts de automação.
* **Custo-eficiência:** Reduzir desperdícios aplicando dimensionamento automático (Auto Scaling) nas EC2s, escalando horizontalmente apenas quando o uso agregado de CPU ultrapassar 75% e escalando para baixo (para o mínimo de 1 instância de standby) durante o período da madrugada (23h às 05h).

---

### 8. Aprovação e Histórico de Versões

| **Versão** | **Data** | **Descrição da Alteração** | **Autor(es)** |
| :--- | :--- | :--- | :--- |
| 1.0 | 20/08/2026 | Elaboração inicial do Documento de Visão como exemplo técnico padrão para os projetos do 5º período. | Prof. Arquiteto de Soluções AWS |
