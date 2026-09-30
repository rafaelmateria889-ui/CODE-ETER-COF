# Validação do protótipo 0.1

Testes executados no binário oficial **Ikemen GO 1.0.0 para Linux**, com OpenGL/Mesa llvmpipe e Xvfb. Não foi usado um mockup de navegador.

## Evidências observadas

- Menu → seleção de Simon/Techblade → confirmação da arena → partida.
- P1: caminhada, salto/pouso, ataque forte, rasteira, especial, teleporte.
- P2: entrada pelo segundo conjunto de teclas, especial de Techblade e recuperação após derrubada.
- Defesa de normal: estados 150/151 de Techblade com **vida mantida em 1000**.
- Agarrão: Simon entrou em 800 → 810; vítima entrou em 820.
- Super por duplo quarto de lua + dois socos: estado 3000; barra passou de **3000 para 2000**.
- Partida por entradas de teclado automatizadas, sem zerar a vida por comando de debug: Techblade chegou a **0 de vida em dois rounds**; Simon entrou em vitória 180 duas vezes; partida encerrou.
- O teste de combate usa reset de round e barra cheia para isolar defesa, agarrão e super. A sequência final de dois rounds é vencida por ataques normais do motor, com a especial repetida por entradas.
- Três verificações automatizadas passaram: integridade/decodificação dos SFF e referências AIR; layouts de teclado disjuntos; estados de ambos os personagens e proteção de custo do super.
- Compilação/carregamento dos dois personagens sem erros no log final.

O log de telemetria do teste final registrou KO nos frames 2274 e 3544; vitória de Simon nos frames 2319 e 3589. Esses números pertencem à execução de validação, não são métricas de latência.

## Como reproduzir

Os testes estáticos precisam de Python e Pillow:

    python3 -m unittest discover -s tests -v

O teste nativo é uma ferramenta de desenvolvimento para Linux. Requer o motor extraído, Xvfb, xkbcomp, xdotool, XTest e Pillow com X11. Configure ETER_RUNTIME e ETER_TEST_DEPS conforme o cabeçalho de tests/native_smoke.py; compile tests/headless_sdl.c em headless_sdl.so apenas no ambiente de teste.

    python3 tests/native_smoke.py
    python3 tests/native_smoke.py --menu
    python3 tests/native_smoke.py --combat

O adaptador SDL do teste desliga a enumeração de joystick/haptic/sensores indisponíveis no ambiente virtual. Ele **não é incluído nem carregado pelo iniciador do jogo**, e não valida controles físicos.

## Ainda não verificado

- Execução do instalador/executável em Windows real.
- Controle físico Xbox, DualShock/DualSense ou genérico.
- Duas pessoas reais completando partidas, remapeamento em hardware e ergonomia.
- Rematch completo após a tela de resultado.
- Online entre computadores/redes distintas, RTT/jitter e comportamento real de rollback.
- Balanceamento, proteção contra todos os infinitos e fidelidade final dos quadros de animação.

O resultado é um protótipo de combate local em evolução. A Etapa D da especificação e o aceite final do jogo permanecem abertos.

