# CODE-ETER-COF

Protótipo de um jogo de luta 2D autoral, **1 contra 1 em rounds**, com dois personagens: Simon, um lutador de portais e invocações, e Techblade, um samurai ciborgue de pressão rápida. `CODE-ETER-COF` é o nome do repositório; o título definitivo do jogo ainda pode ser decidido.

## Estado

**Pré-produção.** Este repositório começa com a [especificação de implementação](docs/ESPECIFICACAO.md). Ainda não contém uma versão jogável. O título é provisório.

## Escopo inicial

- Dois personagens selecionáveis, partida local e **online 1 contra 1 com rollback**.
- Combate lateral com rounds, defesa, agarrões, especiais, barra e supers.
- Primeiro alvo: Windows desktop, sujeito à validação do projeto.
- Motor inicial proposto: Ikemen GO; uma mudança de motor exige registrar o bloqueio técnico e a decisão.
- Online: priorizar resposta rápida e conexão estável; o ping em ms depende das redes dos jogadores e deve ser medido, não prometido.

## Próximo marco

Implementar a **Etapa A** do documento de especificação: seleção, arena, controles de dois jogadores, regras de round, golpes básicos e uma especial por personagem. O marco só está concluído quando duas pessoas conseguem terminar uma partida e iniciar uma revanche.

Depois do núcleo local, a **Etapa D é obrigatória**: conexão online real entre redes distintas, rollback, partida completa, revanche e documentação de latência/portas. O repositório ainda está em pré-produção e não contém esse recurso implementado.

## Recursos e direitos

Personagens e golpes são conceitos autorais. As imagens compartilhadas pelo criador são referências visuais; não são sprites de jogo. Não incluir recursos de *The King of Fighters* nem de outros jogos sem autorização. Registrar licença e origem de toda dependência e recurso externo antes de distribuí-los.
