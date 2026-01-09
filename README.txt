================================================================================
  BOT ESTAT BETS - Buscador de Estatísticas de Futebol
================================================================================

Scripts Python para buscar automaticamente estatísticas de jogadores de 
múltiplas ligas europeias do site fbref.com.

================================================================================
  LIGAS SUPORTADAS
================================================================================

- Premier League (Inglaterra) - buscar_estatisticas.py
- La Liga (Espanha) - buscar_estatisticas_multi_liga.py
- Bundesliga (Alemanha) - buscar_estatisticas_multi_liga.py
- Serie A (Itália) - buscar_estatisticas_multi_liga.py
- Primeira Liga (Portugal) - buscar_estatisticas_multi_liga.py
- Ligue 1 (França) - buscar_estatisticas_multi_liga.py
- Championship (Inglaterra - Série B) - buscar_estatisticas_multi_liga.py

================================================================================
  ESTATÍSTICAS COLETADAS
================================================================================

O script busca as seguintes informações para cada jogador em cada partida:

- MINUTES: Minutos jogados
- GOALS: Gols marcados  
- ASSISTS: Assistências
- xG: Expected Goals (até 4 casas decimais)
- xA: Expected Assists (até 4 casas decimais)

================================================================================
  INSTALAÇÃO
================================================================================

1. PRÉ-REQUISITOS
   - Python 3.8 ou superior
   - pip (gerenciador de pacotes Python)

2. CLONAR O REPOSITÓRIO

   git clone https://github.com/chili-guy/BOT_ESTAT_BETS.git
   cd BOT_ESTAT_BETS

3. CRIAR AMBIENTE VIRTUAL (RECOMENDADO)

   # Criar ambiente virtual
   python3 -m venv venv

   # Ativar ambiente virtual
   # Linux/Mac:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate

4. INSTALAR DEPENDÊNCIAS

   pip install -r requirements.txt

================================================================================
  COMO USAR
================================================================================

SCRIPT 1: PREMIER LEAGUE (buscar_estatisticas.py)

USO BÁSICO:

   python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31

SCRIPT 2: MÚLTIPLAS LIGAS (buscar_estatisticas_multi_liga.py)

USO BÁSICO:

   python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30

PARÂMETROS DISPONÍVEIS (Premier League):

   --inicio    Data de início (YYYY-MM-DD)      OBRIGATÓRIO
               Exemplo: --inicio 2025-10-01

   --fim       Data de fim (YYYY-MM-DD)         OBRIGATÓRIO
               Exemplo: --fim 2025-10-31

   --output    Arquivo Excel de saída           OPCIONAL
               Padrão: premier.xlsx
               Exemplo: --output resultado.xlsx

   --limit     Limitar número de jogos          OPCIONAL
               Exemplo: --limit 10

   --test      Modo teste (não salva arquivo)   OPCIONAL
               Exemplo: --test

PARÂMETROS DISPONÍVEIS (Múltiplas Ligas):

   --liga      Liga a buscar                    OBRIGATÓRIO
               Opções: laliga, bundesliga, seriea, portugal, ligue1, championship
               Exemplo: --liga laliga

   --inicio    Data de início (YYYY-MM-DD)      OBRIGATÓRIO
               Exemplo: --inicio 2025-09-01

   --fim       Data de fim (YYYY-MM-DD)         OBRIGATÓRIO
               Exemplo: --fim 2025-09-30

   --output    Arquivo Excel de saída           OPCIONAL
               Padrão: {liga}_{datas}.xlsx
               Exemplo: --output minha_planilha.xlsx

   --limit     Limitar número de jogos          OPCIONAL
               Exemplo: --limit 10

   --test      Modo teste (não salva arquivo)   OPCIONAL
               Exemplo: --test

EXEMPLOS DE USO - PREMIER LEAGUE:

1. Buscar dados de um mês específico:
   
   python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31

2. Modo teste (não salva, apenas mostra resultados):
   
   python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --test

3. Limitar número de jogos (útil para testes):
   
   python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --limit 3 --test

EXEMPLOS DE USO - MÚLTIPLAS LIGAS:

1. La Liga (Espanha):
   
   python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30

2. Bundesliga (Alemanha):
   
   python buscar_estatisticas_multi_liga.py --liga bundesliga --inicio 2025-09-01 --fim 2025-09-30

3. Serie A (Itália):
   
   python buscar_estatisticas_multi_liga.py --liga seriea --inicio 2025-09-01 --fim 2025-09-30

4. Primeira Liga (Portugal):
   
   python buscar_estatisticas_multi_liga.py --liga portugal --inicio 2025-09-01 --fim 2025-09-30

5. Ligue 1 (França):
   
   python buscar_estatisticas_multi_liga.py --liga ligue1 --inicio 2025-09-01 --fim 2025-09-30

6. Championship (Inglaterra Série B):
   
   python buscar_estatisticas_multi_liga.py --liga championship --inicio 2025-09-01 --fim 2025-09-30

7. Modo teste e limitar jogos:
   
   python buscar_estatisticas_multi_liga.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30 --limit 1 --test

VER AJUDA COMPLETA:

   python buscar_estatisticas.py --help
   python buscar_estatisticas_multi_liga.py --help

================================================================================
  VALIDAÇÃO DE DADOS
================================================================================

SCRIPT DE VALIDAÇÃO AUTOMÁTICA:

   python validar_ligas.py

Este script testa todas as ligas automaticamente para garantir que estão 
funcionando corretamente.

COMPARAÇÃO COM O SITE:

   python comparar_dados.py

Este script compara os dados extraídos com os dados do site fbref.com para 
garantir precisão.

TODOS OS SCRIPTS FORAM VALIDADOS E ESTÃO FUNCIONANDO CORRETAMENTE!

================================================================================
  ESTRUTURA DOS DADOS
================================================================================

A planilha gerada contém as seguintes colunas principais:

- Player: Nome do jogador
- Team: Time do jogador
- Date: Data do jogo
- Opponent: Time adversário
- Minutes: Minutos jogados
- Goals: Gols marcados
- Assists: Assistências
- xG: Expected Goals (4 casas decimais)
- xA: Expected Assists (4 casas decimais)
- Confronto: Formato "Time|Adversário|Data"
- Location: Local do jogo (home/away)
- Year: Ano do jogo
- Month: Mês do jogo

================================================================================
  FUNCIONAMENTO
================================================================================

1. O script acessa o site fbref.com
2. Busca os jogos no período especificado
3. Para cada jogo, extrai estatísticas de todos os jogadores (ambos os times)
4. Filtra automaticamente linhas de subtotal/agregado (990 minutos)
5. Remove duplicatas automaticamente
6. Ordena por data
7. Salva na planilha Excel especificada

================================================================================
  IMPORTANTE
================================================================================

- Rate Limiting: O script inclui pausas entre requisições para respeitar o site
- Dados Disponíveis: Só busca dados de jogos já jogados (com placar)
- Jogos Futuros: Jogos que ainda não foram jogados são automaticamente pulados
- Estrutura do Site: Se o fbref.com mudar sua estrutura HTML, o script pode 
  precisar de ajustes

================================================================================
  SOLUÇÃO DE PROBLEMAS
================================================================================

O SCRIPT NÃO ENCONTRA DADOS:

1. Verifique sua conexão com a internet
2. Verifique se os dados estão disponíveis no site fbref.com
3. Use --test para ver o que está sendo encontrado
4. Use --limit 1 para testar com apenas 1 jogo

ERRO AO SALVAR ARQUIVO:

- Verifique se tem permissão de escrita no diretório
- Verifique se o caminho do arquivo está correto
- Se usar caminho absoluto, certifique-se de que o diretório existe 
  (ou será criado automaticamente)

RATE LIMIT (429):

- O script aguarda automaticamente quando recebe rate limit
- Aguarde alguns minutos e tente novamente
- Considere usar --limit para processar menos jogos por vez

================================================================================
  ESTRUTURA DO PROJETO
================================================================================

BOT_ESTAT_BETS/
├── buscar_estatisticas.py          Script principal - Premier League
├── buscar_estatisticas_multi_liga.py  Script principal - Múltiplas Ligas
├── validar_ligas.py                 Script de validação automática
├── comparar_dados.py                Script de comparação com site
├── README.txt                       Este arquivo
├── README.md                        Documentação em Markdown
├── README_MULTI_LIGA.md            Documentação detalhada multi-liga
├── requirements.txt                 Dependências Python
└── venv/                            Ambiente virtual (não commitado)

================================================================================
  DEPENDÊNCIAS
================================================================================

- pandas >= 2.0.0
- openpyxl >= 3.1.0
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- cloudscraper >= 1.2.0

================================================================================
  LICENÇA
================================================================================

Este projeto é open source e está disponível para uso livre.

================================================================================
  CONTRIBUINDO
================================================================================

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

================================================================================
  SUPORTE
================================================================================

Para questões ou problemas, abra uma issue no repositório GitHub:
https://github.com/chili-guy/BOT_ESTAT_BETS

================================================================================

Desenvolvido com ❤️ para facilitar a coleta de estatísticas de futebol

Para mais detalhes sobre o script de múltiplas ligas, consulte README_MULTI_LIGA.md

================================================================================



