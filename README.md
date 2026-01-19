# 🤖 BOT ESTAT BETS - Buscador de Estatísticas de Futebol via FotMob API

Script Python para buscar automaticamente estatísticas detalhadas de jogadores de múltiplas ligas europeias usando a **FotMob API** - uma alternativa confiável e estável ao scraping de sites.

## 🌟 Características Principais

- ✅ **API Oficial**: Utiliza a API pública do FotMob (mais estável que scraping)
- ✅ **Sem Bloqueios**: Não sofre com proteções Cloudflare ou bloqueios 403
- ✅ **7 Ligas Principais**: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Primeira Liga e Championship
- ✅ **Estatísticas Completas**: Minutes, Goals, Assists, xG, xA e **SH (Total de Chutes)**
- ✅ **Exportação Excel**: Dados organizados em planilhas prontas para análise
- ✅ **Filtro por Período**: Busque dados de qualquer intervalo de datas
- ✅ **Validação Automática**: Scripts de teste incluídos

## 🏆 Ligas Suportadas

| Liga | Código | País |
|------|--------|------|
| **Premier League** | `premier` | Inglaterra |
| **La Liga** | `laliga` | Espanha |
| **Bundesliga** | `bundesliga` | Alemanha |
| **Serie A** | `seriea` | Itália |
| **Ligue 1** | `ligue1` | França |
| **Primeira Liga** | `portugal` | Portugal |
| **Championship** | `championship` | Inglaterra (Série B) |

## 📊 Estatísticas Coletadas

O script busca as seguintes informações para cada jogador em cada partida:

- **MINUTES**: Minutos jogados no jogo
- **GOALS**: Gols marcados
- **ASSISTS**: Assistências concedidas
- **xG**: Expected Goals (até 4 casas decimais)
- **xA**: Expected Assists (até 4 casas decimais)
- **SH**: Total de chutes (shots) realizados

### Dados Adicionais Incluídos

- **Player**: Nome do jogador
- **Team**: Time do jogador
- **Date**: Data do jogo
- **Opponent**: Time adversário
- **Location**: Local do jogo (home/away)
- **Confronto**: Formato "Time|Adversário|Data"
- **Year**: Ano do jogo
- **Month**: Mês do jogo
- **adj**: Campo de ajuste (0 por padrão)

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conexão com internet

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

As dependências principais são:
- `pandas >= 2.0.0` - Manipulação de dados
- `openpyxl >= 3.1.0` - Exportação para Excel
- `requests >= 2.31.0` - Requisições HTTP

## 📖 Como Usar

### Uso Básico

```bash
python buscar_estatisticas_fotmob.py --liga <LIGA> --inicio <DATA_INICIO> --fim <DATA_FIM>
```

### Parâmetros Disponíveis

| Parâmetro | Descrição | Obrigatório | Exemplo |
|-----------|-----------|-------------|---------|
| `--liga` | Liga a buscar | ✅ Sim | `--liga bundesliga` |
| `--inicio` | Data de início (YYYY-MM-DD) | ✅ Sim | `--inicio 2025-08-01` |
| `--fim` | Data de fim (YYYY-MM-DD) | ✅ Sim | `--fim 2025-08-31` |
| `--output` | Arquivo Excel de saída | ❌ Não | `--output resultado.xlsx` |
| `--limit` | Limitar número de jogos | ❌ Não | `--limit 10` |
| `--test` | Modo teste (não salva arquivo) | ❌ Não | `--test` |

### Exemplos de Uso

#### 1. Buscar dados da Bundesliga de um mês

```bash
python buscar_estatisticas_fotmob.py --liga bundesliga --inicio 2025-08-01 --fim 2025-08-31
```

**Resultado**: Arquivo `bundesliga_2025-08-01_2025-08-31.xlsx` será criado.

#### 2. Premier League com arquivo personalizado

```bash
python buscar_estatisticas_fotmob.py --liga premier --inicio 2025-09-01 --fim 2025-09-30 --output premier_setembro.xlsx
```

#### 3. Modo teste (não salva, apenas mostra resultados)

```bash
python buscar_estatisticas_fotmob.py --liga laliga --inicio 2025-08-22 --fim 2025-08-24 --test
```

#### 4. Limitar número de jogos (útil para testes rápidos)

```bash
python buscar_estatisticas_fotmob.py --liga seriea --inicio 2025-08-01 --fim 2025-08-31 --limit 3 --test
```

#### 5. La Liga (Espanha)

```bash
python buscar_estatisticas_fotmob.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30
```

#### 6. Serie A (Itália)

```bash
python buscar_estatisticas_fotmob.py --liga seriea --inicio 2025-09-01 --fim 2025-09-30
```

#### 7. Ligue 1 (França)

```bash
python buscar_estatisticas_fotmob.py --liga ligue1 --inicio 2025-09-01 --fim 2025-09-30
```

#### 8. Primeira Liga (Portugal)

```bash
python buscar_estatisticas_fotmob.py --liga portugal --inicio 2025-09-01 --fim 2025-09-30
```

#### 9. Championship (Inglaterra - Série B)

```bash
python buscar_estatisticas_fotmob.py --liga championship --inicio 2025-09-01 --fim 2025-09-30
```

### Ver Ajuda Completa

```bash
python buscar_estatisticas_fotmob.py --help
```

## 📁 Estrutura dos Dados de Saída

A planilha Excel gerada contém as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| **Player** | Texto | Nome completo do jogador |
| **Team** | Texto | Nome do time |
| **Date** | Data | Data do jogo (YYYY-MM-DD) |
| **Opponent** | Texto | Time adversário |
| **Minutes** | Número | Minutos jogados |
| **Goals** | Número | Gols marcados |
| **Assists** | Número | Assistências |
| **xG** | Decimal | Expected Goals (4 casas decimais) |
| **xA** | Decimal | Expected Assists (4 casas decimais) |
| **SH** | Número | Total de chutes realizados |
| **Confronto** | Texto | Formato "Time\|Adversário\|Data" |
| **Location** | Texto | "home" ou "away" |
| **Year** | Número | Ano do jogo |
| **Month** | Número | Mês do jogo (1-12) |
| **adj** | Número | Campo de ajuste (0 por padrão) |

### Exemplo de Dados

```
Player          | Team            | Date       | Opponent    | Minutes | Goals | Assists | xG    | xA    | SH
----------------|-----------------|------------|-------------|---------|-------|---------|-------|-------|----
Harry Kane      | FC Bayern München | 2025-08-22 | RB Leipzig | 86      | 3     | 0       | 0.75  | 0.08  | 5
Michael Olise   | FC Bayern München | 2025-08-22 | RB Leipzig | 90      | 2     | 0       | 0.36  | 0.35  | 5
Luis Diaz       | FC Bayern München | 2025-08-22 | RB Leipzig | 90      | 1     | 2       | 0.20  | 0.16  | 1
```

## ⚙️ Funcionamento

1. **Acesso à API**: O script faz requisições para a API pública do FotMob
2. **Busca de Jogos**: Filtra os jogos da liga selecionada no período especificado
3. **Extração de Dados**: Para cada jogo, extrai estatísticas de todos os jogadores (ambos os times)
4. **Filtragem**: Remove automaticamente jogadores que não jogaram (0 minutos)
5. **Remoção de Duplicatas**: Remove registros duplicados automaticamente
6. **Ordenação**: Ordena os dados por data
7. **Exportação**: Salva tudo em uma planilha Excel organizada

## 🧪 Validação e Testes

### Validar Extração de Dados

Execute uma extração de teste para verificar se está funcionando:

```bash
python buscar_estatisticas_fotmob.py --liga bundesliga --inicio 2025-08-22 --fim 2025-08-24 --limit 3 --test
```

### Testar Todas as Ligas

Execute extrações rápidas para todas as ligas:

```bash
# O script testa cada liga automaticamente
python3 << 'EOF'
from buscar_estatisticas_fotmob import FotMobScraper, scrape_league_period, FOTMOB_LEAGUE_IDS
import pandas as pd

scraper = FotMobScraper()
start_date = pd.to_datetime('2025-08-22')
end_date = pd.to_datetime('2025-08-24')

for league_key in FOTMOB_LEAGUE_IDS.keys():
    stats = scrape_league_period(league_key, start_date, end_date, scraper, limit_games=1)
    print(f"{league_key}: {len(stats)} registros")
EOF
```

## ⚠️ Importante

- **Rate Limiting**: O script inclui pausas de 1 segundo entre requisições para respeitar a API
- **Dados Disponíveis**: Só busca dados de jogos já finalizados (com estatísticas disponíveis)
- **Período de Dados**: A API do FotMob mantém dados históricos extensos
- **Timezone**: As datas são salvas sem timezone para compatibilidade com Excel
- **Duplicatas**: O script remove automaticamente registros duplicados baseado em Player, Team, Date e Opponent

## 🐛 Solução de Problemas

### O script não encontra dados

1. **Verifique a conexão com a internet**
   ```bash
   ping www.fotmob.com
   ```

2. **Verifique se existem jogos no período**
   - Use `--test` para ver o que está sendo encontrado
   - Use `--limit 1` para testar com apenas 1 jogo

3. **Verifique o código da liga**
   ```bash
   python buscar_estatisticas_fotmob.py --help
   # Veja a lista de ligas disponíveis
   ```

### Erro ao salvar arquivo Excel

- **Verifique permissões**: Certifique-se de ter permissão de escrita no diretório
- **Verifique o caminho**: Se usar caminho absoluto, certifique-se de que o diretório existe
- **Arquivo aberto**: Feche o arquivo Excel se estiver aberto em outro programa

### Erro de conexão com API

- **Timeout**: Aguarde alguns segundos e tente novamente
- **API indisponível**: Verifique o status do site FotMob em `https://www.fotmob.com`
- **Firewall**: Verifique se seu firewall não está bloqueando requisições HTTPS

### Dados parecem incorretos

- **Validação**: Compare alguns registros com o site FotMob manualmente
- **Timezone**: Verifique se as datas estão corretas (podem variar por timezone)
- **Jogos cancelados**: Alguns jogos podem ter sido cancelados ou adiados

## 📝 Estrutura do Projeto

```
BOT_ESTAT_BETS/
├── buscar_estatisticas_fotmob.py    # Script principal - Bot FotMob
├── buscar_estatisticas_multi_liga.py # Script alternativo (FBref - pode ter bloqueios)
├── buscar_estatisticas.py            # Script antigo Premier League (FBref)
├── validar_acesso.py                 # Script para validar acesso a sites
├── testar_alternativas.py            # Script para testar fontes alternativas
├── validar_ligas.py                  # Script de validação automática
├── comparar_dados.py                 # Script de comparação com site
├── README.md                         # Este arquivo (documentação principal)
├── README.txt                        # Documentação em formato texto
├── VALIDACAO_FOTMOB.md              # Documentação de validação
├── SOLUCAO_403.md                   # Documentação sobre problemas 403
├── requirements.txt                  # Dependências Python
└── venv/                            # Ambiente virtual (não commitado)
```

## 🔧 Dependências

Todas as dependências estão listadas em `requirements.txt`:

```
pandas>=2.0.0          # Manipulação de dados
openpyxl>=3.1.0        # Exportação para Excel
requests>=2.31.0       # Requisições HTTP
```

**Nota**: Este bot usa apenas `requests` para acessar a API do FotMob. Não são necessárias bibliotecas de scraping como `beautifulsoup4` ou `cloudscraper`, tornando-o mais leve e confiável.

## 🔄 Comparação com Versão FBref

| Característica | FotMob (Atual) | FBref (Legado) |
|----------------|----------------|----------------|
| **Método** | API oficial | Web scraping |
| **Estabilidade** | ✅ Alta | ⚠️ Bloqueios frequentes |
| **Cloudflare** | ✅ Não aplicável | ❌ Problemas constantes |
| **Velocidade** | ✅ Rápido | ⚠️ Depende de delays |
| **Manutenção** | ✅ Baixa necessidade | ⚠️ Requer ajustes frequentes |
| **Estatísticas SH** | ✅ Disponível | ⚠️ Pode variar |

**Recomendação**: Use `buscar_estatisticas_fotmob.py` como solução principal.

## 📚 Documentação Adicional

- **`VALIDACAO_FOTMOB.md`** - Documentação detalhada da validação realizada
- **`SOLUCAO_403.md`** - Soluções para problemas de bloqueio (FBref)
- **`README.txt`** - Versão texto da documentação

## 📄 Licença

Este projeto é open source e está disponível para uso livre.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

- Abrir issues para reportar bugs ou sugerir melhorias
- Enviar pull requests com correções ou novas funcionalidades
- Melhorar a documentação

## 📧 Suporte

Para questões ou problemas:

1. **Verifique a documentação**: Leia este README e a seção de solução de problemas
2. **Abra uma issue**: [GitHub Issues](https://github.com/chili-guy/BOT_ESTAT_BETS/issues)
3. **Teste com `--test`**: Use o modo teste para diagnóstico

## ✅ Status do Projeto

- ✅ **API FotMob**: Funcionando perfeitamente
- ✅ **Todas as ligas**: Validadas e operacionais
- ✅ **Todas as estatísticas**: Incluindo SH (chutes)
- ✅ **Exportação Excel**: Funcionando corretamente
- ✅ **Validação**: Testes automatizados incluídos

---

**Desenvolvido com ❤️ para facilitar a coleta de estatísticas de futebol**

**Versão**: 2.0 (FotMob API)  
**Última atualização**: Janeiro 2025
