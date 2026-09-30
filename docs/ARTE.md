# Arte e reprodução

Modo utilizado: ferramenta integrada GPT Image. As folhas geradas são os arquivos-fonte preservados; o gerador apenas prepara os sprites para o formato nativo do jogo.

- `assets/source/simon.png`: primeira folha.
- `assets/source/simon-v2.png`: versão usada pelo jogo, refinada a partir das duas referências faciais.
- `assets/source/techblade.png`: folha de Techblade.
- `tools/build_assets.py`: extração com área adicional para extremidades, limpeza de fragmentos de células vizinhas, origem fixa e conversão para paleta/SFF.

São 24 células por folha; os 448 registros de animação de cada personagem reutilizam poses e NÃO representam 448 desenhos únicos. A fluidez da simulação é independente da quantidade de desenhos. É necessário desenhar mais transições e golpes exclusivos para alcançar o polimento final de uma produção comercial.

## Direção enviada ao gerador

Folha 1536×1024 em 6 colunas × 4 linhas, fundo transparente, pixel art de luta 2D com anatomia atlética e sombreamento detalhado inspirado nos clássicos arcade. Todos os lutadores voltados para a direita, escala e origem consistentes. Primeira linha: guarda/idle; segunda: caminhada; terceira: ataque com preparação, impacto e recuperação; quarta: agachar, saltar, chute alto, rasteira, dano e queda.

Simon: uniforme militar preto, rosto descoberto, portais vermelhos e mão invocada. Na edição, a folha selecionada foi o alvo exato; as duas imagens anexas serviram de referência para rosto, cabelo castanho ondulado e olhos azuis. Manter camisa militar preta, calça cargo preta, botas e luvas; remover a faixa vermelha e reservar o vermelho aos efeitos.

Techblade: samurai inteiramente ciborgue, capuz e armadura preta, visor laranja, braços e mãos 100% mecânicos, katana quente laranja, sem pele visível.

## Próximo passo visual

Mais quadros exclusivos de socos, golpes agachados/aéreos, agarrões e supers; revisão manual de alinhamento e volume; animação de tentáculos e servo. As referências de rosto têm mais detalhe do que é legível no sprite final.

