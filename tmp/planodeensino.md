## PLANOS DE ENSINO AJUSTADOS

### Ajuste na Disciplina: Big Data e Cloud Computing

**Conteúdo Programático (Revisado):**

| **Módulo** | **Conteúdo** |
| :--- | :--- |
| 1. Introdução à Nuvem AWS | Modelos de serviço; Console AWS; AWS CLI; IAM. |
| 2. Rede e Segurança | VPC, sub-redes, Internet Gateway, NAT Gateway, Security Groups, NACLs. |
| 3. Computação (EC2) | Criação de instâncias; AMIs; Pares de chaves (SSH); User Data; Elastic IP. |
| 4. Armazenamento (S3) | Buckets, objetos, versionamento, políticas de acesso, lifecycle, CloudFront (CDN). |
| 5. Banco de Dados (RDS) | Configuração de instâncias, Multi-AZ, Read Replicas, Snapshots, Parameter Groups. |
| 6. Banco de Dados NoSQL (DynamoDB) | Tabelas, índices, capacidade provisionada vs on-demand, integração com aplicações. |
| **7. Deploy Manual de Aplicações** | Configuração de ambiente EC2 (Gunicorn + Nginx); Variáveis de ambiente; Secrets Manager. **Apenas deploy manual via console.** |
| ~~8. CI/CD e Serverless~~ | ~~(Removido)~~ |

**Cronograma (Semanas 12-15 ajustadas):**

| **Semana** | **Conteúdo** | **Entregável** |
| :--- | :--- | :--- |
| 12 | Secrets Manager e Parameter Store. | Segredos gerenciados. |
| 13 | Otimizações: Elastic IP, Load Balancer (ALB). | API com ALB. |
| 14 | Introdução a serviços de Big Data (EMR, Redshift, Glue, Athena). | Visão geral. |
| 15 | Revisão e ajustes finais do projeto prático. | Projeto finalizado. |
| 16 | **AVALIAÇÃO 2 (P2):** Projeto prático final (API implantada manualmente). | API pública + GitHub. |

---

### Ajuste na Disciplina: Projeto de Cloud

**Conteúdo Programático (Revisado com Novos Módulos):**

| **Módulo** | **Conteúdo** |
| :--- | :--- |
| 1. Arquitetura e Requisitos | AWS Well-Architected Framework; Definição de SLAs, SLOs e métricas. |
| 2. Projeto de Rede e Segurança | VPC avançada; IAM; Security Groups; NACLs; KMS. |
| 3. Dimensionamento de Recursos | EC2, RDS, S3: cálculos e justificativas. |
| **4. Estratégias de Deploy com Containers** | **Introdução ao Docker; Criação de Dockerfile para Django; Registro de imagens no ECR; Orquestração com ECS (Fargate) ou EKS.** |
| **5. CI/CD Automatizado** | **CodePipeline, CodeBuild, CodeDeploy; Pipeline com build da imagem Docker e deploy no ECS/EKS; Rollback automatizado.** |
| **6. Serverless (Complementar)** | **AWS Lambda e API Gateway como alternativa para microsserviços; Comparação com arquitetura baseada em containers.** |
| 7. Continuidade e Recuperação | RPO/RTO; Backup; Disaster Recovery (Pilot Light, Warm Standby). |
| 8. Custo e FinOps | AWS Pricing Calculator; TCO; Savings Plans; Spot Instances. |
| 9. Validação e Simulação | Deploy real em sandbox usando CI/CD e containers; Coleta de métricas; Relatório de validação. |

**Cronograma (Semanas 10-16 ajustadas):**

| **Semana** | **Conteúdo / Atividade** | **Produto Entregável** |
| :--- | :--- | :--- |
| 10 | **Workshop 6:** Introdução a Containers (Docker). Criação de Dockerfile para a API Django. | Dockerfile funcional. |
| 11 | **Workshop 7:** Registro de Imagens (ECR) e Orquestração Básica (ECS Fargate). | Imagem no ECR; Cluster ECS configurado. |
| 12 | **Workshop 8:** CI/CD com CodePipeline, CodeBuild e CodeDeploy (deploy automatizado no ECS). | Pipeline funcional com deploy automático. |
| 13 | **Workshop 9:** Serverless (Lambda + API Gateway) como alternativa para microsserviços. | Função Lambda simples integrada à API Gateway. |
| 14 | **Workshop 10:** Estratégias de Deploy com Containers (Blue-Green, Canary, Rolling) usando ECS. | Plano de deploy com containers. |
| 15 | Consolidação do Plano de Implantação (incluindo containers e CI/CD). | **DAS - Versão Preliminar** com seção de containers/CI/CD. |
| 16 | **Simulação Prática:** Deploy real usando CI/CD e containers em sandbox. | Relatório de simulação (comparando planejado x executado). |

---

## NOVA ESTRUTURA DE DOCUMENTOS RUP/UP PARA PROJETO DE CLOUD (ATUALIZADA)

| **Semana** | **Atividade** | **Documento RUP/UP** | **Descrição** |
| :--- | :--- | :--- | :--- |
| 10 | Dockerfile e ECR | **Modelo de Implantação (Diagrama de Deploy com Containers)** | Diagrama mostrando a arquitetura com containers (ECS) e registro de imagens (ECR). |
| 11 | Orquestração (ECS) | **Modelo de Implantação (Diagrama de Componentes com Containers)** | Componentes: Cluster ECS, Task Definitions, Services, Load Balancer. |
| 12 | CI/CD Pipeline | **Modelo de Design (Diagrama de Atividades - CI/CD)** | Fluxo completo: commit → build (CodeBuild) → deploy (CodeDeploy) → validação. |
| 13 | Serverless (Lambda/API Gateway) | **Modelo de Análise (Alternativas Arquiteturais)** | Comparação entre arquitetura baseada em containers e serverless. |
| 14 | Estratégias de Deploy (Blue-Green, Canary) | **Modelo de Design (Diagramas de Sequência - Deploy)** | Sequência de passos para deploy Blue-Green com ECS. |
| 15 | DAS - Versão Preliminar | **Documento de Arquitetura de Software (DAS) v1** | Inclui seção de containers, CI/CD e serverless. |
| 16 | Simulação Prática | **Relatório de Teste (Validação)** | Resultados do deploy automatizado e comparações. |

---

## EXEMPLO DE ATIVIDADE PRÁTICA - WORKSHOP 8 (CI/CD com Containers)

### Objetivo
Criar um pipeline CI/CD que, a cada commit no repositório GitHub, construa uma imagem Docker da API Django, envie para o ECR e faça deploy automatizado no ECS Fargate.

### Passos (para o aluno documentar no DAS)

1. **Criação do Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. **Registro no ECR:**
   - Criar repositório no ECR.
   - Autenticar via AWS CLI.
   - Build e push da imagem.

3. **Configuração do ECS Fargate:**
   - Task Definition com a imagem do ECR.
   - Service com Load Balancer.
   - Security Groups.

4. **Pipeline no CodePipeline:**
   - **Source:** GitHub (branch main).
   - **Build:** CodeBuild com `buildspec.yml` (build da imagem e push para ECR).
   - **Deploy:** CodeDeploy (ou ação de deploy do ECS) que atualiza o Service no ECS.

5. **Validação:**
   - Testar se a nova versão está rodando.
   - Em caso de falha, fazer rollback automático.

### Artefato Gerado (para o DAS)
- Diagrama de Atividades do Pipeline.
- Justificativa da escolha (ECS Fargate vs EC2 vs EKS).
- Estimativa de custo adicional (CodePipeline, CodeBuild, ECR storage, ECS).

---

## MATRIZ DE RESPONSABILIDADES ATUALIZADA

| **Atividade** | **Big Data e Cloud Computing** | **Projeto de Cloud** |
| :--- | :--- | :--- |
| Criar conta AWS e IAM | ✅ (Mão na massa) | ❌ (Pressupõe que já foi feito) |
| Configurar VPC, sub-redes, Security Groups | ✅ (Mão na massa) | ✅ (Projeta e documenta a arquitetura) |
| Criar instâncias EC2 e RDS | ✅ (Mão na massa) | ✅ (Dimensiona e justifica a escolha) |
| Desenvolver API Django REST Framework | ✅ (Mão na massa) | ❌ (Pressupõe que a API já existe) |
| **Deploy manual via console** | ✅ (Mão na massa) | ❌ |
| **Deploy automatizado via CI/CD** | ❌ | ✅ (Planeja, documenta e simula) |
| **Containerização (Docker, ECS)** | ❌ (Não faz) | ✅ (Planeja, documenta e simula) |
| **Serverless (Lambda, API Gateway)** | ❌ (Não faz) | ✅ (Planeja, documenta e compara) |
| Estimar custos e dimensionar recursos | ❌ (Não faz) | ✅ (Foco principal) |
| Planejar backup e DR | ❌ (Não faz) | ✅ (Foco principal) |
| Estratégias de deploy (Blue-Green, Canary) | ❌ (Não faz) | ✅ (Foco principal) |
| Documento de Arquitetura de Software (DAS) | ❌ (Não faz) | ✅ (Produto final) |
| Defesa oral do projeto | ❌ (Não faz) | ✅ (Apresentação para banca) |

---

## CONCLUSÃO E RECOMENDAÇÃO

Sua proposta é **altamente recomendada** e deve ser implementada pelos seguintes motivos:

1. **Especialização dos focos:** Big Data fica com a base prática e manual; Projeto Cloud assume a automação, containers e modernização.
2. **Atualização do currículo:** Containers e CI/CD são competências essenciais para arquitetos de nuvem hoje.
3. **Melhor aproveitamento da carga horária:** Os 140h do Projeto Cloud agora têm conteúdo mais denso e alinhado com o mercado.
4. **RUP/UP enriquecido:** Os artefatos de design e implantação ganham novas dimensões (pipelines, orquestração, serverless).

### Próximos Passos Sugeridos

1. **Revisar a ementa oficial** do curso para refletir essa mudança.
2. **Atualizar o Manual de Projetos de Extensão** (se houver) para incluir a entrega de um Dockerfile e pipeline como parte do projeto.
3. **Capacitar os professores** de Projeto Cloud em Docker e ECS (se necessário).
4. **Disponibilizar laboratórios AWS** com orçamento suficiente para os alunos testarem CI/CD (custos são baixos, mas precisam ser previstos).

Se precisar de mais detalhes sobre como adaptar os workshops, os artefatos RUP ou as avaliações para incluir containers e CI/CD, estou à disposição!