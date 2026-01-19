#!/usr/bin/env python3
"""
Script simples para comparar dados extraídos pelo script com dados do site
"""

import cloudscraper
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import sys
sys.path.insert(0, '.')
from buscar_estatisticas_multi_liga import scrape_period, LeagueScraper

def extrair_dados_site(match_url):
    """Extrai dados diretamente do site"""
    print(f"\n{'='*70}")
    print(f"🌐 EXTRAINDO DADOS DO SITE")
    print(f"{'='*70}")
    print(f"URL: {match_url}\n")
    
    scraper = cloudscraper.create_scraper()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    }
    scraper.headers.update(headers)
    
    response = scraper.get(match_url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    all_tables = soup.find_all('table', {'id': re.compile(r'.*')})
    
    # Encontrar tabelas summary
    summary_tables = []
    for table in all_tables:
        table_id = table.get('id', '').lower()
        if 'summary' in table_id and 'stats' in table_id:
            summary_tables.append(table)
    
    dados_site = []
    
    for stats_table in summary_tables:
        rows = stats_table.find_all('tr')[1:]
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 3:
                continue
            
            player_name = ""
            minutes = 0
            goals = 0
            assists = 0
            xg = 0.0
            xa = 0.0
            
            for cell in cells:
                data_stat = cell.get('data-stat', '').lower()
                text = cell.get_text(strip=True)
                
                if data_stat == 'player':
                    player_name = text
                elif data_stat == 'minutes':
                    try:
                        minutes = int(re.sub(r'[^\d]', '', text) or 0)
                    except:
                        pass
                elif data_stat == 'goals':
                    try:
                        goals = int(re.sub(r'[^\d]', '', text) or 0)
                    except:
                        pass
                elif data_stat == 'assists':
                    try:
                        assists = int(re.sub(r'[^\d]', '', text) or 0)
                    except:
                        pass
                elif data_stat == 'xg':
                    try:
                        text_clean = text.replace(',', '.')
                        text_clean = re.sub(r'[^\d.]', '', text_clean)
                        if text_clean:
                            xg = float(text_clean)
                    except:
                        pass
                elif data_stat == 'xg_assist':
                    try:
                        text_clean = text.replace(',', '.')
                        text_clean = re.sub(r'[^\d.]', '', text_clean)
                        if text_clean:
                            xa = float(text_clean)
                    except:
                        pass
            
            if not player_name or player_name in ['Player', '', 'Reserves', 'Team Total']:
                continue
            
            # Filtrar subtotais
            if 'player' in player_name.lower() and any(char.isdigit() for char in player_name):
                continue
            if minutes > 120:
                continue
            if re.match(r'^\d+\s+[Pp]layers?$', player_name.strip()):
                continue
            
            dados_site.append({
                'Player': player_name,
                'Minutes': minutes,
                'Goals': goals,
                'Assists': assists,
                'xG': xg,
                'xA': xa
            })
    
    return dados_site

def comparar(dados_site, dados_script):
    """Compara dados do site com dados do script"""
    print(f"\n{'='*70}")
    print(f"📊 COMPARAÇÃO DE DADOS")
    print(f"{'='*70}\n")
    
    # Converter para DataFrame para facilitar comparação
    df_site = pd.DataFrame(dados_site)
    df_script = pd.DataFrame(dados_script)
    
    # Normalizar nomes (lowercase) para comparação
    df_site['Player_lower'] = df_site['Player'].str.lower().str.strip()
    df_script['Player_lower'] = df_script['Player'].str.lower().str.strip()
    
    # Merge pelos nomes
    merged = df_site.merge(
        df_script,
        on='Player_lower',
        how='outer',
        suffixes=('_site', '_script'),
        indicator=True
    )
    
    erros = []
    acertos = []
    
    # Comparar jogadores que estão em ambos
    both = merged[merged['_merge'] == 'both']
    
    print(f"📋 Total de jogadores no site: {len(df_site)}")
    print(f"📋 Total de jogadores no script: {len(df_script)}")
    print(f"📋 Jogadores em ambos: {len(both)}\n")
    
    for idx, row in both.iterrows():
        player = row['Player_site']
        print(f"👤 {player}:")
        
        campos_ok = []
        campos_erro = []
        
        for campo in ['Minutes', 'Goals', 'Assists', 'xG', 'xA']:
            val_site = row[f'{campo}_site']
            val_script = row[f'{campo}_script']
            
            # Para xG e xA, comparar com tolerância
            if campo in ['xG', 'xA']:
                val_site = float(val_site)
                val_script = float(val_script)
                diff = abs(val_site - val_script)
                if diff < 0.0001:
                    status = "✅"
                    campos_ok.append(campo)
                else:
                    status = "❌"
                    campos_erro.append((campo, val_site, val_script))
            else:
                val_site = int(val_site) if pd.notna(val_site) else 0
                val_script = int(val_script) if pd.notna(val_script) else 0
                if val_site == val_script:
                    status = "✅"
                    campos_ok.append(campo)
                else:
                    status = "❌"
                    campos_erro.append((campo, val_site, val_script))
            
            print(f"  {status} {campo}: Site={val_site} | Script={val_script}")
        
        if campos_erro:
            erros.append((player, campos_erro))
        else:
            acertos.append(player)
        
        print()
    
    # Jogadores apenas no site
    only_site = merged[merged['_merge'] == 'left_only']
    if len(only_site) > 0:
        print(f"⚠️  Jogadores apenas no site ({len(only_site)}):")
        for idx, row in only_site.iterrows():
            print(f"  - {row['Player_site']}")
        print()
    
    # Jogadores apenas no script
    only_script = merged[merged['_merge'] == 'right_only']
    if len(only_script) > 0:
        print(f"⚠️  Jogadores apenas no script ({len(only_script)}):")
        for idx, row in only_script.iterrows():
            print(f"  - {row['Player_script']}")
        print()
    
    # Resumo
    print(f"{'='*70}")
    print(f"📊 RESUMO DA VALIDAÇÃO")
    print(f"{'='*70}")
    print(f"✅ Jogadores corretos: {len(acertos)}/{len(both)}")
    print(f"❌ Jogadores com erros: {len(erros)}/{len(both)}")
    
    if erros:
        print(f"\n❌ ERROS ENCONTRADOS:")
        for player, campos in erros:
            print(f"\n  {player}:")
            for campo, val_site, val_script in campos:
                print(f"    - {campo}: Site={val_site} | Script={val_script}")
    else:
        print(f"\n🎉 TODOS OS DADOS ESTÃO CORRETOS!")
    
    return len(erros) == 0

if __name__ == "__main__":
    # Jogo para validar: Sevilla vs Elche - 12/09/2025
    match_url = "https://fbref.com/en/matches/13448b32/Sevilla-Elche-September-12-2025-La-Liga"
    
    print("="*70)
    print("🔍 VALIDAÇÃO DE DADOS - COMPARANDO SITE vs SCRIPT")
    print("="*70)
    
    # 1. Extrair dados do site
    dados_site = extrair_dados_site(match_url)
    print(f"✅ Extraídos {len(dados_site)} jogadores do site")
    
    # 2. Extrair dados do script
    print(f"\n{'='*70}")
    print(f"🚀 EXTRAINDO DADOS DO SCRIPT")
    print(f"{'='*70}\n")
    
    scraper = LeagueScraper()
    scraper._ensure_initialized()
    
    start_date = pd.to_datetime('2025-09-12')
    end_date = pd.to_datetime('2025-09-12')
    
    dados_script = scrape_period(12, 'La Liga', start_date, end_date, scraper, limit_games=1)
    
    print(f"✅ Extraídos {len(dados_script)} jogadores do script")
    
    # Converter para formato de comparação
    dados_script_comparacao = []
    for item in dados_script:
        dados_script_comparacao.append({
            'Player': item['Player'],
            'Minutes': item['Minutes'],
            'Goals': item['Goals'],
            'Assists': item['Assists'],
            'xG': float(item['xG']),
            'xA': float(item['xA'])
        })
    
    # 3. Comparar
    sucesso = comparar(dados_site, dados_script_comparacao)
    
    sys.exit(0 if sucesso else 1)


