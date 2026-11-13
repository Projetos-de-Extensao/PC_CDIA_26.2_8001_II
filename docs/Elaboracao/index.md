# Elaboração

Objetivo da fase: estabilizar a arquitetura antes da construção, reduzindo os riscos técnicos principais. Na AP2 eram três: modelar dados relacionais, documentos e vetores no mesmo banco; garantir consistência transacional; e rodar tudo em uma instância EC2 sem perder dados.

## Resumo

| Risco | Como foi tratado | Resultado |
|---|---|---|
| Três modelos de dados em um banco | PostgreSQL 17 com JSONB, índice GIN e pgvector | 21 testes passando contra o Postgres real |
| Consistência ao registrar fotos | `transaction.atomic()` em `ingest_photo` | rollback comprovado em quatro cenários |
| Instância única com banco em container | volume `pgdata`, healthcheck, backup com `pg_dump` | dados mantidos após `down`/`up`; restauração em 281 ms |
| Memória para o dlib | medição de memória e comparação de instâncias | t3.medium (4 GB) |

## Artefatos

| Documento | Conteúdo |
|---|---|
| [Casos de Uso Arquiteturais](cua.md) | UC-01 a UC-07, diagrama e matriz requisito → caso de uso → componente → teste |
| [Pacotes e Subsistemas](maps.md) | camadas, apps Django, dados, infraestrutura, segurança e dependências |
| [Dimensionamento Computacional](dim_comp.md) | medições, escolha da t3.medium, custo mensal e classes de análise (PlantUML) |
| [Dimensionamento do Banco](dimrbd.md) | volumetria por evento, crescimento, disco, backup e comparação com RDS |
| [Sequência e Comunicação](seq_com.md) | registro transacional, consulta JSONB, busca vetorial e deploy |

## Decisões que seguem para a Transição

- Deploy em EC2 Ubuntu 24.04 t3.medium, com Security Group liberando 22 e 8000.
- `docker compose up -d --build` como único comando de implantação.
- Backup diário com `pg_dump` enviado ao S3.
