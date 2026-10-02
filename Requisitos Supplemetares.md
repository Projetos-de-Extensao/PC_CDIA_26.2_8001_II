# Documento de Requisitos Suplementares (v1.0)

## SBrT PhotoMatch

**Projeto:** Desafio de Arquitetura de Nuvem — Case 2 (adaptado)
**Data:** 04/09/2026
**Status:** Versão inicial para validação arquitetural

---

## 1. Propósito e Escopo

Este documento define os requisitos não funcionais, os objetivos de nível de serviço (SLOs) e as condições operacionais do **SBrT PhotoMatch**: aplicação web de recuperação de fotos por reconhecimento facial, para demonstração pública durante o SBrT2026.

O escopo inclui: API de busca por similaridade facial, armazenamento do acervo em Amazon S3, frontend de upload, infraestrutura elástica na AWS.

Não fazem parte deste documento: a geração/reprocessamento do acervo de embeddings (já concluído na fase de pesquisa), autenticação de usuários e retenção de dados de longo prazo.

## 2. Contexto e Restrições

| Item | Premissa ou Restrição |
|---|---|
| Acervo | 1.427 imagens, 3.344 rostos já indexados (embeddings prontos) |
| Janela de uso real | 4 dias (29/09–02/10/2026), horário comercial do evento |
| Volume esperado | Dezenas a poucas centenas de buscas, concentradas nos horários de pôster |
| Threshold de matching | τ = 0,60 (distância euclidiana), definido no artigo |
| Orçamento | US$ 20–30 no mês do evento; próximo de zero fora dele |
| Equipe | 1 pessoa |
| Regulamentação | LGPD |

## 3. Definições e Indicadores

- **p95:** valor abaixo do qual estão 95% das medições.
- **τ:** distância euclidiana limite para considerar duas embeddings como a mesma pessoa.
- **RPO/RTO:** não críticos neste projeto — não há dados transacionais de negócio, apenas leitura de um acervo estático já existente.

## 4. Requisitos de Desempenho e Capacidade

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-PER-01 | A busca deve responder em tempo aceitável para uso presencial. | p95 abaixo de 5s por requisição (embedding + varredura). |
| RNF-PER-02 | O sistema deve suportar múltiplos acessos simultâneos no pico do pôster. | Sem erro 5xx sob rajada estimada de dezenas de acessos concorrentes. |
| RNF-CAP-01 | A capacidade deve escalar durante o evento e reduzir depois. | Auto Scaling Group aumenta instâncias entre 29/09–02/10 e reduz ao mínimo após. |

## 5. Requisitos de Disponibilidade e Confiabilidade

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-CON-01 | A aplicação deve estar no ar durante o horário do evento. | Sem indisponibilidade não planejada entre 09h–18h, 29/09–02/10. |
| RNF-CON-02 | Falha de uma instância não deve derrubar o serviço. | O Load Balancer redireciona tráfego para uma instância saudável em caso de falha. |

## 6. Requisitos de Segurança e Privacidade

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-SEG-01 | Toda comunicação deve ser criptografada. | Acesso somente via HTTPS/TLS. |
| RNF-SEG-02 | Selfies enviadas não podem ser retidas. | A imagem da selfie é descartada após a resposta da busca; não é persistida em S3 nem em log. |
| RNF-SEG-03 | O acervo de fotos deve ser servido de forma controlada. | Fotos entregues via URL do S3, sem expor o bucket publicamente por listagem. |
| RNF-SEG-04 | O tratamento de dados deve observar a LGPD. | A coleta da selfie tem finalidade única e definida (busca), sem uso ou retenção posterior. |

## 7. Requisitos de Operação e Observabilidade

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-OPS-01 | O uso e a saúde da aplicação devem ser monitorados durante o evento. | CloudWatch acompanha CPU, latência e erros da API. |
| RNF-OPS-02 | O custo deve ser acompanhado. | AWS Budgets alerta em 80% e 100% do orçamento definido. |

## 8. Requisitos de Manutenibilidade e Entrega

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-MAN-01 | A aplicação deve estar pronta antes do início do evento. | Deploy validado até 28/09/2026. |
| RNF-MAN-02 | A infraestrutura deve poder ser recriada rapidamente. | Configuração de EC2/ASG documentada ou versionada em script. |

## 9. Requisitos de Usabilidade

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-USA-01 | O upload deve funcionar bem em celular (acesso via QR Code). | Interface responsiva, testada em navegador mobile. |
| RNF-USA-02 | O usuário deve entender o resultado da busca. | Mensagem clara quando nenhuma foto corresponder à selfie enviada. |

## 10. Requisitos de Custo

| ID | Requisito | Critério de Aceitação |
|---|---|---|
| RNF-CUS-01 | O custo mensal não deve ultrapassar o orçamento pessoal definido. | Fatura AWS do mês do evento abaixo de US$ 30. |
| RNF-CUS-02 | A infraestrutura deve reduzir custo fora da janela do evento. | Auto Scaling volta ao mínimo (idealmente 0–1 instância) após 02/10/2026. |

## 11. SLA e Responsabilidades

Não há SLA contratual — trata-se de uma demonstração acadêmica. Meta informal: disponibilidade durante o horário do evento (09h–18h, 29/09–02/10/2026).

| Responsável | Obrigações Principais |
|---|---|
| AWS | Disponibilidade dos serviços gerenciados contratados |
| Nicholas | Deploy, configuração, monitoramento, custo e resposta a falhas durante o evento |

## 12. Dependências, Riscos e Decisões Pendentes

| Item | Impacto | Tratamento |
|---|---|---|
| Rajada de acesso concentrada no horário do pôster | Pode gerar lentidão momentânea | Auto Scaling + teste de carga leve antes do evento |
| Selfies de pessoas fora do acervo do SBrT2025 | Sistema pode não retornar nenhuma foto | Mensagem clara de "nenhuma correspondência encontrada" |
| Escolha entre EC2 fixo vs. Lambda para a API | Impacta custo e complexidade | Definir na fase de elaboração, com base em teste de latência do embedding |
| Exposição do bucket S3 do acervo | Risco de acesso indevido às fotos | Definir bucket privado + URLs assinadas antes do go-live |

## 13. Critérios de Aprovação

O documento será considerado aprovado quando:

1. todos os requisitos críticos (desempenho, disponibilidade, privacidade) tiverem critério de aceitação definido;
2. a arquitetura proposta no DAS cobrir Auto Scaling, S3 e monitoramento básico;
3. o custo estimado estiver dentro do orçamento pessoal ou tiver exceção justificada;
4. o tratamento da selfie do usuário estiver alinhado com a LGPD.

## 14. Histórico de Versões

| Versão | Data | Descrição | Autor |
|---|---|---|---|
| 1.0 | 04/09/2026 | Criação do Documento de Requisitos Suplementares | Nicholas Borges de Vasconcelos |
