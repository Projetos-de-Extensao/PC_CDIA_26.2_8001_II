# Iniciação

Objetivo da fase: definir o escopo do PhotoMatch, os stakeholders e as restrições que orientam a arquitetura.

| Artefato | Conteúdo |
|---|---|
| [Documento de Visão](dv.md) | problema, stakeholders, funcionalidades RF-01 a RF-07, recursos da arquitetura e restrições |
| [Requisitos Suplementares](rs.md) | requisitos não funcionais, decisão por EC2 + Docker + PostgreSQL, custo, SLA e riscos |

Principais decisões da fase (v2.0, AP2):

- sair do Elastic Beanstalk para uma instância EC2 com Docker Compose;
- trocar SQLite/RDS por PostgreSQL 17 com pgvector em container, com volume persistente;
- usar o mesmo banco para dados relacionais, documentos JSONB e vetores de rosto.
