# Arte e reprodução

Modo utilizado: ferramenta integrada GPT Image. As folhas geradas são os arquivos-fonte preservados; o gerador apenas prepara os sprites para o formato nativo do jogo.

- `assets/source/simon.png`: primeira folha.
- `assets/source/simon-v2.png`: versão usada pelo jogo, refinada a partir das duas referências faciais.
- `assets/source/techblade.png`: folha de Techblade.
- `tools/build_assets.py`: extração com área adicional para extremidades, limpeza de fragmentos de células vizinhas, origem fixa e conversão para paleta/SFF.

As folhas iniciais têm 24 células cada. A versão 0.2 acrescenta 24 poses de combate (12 por personagem) e 12 poses de servo/tentáculos. Os registros AIR reutilizam desenhos e NÃO representam centenas de desenhos únicos. A fluidez da simulação é independente da quantidade de desenhos. É necessário desenhar mais transições e golpes exclusivos para alcançar o polimento final de uma produção comercial.

## Direção enviada ao gerador

Folha 1536×1024 em 6 colunas × 4 linhas, fundo transparente, pixel art de luta 2D com anatomia atlética e sombreamento detalhado inspirado nos clássicos arcade. Todos os lutadores voltados para a direita, escala e origem consistentes. Primeira linha: guarda/idle; segunda: caminhada; terceira: ataque com preparação, impacto e recuperação; quarta: agachar, saltar, chute alto, rasteira, dano e queda.

Simon: uniforme militar preto, rosto descoberto, portais vermelhos e mão invocada. Na edição, a folha selecionada foi o alvo exato; as duas imagens anexas serviram de referência para rosto, cabelo castanho ondulado e olhos azuis. Manter camisa militar preta, calça cargo preta, botas e luvas; remover a faixa vermelha e reservar o vermelho aos efeitos.

Techblade: samurai inteiramente ciborgue, capuz e armadura preta, visor laranja, braços e mãos 100% mecânicos, katana quente laranja, sem pele visível.

## Novos arquivos da versão 0.2

- `assets/source/combat-extra.png`: 24 poses, seis colunas/quatro linhas; Simon agachado, Simon salto/chute, Techblade agachado/corte, Techblade salto/corte. Fundo transparente, roupa preta e identidades preservadas.
- `assets/source/summons.png`: 12 poses em seis colunas/duas linhas; servo esquelético emerge, desfere um golpe e desaparece; tentáculos saem de um portal vermelho, estendem e recolhem. Sem sangue nem vítima desenhada no atlas.

Prompts: novas folhas complementares com escala/origem consistentes, contornos e sombreamento de luta arcade, sem texto/grid, extremidades contidas nas células; referências Simon v2 e Techblade para a folha de combate. Usada a ferramenta integrada GPT Image. A extração e a conversão são operações do build, não novos desenhos.

## Próximo passo visual

Mais transições exclusivas de socos e vitória, revisão manual de volume e super; evitar prometer polimento comercial com os quadros atuais. As referências de rosto têm mais detalhe do que é legível no sprite final.

