# Origem e licenças

## Conteúdo autoral do projeto

Conceitos e nomes Simon e Techblade: fornecidos por Rafael Santos Materia. Código de personagens, geradores, arena de treino, menus próprios e efeitos sonoros sintetizados foram produzidos para este projeto.

As folhas em `assets/source/` foram geradas com GPT Image. Simon v2 usa como referência as imagens fornecidas pelo criador. Não são sprites extraídos de The King of Fighters. As imagens de referência não são incluídas no download do motor. O projeto não estabelece aqui uma licença geral de redistribuição para personagens e arte do usuário.

## Ikemen GO 1.0.0

Origem: https://github.com/ikemen-engine/Ikemen-GO/releases/tag/v1.0.0

Motor e scripts: licença MIT, autores listados no `LICENSES.txt` da distribuição oficial. O iniciador baixa a distribuição oficial sem recompilar o núcleo e preserva os avisos.

Interface de luta, fontes e recursos comuns incluídos com o motor: licenças Creative Commons da distribuição, incluindo CC BY 3.0. Créditos declarados pelo motor: Ohmga Shironeko (motif/lifebar), SuperFromND (sons), President Devon e Rurouni (mensagens e ícones), Shiyo Kakuge (efeitos), Cylia Margatroid e Rurouni (logos), Miguel Young (vozes), Gacel (fonte default-3x5). Os avisos completos acompanham o motor em runtime/LICENSES.txt.

FFmpeg é fornecido pelo motor sob LGPL v2.1; o código-fonte correspondente está no mesmo release oficial em `src_ffmpeg.tar.gz`.

O roster do jogo contém apenas Simon e Techblade. Personagens de exemplo da distribuição do motor não fazem parte da seleção deste projeto.

## Ferramentas de desenvolvimento

Pillow: HPND, usada para empacotar sprites e validar arquivos; não é necessária para jogar no Windows. Xvfb, xdotool e a biblioteca de testes SDL são recursos de validação em Linux, não acompanham o instalador do jogador.

