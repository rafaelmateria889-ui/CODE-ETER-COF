# Validação 0.2

Motor oficial Ikemen GO 1.0.0 para Linux, OpenGL/Mesa llvmpipe e Xvfb. Todos os testes de jogo executam o binário nativo; nenhuma imagem foi apresentada como jogo.

## Resultados observados

- Teclado: menus, seleção, luta, caminhada, salto, normais, defesa, agarrão e especiais.
- Mecânicas: estados 1400,1300,1310,3000,3100,1101 de Simon; vítima 3110; servo máximo 1, removido ao final. Super confirmado totalizou 265 de dano; o super defendido não entrou em 3100 e consumiu 1000 de barra. O teste isolado de confirmação causou 265 de dano na execução isolada (vida 1000→735).
- Partida pelo menu: dois KOs, duas vitórias 180, retorno à seleção e nova introdução 190/vida 1000 para ambos, sem fechar processo. É nova partida pela seleção; não botão próprio de revanche imediata.
- Dois controles SDL virtuais: P1 estados 20/200/220, P2 estados 20/200/1100; dano observado nos dois lados. Validam caminho SDL e mapeamentos; não Bluetooth, USB, rumble ou hardware físico.
- Rollback: duas instâncias oficiais por loopback, entrada do sistema nos dois lados, servo, portal, agarrão, super inicial e golpes. Dois KOs, duas vitórias, nenhum evento de dessíncronia; endpoints de vida/barra iguais nos dois pares. Esse teste não comprova RTT/jitter de Internet ou NAT.
- Desconexão em loopback: encerramento do visitante produziu aviso de interrupção e EventCodeDisconnectedFromPeer no anfitrião, sem panic.
- Testes estáticos: todos os sprites SFF são decodificáveis, AIR referencia sprites existentes, teclados disjuntos, estados/guards de super/invocação definidos. Sem avisos de compilação no teste final de mecânicas.

Capturas: gameplay.png (nova partida), servo.png e super.png. Folhas originais em assets/source.

## Reproduzir

    python3 -m pip install 'Pillow>=11,<14'
    python3 -m unittest discover -s tests -v
    python3 -m py_compile tools/*.py tests/*.py

Execução nativa requer ETER_RUNTIME (motor extraído), ETER_TEST_DEPS (Xvfb/xdotool em x11/), xkbcomp, XTest e Pillow. Compile headless_sdl.c com gcc -shared -fPIC -ldl em headless_sdl.so apenas para o ambiente sem hardware.

    python3 tests/native_smoke.py --mechanics
    python3 tests/native_smoke.py --rematch
    python3 tests/network_smoke.py

Para controles virtuais: compile tests/virtual_sdl.c em virtual_sdl.so, configure ETER_SDL_SHIM e ETER_PAD_INPUT (arquivo de máscaras), execute native_smoke.py --controller. Os adaptadores de teste nunca são carregados por JOGAR.bat/jogar.sh.

Workflow .github/workflows/validate.yml: testes estáticos Linux; parser PowerShell, download com hash, instalação, arquivos, execução nativa -h e preservação de configurações no Windows; publica ZIP somente se as verificações Windows passam. Consulte o status do workflow do commit; linha de comando não comprova luta/renderização Windows.

## Aceites pendentes

Partida Windows com GPU real; controle físico; duas pessoas e ergonomia; online em redes diferentes, nova partida online, ping/jitter/perda e desconexão; playtest competitivo/infinitos; polimento comercial de cada transição. A Etapa D e o aceite final seguem abertos. É um protótipo executável em evolução.
