# Dimensionamento do Banco de Dados (v1.0)

## SBrT PhotoMatch

**Fase:** Elaboração
**Data:** 11/11/2026

---

## 1. Objetivo

Estimar o volume e o crescimento do PostgreSQL do PhotoMatch, definir o armazenamento e a política de backup, e comparar o banco em container com volume Docker na EC2 com o Amazon RDS.

## 2. Medições de base

Medido no container `db` com os dados de demonstração (1 evento, 24 fotos, 48 rostos), em 11/11/2026:

| Medida | Valor | Fonte |
|---|---|---|
| Tamanho de uma linha de `gallery_face` | 656 bytes (520 do vetor de 128 dimensões) | `pg_column_size` |
| Tamanho de uma linha de `gallery_photo` (com `metadata`) | 280 bytes | `pg_column_size` |
| Ocupação em disco por rosto (heap, com sobrecarga de página) | 682 bytes | `pg_relation_size / n_live_tup` |
| Ocupação em disco por foto | 341 bytes | `pg_relation_size / n_live_tup` |
| Banco completo (tabelas do Django incluídas) | 9,2 MB | `pg_database_size` |
| Índice GIN `photo_metadata_gin` | 24 KB para 24 fotos | `pg_relation_size` |
| Backup `pg_dump -Fc` | 84 KB, gerado em 110 ms | teste de backup |
| Restauração em banco novo | 281 ms; 24 fotos, 48 rostos e índice GIN conferidos | teste de restauração |

O vetor domina o tamanho do rosto: 128 valores × 4 bytes + 8 bytes de cabeçalho = 520 bytes.

## 3. Volumetria por evento

Referência: acervo do SBrT 2025, com 1.427 fotos e 3.344 rostos. Arredondado para 1.500 fotos, 3.500 rostos e 2 etiquetas por foto.

| Tabela | Linhas | Bytes por linha | Heap | Índices (estimado) | Total |
|---|---|---|---|---|---|
| `gallery_face` | 3.500 | 682 | 2,39 MB | 0,45 MB (pk, único, FK) | 2,84 MB |
| `gallery_photo` | 1.500 | 341 | 0,51 MB | 0,75 MB (pk, único, 3 FKs, GIN) | 1,26 MB |
| `gallery_photo_tags` | 3.000 | 40 | 0,12 MB | 0,20 MB | 0,32 MB |
| `gallery_event`, `gallery_session`, `gallery_photographer`, `gallery_tag` | dezenas | — | < 0,1 MB | < 0,1 MB | 0,10 MB |
| **Total por evento** | | | | | **≈ 4,5 MB** |

### Memória de cálculo

- Rostos: 3.500 × 682 B = 2.387.000 B ≈ 2,39 MB.
- Fotos: 1.500 × 341 B = 511.500 B ≈ 0,51 MB.
- Índices B-tree de rostos: 3 índices × 3.500 entradas × ≈ 40 B ≈ 0,42 MB.
- Índices de fotos: 6 índices, estimados em 1,5 × o heap, porque o GIN indexa cada chave e valor do JSON.
- Total: 2,84 + 1,26 + 0,32 + 0,10 ≈ 4,5 MB por evento.

## 4. Crescimento

| Horizonte | Eventos acumulados | Dados | Banco com tabelas base (9,2 MB) |
|---|---|---|---|
| Ano 1 | 12 | 54 MB | 63 MB |
| Ano 3 | 36 | 162 MB | 171 MB |
| Ano 5 | 60 | 270 MB | 279 MB |

Premissa: um evento por mês do tamanho do SBrT. Mesmo em cinco anos o banco cabe com folga na RAM da t3.medium, então quase todas as leituras vêm do cache.

## 5. Armazenamento

| Uso do disco EBS (gp3, 20 GB) | Tamanho |
|---|---|
| Ubuntu 24.04 e pacotes | 3 GB |
| Imagens Docker (`web` 1,41 GB, `db` 627 MB) | 2 GB |
| Cache de build do Docker (dlib, wheels) | até 3 GB |
| Volume `pgdata` em 5 anos | 0,3 GB |
| WAL do PostgreSQL (`max_wal_size` padrão) | até 1 GB |
| Backups locais temporários | < 0,1 GB |
| **Total** | **≈ 9,4 GB de 20 GB** |

20 GB deixa margem para novas versões da imagem; `docker image prune` libera imagens antigas.

### Busca vetorial e índice

Hoje a busca compara a selfie com todos os rostos (varredura exata). Com 3.500 rostos ela leva poucos milissegundos (p95 de 4,2 ms medido com o conjunto de demonstração). Se o acervo passar de 100 mil rostos, a opção é um índice aproximado HNSW do pgvector:

```python
HnswIndex(name="face_embedding_hnsw", fields=["embedding"], m=16, ef_construction=64, opclasses=["vector_l2_ops"])
```

## 6. Backup e restauração

| Item | Política |
|---|---|
| Ferramenta | `pg_dump -Fc` (formato custom, comprimido) |
| Frequência | diária, pelo cron da EC2 |
| Retenção | 7 diários + 4 semanais |
| Destino | `s3://<bucket-do-projeto>/backups/` (fora da instância) |
| Tamanho por evento | ≈ 5 MB (84 KB para 24 fotos ≈ 3,5 KB por foto com rostos) |
| RPO | 24 h |
| RTO | 30 min (nova instância, `docker compose up`, `pg_restore`) |

```bash
# backup (pg_dump -Fc, retenção local de 7 dias, cópia opcional para o S3)
BACKUP_S3_URI=s3://<bucket-do-projeto>/backups/ sh scripts/backup.sh

# restauração (pg_restore --clean --if-exists)
sh scripts/restore.sh /home/ubuntu/backups/photomatch_AAAA-MM-DD_HHMM.dump
```

Os dois scripts foram testados em 11/11/2026 contra o ambiente Docker: backup de 84 KB e restauração com as 24 fotos de volta e a API respondendo.

## 7. Volume Docker na EC2 × Amazon RDS

| Critério | Volume Docker na EC2 (escolhido) | Amazon RDS PostgreSQL |
|---|---|---|
| Custo adicional | US$ 0 (usa o EBS da instância) | db.t4g.micro single-AZ ≈ US$ 11,68 + 20 GB ≈ US$ 2,30 = ≈ US$ 14/mês; Multi-AZ dobra |
| pgvector | imagem `pgvector/pgvector:pg17` | suportado como extensão |
| Backup | manual (`pg_dump` + cron + S3) | automático, com restauração para um ponto no tempo |
| Alta disponibilidade | nenhuma: instância única | Multi-AZ opcional |
| Atualizações e patches | o operador atualiza a imagem | gerenciados pela AWS |
| Mesmo ambiente local e na nuvem | sim, o mesmo Compose | não, o local continua em container |
| Rede | Postgres só na rede interna do Compose | security group próprio; precisa da mesma VPC |
| Requisito da AP2 | atende (container `db` com volume) | não atende o B2 |

**Decisão:** volume Docker na EC2. O banco é pequeno (menos de 300 MB em cinco anos), o enunciado pede o Postgres em container e a perda máxima de um dia é aceitável para um acervo que pode ser reimportado dos arquivos `.pkl`. Para uso contínuo em produção com escritas frequentes, o caminho é migrar para RDS com Multi-AZ: basta apontar `POSTGRES_HOST` para o endpoint, sem mudar o código.

## 8. Histórico de versões

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 11/11/2026 | Volumetria medida, crescimento, backup testado e comparação com RDS | Nicholas Borges de Vasconcelos |
