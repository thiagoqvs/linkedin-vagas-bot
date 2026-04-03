# LinkedIn Vagas Bot v2

Script simples em Python para gerar buscas filtradas de vagas no LinkedIn, com foco em vagas remotas e abertura em lotes menores.

## O que ele faz

- Gera links de busca prontos do LinkedIn
- Filtra por cargos e palavras-chave
- Exclui termos fora do foco
- Salva as buscas em TXT e CSV
- Abre as buscas em lotes de 3 ou 5 para não sobrecarregar o navegador

## O que ele não faz

- Não faz scraping
- Não faz login automático
- Não aplica em vagas
- Não interage com sua conta do LinkedIn

## Como usar

```bash
python linkedin_vagas_bot_v2.py
```

## Sugestão de uso

- Use lote 3 quando quiser abrir poucas buscas por vez
- Use lote 5 quando quiser acelerar
- Ajuste o bloco CONFIG com seus cargos e tecnologias

## Ideias para próximas versões

- Histórico de buscas abertas
- Controle de vagas já vistas
- Exportação com status
- Interface gráfica simples
