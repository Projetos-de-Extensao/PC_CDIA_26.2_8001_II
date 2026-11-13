---
hide:
  - navigation
  - toc
---

<div class="bdcc-hero">
  <div class="bdcc-hero__content">

    <h1 class="bdcc-title">
      PhotoMatch
    </h1>

    <div class="bdcc-grid">
      <section class="bdcc-card">
        <h2 class="bdcc-card__title">O que é</h2>
        <p class="bdcc-note">
          API e site que encontram, a partir de uma selfie, as fotos de um evento em que a pessoa aparece. Usado ao vivo no SBrT 2026.
        </p>
      </section>

      <section class="bdcc-card">
        <h2 class="bdcc-card__title">Arquitetura (AP2)</h2>
        <div class="bdcc-list">
          <div class="bdcc-list__item">
            <span class="bdcc-pill bdcc-pill--blue">Aplicação</span>
            <span class="bdcc-list__value">Django 5.2, Django REST Framework, Gunicorn</span>
          </div>
          <div class="bdcc-list__item">
            <span class="bdcc-pill bdcc-pill--blue">Dados</span>
            <span class="bdcc-list__value">PostgreSQL 17: relacional, JSONB (GIN) e pgvector</span>
          </div>
          <div class="bdcc-list__item">
            <span class="bdcc-pill bdcc-pill--blue">Infraestrutura</span>
            <span class="bdcc-list__value">EC2 + Docker Compose (web e db), volume persistente, S3</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</div>

## Documentação RUP

| Fase | Documentos |
|---|---|
| [Iniciação](Iniciacao/index.md) | [Documento de Visão](Iniciacao/dv.md), [Requisitos Suplementares](Iniciacao/rs.md) |
| [Elaboração](Elaboracao/index.md) | [Casos de Uso Arquiteturais](Elaboracao/cua.md), [Pacotes e Subsistemas](Elaboracao/maps.md), [Dimensionamento Computacional](Elaboracao/dim_comp.md), [Dimensionamento do Banco](Elaboracao/dimrbd.md), [Sequência e Comunicação](Elaboracao/seq_com.md) |
| [Transição](Transicao/index.md) | [Atividades de Deploy](Transicao/ativ_deploy.md) |

## Visão da arquitetura

```mermaid
flowchart LR
    user[Participante] -- HTTP :8000 --> web
    dev[Operador] -- git push / git pull --> ec2
    subgraph ec2[EC2 Ubuntu - Security Group 22 e 8000]
        web[web: Django + DRF + Gunicorn] -- rede interna --> db[(db: PostgreSQL 17 + pgvector)]
        db --- vol[[volume pgdata]]
    end
    web -.-> s3[(S3: fotos)]
```

O código, o passo a passo de execução e as evidências do deploy estão no [README do repositório](https://github.com/Projetos-de-Extensao/PC_CDIA_26.2_8001_II#readme).
