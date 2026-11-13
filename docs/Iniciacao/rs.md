# Documento de Requisitos Suplementares (v2.0)

## SBrT PhotoMatch

**Fase:** Iniciação, revisada para a AP2
**Data:** 11/11/2026
**Status:** Aprovado para a entrega da AP2

---

## 1. Propósito e escopo

Este documento define os requisitos não funcionais, metas de serviço e condições de operação do PhotoMatch na arquitetura da AP2: API Django em Docker Compose sobre uma instância EC2, com PostgreSQL multimodelo em container.

Inclui: desempenho, disponibilidade, segurança, operação, custo, SLA e riscos. Não inclui alta disponibilidade multi-AZ nem escalonamento automático, que deixam de ser necessários fora da janela de um evento ao vivo (ver seção 12).

## 2. Decisão de arquitetura registrada

| Decisão | Alternativas avaliadas | Motivo |
|---|---|---|
| **EC2 + Docker Compose** no lugar do Elastic Beanstalk | Beanstalk (AP1), ECS/Fargate | O cliente pediu a remoção da dependência do Beanstalk. Compose dá o mesmo ambiente no notebook e na EC2, com controle total e custo de uma única instância. |
| **PostgreSQL 17 + pgvector em container** no lugar de SQLite/RDS | SQLite, RDS PostgreSQL | SQLite não tem JSONB, GIN nem vetores. RDS custaria uma segunda cobrança mensal; para o volume medido (menos de 10 MB por evento) o container com volume e `pg_dump` é suficiente. A comparação está em `dimrbd.md`. |
| **Gunicorn** no lugar do `runserver` | `runserver` | Servidor de produção, com vários workers e timeout configurado. |
| **Modelo multimodelo no mesmo banco** | Banco de documentos ou de vetores separado | Um único Postgres atende relacional (ACID), documento (JSONB) e vetor (pgvector), sem sincronizar sistemas. |

## 3. Contexto e restrições

| Item | Premissa ou restrição |
|---|---|
| Volume por evento | cerca de 1.500 fotos e 3.500 rostos (acervo do SBrT 2025: 1.427 fotos, 3.344 rostos em 1.219 fotos) |
| Eventos simultâneos | 2 eventos publicados na página, cada um com sua pasta de fotos |
| Usuários simultâneos | dezenas, concentrados em horários de pôster ou de avaliação |
| Limiar de busca | τ = 0,60 (distância euclidiana) |
| Stack obrigatória | Django, DRF, PostgreSQL, psycopg, Docker Compose, EC2 |
| Orçamento | até US$ 40 por mês com a instância ligada |
| Equipe | 1 pessoa (projeto individual) |
| Regulamentação | LGPD |

## 4. Desempenho e capacidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-PER-01 | A busca vetorial deve responder rapidamente. | p95 abaixo de 500 ms medido no servidor. Medido em 11/11/2026: p50 2,7 ms e p95 4,2 ms (30 buscas, dados de demonstração). |
| RNF-PER-02 | A busca por selfie deve ser aceitável para uso no celular. | Abaixo de 5 s por requisição, incluindo o cálculo do embedding pelo dlib. |
| RNF-PER-03 | Filtros por metadados devem usar índice. | Filtro `?metadata__<chave>=` gera consulta `@>` atendida pelo índice GIN `photo_metadata_gin`. |
| RNF-CAP-01 | A instância deve comportar web e banco com folga. | Uso de memória abaixo de 70% da RAM no pico (ver `dim_comp.md`). |

## 5. Disponibilidade e confiabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-DIS-01 | A API deve ficar no ar até a avaliação. | `GET /health` retorna 200 pelo IP público em 13/11/2026. |
| RNF-DIS-02 | Containers devem voltar sozinhos após falha ou reinício da instância. | `restart: unless-stopped` em `web` e `db`; serviço do Docker habilitado no boot. |
| RNF-DIS-03 | O `web` só sobe com o banco pronto. | `depends_on` com `condition: service_healthy` e healthcheck `pg_isready`. |
| RNF-CON-01 | Dados não podem ser perdidos em reinício. | Contagem de `gallery_photo` igual antes e depois de `docker compose down` / `up`. |
| RNF-CON-02 | Registro de foto é atômico. | Falha em qualquer regra desfaz foto, etiquetas e rostos (teste `test_bad_embedding_rolls_back_every_table`). |

## 6. Segurança e privacidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-SEG-01 | Nenhum segredo versionado. | `.env` no `.gitignore`; `.env.example` sem senhas reais; `SECRET_KEY` e senhas lidas do ambiente. |
| RNF-SEG-02 | O banco não pode ser exposto. | Serviço `db` sem `ports`; Security Group sem regra para 5432. |
| RNF-SEG-03 | Acesso administrativo restrito. | SSH (22) liberado só para o IP do operador; superusuário criado por variáveis de ambiente. |
| RNF-SEG-04 | Escrita na API só autenticada. | `IsAuthenticatedOrReadOnly`; POST anônimo retorna 403 (teste `test_anonymous_users_cannot_write`). |
| RNF-SEG-05 | Selfies não são retidas (LGPD). | A imagem é lida em memória na requisição e não é gravada em disco, banco ou log. |
| RNF-SEG-06 | O container não roda como root. | Usuário `app` (uid 1000) no Dockerfile. |

## 7. Operação e observabilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-OPS-01 | Saúde verificável. | Healthcheck do container em `/health`; `docker compose ps` mostra `healthy`. |
| RNF-OPS-02 | Logs acessíveis. | `docker compose logs web` mostra migrações, criação do superusuário e Gunicorn. |
| RNF-OPS-03 | Deploy repetível. | Fluxo `git push` → `sh scripts/deploy.sh` (`git pull` + `docker compose up -d --build` + espera do healthcheck); `migrate` e `collectstatic` no entrypoint. |
| RNF-OPS-04 | Backup do banco. | `scripts/backup.sh` diário pelo cron, com retenção de 7 dias e cópia opcional no S3; `scripts/restore.sh` testado em 11/11/2026. |

## 8. Custo

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-CUS-01 | Custo mensal previsível. | Estimativa de US$ 36 por mês (t3.medium on-demand, EBS 20 GB, IPv4 público), detalhada em `dim_comp.md`. |
| RNF-CUS-02 | Sem serviços gerenciados ociosos. | Nenhum RDS, ALB ou NAT Gateway na AP2. |
| RNF-CUS-03 | Alerta de gasto. | AWS Budgets com alerta em 80% e 100% de US$ 40. |

## 9. Manutenibilidade

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RNF-MAN-01 | Código testado. | `python manage.py test gallery search` com 21 testes passando no container. |
| RNF-MAN-02 | Esquema versionado. | Migrações em `gallery/migrations` e `search/migrations`, incluindo o índice GIN e a extensão `vector`. |
| RNF-MAN-03 | Configuração por ambiente. | `POSTGRES_*`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` lidos do ambiente. |

## 10. SLA e responsabilidades

Não há SLA contratual: é um projeto acadêmico. A meta (SLO) é **99% de disponibilidade mensal** durante o período de avaliação, medida pelo `/health`. Uma instância única sem redundância não garante mais que isso; o tempo de recuperação esperado (RTO) é de 30 minutos e a perda máxima (RPO) é de 24 horas, limitada pelo backup diário.

| Responsável | Obrigações |
|---|---|
| AWS | Disponibilidade da instância EC2, do EBS e do S3 |
| Nicholas Borges de Vasconcelos (autor) | Deploy, segredos, backup, monitoramento e resposta a falhas |

## 11. Riscos

| Risco | Probabilidade | Impacto | Tratamento |
|---|---|---|---|
| Falha da instância única | Baixa | Alto (API fora do ar) | `restart: unless-stopped`, backup diário e roteiro de recriação em `ativ_deploy.md` |
| Falta de memória ao compilar o dlib | Média em t3.small | Médio (build falha) | t3.medium ou swap de 2 GB |
| `docker compose down -v` por engano | Baixa | Alto (apaga o volume) | Proibido no roteiro; backup diário |
| Segredo enviado ao Git | Baixa | Alto (−10 pontos e vazamento) | `.gitignore`, revisão do `git status` antes do commit |
| IP público muda ao parar a instância | Média | Médio (links quebram) | Elastic IP ou não parar a instância até a avaliação |
| Crescimento do acervo para dezenas de milhares de rostos | Baixa | Médio (busca exata mais lenta) | Índice HNSW do pgvector (ver `dimrbd.md`) |

## 12. Mudanças em relação à v1.0

- Auto Scaling, ALB e CloudFront saem do escopo: o pico do evento ao vivo passou, e a AP2 pede uma instância EC2 com Compose.
- HTTPS passa a ser opcional (extra de infraestrutura); a API é servida por HTTP no IP público.
- RPO e RTO passam a importar, porque o banco agora recebe escritas pela API.

## 13. Histórico de versões e aprovação

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 04/09/2026 | Requisitos para o evento ao vivo (AP1) | Nicholas Borges de Vasconcelos |
| 2.0 | 11/11/2026 | Revisão para EC2 + Docker + PostgreSQL (AP2) | Nicholas Borges de Vasconcelos |

| Papel | Nome | Decisão | Data |
|---|---|---|---|
| Responsável técnico | Nicholas Borges de Vasconcelos | Aprovado | 11/11/2026 |
| Cliente / avaliador | Prof. Jonh Carvalho | Avaliação na apresentação da AP2 | 13/11/2026 |
