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