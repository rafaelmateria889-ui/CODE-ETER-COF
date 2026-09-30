# Online — versão 0.2

## Conectar

Use a mesma versão do pacote nos dois computadores. Abra JOGAR.bat e escolha ONLINE no menu.

1. Quem hospeda escolhe Host/Hospedar e aguarda.
2. Quem entra escolhe Join/Add/New Address, dá um nome à conexão e informa o IPv4 do anfitrião. Na mesma rede, use o IP local; entre redes, use o IP público ou o endereço de uma VPN de rede privada instalada e configurada pelos jogadores.
3. Após conectar, escolha Versus no menu online, selecione os dois personagens e confirme a arena.
4. Ao fim, confirme a tela de resultado e volte à seleção para iniciar outra partida. Esc sai/cancela; não altere arquivos do jogo durante uma sessão.

Os nomes dos submenus internos podem aparecer em inglês. Nenhuma conta própria ou matchmaking foi implementado.

## Portas reais do motor fixado

| Fluxo | Protocolo | Porta |
|---|---|---|
| Conexão inicial ao anfitrião | TCP | 7500 |
| Rollback: socket local do anfitrião | UDP | 7600 |
| Rollback: socket local de quem entra | UDP | 7550 |

A porta TCP vem de Netplay.ListenPort. Nesta versão oficial do motor, as portas UDP são fixadas em src/rollback.go (InitP1/InitP2), e não mudam ao editar ListenPort. Entre redes, o anfitrião pode precisar encaminhar TCP 7500 e UDP 7600 para seu PC; o visitante, UDP 7550 para seu PC. Permita esses fluxos no firewall apenas ao aplicativo/rede apropriados. CGNAT pode impedir encaminhamento; nesse caso use uma rede VPN compartilhada entre os jogadores ou obtenha um endereço roteável com seu provedor. Não há atravessamento automático de NAT garantido.

A implementação consultada é a tag v1.0.0 de https://github.com/ikemen-engine/Ikemen-GO, src/netplay.go e src/rollback.go.

## Atraso e diagnóstico

Rollback habilitado, atraso inicial **2 frames** (33,3ms de atraso de comando configurado a 60 Hz; não é o ping total nem uma medição da latência ponta a ponta). Opções → Network/Netplay → Frame Delay permite ajuste de 0 a 10. Teste 2 inicialmente, reduza para 1/0 somente se o comportamento continuar estável nos dois lados. Não há valor mínimo garantido.

A interface usada não oferece um painel próprio de RTT/jitter. Para diagnóstico, em runtime/save/eter.ini, defina Rollback.LogsEnabled=1 e reinicie ambos; logs ficam em runtime/save/logs. Isso pode reduzir desempenho; desligue após o teste. Os logs permitem verificar sincronização, sessões e desconexões, mas não devem ser apresentados como medida de ping. Ping de sistema ao endereço do par é apenas ICMP e pode diferir do fluxo do jogo.

## O que foi testado

Duas instâncias oficiais Linux, comunicação TCP+UDP por loopback, atraso 2, golpes por teclas do sistema, invocação, portal, agarrão, ataque dos dois lados, dois KOs e vitórias com vida/barra iguais nos dois pares. Nenhum evento de dessíncronia foi registrado nessa execução. Esse teste não mede Internet, NAT ou redes diferentes.

Aceite final pendente: dois PCs em redes distintas, partida, nova partida sem desconectar, teleporte, servo, agarrão, super confirmado, perda/jitter e desconexão. Controle físico e uma partida Windows com GPU real também precisam ser verificados. Não chamamos a Etapa D de concluída.
