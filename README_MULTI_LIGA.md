# 🚀 Buscador de Estatísticas - Múltiplas Ligas

Script genérico para buscar estatísticas de jogadores de múltiplas ligas europeias do fbref.com.

## 📊 Ligas Suportadas

- **La Liga** (Espanha) - `--liga laliga`
- **Bundesliga** (Alemanha) - `--liga bundesliga`
- **Serie A** (Itália) - `--liga seriea`
- **Primeira Liga** (Portugal) - `--liga portugal`
- **Ligue 1** (França) - `--liga ligue1`
- **Championship** (Inglaterra - Série B) - `--liga championship`
- **Premier League** (Inglaterra - Série A) - `--liga premier`

## 📈 Estatísticas Extraídas

Para cada jogador em cada partida:
- **MINUTES**: Minutos jogados
- **GOALS**: Gols marcados
- **ASSISTS**: Assistências
- **xG**: Expected Goals (4 casas decimais)
- **xA**: Expected Assists (4 casas decimais)

## 🔧 Requisitos

```bash
pip install -r requirements.txt
```

Dependências:
- pandas
- openpyxl
- requests
- beautifulsoup4
- lxml
- cloudscraper (recomendado para contornar proteções anti-bot)

## 🚀 Uso

### Exemplo 1: La Liga
```bash
python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30
```

### Exemplo 2: Bundesliga
```bash
python buscar_estatisticas_multi_liga.py --liga bundesliga --inicio 2025-09-01 --fim 2025-09-30
```

### Exemplo 3: Serie A
```bash
python buscar_estatisticas_multi_liga.py --liga seriea --inicio 2025-09-01 --fim 2025-09-30
```

### Exemplo 4: Primeira Liga (Portugal)
```bash
python buscar_estatisticas_multi_liga.py --liga portugal --inicio 2025-09-01 --fim 2025-09-30
```

### Exemplo 5: Ligue 1
```bash
python buscar_estatisticas_multi_liga.py --liga ligue1 --inicio 2025-09-01 --fim 2025-09-30
```

### Exemplo 6: Championship (Inglaterra Série B)
```bash
python buscar_estatisticas_multi_liga.py --liga championship --inicio 2025-09-01 --fim 2025-09-30
```

### Modo Teste (não salva arquivo)
```bash
python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30 --limit 1 --test
```

### Limitar número de jogos
```bash
python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30 --limit 5
```

### Salvar em arquivo específico
```bash
python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30 --output minha_planilha.xlsx
```

## 📋 Parâmetros

| Parâmetro | Descrição | Obrigatório | Exemplo |
|-----------|-----------|-------------|---------|
| `--liga` | Liga a buscar (laliga, bundesliga, seriea, portugal, ligue1, championship, premier) | ✅ Sim | `--liga laliga` |
| `--inicio` | Data de início (YYYY-MM-DD) | ✅ Sim | `--inicio 2025-09-01` |
| `--fim` | Data de fim (YYYY-MM-DD) | ✅ Sim | `--fim 2025-09-30` |
| `--output` | Arquivo Excel de saída | ❌ Não | `--output resultado.xlsx` |
| `--limit` | Limitar número de jogos | ❌ Não | `--limit 10` |
| `--test` | Modo teste (não salva) | ❌ Não | `--test` |

## 📁 Estrutura do Arquivo de Saída

O arquivo Excel gerado contém as seguintes colunas:
- Player
- Team
- Date
- Opponent
- Minutes
- Goals
- Assists
- xG (4 casas decimais)
- xA (4 casas decimais)
- Confronto
- Location (home/away)
- adj
- Year
- Month

## ✅ Validação

Todas as ligas foram testadas e validadas:
- ✅ La Liga (Espanha) - Testado e funcionando
- ✅ Bundesliga (Alemanha) - Testado e funcionando
- ✅ Serie A (Itália) - Testado e funcionando
- ✅ Primeira Liga (Portugal) - Testado e funcionando
- ✅ Ligue 1 (França) - Testado e funcionando
- ✅ Championship (Inglaterra Série B) - Testado e funcionando

## 🧪 Script de Validação

Para testar todas as ligas automaticamente:
```bash
python validar_ligas.py
```

Este script testa cada liga com 1 jogo para verificar se está funcionando corretamente.

## ⚠️ Notas Importantes

1. **Rate Limiting**: O script inclui delays automáticos para evitar bloqueios. Se receber erro 429, o script aguardará automaticamente.

2. **xG e xA**: Os valores são formatados com exatamente 4 casas decimais (ex: 0.1000, 0.0000).

3. **Filtros Automáticos**: O script remove automaticamente:
   - Linhas de subtotais (ex: "16 Players")
   - Jogadores com minutos anormalmente altos (>120)
   - Jogos futuros (sem placar)

4. **Formato de Datas**: Use sempre o formato YYYY-MM-DD para as datas.

## 🔍 Troubleshooting

### Erro 429 (Rate Limit)
- O script aguarda automaticamente 30 segundos e tenta novamente
- Se persistir, aguarde alguns minutos e execute novamente

### Nenhum dado encontrado
- Verifique se há jogos no período especificado
- Verifique se os jogos já foram jogados (têm placar)
- Teste com um período maior ou mais recente

### Link de jogo não encontrado
- O script tem múltiplos fallbacks para encontrar links
- Se falhar, verifique se o jogo realmente existe no fbref.com

## 📝 Exemplo Completo

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Buscar dados da La Liga de setembro de 2025
python buscar_estatisticas_multi_liga.py \
  --liga laliga \
  --inicio 2025-09-01 \
  --fim 2025-09-30 \
  --output laliga_setembro_2025.xlsx

# O arquivo será salvo como: laliga_setembro_2025.xlsx
```

## 📊 Resultados

O script gera um arquivo Excel com todas as estatísticas encontradas. Os valores de xG e xA são formatados com 4 casas decimais e aplicados diretamente no Excel.

---

**Desenvolvido para extrair dados de fbref.com**


