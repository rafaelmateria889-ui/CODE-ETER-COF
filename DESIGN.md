# Protótipo 0.1 — decisões e escopo

Mantido Ikemen GO 1.0.0; jogo nativo com simulação de luta a 60 passos/s. Não houve migração de motor.

## Núcleo

A=x, B=a, C=y, D=b na nomenclatura interna do Ikemen. Os layouts de teclado têm teclas distintas. Motions aceitam até 24 frames e buffer de botão de 4 frames; o super aceita 32. Direcionais mantidos usam buffer de 1 frame. O motor resolve troca de lado, colisões e estados comuns.

Os golpes têm hitboxes por trecho da animação. Normais iniciam em 6 frames e têm 6 frames ativos, com duração total inicial entre 21 e 36. Especiais ofensivos começam em 9 frames, têm 9 frames ativos e recuperação mais longa. Cada HitDef é criado uma única vez por ação. Quedas e limite de juggle usam regras do motor. Não foi feito balanceamento competitivo.

A cadeia leve → forte → especial só fica disponível após contato. Não há cancelamento de forte de volta para leve. Teleporte tem preparação e recuperação, com intangibilidade somente em uma janela curta. Agarrões verificam distância e rejeitam adversários no ar ou em stun.

## Diferenças da especificação de produção

Esta é a primeira entrega jogável, não a conclusão de A–D. As variantes leve/forte dos especiais ainda compartilham uma versão; Simon tem um antiaéreo provisório para testar o espaço aéreo. Servo/minion, tentáculos articulados e armas invocadas continuam pendentes.

Os supers iniciais são ataques únicos com pausa, custo de barra e derrubada; não são ainda sequências cinematográficas confirmadas. Alguns ataques compartilham poses, e o agachamento/ataque aéreo precisa de mais quadros exclusivos. A aparência mira jogos clássicos 2D com identidade própria.

Arte de Simon atualizada com cabelo castanho ondulado e uniforme preto a partir das referências do usuário. Techblade mantém capuz, visor laranja, armadura preta, membros mecânicos e katana incandescente. O cenário permanece um laboratório simples.

Rollback e menus de conexão vêm do motor fixado; a validação em redes distintas segue pendente. O controlador de teste sem hardware não faz parte da instalação do jogador.

