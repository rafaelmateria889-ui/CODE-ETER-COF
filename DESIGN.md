# Protótipo 0.2 — decisões e escopo

Ikemen GO 1.0.0, motor oficial sem mudanças no núcleo, luta a 60ticks/s. Local 1v1, quatro botões, defesa alta/baixa, agarrão, corridas, salto, leves→fortes→especiais após contato, barra, melhor de três e 99 segundos. O motor aplica juggle, colisão e troca de lado.

## Combate desta versão

Normais começam em 6/9/12/12 frames e têm 6 frames ativos, durações 21/27/33/36 e danos 38/52/78/92. Especiais base ofensivos começam em 9 e têm 9 frames ativos. Variantes fortes têm recuperação maior; dados em docs/frame-data.json. O agarrão normal começa em 6, dano 135; tentáculos 175/195 e falha de 42/48 frames. Agarrões rejeitam ar e stun, incluindo defesa em stun. Teleporte tem preparação e recuperação com curta janela de intangibilidade; forte tenta ultrapassar o rival quando existe espaço.

Servo: invoca no frame 21, ataca uma vez após 32 ticks próprios, expira aos 66, cooldown de 120 ticks e limite de um. Sai ao receber golpe, ao interromper Simon ou ao acabar o round. Não forma obstáculo corporal. O agarrão rejeita stun para não produzir agarrão inevitável durante bloqueio do servo.

Super: custa 1000, primeiro ataque 45; só captura com MoveHit, alvo presente e vivo. Após confirmar, aplica 3×45 e final 85, total 265 antes de modificadores do motor. Bloqueio/erro não iniciam sequência; custo permanece. Vítima tem estado de saída de segurança. Não existe repetição infinita da sequência.

## Arte

Simon com rosto/cabelo das referências e uniforme militar preto; Techblade mecânico com armadura preta e katana laranja.24 novas poses de combate e12 de invocações. Alguns normais ainda compartilham arte; não há centenas de quadros únicos. Cenário continua laboratório provisório.

## Validação e limites

Execução nativa Linux, partida completa, nova partida pelo menu, servo/grab/super, dois controles SDL virtuais e dois pares rollback em loopback. Instalação/CLI Windows no workflow. Isso não comprova uma partida Windows com GPU real, controle físico, ergonomia ou Internet. Não foi feito balanceamento competitivo nem prova de ausência de todo infinito possível. Consulte docs/TESTES.md e docs/ONLINE.md; o aceite final A–D não é declarado completo.
