# Diagramas de Sequência e Comunicação (v1.0)

## SBrT PhotoMatch

**Fase:** Elaboração
**Data:** 11/11/2026

---

## 1. Fluxos críticos

| Fluxo | Por que é crítico | Caso de uso |
|---|---|---|
| Registro transacional de foto | grava em quatro tabelas e precisa de rollback | UC-02 |
| Consulta por metadados JSONB | depende do índice GIN | UC-03 |
| Busca por similaridade | une o motor de rosto e o pgvector | UC-01 |
| Deploy na EC2 | envolve Git, Docker, segredos e migrações | UC-06 |

## 2. Registro transacional de foto (UC-02)

```mermaid
sequenceDiagram
    autonumber
    actor F as Fotógrafo
    participant V as PhotoViewSet.ingest
    participant S as PhotoIngestSerializer
    participant I as ingest_photo
    participant DB as PostgreSQL

    F->>V: POST /api/photos/ingest/ (JSON, autenticado)
    V->>S: is_valid()
    S->>DB: SELECT evento, sessão, fotógrafo e checa se o arquivo já existe
    alt dados inválidos
        S-->>F: 400 com erros por campo
    end
    V->>I: ingest_photo(**dados)
    I->>DB: BEGIN
    I->>DB: INSERT gallery_photo
    I->>DB: SELECT/INSERT gallery_tag (get_or_create)
    I->>DB: INSERT gallery_photo_tags
    I->>I: regras: sessão do evento, data, 1 a 50 rostos, 128 valores
    alt regra violada
        I->>DB: ROLLBACK
        I-->>V: BusinessRuleError
        V-->>F: 400 {"detail": mensagem}
    else regras ok
        I->>DB: SAVEPOINT
        I->>DB: INSERT gallery_face (lote)
        alt face_index repetido (IntegrityError)
            I->>DB: ROLLBACK
            V-->>F: 400 {"detail": "face_index repetido na mesma foto."}
        else
            I->>DB: COMMIT
            V->>DB: SELECT foto com tags e rostos
            V-->>F: 201 com a foto aninhada
        end
    end
```

## 3. Consulta por metadados JSONB (UC-03)

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant V as PhotoViewSet.list
    participant M as metadata_filter
    participant DB as PostgreSQL

    C->>V: GET /api/photos/?metadata__camera__make=Canon&metadata__iso=800
    V->>M: parâmetros da URL
    M->>M: camera__make=Canon vira {"camera": {"make": "Canon"}}
    M->>M: iso=800 vira {"iso": "800"} OU {"iso": 800}
    M-->>V: Q(metadata @> ...) & Q(...)
    V->>DB: SELECT ... WHERE metadata @> '{"camera":{"make":"Canon"}}' AND (...)
    Note over DB: índice GIN photo_metadata_gin atende o operador @>
    DB-->>V: fotos
    V-->>C: 200, página com 20 fotos
```

## 4. Busca por similaridade (UC-01)

```mermaid
sequenceDiagram
    autonumber
    actor P as Participante
    participant A as similarity_search
    participant FE as face_engine (dlib)
    participant SV as find_similar_photos
    participant DB as PostgreSQL + pgvector

    P->>A: POST /api/search/ (image ou embedding)
    opt enviou imagem
        A->>FE: load_image_rgb + get_query_embedding
        FE-->>A: vetor de 128 valores (ou nenhum rosto: 400)
    end
    A->>SV: vetor, limiar 0,60, evento opcional
    SV->>DB: SELECT ... embedding <-> vetor AS distance WHERE distance <= 0.60 ORDER BY distance
    DB-->>SV: rostos mais próximos
    SV->>SV: agrupa por foto, guarda a menor distância
    SV-->>A: lista de fotos
    A-->>P: 200 {"count", "results"}
    Note over A: a imagem fica só na memória da requisição
```

## 5. Deploy na EC2 (UC-06)

```mermaid
sequenceDiagram
    autonumber
    actor O as Operador
    participant W as Notebook Windows
    participant GH as GitHub
    participant E as EC2
    participant DC as Docker Compose
    participant DB as container db
    participant WEB as container web

    O->>W: git commit
    W->>GH: git push
    O->>E: ssh ubuntu@IP
    E->>GH: git pull
    O->>DC: docker compose up -d --build
    DC->>DC: build da imagem web (camadas em cache)
    DC->>DB: inicia (volume pgdata)
    DB-->>DC: healthcheck pg_isready ok
    DC->>WEB: inicia (depende de db saudável)
    WEB->>DB: migrate
    WEB->>WEB: collectstatic
    WEB->>DB: createsuperuser (se não existe), seed_demo (se não existe)
    WEB->>WEB: exec gunicorn :8000
    DC-->>O: containers healthy
    O->>E: curl http://IP:8000/health
```

## 6. Diagrama de comunicação

Mensagens numeradas entre os objetos no registro de foto e na busca.

```mermaid
flowchart LR
    F([Fotógrafo]) -- "1: POST ingest" --> V[PhotoViewSet]
    V -- "2: is_valid" --> S[PhotoIngestSerializer]
    V -- "3: ingest_photo" --> I[IngestService]
    I -- "4: INSERT photo, tags, faces" --> DB[(PostgreSQL)]
    P([Participante]) -- "5: POST search" --> A[similarity_search]
    A -- "6: get_query_embedding" --> FE[face_engine]
    A -- "7: find_similar_photos" --> SV[SimilarityService]
    SV -- "8: SELECT ... <-> ..." --> DB
```

## 7. Matriz de rastreabilidade

| Requisito | Caso de uso | Fluxo / diagrama | Componente | Teste / evidência |
|---|---|---|---|---|
| RF-03, RNF-CON-02 | UC-02 | seção 2 | `ingest_photo` | `test_ingest_writes_photo_tags_and_faces`, `test_bad_embedding_rolls_back_every_table`, `test_duplicate_face_index_rolls_back` |
| RF-04, RNF-PER-03 | UC-03 | seção 3 | `metadata_filter`, índice GIN | `test_filter_by_nested_json_key`, `test_filter_matches_typed_json_value`, `test_metadata_has_gin_index` |
| RF-01, RNF-PER-01 | UC-01 | seção 4 | `find_similar_photos`, pgvector | `test_vector_search_returns_closest_photo_first`; p95 de 4,2 ms medido |
| RNF-OPS-03, RNF-DIS-03 | UC-06 | seção 5 | `docker-compose.yml`, `entrypoint.sh` | logs do `web` e `docker ps` no README |
| RNF-CON-01 | UC-06 | seção 5 | volume `pgdata` | contagem antes e depois de `down`/`up` |

## 8. Histórico de versões

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 11/11/2026 | Fluxos críticos da AP2 | Nicholas Borges de Vasconcelos |
