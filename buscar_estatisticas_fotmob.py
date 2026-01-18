#!/usr/bin/env python3
"""
Script para buscar estatísticas usando FotMob API (alternativa ao FBref)
Busca: MINUTES, GOALS, ASSISTS, XG, XA
"""

import requests
import pandas as pd
import time
from datetime import datetime
import argparse
import sys
import json

# IDs das ligas no FotMob
FOTMOB_LEAGUE_IDS = {
    'premier': {'id': 47, 'name': 'Premier League', 'country': 'Inglaterra'},
    'laliga': {'id': 87, 'name': 'La Liga', 'country': 'Espanha'},
    'bundesliga': {'id': 54, 'name': 'Bundesliga', 'country': 'Alemanha'},
    'seriea': {'id': 55, 'name': 'Serie A', 'country': 'Itália'},
    'ligue1': {'id': 53, 'name': 'Ligue 1', 'country': 'França'},
    'portugal': {'id': 48, 'name': 'Primeira Liga', 'country': 'Portugal'},
    'championship': {'id': 50, 'name': 'Championship', 'country': 'Inglaterra (Série B)'},
}

class FotMobScraper:
    """Scraper para buscar dados do FotMob API"""
    
    def __init__(self):
        self.base_url = "https://www.fotmob.com/api"
        self.session = requests.Session()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.fotmob.com/'
        }
        self.session.headers.update(headers)
    
    def get_league_matches(self, league_id, season=None):
        """Busca jogos de uma liga"""
        url = f"{self.base_url}/leagues?id={league_id}&type=league"
        
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            if 'fixtures' in data and 'allMatches' in data['fixtures']:
                matches = data['fixtures']['allMatches']
                return matches
            return []
            
        except Exception as e:
            print(f"  ❌ Erro ao buscar jogos: {e}")
            return []
    
    def get_match_details(self, match_id):
        """Busca detalhes de um jogo específico"""
        url = f"{self.base_url}/matchDetails?matchId={match_id}"
        
        try:
            time.sleep(1)  # Rate limiting
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"    ❌ Erro ao buscar detalhes do jogo {match_id}: {e}")
            return None
    
    def extract_player_stats(self, match_data, match_date, home_team, away_team):
        """Extrai estatísticas de jogadores de um jogo"""
        player_stats = []
        
        if 'content' not in match_data or 'playerStats' not in match_data['content']:
            return []
        
        player_stats_data = match_data['content']['playerStats']
        
        # Obter times
        teams = {}
        for player_id, player_data in player_stats_data.items():
            team_id = player_data.get('teamId')
            team_name = player_data.get('teamName', '')
            if team_id and team_id not in teams:
                teams[team_id] = team_name
        
        # Determinar qual time é home e away
        team_names = list(teams.values())
        if len(team_names) == 2:
            actual_home = team_names[0]
            actual_away = team_names[1]
        else:
            actual_home = home_team
            actual_away = away_team
        
        # Extrair estatísticas de cada jogador
        for player_id, player_data in player_stats_data.items():
            player_name = player_data.get('name', '')
            team_name = player_data.get('teamName', '')
            
            if not player_name:
                continue
            
            # Determinar se é home ou away
            location = 'home' if team_name == actual_home else 'away'
            opponent = actual_away if location == 'home' else actual_home
            
            # Inicializar estatísticas
            minutes = 0
            goals = 0
            assists = 0
            xg = 0.0
            xa = 0.0
            
            # Extrair do array stats
            if 'stats' in player_data and isinstance(player_data['stats'], list):
                for stat_group in player_data['stats']:
                    if isinstance(stat_group, dict) and 'stats' in stat_group:
                        stats_dict = stat_group['stats']
                        
                        # Procurar cada estatística
                        for stat_key, stat_value in stats_dict.items():
                            if isinstance(stat_value, dict) and 'stat' in stat_value:
                                stat_info = stat_value['stat']
                                if isinstance(stat_info, dict) and 'value' in stat_info:
                                    value = stat_info['value']
                                    key_lower = stat_key.lower()
                                    
                                    if 'minute' in key_lower:
                                        try:
                                            minutes = int(float(value))
                                        except:
                                            minutes = 0
                                    elif 'goal' in key_lower and 'xg' not in key_lower and 'expected' not in key_lower:
                                        try:
                                            goals = int(float(value))
                                        except:
                                            goals = 0
                                    elif 'assist' in key_lower and 'xa' not in key_lower and 'expected' not in key_lower:
                                        try:
                                            assists = int(float(value))
                                        except:
                                            assists = 0
                                    elif 'xg' in key_lower or 'expectedgoal' in key_lower:
                                        try:
                                            xg = float(value)
                                        except:
                                            xg = 0.0
                                    elif 'xa' in key_lower or 'expectedassist' in key_lower:
                                        try:
                                            xa = float(value)
                                        except:
                                            xa = 0.0
            
            # Filtrar jogadores sem minutos (não jogaram)
            if minutes == 0:
                continue
            
            # Remover timezone da data para Excel
            if hasattr(match_date, 'tz_localize') and match_date.tz is not None:
                match_date_naive = match_date.tz_localize(None)
            else:
                match_date_naive = match_date
            
            stats = {
                'Player': player_name,
                'Team': team_name,
                'Date': match_date_naive,
                'Opponent': opponent,
                'Minutes': minutes,
                'Goals': goals,
                'Assists': assists,
                'xG': round(xg, 4) if xg else 0.0,
                'xA': round(xa, 4) if xa else 0.0,
                'Confronto': f"{team_name}|{opponent}|{match_date_naive.strftime('%Y-%m-%d')}",
                'Location': location,
                'Year': match_date_naive.year,
                'Month': match_date_naive.month,
                'adj': 0
            }
            player_stats.append(stats)
        
        return player_stats


def scrape_league_period(league_key, start_date, end_date, scraper, limit_games=None):
    """Busca estatísticas de um período específico"""
    if league_key not in FOTMOB_LEAGUE_IDS:
        print(f"❌ Liga '{league_key}' não suportada")
        return []
    
    league_info = FOTMOB_LEAGUE_IDS[league_key]
    league_id = league_info['id']
    league_name = league_info['name']
    
    print(f"\n📊 Buscando jogos da {league_name}...")
    
    # Buscar todos os jogos da liga
    matches = scraper.get_league_matches(league_id)
    
    if not matches:
        print("  ❌ Nenhum jogo encontrado")
        return []
    
    print(f"  ✅ Encontrados {len(matches)} jogos")
    
    # Filtrar jogos por data
    filtered_matches = []
    for match in matches:
        try:
            # Tentar extrair data do jogo
            if 'status' in match and 'utcTime' in match['status']:
                match_time_str = match['status']['utcTime']
                # utcTime pode ser string ISO ou timestamp
                if isinstance(match_time_str, str):
                    match_date = pd.to_datetime(match_time_str)
                else:
                    match_date = datetime.fromtimestamp(match_time_str / 1000)
                
                # Normalizar para comparar apenas a data (sem hora)
                match_date_normalized = match_date.normalize() if hasattr(match_date, 'normalize') else match_date.replace(hour=0, minute=0, second=0, microsecond=0)
                start_normalized = start_date.normalize() if hasattr(start_date, 'normalize') else start_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_normalized = end_date.normalize() if hasattr(end_date, 'normalize') else end_date.replace(hour=0, minute=0, second=0, microsecond=0)
                
                # Se match_date é timezone-aware, converter para naive
                if hasattr(match_date_normalized, 'tz_localize') and match_date_normalized.tz is not None:
                    match_date_normalized = match_date_normalized.tz_localize(None)
                
                if start_normalized <= match_date_normalized <= end_normalized:
                    filtered_matches.append(match)
        except Exception as e:
            continue
    
    print(f"  📅 {len(filtered_matches)} jogos no período {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}")
    
    if limit_games:
        filtered_matches = filtered_matches[:limit_games]
        print(f"  ⚠️  Limitando a {limit_games} jogos")
    
    all_player_stats = []
    
    for i, match in enumerate(filtered_matches, 1):
        match_id = match.get('id')
        home_team = match.get('home', {}).get('name', '')
        away_team = match.get('away', {}).get('name', '')
        
        try:
            match_time_str = match['status']['utcTime']
            if isinstance(match_time_str, str):
                match_date = pd.to_datetime(match_time_str)
            else:
                match_date = datetime.fromtimestamp(match_time_str / 1000)
        except:
            continue
        
        print(f"\n  [{i}/{len(filtered_matches)}] Processando: {home_team} vs {away_team} ({match_date.strftime('%Y-%m-%d')})")
        
        # Buscar detalhes do jogo
        match_data = scraper.get_match_details(match_id)
        
        if not match_data:
            print(f"    ⚠️  Não foi possível obter dados do jogo")
            continue
        
        # Extrair estatísticas
        player_stats = scraper.extract_player_stats(match_data, match_date, home_team, away_team)
        
        if player_stats:
            print(f"    ✅ {len(player_stats)} jogadores processados")
            all_player_stats.extend(player_stats)
        else:
            print(f"    ⚠️  Nenhuma estatística encontrada")
    
    return all_player_stats


def main():
    parser = argparse.ArgumentParser(
        description='Busca estatísticas usando FotMob API (MINUTES, GOALS, ASSISTS, XG, XA)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ligas disponíveis:
  --liga premier       Premier League
  --liga laliga        La Liga
  --liga bundesliga    Bundesliga
  --liga seriea        Serie A
  --liga ligue1        Ligue 1
  --liga portugal      Primeira Liga
  --liga championship  Championship

Exemplos:
  python buscar_estatisticas_fotmob.py --liga bundesliga --inicio 2024-09-01 --fim 2024-09-30
  python buscar_estatisticas_fotmob.py --liga bundesliga --inicio 2024-09-01 --fim 2024-09-30 --limit 5 --test
        """
    )
    
    parser.add_argument('--liga', type=str, required=True,
                       choices=list(FOTMOB_LEAGUE_IDS.keys()),
                       help='Liga a buscar')
    parser.add_argument('--inicio', type=str, required=True,
                       help='Data de início (YYYY-MM-DD)')
    parser.add_argument('--fim', type=str, required=True,
                       help='Data de fim (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, default=None,
                       help='Arquivo Excel de saída')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limitar número de jogos')
    parser.add_argument('--test', action='store_true',
                       help='Modo teste - não salva arquivo')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔍 BUSCADOR DE ESTATÍSTICAS - FOTMOB API")
    print("="*70)
    print(f"Liga: {FOTMOB_LEAGUE_IDS[args.liga]['name']}")
    print(f"Período: {args.inicio} até {args.fim}")
    print(f"Modo: {'TESTE' if args.test else 'PRODUÇÃO'}")
    print("="*70)
    
    try:
        start_date = pd.to_datetime(args.inicio)
        end_date = pd.to_datetime(args.fim)
    except:
        print("❌ Erro: Datas inválidas. Use formato YYYY-MM-DD")
        sys.exit(1)
    
    scraper = FotMobScraper()
    
    # Buscar dados
    print("\n🚀 Iniciando busca...")
    all_stats = scrape_league_period(args.liga, start_date, end_date, scraper, args.limit)
    
    if not all_stats:
        print("\n⚠️  Nenhum dado foi encontrado.")
        sys.exit(1)
    
    # Criar DataFrame
    df = pd.DataFrame(all_stats)
    
    # Remover duplicatas
    initial_count = len(df)
    df = df.drop_duplicates(subset=['Player', 'Team', 'Date', 'Opponent'], keep='first')
    duplicates_removed = initial_count - len(df)
    
    if duplicates_removed > 0:
        print(f"\n🧹 Removidas {duplicates_removed} duplicatas")
    
    # Ordenar por data
    df = df.sort_values('Date').reset_index(drop=True)
    
    print(f"\n✅ Total: {len(df)} registros de jogadores")
    
    if args.test:
        print("\n🧪 MODO TESTE - Primeiras linhas:")
        print(df.head(10).to_string())
        print(f"\n📊 Resumo:")
        print(f"  - Jogadores únicos: {df['Player'].nunique()}")
        print(f"  - Jogos: {df['Date'].nunique()}")
        print(f"  - Período: {df['Date'].min()} até {df['Date'].max()}")
    else:
        # Salvar em Excel
        if args.output:
            output_file = args.output
        else:
            league_name = args.liga
            output_file = f"{league_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}_fotmob.xlsx"
        
        df.to_excel(output_file, index=False)
        print(f"\n💾 Dados salvos em: {output_file}")


if __name__ == "__main__":
    main()

