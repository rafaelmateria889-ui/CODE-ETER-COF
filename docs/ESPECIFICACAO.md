# Jogo de luta 2D — Simon vs. Techblade

**Especificação de produção para GPT‑6 Astra**  
**Versão:** 1.0 · **Data:** 28/09/2026  
**Título do projeto:** provisório; o usuário ainda não escolheu o nome comercial.

## 1. Missão para o agente implementador

Crie um **protótipo realmente jogável** de um jogo de luta **2D lateral, 1 contra 1**, inspirado no ritmo e na leitura competitiva de *The King of Fighters*. Há exatamente dois personagens selecionáveis neste marco: **Simon** e **Techblade**. O jogador pode escolher qualquer um; os dois podem ser controlados por pessoas no mesmo computador. Inclua combate contra CPU simples se couber sem atrasar o núcleo local.

Este é um jogo autoral. Crie código, regras, sons temporários, interface e arte temporária originais. Não importe sprites, áudio, cenários, logotipos, nomes de golpes ou personagens de KOF ou de outros jogos. As imagens do usuário são **referências de identidade**, não sprites prontos nem autorização para copiar ativos de terceiros. Entregue arquivos editáveis, instruções de execução e um build jogável quando o ambiente permitir. Não apresente imagens estáticas ou um vídeo como se fossem um jogo.

### Decisões fechadas pelo usuário

- Formato **1 contra 1 em rounds**, sem sistema de equipes/tag.
- Não é *beat ’em up*: **não usar OpenBOR**, fases com rolagem lateral ou hordas de inimigos.
- Simon: portais interdimensionais, transporte e invocação de mãos, tentáculos, pequenos servos/esqueletos e, futuramente, armas; arquétipo **rushdown/grappler**.
- Techblade: samurai ciborgue de investida agressiva; arquétipo **rushdown puro**.

### Hipóteses de trabalho editáveis

- Primeira plataforma: **Windows desktop**, partida local no mesmo teclado ou com controles conectados. Não houve decisão sobre web, celular ou console.
- O jogo final exige **partida online 1 contra 1 com rollback**. A primeira etapa local continua como base de teste; a entrega final não está concluída sem uma partida online real entre dois computadores.
- Visual final ainda indefinido: protótipo pode usar formas, silhuetas ou sprites temporários originais, desde que os personagens sejam distinguíveis e a leitura das hitboxes seja clara.
- O nome do jogo, cenário narrativo, classificação etária e duração final do projeto continuam em aberto. Não os fixe como canon.

## 2. Stack e abordagem

**Escolha inicial:** Ikemen GO, pois foi feito para jogos de luta 2D, suporta recursos compatíveis com M.U.G.E.N, programação de personagens em seus formatos próprios, personalização de interface/modos e jogo 1 contra 1. Documentação e código: <https://github.com/ikemen-engine/Ikemen-GO> e <https://ikemen-engine.github.io/>.

Primeiro verifique a versão atual, sua documentação, licença, exemplos de personagem e processo de build. **Não altere o núcleo do motor se o conteúdo puder ser implementado como personagens, cenário e configuração.** Guarde scripts e dados editáveis de cada personagem em pastas claras. Use somente recursos que funcionem na versão escolhida; registre a versão e a origem das dependências.

Se houver bloqueio técnico concreto para produzir o protótipo em Ikemen GO, documente o bloqueio e use **Godot 4 .NET + C#** como alternativa, com simulação de combate a 60 ticks/s, estado explícito dos personagens e colisões controladas pelo código. O projeto [Sakuga Engine](https://github.com/NoisyChain/Sakuga-Engine) e o [Godot Rollback Fighter Demo](https://github.com/blast-harbour/Godot-Rollback-Fighter-Demo) são referências de estudo, não dependências obrigatórias. Não misture dois motores no produto final. Não use a física dinâmica padrão da Godot como autoridade de golpes se houver intenção de rollback futuro, porque sua física não garante determinismo entre execuções.

**Prioridade:** combate local funcional > online com rollback medido > leitura visual > polimento > CPU. O motor já oferece netplay com rollback; valide a versão escolhida e configure o modo de jogo para duas pessoas. Não construa contas, loja, matchmaking ou servidor dedicado antes de validar o fluxo básico de conexão.

### Objetivo de latência online

"O menor ms possível" é uma meta de experiência, não um número garantido: RTT depende da distância, rotas, provedor e rede dos jogadores. Priorize baixo atraso **de entrada**, estabilidade e ausência de dessíncronia. No Ikemen GO, confirme as opções reais da versão fixada para rollback, atraso local em frames e portas; não assuma que zerar o atraso é sempre melhor. Comece com padrão estável e ajuste por testes. Mostre ou registre RTT/ping, jitter quando disponível, atraso configurado, rollbacks e desconexões. Diferencie RTT em milissegundos de atraso de comando em frames.

O README deve explicar como hospedar e entrar em uma partida, incluindo exigências de rede/porta encontradas na versão escolhida. Se a conexão direta falhar por NAT ou firewall, documente o caso e uma solução de conexão válida; não afirme que matchmaking ou atravessamento automático de NAT existem sem implementar/testar.

## 3. Referências visuais e identidade

O usuário enviou duas imagens nesta conversa. Elas devem ser anexadas novamente ao agente implementador se ele não tiver acesso aos arquivos. Associação:

1. **Simon:** `GPT_Image_2_-_natural_taken_photo___iphone_grain_film__different_posing__diferen(2).png`. Homem jovem com rosto visível, cabelo escuro médio, roupa tática preta. Efeitos de portais em vermelho escuro, com contorno irregular/espinhos; as criaturas invocadas devem ter leitura separada do corpo dele.
2. **Techblade:** `u9298842377_A_cybernetic_ninja_leaps_through_a_dark_smoke-fil_9f18daa8-e148-4dcd-a9fc-293ff0ffa65b_3.png`. Capuz e armadura preta, visor laranja, **braços e mãos totalmente mecânicos, sem pele humana**, katana laranja incandescente. Preservar esses traços em idle, movimento, ataques e retratos.

Traduza as fotos/conceitos para sprites ou silhuetas próprios do jogo. Não suponha que uma única foto contenha os quadros de animação necessários. Se faltarem recursos finais, implemente placeholders honestos e substituíveis; não marque o jogo como visualmente finalizado.

### Linguagem visual durante a luta

- Personagens sempre distinguíveis diante do cenário, inclusive sem efeitos.
- Portal de Simon: vermelho; breve indicação do ponto de saída antes de um golpe invocado; corpo permanece rastreável no teleporte.
- Lâmina de Techblade: laranja; rastro curto que mostra direção e alcance, sem cobrir o oponente.
- Hurtboxes e hitboxes não precisam aparecer ao jogador, mas devem ter opção de depuração.
- Câmera lateral, arena plana, limites claros, personagens sempre visíveis. Sem movimentação em profundidade.

## 4. Loop de jogo do primeiro marco

Menu inicial → partida local **ou online** → conexão entre dois jogadores quando online → seleção entre Simon/Techblade para P1 e P2 → uma arena → contagem inicial → round → KO ou tempo esgotado → próximo round → vencedor da partida → revanche ou voltar à seleção.

- Melhor de **3 rounds** (primeiro a vencer 2); 99 segundos por round como valor inicial configurável.
- Vida inicial igual para ambos; barra de especial inicial vazia, com máximo de 3 unidades. Ajustar números com playtest.
- Em timeout, vence quem tiver maior **percentual** de vida; empate leva a um round decisivo ou regra de empate explícita, sem travar a partida.
- Rounds resetam posições, vida e invocações ativas; a política de barra entre rounds deve estar configurada e visível. Para o primeiro marco, **preservar barra** entre rounds.
- Pause, reinício de partida e volta ao menu precisam funcionar.

## 5. Controles e regras comuns

Layout de **quatro botões de ataque** inspirado em jogos clássicos: `A` = soco leve, `B` = chute leve, `C` = soco forte, `D` = chute forte. Diante do oponente, `→` avança e `←` recua/defende; `↓` agacha; `↑` salta. Direções são **relativas ao lado para o qual o lutador está olhando**; comandos devem inverter corretamente após troca de lado.

- P1 e P2 têm mapeamentos editáveis e que não conflitam. Suportar ao menos dois dispositivos de entrada ou dois conjuntos de teclas; exibir controles no menu.
- Defesa alta e baixa; golpes baixos exigem defesa baixa, saltos podem abrir defesa baixa; agarrões não são bloqueados normalmente.
- Caminhada, agachamento, salto, avanço rápido, recuo rápido, giro ao trocar de lado, hitstun, blockstun, queda/levantada e agarrão normal.
- Buffer curto de entradas para diagonais e sequências; não exigir digitação perfeita de um único frame. Consumo de botão e prioridade de comando devem impedir disparos duplicados.
- Hitstop, hitstun, pushback, limites de arena, proteção contra infinitos e aumento de barra por acerto/defesa. Nenhum lutador deve atravessar o outro fora de teleporte intencional.
- Estado de luta separado de animação/renderização. Use dados para dano, deslocamento, startup, active, recovery, propriedades de golpe e cancelamento; não espalhe números mágicos por scripts.
- HUD: dois nomes, vida, barra, cronômetro, vitórias de round, indicador de combo e aviso de KO. Exibir silhuetas/retratos temporários sem copiar assets de terceiros.

### Alvos provisórios de sensação, não promessa de balanceamento

- Simulação de combate a **60 passos por segundo**. Usar frames para golpes e estados, mesmo que a renderização varie.
- Normal leve: início rápido, dano pequeno. Golpe forte: início/recovery maior, ganho de alcance ou conversão.
- Agarrão especial: alcance curto e falha reconhecível. Teleporte: começo e fim legíveis, com recuperação se antecipado pelo adversário.
- Supers gastam **1 unidade de barra** no protótipo e só entram na animação completa após confirmar o primeiro acerto.
- Parâmetros exatos de frames/dano entram em arquivos de configuração e devem ser ajustados jogando. Não alegar que estão balanceados sem teste.

## 6. Simon — rushdown/grappler

**Fantasia mecânica:** aproximar-se por ângulos inesperados, forçar a escolha entre bloquear uma invocação curta ou evitar um agarrão, e reposicionar-se por portal. É agressivo; não deve se tornar um personagem de controle de tela permanente.

| Movimento | Comando proposto | Função e contrajogo |
|---|---|---|
| Normais A/B/C/D | Botões | Socos e chutes próximos; `C` pode projetar uma mão de portal a curta/média distância com recovery maior. |
| **Fenda de Entrada** | `↓↘→ + A/C` | Teleporte curto. `A`: reaparece à frente; `C`: tenta trocar de lado se houver espaço. O reaparecimento deve ser antecipável e punível em uso descuidado. |
| **Mão do Limiar** | `↓↙← + A/C` | Mão invocada aparece à frente. `A` é curta/rápida; `C` tem mais alcance e preparo. Não cria armadilha permanente. |
| **Abraço do Abismo** | `→↓↘ + B/D` | Agarrão especial de perto por tentáculos. `B` prioriza rapidez; `D`, alcance modestamente maior e recovery maior. Falha contra rival fora do alcance ou que já escapou saltando. |
| **Servo da Fenda** | `↓↙← + B/D` | Pequeno esqueleto/minion aparece, executa **uma única ação** e desaparece. Uma invocação ativa por vez; startup, alcance e duração limitados. Não pode agarrar durante bloqueio sem janela de resposta. |
| **Super: Brecha Entre Mundos** | `↓↘→↓↘→ + A+C` | Gasta 1 barra. O primeiro golpe precisa acertar; então mão e tentáculo completam sequência curta e arremesso. |

**Restrição essencial:** teleporte + minion + agarrão não pode produzir uma sequência inevitável. Proibir novo minion enquanto outro está ativo; impedir invocação durante hitstun; dar recovery ao teleporte e à falha do agarrão. Implementar cada variante somente quando a versão base estiver jogável.

**Depois do primeiro marco:** invocação de armas de outros universos e variações de criaturas, com função e custo definidos antes de adicioná-las.

## 7. Techblade — rushdown puro

**Fantasia mecânica:** chegar perto com deslocamentos rápidos, pressionar com golpes mecânicos e confirmar cortes de katana. É direto, veloz e perigoso; investidas defendidas devem abrir resposta.

| Movimento | Comando proposto | Função e contrajogo |
|---|---|---|
| Normais A/B/C/D | Botões | Mão/braço mecânico no curto alcance; cortes de katana nos fortes. `C/D` têm mais alcance e recuperação. |
| **Investida Ígnea** | `↓↘→ + A/C` | Avanço com corte horizontal. `A` curto/rápido; `C` maior alcance e recovery. Não é seguro em defesa por padrão. |
| **Corte Ascendente** | `→↓↘ + A/C` | Antiaéreo. Versão forte sobe mais/causa mais dano, mas é fortemente punível se falhar ou for defendida. |
| **Passo Fantasma** | `↓↙← + B/D` | Deslocamento curto de reposição sem ataque automático; `D` cobre mais distância. Invulnerabilidade, se houver, deve ser breve e explicitamente definida. |
| **Corte de Pressão** | `↓↙← + A/C` | Golpe de curta distância com ritmo diferente dos normais; versão `C` permite conversão ao acertar, mas deixa abertura na defesa. |
| **Super: Sobrecarga da Lâmina** | `↓↘→↓↘→ + A+C` | Gasta 1 barra. Primeiro corte confirma a sequência; finaliza em descarga laranja. |

**Restrição essencial:** ataques longos de katana não devem ser simultaneamente rápidos, seguros e de grande alcance. Sem projétil de tela inteira no primeiro marco; a identidade é aproximação e pressão.

## 8. Implementação em etapas obrigatórias

### Etapa A — vertical slice mínimo

1. Projeto inicializável; tela de seleção simples; arena plana; duas figuras temporárias distintas.
2. Dois jogadores locais com direções independentes; posições corretas, colisão corporal, vida, cronômetro, rounds e resultado.
3. Quatro normais por personagem, defesa alta/baixa, agarrão normal, salto e deslocamentos.
4. Uma especial de cada personagem: **Mão do Limiar** e **Investida Ígnea**.
5. Hitboxes/hurtboxes por ação, hitstop, dano, stun, pushback e opção de debug.

**Aceite A:** duas pessoas conseguem completar uma partida de melhor de três, atacar, defender e dar revanche sem fechar o jogo.

### Etapa B — identidades completas

1. Demais especiais, teleporte, agarrão de tentáculos, servo, passo e antiaéreo.
2. Barra e super de cada um; efeitos temporários que não ocultem a ação.
3. Revisão de comando, cancelamento, recuperação, troca de lado e comportamento junto às bordas.

**Aceite B:** cada movimento listado responde ao comando na tela de treino; especial falhado tem reação coerente; nenhum golpe causa combo infinito reproduzível.

### Etapa C — apresentação e entrega

1. Integrar arte própria coerente com referências ou manter placeholders claramente marcados se faltarem quadros.
2. Animações mínimas por personagem: idle, andar frente/trás, agachar, salto/subida/queda, defesa em pé/agachado, dano alto/baixo, queda, levantar, vitória, derrota, quatro normais, especiais, agarrão e super.
3. Sons temporários originais ou licenciados de forma compatível; volumes separados e opção de silenciar.
4. Menu, ajuda de controles, revanche, treino, README de execução e atribuições/licenças.

**Aceite C:** entregar projeto editável, instruções reproduzíveis e artefato jogável para a plataforma disponível; declarar com precisão o que usa placeholder e o que foi testado.

### Etapa D — online obrigatório

1. Fixar e registrar versão estável do motor, ativar rollback e verificar se personagens, invocações, super, HUD e regras do round permanecem sincronizados.
2. Oferecer fluxo de hospedar/entrar acessível pelo menu ou pela interface do motor; informar endereçamento e portas necessários sem expor credenciais.
3. Mostrar ping/RTT e atraso em frames se o motor expuser esses dados; caso contrário, registrar o que pode ser medido em logs e documentar a limitação.
4. Testar duas máquinas em redes distintas, com condições normais e com latência/perda simuladas quando houver ferramenta adequada. Cobrir teleporte, servo, agarrão, KO, revanche e desconexão.
5. Ajustar atraso de entrada com base em testes, preservar integridade dos comandos e evitar dessíncronia. Nunca prometer ping de 0 ms.

**Aceite D:** duas pessoas em computadores e redes diferentes conseguem conectar, escolher personagens, completar uma partida e jogar revanche; se ocorrer desconexão, ambos recebem saída clara. Relatar RTT observado, configuração de atraso e qualquer limitação de rede/portas. Não declarar D concluída apenas com teste em localhost.

## 9. Modo de treino e depuração

- Treino com vida regenerável, barra cheia opcional e dummy parado, defendendo ou saltando.
- Exibir entrada reconhecida, estado de cada lutador, frame de ação e caixas de ataque/dano em toggle.
- Comando para resetar posições. Isto é ferramenta de desenvolvimento; pode ter interface simples.
- Quando um teste automatizado for útil, cubra parsing de comandos, dano único por hit, vitória por KO/timeout, reset de rounds, limites de arena e troca de lado. Acrescente teste de regressão para bugs encontrados.

## 10. Estrutura de entrega esperada

O agente implementador deve fornecer:

1. **Projeto completo**, organizado por motor, personagens, arena, HUD, áudio e recursos.
2. `README.md` com versão exata do motor, dependências, instalação, como executar, controles P1/P2, debug/treino e como gerar build.
3. `DESIGN.md` ou dados equivalentes com tabela de movimentos efetivamente implementados e diferenças desta especificação.
4. `LICENSES.md` com origem e licença de cada dependência e recurso externo. Imagens do usuário permanecem referências fornecidas pelo usuário; não tratá-las como recurso livre de terceiros.
5. Evidência de execução: resultado de build/teste e, se possível, captura curta do jogo rodando. Se não puder executar no ambiente, relatar precisamente o bloqueio; não afirmar que está jogável sem executar.
6. Evidência separada de partida online entre redes distintas, com configuração usada, RTT observado, comportamento de rollback e eventuais problemas. Se o ambiente não permitir esse teste, marcar online como **não verificado**.

## 11. Critérios de aceitação finais

- Jogo **1 contra 1**, sem equipes, sem hordas e sem OpenBOR.
- P1 pode escolher Simon e P2 Techblade, e vice-versa; ambos podem jogar com o mesmo personagem se a implementação permitir seleção espelhada.
- Dois jogadores controlam lutadores simultaneamente em partida local completa; rounds terminam por KO ou cronômetro.
- Simon usa portais tanto para deslocamento quanto para invocar pelo menos mão, tentáculo e um servo temporário; agarrão especial é distinto de golpe bloqueável.
- Techblade usa katana laranja, investida, antiaéreo, deslocamento e super; corpo permanece totalmente ciborgue onde a referência mostra armadura e braços.
- Golpes têm telegraph/recovery; bloqueio, acerto e erro provocam resultados distintos; barra não fica negativa; não há soft lock após KO, pause ou revanche.
- Instruções permitem que outra pessoa rode o projeto. Recursos finais ausentes são indicados como placeholders.
- Partida online 1 contra 1 utiliza rollback, tem fluxo claro de conexão e suporta partida completa e revanche entre redes distintas. Não prometer valor fixo de ping ou latência física.

## 12. Instrução operacional para GPT‑6 Astra

Use este arquivo como especificação. Primeiro examine o workspace e o motor escolhido; em seguida implemente a **Etapa A**, rode o protótipo e corrija problemas concretos. Prossiga para B, C e **D (online obrigatório)**. Tome decisões técnicas rotineiras sem pedir autorização; registre alterações de escopo. Se as imagens não estiverem disponíveis no seu contexto, solicite-as ou trabalhe com as descrições acima, deixando claro que a fidelidade visual ainda não foi verificada. Pergunte ao usuário apenas por uma decisão que realmente impeça o avanço. No final, entregue arquivos, comandos de execução, testes realizados e pendências reais — sem chamar um mockup de produto jogável.
