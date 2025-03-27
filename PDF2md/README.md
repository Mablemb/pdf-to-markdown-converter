# PDF para Markdown Converter

Um utilitário de linha de comando para converter arquivos PDF para formato Markdown com barra de progresso e indicador de atividade.

## Características

- Conversão de PDF para formato Markdown
- Indicador de progresso durante a conversão
- Animação de spinner durante a análise inicial do PDF
- Verificação automática de arquivos duplicados
- Criação automática de diretórios de saída
- Tratamento robusto de erros e permissões

## Requisitos

- Python 3.6 ou superior
- pymupdf4llm
- tqdm

## Instalação

Instale as dependências diretamente:

```bash
pip install pymupdf4llm tqdm
```

## Uso

### Linha de comando

```bash
python pdf_to_markdown.py caminho/do/arquivo.pdf caminho/para/saida.md
```

### Como módulo Python

```python
from pdf_to_markdown import convert_pdf_to_markdown

# Converter um PDF para Markdown
resultado = convert_pdf_to_markdown("caminho/do/arquivo.pdf", "caminho/para/saida.md")

if resultado:
    print("Conversão realizada com sucesso!")
else:
    print("A conversão falhou.")
```

## Solução de Problemas

### Erro de Permissão

Se você encontrar erros de permissão como:
```
ERROR: Sem permissão para criar o diretório: caminho/do/diretório
```

Tente uma das seguintes soluções:

1. Execute o script com privilégios de administrador
2. Escolha um diretório de saída onde você tenha permissões de escrita
3. Verifique se o diretório de saída não está sendo usado por outro processo

### Arquivos Duplicados

Se o arquivo de saída já existir, a conversão será pulada para evitar sobrescrever o arquivo:
```
Arquivo já existe na pasta de saída: caminho/para/arquivo.md
Pulando conversão para evitar sobrescrita.
```

Para converter novamente, primeiro remova o arquivo existente ou especifique um caminho diferente.
