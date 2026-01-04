# 🤖 BOT ESTAT BETS - Buscador de Estatísticas da Premier League

Script Python para buscar automaticamente estatísticas de jogadores da Premier League do site fbref.com.

## 📊 Estatísticas Coletadas

O script busca as seguintes informações para cada jogador em cada partida:

- **MINUTES**: Minutos jogados
- **GOALS**: Gols marcados  
- **ASSISTS**: Assistências
- **xG**: Expected Goals (até 4 casas decimais)
- **xA**: Expected Assists (até 4 casas decimais)

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Clonar o Repositório

```bash
git clone https://github.com/chili-guy/BOT_ESTAT_BETS.git
cd BOT_ESTAT_BETS
```

### 3. Criar Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Uso Básico

```bash
# Buscar dados de um período específico
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31
```

### Parâmetros Disponíveis

| Parâmetro | Descrição | Obrigatório | Exemplo |
|-----------|-----------|-------------|---------|
| `--inicio` | Data de início (YYYY-MM-DD) | ✅ Sim | `--inicio 2025-10-01` |
| `--fim` | Data de fim (YYYY-MM-DD) | ✅ Sim | `--fim 2025-10-31` |
| `--output` | Arquivo Excel de saída | ❌ Não (padrão: premier.xlsx) | `--output resultado.xlsx` |
| `--limit` | Limitar número de jogos | ❌ Não | `--limit 10` |
| `--test` | Modo teste (não salva arquivo) | ❌ Não | `--test` |

### Exemplos de Uso

#### 1. Buscar dados de um mês específico

```bash
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31
```

#### 2. Buscar dados de um período maior

```bash
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-12-31
```

#### 3. Modo teste (não salva, apenas mostra resultados)

```bash
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --test
```

#### 4. Limitar número de jogos (útil para testes)

```bash
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --limit 3 --test
```

#### 5. Especificar arquivo de saída customizado

```bash
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --output minha_planilha.xlsx
```

#### 6. Salvar em outro diretório

```bash
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --output /caminho/completo/resultado.xlsx
```

### Ver Ajuda Completa

```bash
python buscar_estatisticas.py --help
```

## 📁 Estrutura dos Dados

A planilha gerada contém as seguintes colunas principais:

- **Player**: Nome do jogador
- **Team**: Time do jogador
- **Date**: Data do jogo
- **Opponent**: Time adversário
- **Minutes**: Minutos jogados
- **Goals**: Gols marcados
- **Assists**: Assistências
- **xG**: Expected Goals (4 casas decimais)
- **xA**: Expected Assists (4 casas decimais)
- **Confronto**: Formato "Time|Adversário|Data"
- **Location**: Local do jogo (home/away)
- **Year**: Ano do jogo
- **Month**: Mês do jogo

## ⚙️ Funcionamento

1. O script acessa o site fbref.com
2. Busca os jogos no período especificado
3. Para cada jogo, extrai estatísticas de todos os jogadores (ambos os times)
4. Filtra automaticamente linhas de subtotal/agregado (990 minutos)
5. Remove duplicatas automaticamente
6. Ordena por data
7. Salva na planilha Excel especificada

## ⚠️ Importante

- **Rate Limiting**: O script inclui pausas entre requisições para respeitar o site
- **Dados Disponíveis**: Só busca dados de jogos já jogados (com placar)
- **Jogos Futuros**: Jogos que ainda não foram jogados são automaticamente pulados
- **Estrutura do Site**: Se o fbref.com mudar sua estrutura HTML, o script pode precisar de ajustes

## 🐛 Solução de Problemas

### O script não encontra dados

1. Verifique sua conexão com a internet
2. Verifique se os dados estão disponíveis no site fbref.com
3. Use `--test` para ver o que está sendo encontrado
4. Use `--limit 1` para testar com apenas 1 jogo

### Erro ao salvar arquivo

- Verifique se tem permissão de escrita no diretório
- Verifique se o caminho do arquivo está correto
- Se usar caminho absoluto, certifique-se de que o diretório existe (ou será criado automaticamente)

### Rate Limit (429)

- O script aguarda automaticamente quando recebe rate limit
- Aguarde alguns minutos e tente novamente
- Considere usar `--limit` para processar menos jogos por vez

## 📝 Estrutura do Projeto

```
BOT_ESTAT_BETS/
├── buscar_estatisticas.py    # Script principal
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
└── venv/                      # Ambiente virtual (não commitado)
```

## 🔧 Dependências

- pandas >= 2.0.0
- openpyxl >= 3.1.0
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- cloudscraper >= 1.2.0

## 📄 Licença

Este projeto é open source e está disponível para uso livre.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

## 📧 Suporte

Para questões ou problemas, abra uma issue no repositório GitHub.

---

**Desenvolvido com ❤️ para facilitar a coleta de estatísticas da Premier League**
