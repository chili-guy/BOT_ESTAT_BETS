================================================================================
  BOT ESTAT BETS - Buscador de Estatísticas de Futebol via FotMob API
================================================================================

Script Python para buscar automaticamente estatísticas detalhadas de 
jogadores de múltiplas ligas europeias usando a FotMob API - uma alternativa 
confiável e estável ao scraping de sites.

================================================================================
  CARACTERÍSTICAS PRINCIPAIS
================================================================================

✅ API Oficial: Utiliza a API pública do FotMob (mais estável que scraping)
✅ Sem Bloqueios: Não sofre com proteções Cloudflare ou bloqueios 403
✅ 7 Ligas Principais: Premier League, La Liga, Bundesliga, Serie A, 
   Ligue 1, Primeira Liga e Championship
✅ Estatísticas Completas: Minutes, Goals, Assists, xG, xA e SH (Total de Chutes)
✅ Exportação Excel: Dados organizados em planilhas prontas para análise
✅ Filtro por Período: Busque dados de qualquer intervalo de datas
✅ Validação Automática: Scripts de teste incluídos

================================================================================
  LIGAS SUPORTADAS
================================================================================

| Liga              | Código        | País                    |
|-------------------|---------------|-------------------------|
| Premier League    | premier       | Inglaterra              |
| La Liga           | laliga        | Espanha                 |
| Bundesliga        | bundesliga    | Alemanha                |
| Serie A           | seriea        | Itália                  |
| Ligue 1           | ligue1        | França                  |
| Primeira Liga     | portugal      | Portugal                |
| Championship      | championship  | Inglaterra (Série B)    |

================================================================================
  ESTATÍSTICAS COLETADAS
================================================================================

O script busca as seguintes informações para cada jogador em cada partida:

- MINUTES: Minutos jogados no jogo
- GOALS: Gols marcados
- ASSISTS: Assistências concedidas
- xG: Expected Goals (até 4 casas decimais)
- xA: Expected Assists (até 4 casas decimais)
- SH: Total de chutes (shots) realizados

DADOS ADICIONAIS INCLUÍDOS:

- Player: Nome do jogador
- Team: Time do jogador
- Date: Data do jogo
- Opponent: Time adversário
- Location: Local do jogo (home/away)
- Confronto: Formato "Time|Adversário|Data"
- Year: Ano do jogo
- Month: Mês do jogo
- adj: Campo de ajuste (0 por padrão)

================================================================================
  INSTALAÇÃO
================================================================================

1. PRÉ-REQUISITOS

   - Python 3.8 ou superior
   - pip (gerenciador de pacotes Python)
   - Conexão com internet

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

   As dependências principais são:
   - pandas >= 2.0.0        Manipulação de dados
   - openpyxl >= 3.1.0      Exportação para Excel
   - requests >= 2.31.0     Requisições HTTP

================================================================================
  COMO USAR
================================================================================

USO BÁSICO:

   python buscar_estatisticas_fotmob.py --liga <LIGA> --inicio <DATA_INICIO> --fim <DATA_FIM>

PARÂMETROS DISPONÍVEIS:

   --liga      Liga a buscar                    OBRIGATÓRIO
               Opções: premier, laliga, bundesliga, seriea, ligue1, 
                       portugal, championship
               Exemplo: --liga bundesliga

   --inicio    Data de início (YYYY-MM-DD)      OBRIGATÓRIO
               Exemplo: --inicio 2025-08-01

   --fim       Data de fim (YYYY-MM-DD)         OBRIGATÓRIO
               Exemplo: --fim 2025-08-31

   --output    Arquivo Excel de saída           OPCIONAL
               Padrão: {liga}_{datas}.xlsx
               Exemplo: --output resultado.xlsx

   --limit     Limitar número de jogos          OPCIONAL
               Exemplo: --limit 10

   --test      Modo teste (não salva arquivo)   OPCIONAL
               Exemplo: --test

================================================================================
  EXEMPLOS DE USO
================================================================================

1. BUSCAR DADOS DA BUNDESLIGA DE UM MÊS:

   python buscar_estatisticas_fotmob.py --liga bundesliga --inicio 2025-08-01 --fim 2025-08-31

   Resultado: Arquivo bundesliga_2025-08-01_2025-08-31.xlsx será criado.

2. PREMIER LEAGUE COM ARQUIVO PERSONALIZADO:

   python buscar_estatisticas_fotmob.py --liga premier --inicio 2025-09-01 --fim 2025-09-30 --output premier_setembro.xlsx

3. MODO TESTE (NÃO SALVA, APENAS MOSTRA RESULTADOS):

   python buscar_estatisticas_fotmob.py --liga laliga --inicio 2025-08-22 --fim 2025-08-24 --test

4. LIMITAR NÚMERO DE JOGOS (ÚTIL PARA TESTES RÁPIDOS):

   python buscar_estatisticas_fotmob.py --liga seriea --inicio 2025-08-01 --fim 2025-08-31 --limit 3 --test

5. LA LIGA (ESPANHA):

   python buscar_estatisticas_fotmob.py --liga laliga --inicio 2025-09-01 --fim 2025-09-30

6. SERIE A (ITÁLIA):

   python buscar_estatisticas_fotmob.py --liga seriea --inicio 2025-09-01 --fim 2025-09-30

7. LIGUE 1 (FRANÇA):

   python buscar_estatisticas_fotmob.py --liga ligue1 --inicio 2025-09-01 --fim 2025-09-30

8. PRIMEIRA LIGA (PORTUGAL):

   python buscar_estatisticas_fotmob.py --liga portugal --inicio 2025-09-01 --fim 2025-09-30

9. CHAMPIONSHIP (INGLATERRA - SÉRIE B):

   python buscar_estatisticas_fotmob.py --liga championship --inicio 2025-09-01 --fim 2025-09-30

VER AJUDA COMPLETA:

   python buscar_estatisticas_fotmob.py --help

================================================================================
  ESTRUTURA DOS DADOS DE SAÍDA
================================================================================

A planilha Excel gerada contém as seguintes colunas:

- Player: Nome completo do jogador
- Team: Nome do time
- Date: Data do jogo (YYYY-MM-DD)
- Opponent: Time adversário
- Minutes: Minutos jogados
- Goals: Gols marcados
- Assists: Assistências
- xG: Expected Goals (4 casas decimais)
- xA: Expected Assists (4 casas decimais)
- SH: Total de chutes realizados
- Confronto: Formato "Time|Adversário|Data"
- Location: "home" ou "away"
- Year: Ano do jogo
- Month: Mês do jogo (1-12)
- adj: Campo de ajuste (0 por padrão)

================================================================================
  FUNCIONAMENTO
================================================================================

1. Acesso à API: O script faz requisições para a API pública do FotMob
2. Busca de Jogos: Filtra os jogos da liga selecionada no período especificado
3. Extração de Dados: Para cada jogo, extrai estatísticas de todos os 
   jogadores (ambos os times)
4. Filtragem: Remove automaticamente jogadores que não jogaram (0 minutos)
5. Remoção de Duplicatas: Remove registros duplicados automaticamente
6. Ordenação: Ordena os dados por data
7. Exportação: Salva tudo em uma planilha Excel organizada

================================================================================
  VALIDAÇÃO E TESTES
================================================================================

VALIDAR EXTRAÇÃO DE DADOS:

   python buscar_estatisticas_fotmob.py --liga bundesliga --inicio 2025-08-22 --fim 2025-08-24 --limit 3 --test

TESTAR TODAS AS LIGAS:

   Execute uma extração rápida para cada liga usando o modo --limit 1 --test

================================================================================
  IMPORTANTE
================================================================================

- Rate Limiting: O script inclui pausas de 1 segundo entre requisições para 
  respeitar a API
- Dados Disponíveis: Só busca dados de jogos já finalizados (com estatísticas 
  disponíveis)
- Período de Dados: A API do FotMob mantém dados históricos extensos
- Timezone: As datas são salvas sem timezone para compatibilidade com Excel
- Duplicatas: O script remove automaticamente registros duplicados baseado em 
  Player, Team, Date e Opponent

================================================================================
  SOLUÇÃO DE PROBLEMAS
================================================================================

O SCRIPT NÃO ENCONTRA DADOS:

1. Verifique a conexão com a internet
   ping www.fotmob.com

2. Verifique se existem jogos no período
   - Use --test para ver o que está sendo encontrado
   - Use --limit 1 para testar com apenas 1 jogo

3. Verifique o código da liga
   python buscar_estatisticas_fotmob.py --help

ERRO AO SALVAR ARQUIVO EXCEL:

- Verifique permissões: Certifique-se de ter permissão de escrita no diretório
- Verifique o caminho: Se usar caminho absoluto, certifique-se de que o 
  diretório existe
- Arquivo aberto: Feche o arquivo Excel se estiver aberto em outro programa

ERRO DE CONEXÃO COM API:

- Timeout: Aguarde alguns segundos e tente novamente
- API indisponível: Verifique o status do site FotMob em 
  https://www.fotmob.com
- Firewall: Verifique se seu firewall não está bloqueando requisições HTTPS

DADOS PARECEM INCORRETOS:

- Validação: Compare alguns registros com o site FotMob manualmente
- Timezone: Verifique se as datas estão corretas (podem variar por timezone)
- Jogos cancelados: Alguns jogos podem ter sido cancelados ou adiados

================================================================================
  ESTRUTURA DO PROJETO
================================================================================

BOT_ESTAT_BETS/
├── buscar_estatisticas_fotmob.py    Script principal - Bot FotMob
├── buscar_estatisticas_multi_liga.py Script alternativo (FBref)
├── buscar_estatisticas.py            Script antigo Premier League (FBref)
├── validar_acesso.py                 Script para validar acesso a sites
├── testar_alternativas.py            Script para testar fontes alternativas
├── validar_ligas.py                  Script de validação automática
├── comparar_dados.py                 Script de comparação com site
├── README.md                         Documentação principal (Markdown)
├── README.txt                        Este arquivo (texto)
├── VALIDACAO_FOTMOB.md              Documentação de validação
├── SOLUCAO_403.md                   Documentação sobre problemas 403
├── requirements.txt                  Dependências Python
└── venv/                            Ambiente virtual (não commitado)

================================================================================
  DEPENDÊNCIAS
================================================================================

Todas as dependências estão listadas em requirements.txt:

pandas>=2.0.0          # Manipulação de dados
openpyxl>=3.1.0        # Exportação para Excel
requests>=2.31.0       # Requisições HTTP

NOTA: Este bot usa apenas requests para acessar a API do FotMob. Não são 
necessárias bibliotecas de scraping como beautifulsoup4 ou cloudscraper, 
tornando-o mais leve e confiável.

================================================================================
  COMPARAÇÃO COM VERSÃO FBREF
================================================================================

Característica       FotMob (Atual)        FBref (Legado)
-------------------  -------------------   -------------------
Método               API oficial           Web scraping
Estabilidade         ✅ Alta               ⚠️ Bloqueios frequentes
Cloudflare           ✅ Não aplicável      ❌ Problemas constantes
Velocidade           ✅ Rápido             ⚠️ Depende de delays
Manutenção           ✅ Baixa necessidade  ⚠️ Requer ajustes frequentes
Estatísticas SH      ✅ Disponível         ⚠️ Pode variar

RECOMENDAÇÃO: Use buscar_estatisticas_fotmob.py como solução principal.

================================================================================
  DOCUMENTAÇÃO ADICIONAL
================================================================================

- VALIDACAO_FOTMOB.md: Documentação detalhada da validação realizada
- SOLUCAO_403.md: Soluções para problemas de bloqueio (FBref)
- README.md: Versão Markdown completa da documentação

================================================================================
  LICENÇA
================================================================================

Este projeto é open source e está disponível para uso livre.

================================================================================
  CONTRIBUINDO
================================================================================

Contribuições são bem-vindas! Sinta-se livre para:

- Abrir issues para reportar bugs ou sugerir melhorias
- Enviar pull requests com correções ou novas funcionalidades
- Melhorar a documentação

================================================================================
  SUPORTE
================================================================================

Para questões ou problemas:

1. Verifique a documentação: Leia este README e a seção de solução de problemas
2. Abra uma issue: https://github.com/chili-guy/BOT_ESTAT_BETS/issues
3. Teste com --test: Use o modo teste para diagnóstico

================================================================================
  STATUS DO PROJETO
================================================================================

✅ API FotMob: Funcionando perfeitamente
✅ Todas as ligas: Validadas e operacionais
✅ Todas as estatísticas: Incluindo SH (chutes)
✅ Exportação Excel: Funcionando corretamente
✅ Validação: Testes automatizados incluídos

================================================================================

Desenvolvido com ❤️ para facilitar a coleta de estatísticas de futebol

Versão: 2.0 (FotMob API)
Última atualização: Janeiro 2025

================================================================================
