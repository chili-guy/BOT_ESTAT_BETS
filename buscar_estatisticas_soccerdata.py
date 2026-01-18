#!/usr/bin/env python3
"""
Script usando a biblioteca SoccerData para buscar estatísticas
SoccerData já tem lógica para lidar com FBref e pode contornar bloqueios
"""

import sys
import argparse
from datetime import datetime
import pandas as pd

try:
    import soccerdata as sd
    HAS_SOCCERDATA = True
except ImportError:
    HAS_SOCCERDATA = False
    print("❌ SoccerData não está instalado")
    print("💡 Instale com: pip install soccerdata")
    sys.exit(1)

def main():
    """Função principal usando SoccerData"""
    parser = argparse.ArgumentParser(
        description='Busca estatísticas usando SoccerData (biblioteca especializada)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ligas disponíveis:
  --liga premier     Premier League
  --liga laliga      La Liga  
  --liga bundesliga  Bundesliga
  --liga seriea      Serie A
  --liga ligue1      Ligue 1

Exemplo:
  python buscar_estatisticas_soccerdata.py --liga bundesliga --season 2024-2025
        """
    )
    
    parser.add_argument('--liga', type=str, required=True,
                       choices=['premier', 'laliga', 'bundesliga', 'seriea', 'ligue1'],
                       help='Liga a buscar')
    parser.add_argument('--season', type=str, default='2024-2025',
                       help='Temporada (ex: 2024-2025)')
    parser.add_argument('--test', action='store_true',
                       help='Modo teste')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔍 BUSCADOR DE ESTATÍSTICAS - SOCCERDATA")
    print("="*70)
    print(f"Liga: {args.liga}")
    print(f"Temporada: {args.season}")
    print("="*70)
    
    # Mapeamento de ligas para SoccerData (nomes exatos requeridos)
    league_map = {
        'premier': 'ENG-Premier League',
        'laliga': 'ESP-La Liga',
        'bundesliga': 'GER-Bundesliga',
        'seriea': 'ITA-Serie A',
        'ligue1': 'FRA-Ligue 1',
    }
    
    league_name = league_map[args.liga]
    
    print(f"\n🔧 Criando scraper para {league_name}...")
    
    try:
        # Criar scraper FBref
        fbref = sd.FBref(leagues=league_name, seasons=args.season)
        
        print(f"✅ Scraper criado!")
        print(f"\n📊 Buscando dados de jogadores...")
        
        # Buscar estatísticas de jogadores
        # SoccerData usa diferentes métodos dependendo dos dados que você quer
        player_stats = fbref.read_player_season_stats(stat_type='standard')
        
        if player_stats is not None and not player_stats.empty:
            print(f"✅ Encontrados dados de {len(player_stats)} jogadores!")
            
            if args.test:
                print("\n🧪 MODO TESTE - Primeiras linhas:")
                print(player_stats.head())
            else:
                # Salvar em Excel
                output_file = f"{args.liga}_{args.season.replace('-', '_')}_soccerdata.xlsx"
                player_stats.to_excel(output_file, index=False)
                print(f"\n✅ Dados salvos em: {output_file}")
                
        else:
            print("⚠️  Não foi possível obter dados de jogadores")
            print("💡 Tentando buscar dados de jogos...")
            
            # Tentar buscar dados de jogos
            try:
                schedule = fbref.read_schedule()
                if schedule is not None and not schedule.empty:
                    print(f"✅ Encontrados {len(schedule)} jogos!")
                    if args.test:
                        print(schedule.head())
                    else:
                        output_file = f"{args.liga}_{args.season.replace('-', '_')}_schedule.xlsx"
                        schedule.to_excel(output_file, index=False)
                        print(f"✅ Dados salvos em: {output_file}")
                else:
                    print("❌ Não foi possível obter dados")
            except Exception as e:
                print(f"❌ Erro ao buscar schedule: {e}")
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 SoccerData pode estar tendo problemas com o FBref bloqueado")
        print("   Tente usar a alternativa com Selenium")

if __name__ == "__main__":
    main()

