#!/usr/bin/env python3
"""
Script para buscar estatísticas usando Understat como alternativa ao FBref
Understat fornece dados xG/xA para várias ligas europeias
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import json
from datetime import datetime
import argparse
import sys

class UnderstatScraper:
    """Scraper para buscar dados do Understat"""
    
    def __init__(self):
        self.base_url = "https://understat.com"
        self.session = requests.Session()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        self.session.headers.update(headers)
        
        # Mapeamento de ligas
        self.leagues = {
            'premier': {'name': 'Premier League', 'id': 'EPL', 'url': 'EPL'},
            'laliga': {'name': 'La Liga', 'id': 'La_liga', 'url': 'La_liga'},
            'bundesliga': {'name': 'Bundesliga', 'id': 'Bundesliga', 'url': 'Bundesliga'},
            'seriea': {'name': 'Serie A', 'id': 'Serie_A', 'url': 'Serie_A'},
            'ligue1': {'name': 'Ligue 1', 'id': 'Ligue_1', 'url': 'Ligue_1'},
        }
    
    def get_matches(self, league_key, season):
        """Busca jogos de uma liga e temporada"""
        if league_key not in self.leagues:
            print(f"❌ Liga '{league_key}' não suportada pelo Understat")
            return []
        
        league = self.leagues[league_key]
        url = f"{self.base_url}/league/{league['url']}/{season}"
        
        print(f"  🔄 Acessando: {url}")
        
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            
            # Understat usa JavaScript para carregar dados, então precisamos extrair do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procurar por scripts que contêm dados JSON
            scripts = soup.find_all('script')
            matches_data = None
            
            for script in scripts:
                if script.string and 'datesData' in script.string:
                    # Extrair dados JSON do script
                    match = re.search(r'datesData\s*=\s*JSON\.parse\(\'(.+?)\'\)', script.string)
                    if match:
                        try:
                            json_str = match.group(1).replace('\\', '')
                            matches_data = json.loads(json_str)
                            break
                        except:
                            pass
            
            if not matches_data:
                print("  ⚠️  Não foi possível extrair dados do Understat")
                print("  💡 Understat carrega dados via JavaScript, pode precisar de Selenium")
                return []
            
            print(f"  ✅ Encontrados dados de {len(matches_data)} jogos")
            return matches_data
            
        except Exception as e:
            print(f"  ❌ Erro ao buscar jogos: {e}")
            return []
    
    def get_match_stats(self, match_id):
        """Busca estatísticas de um jogo específico"""
        url = f"{self.base_url}/match/{match_id}"
        
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            scripts = soup.find_all('script')
            
            # Procurar dados dos jogadores
            players_data = None
            
            for script in scripts:
                if script.string and 'shotsData' in script.string:
                    # Extrair dados dos jogadores
                    match = re.search(r'playersData\s*=\s*JSON\.parse\(\'(.+?)\'\)', script.string)
                    if match:
                        try:
                            json_str = match.group(1).replace('\\', '')
                            players_data = json.loads(json_str)
                            break
                        except:
                            pass
            
            return players_data
            
        except Exception as e:
            print(f"  ❌ Erro ao buscar estatísticas do jogo: {e}")
            return None

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Busca estatísticas usando Understat (alternativa ao FBref)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ligas disponíveis (Understat):
  --liga premier     Premier League
  --liga laliga      La Liga
  --liga bundesliga  Bundesliga
  --liga seriea      Serie A
  --liga ligue1      Ligue 1

Exemplo:
  python buscar_estatisticas_understat.py --liga bundesliga --season 2024
        """
    )
    
    parser.add_argument('--liga', type=str, required=True,
                       choices=['premier', 'laliga', 'bundesliga', 'seriea', 'ligue1'],
                       help='Liga a buscar')
    parser.add_argument('--season', type=str, default='2024',
                       help='Temporada (ex: 2024 para 2023-2024)')
    parser.add_argument('--test', action='store_true',
                       help='Modo teste - não salva arquivo')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔍 BUSCADOR DE ESTATÍSTICAS - UNDERSTAT")
    print("="*70)
    print(f"Liga: {args.liga}")
    print(f"Temporada: {args.season}")
    print(f"Modo: {'TESTE' if args.test else 'PRODUÇÃO'}")
    print("="*70)
    
    scraper = UnderstatScraper()
    
    # Testar acesso
    print("\n🔧 Testando acesso ao Understat...")
    try:
        response = scraper.session.get(scraper.base_url, timeout=15)
        if response.status_code == 200:
            print("  ✅ Understat está acessível!")
        else:
            print(f"  ❌ Status: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"  ❌ Erro ao acessar Understat: {e}")
        sys.exit(1)
    
    # Buscar jogos
    print(f"\n📊 Buscando jogos da {scraper.leagues[args.liga]['name']}...")
    matches = scraper.get_matches(args.liga, args.season)
    
    if not matches:
        print("❌ Não foi possível obter dados do Understat")
        print("💡 Nota: Understat carrega dados via JavaScript.")
        print("   Para extração completa, pode ser necessário usar Selenium.")
        sys.exit(1)
    
    print(f"\n✅ Encontrados {len(matches)} jogos")
    
    if args.test:
        print("\n🧪 MODO TESTE - Exibindo primeiros 3 jogos:")
        for i, match in enumerate(list(matches.items())[:3]):
            print(f"  Jogo {i+1}: {match}")
    
    print("\n" + "="*70)
    print("💡 RECOMENDAÇÃO")
    print("="*70)
    print("Understat carrega dados via JavaScript.")
    print("Para extração completa, recomendo usar Selenium.")
    print("Vou criar um script com Selenium agora...")
    print("="*70)

if __name__ == "__main__":
    main()

