# 📊 Instruções de Uso - Buscador de Estatísticas

## 🎯 Scripts Disponíveis

### Script 1: Premier League (`buscar_estatisticas.py`)

O script `buscar_estatisticas.py` busca na web (fbref.com) as seguintes informações para cada jogador em cada partida da Premier League:

### Script 2: Múltiplas Ligas (`buscar_estatisticas_multi_liga.py`)

O script `buscar_estatisticas_multi_liga.py` busca estatísticas das seguintes ligas:
- La Liga (Espanha)
- Bundesliga (Alemanha)
- Serie A (Itália)
- Primeira Liga (Portugal)
- Ligue 1 (França)
- Championship (Inglaterra - Série B)

## 📊 Estatísticas Coletadas

Ambos os scripts buscam as seguintes informações para cada jogador em cada partida:

- **MINUTES**: Minutos jogados
- **GOALS**: Gols marcados
- **ASSISTS**: Assistências
- **XG**: Expected Goals
- **XA**: Expected Assists

## 📋 Estrutura da Planilha

O script respeita a estrutura da sua planilha existente (`premier.xlsx`), incluindo todas as colunas:

- Player, Team, Date, Opponent
- Minutes, Goals, Assists, xG, xA
- Confronto, Location, adj
- Year, Month
- E outras colunas existentes

## 🚀 Como usar

### 1. Ative o ambiente virtual:
```bash
source venv/bin/activate
```

### 2. Execute o script desejado:

#### Premier League

```bash
# Buscar dados de outubro de 2025
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31

# Modo teste
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --test

# Limitar número de jogos
python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --limit 5 --test
```

#### Múltiplas Ligas

```bash
# La Liga (Espanha)
python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30

# Bundesliga (Alemanha)
python buscar_estatisticas_multi_liga.py --liga bundesliga --inicio 2025-09-01 --fim 2025-09-30

# Serie A (Itália)
python buscar_estatisticas_multi_liga.py --liga seriea --inicio 2025-09-01 --fim 2025-09-30

# Primeira Liga (Portugal)
python buscar_estatisticas_multi_liga.py --liga portugal --inicio 2025-09-01 --fim 2025-09-30

# Ligue 1 (França)
python buscar_estatisticas_multi_liga.py --liga ligue1 --inicio 2025-09-01 --fim 2025-09-30

# Championship (Inglaterra Série B)
python buscar_estatisticas_multi_liga.py --liga championship --inicio 2025-09-01 --fim 2025-09-30

# Modo teste e limitar jogos
python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30 --limit 1 --test
```

## 📝 Parâmetros disponíveis

### Premier League (`buscar_estatisticas.py`)

| Parâmetro | Descrição | Obrigatório | Exemplo |
|-----------|-----------|-------------|---------|
| `--inicio` | Data de início (YYYY-MM-DD) | ✅ Sim | `--inicio 2025-10-01` |
| `--fim` | Data de fim (YYYY-MM-DD) | ✅ Sim | `--fim 2025-10-31` |
| `--output` | Arquivo de saída | ❌ Não (padrão: premier.xlsx) | `--output resultado.xlsx` |
| `--limit` | Limitar número de jogos | ❌ Não | `--limit 10` |
| `--test` | Modo teste (não salva) | ❌ Não | `--test` |

### Múltiplas Ligas (`buscar_estatisticas_multi_liga.py`)

| Parâmetro | Descrição | Obrigatório | Exemplo |
|-----------|-----------|-------------|---------|
| `--liga` | Liga a buscar (laliga, bundesliga, seriea, portugal, ligue1, championship) | ✅ Sim | `--liga laliga` |
| `--inicio` | Data de início (YYYY-MM-DD) | ✅ Sim | `--inicio 2025-09-01` |
| `--fim` | Data de fim (YYYY-MM-DD) | ✅ Sim | `--fim 2025-09-30` |
| `--output` | Arquivo de saída | ❌ Não | `--output minha_planilha.xlsx` |
| `--limit` | Limitar número de jogos | ❌ Não | `--limit 10` |
| `--test` | Modo teste (não salva) | ❌ Não | `--test` |

## ⚙️ Funcionamento

1. O script acessa o site fbref.com
2. Busca os jogos no período especificado
3. Para cada jogo, extrai estatísticas de todos os jogadores (ambos os times)
4. Respeita a estrutura da planilha existente
5. Remove duplicatas automaticamente
6. Ordena por data
7. Salva na planilha especificada

## ⚠️ Importante

- **Rate Limiting**: O script inclui pausas entre requisições para respeitar o site
- **Estrutura do Site**: Se o fbref.com mudar sua estrutura HTML, o script pode precisar de ajustes
- **Dados Disponíveis**: Só busca dados que já estão disponíveis no site

## 🐛 Solução de Problemas

Se o script não encontrar dados:
1. Verifique sua conexão com a internet
2. Verifique se os dados estão disponíveis no site fbref.com
3. Use `--test` para ver o que está sendo encontrado
4. Use `--limit 1` para testar com apenas 1 jogo

## 🧪 Validação de Dados

### Validar todas as ligas automaticamente

```bash
python validar_ligas.py
```

### Comparar dados com o site

```bash
python comparar_dados.py
```

**✅ Todos os scripts foram validados e estão funcionando corretamente!**

## 📖 Ver ajuda completa

```bash
# Premier League
python buscar_estatisticas.py --help

# Múltiplas Ligas
python buscar_estatisticas_multi_liga.py --help
```

## 📚 Documentação Adicional

Para mais detalhes sobre o script de múltiplas ligas, consulte:
- `README_MULTI_LIGA.md` - Documentação completa



