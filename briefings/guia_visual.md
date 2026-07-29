---
escopo: "Desenvolvimento de pacote LaTeX para guias com foco na apresentação visual, mantendo características de acessibilidade"
---
## Organização fixa dos guias

| divisão     | elemento                          |
| ----------- | --------------------------------- |
| pré-textual | falsa folha de rosto              |
| pré-textual | créditos institucionais           |
| pré-textual | folha de rosto                    |
| pré-textual | apresentação                      |
| pré-textual | sumário                           |
| textual     | conteúdo                          |
| pós-textual | apêndices/anexos (glossário etc.) |
| pós-textual | créditos técnicos                 |
## Elementos gráficos (EG)

*Exclusivos para as divisões textual e pós-textual*

Os elementos gráficos (EG) devem ter formato fixo, adequado ao layout dos guias. O guia será gerado por LaTeX; os designers vão criar uma biblioteca de elementos gráficos para cada guia, com cores e formas específicas.

- Fólio (número da página): parte superior da margem externa; deve permitir o uso de EG como background do número (formato padrão: redondo);
- imagem: as imagens (figuras, tabelas etc.) devem permitir a inserção de EG como moldura, começando nas bordas das imagens e se estendendo por 3 em (em outras palavras, o perímetro de cada imagem deve prever uma moldura com 3 em de espessura). É necessário entender como essas molduras podem ser ajustadas flexivelmente conforme o tamanho da imagem;
- separador de seção fantasma (asterismo): a biblioteca de EG deve prever separadores específicos por publicação, para serem usados no lugar de asterismo (⁂);