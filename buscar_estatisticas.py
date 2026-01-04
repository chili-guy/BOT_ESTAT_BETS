#!/usr/bin/env python3
"""
Script para buscar estatísticas de jogadores da Premier League:
MINUTES, GOAL, ASSISTS, XG e XA para cada jogador em cada partida.

Permite buscar partidas por período específico definido pelo usuário.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
from urllib.parse import urljoin
import argparse
import sys

# Tentar importar cloudscraper para contornar proteções anti-bot
try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False
    print("💡 Dica: Instale cloudscraper para melhor proteção anti-bot: pip install cloudscraper")


class PremierLeagueScraper:
    """Scraper para buscar dados da Premier League do fbref.com"""
    
    def __init__(self):
        self.base_url = "https://fbref.com"
        
        # Usar cloudscraper se disponível, senão usar requests normal
        if HAS_CLOUDSCRAPER:
            self.session = cloudscraper.create_scraper()
        else:
            self.session = requests.Session()
        
        # Headers para simular navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/'
        }
        
        if hasattr(self.session, 'headers'):
            self.session.headers.update(headers)
        
        self._initialized = False
    
    def _ensure_initialized(self):
        """Garante que a sessão foi inicializada"""
        if self._initialized:
            return
        
        try:
            if HAS_CLOUDSCRAPER:
                print("  ✅ Usando cloudscraper para contornar proteções anti-bot")
            else:
                print("  ⚠️  Usando requests padrão (pode ter problemas com proteções anti-bot)")
            
            print("  🔄 Estabelecendo conexão inicial...")
            initial_response = self.session.get(self.base_url, timeout=15)
            if initial_response.status_code == 200:
                print("  ✅ Conexão estabelecida com sucesso")
            else:
                print(f"  ⚠️  Resposta inicial: {initial_response.status_code}")
            self._initialized = True
        except Exception as e:
            print(f"  ⚠️  Aviso na conexão inicial: {e}")
            self._initialized = True
    
    def get_player_stats_from_match(self, match_url, team, opponent, date, location):
        """
        Extrai estatísticas de jogadores de um jogo específico.
        Retorna lista de dicionários com: Player, Team, Date, Opponent, Minutes, Goals, Assists, xG, xA
        """
        try:
            if not match_url or '/matches/' not in match_url:
                print(f"    ⚠️  URL inválida: {match_url}")
                return []
            
            print(f"    🔗 Acessando: {match_url}")
            time.sleep(3)  # Rate limiting
            
            response = self.session.get(match_url, timeout=20)
            
            if response.status_code == 429:
                print(f"    ⚠️  Rate limit (429). Aguardando 30 segundos...")
                time.sleep(30)
                response = self.session.get(match_url, timeout=20)
            
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar se é página de jogo válida ou página genérica
            page_title = soup.find('title')
            if page_title:
                title_text = page_title.get_text().lower()
                if 'schedule' in title_text or 'fixtures' in title_text:
                    print(f"    ⚠️  Página parece ser de schedule, não de jogo individual")
                    print(f"    💡 URL pode estar incorreta: {match_url}")
                    return []
            
            player_stats = []
            
            # Debug: listar todas as tabelas encontradas
            all_tables = soup.find_all('table', {'id': re.compile(r'.*')})
            table_ids = [t.get('id', 'N/A') for t in all_tables if t.get('id')]
            
            # Filtrar tabelas relevantes
            relevant_tables = [tid for tid in table_ids if 'sched' not in tid.lower()]
            
            if relevant_tables:
                print(f"    🔍 Tabelas encontradas: {len(relevant_tables)} (primeiras 5: {relevant_tables[:5]})")
            else:
                print(f"    ⚠️  Nenhuma tabela relevante encontrada (todas as tabelas: {table_ids[:5]})")
            
            # Encontrar tabela de estatísticas do time (home ou away)
            stats_table = None
            
            # Padrões para encontrar a tabela correta
            # Nota: fbref usa IDs únicos (ex: stats_4ba7cbea_summary), não stats_home_summary
            # Precisamos buscar por tabelas que contenham "summary" no ID
            
            # Primeiro, buscar todas as tabelas summary disponíveis
            summary_tables = []
            for table in all_tables:
                table_id = table.get('id', '').lower()
                # Buscar tabelas que contenham "summary" no ID (são as tabelas principais de estatísticas)
                if 'summary' in table_id and 'stats' in table_id:
                    summary_tables.append(table)
            
            # Se encontrou tabelas summary, usar baseado na posição (home geralmente é primeira, away é segunda)
            if summary_tables:
                if location == 'home' and len(summary_tables) > 0:
                    stats_table = summary_tables[0]
                    print(f"    ✓ Usando primeira tabela summary para home team")
                elif location == 'away' and len(summary_tables) > 1:
                    stats_table = summary_tables[1]
                    print(f"    ✓ Usando segunda tabela summary para away team")
                elif len(summary_tables) == 1:
                    stats_table = summary_tables[0]
                    print(f"    ✓ Usando única tabela summary disponível")
            
            # Se não encontrou summary, tentar padrões antigos como fallback
            if not stats_table:
                patterns = [
                    f'stats_{location}_summary',
                    f'stats_{location}_players',
                    f'stats_{location}',
                ]
                
                for pattern in patterns:
                    stats_table = soup.find('table', {'id': pattern})
                    if stats_table:
                        break
            
            # Método alternativo: procurar por tabelas com estrutura de estatísticas de jogadores
            if not stats_table:
                for table in all_tables:
                    table_id = table.get('id', '').lower()
                    if 'stats' in table_id and 'summary' in table_id:
                        thead = table.find('thead')
                        if thead:
                            headers = [th.get_text(strip=True).lower() for th in thead.find_all('th')]
                            header_text = ' '.join(headers)
                            if 'player' in header_text and ('min' in header_text or 'goals' in header_text):
                                stats_table = table
                                break
            
            # Último fallback: usar qualquer tabela com player (não recomendado, mas melhor que nada)
            if not stats_table:
                candidate_tables = []
                for table in all_tables:
                    thead = table.find('thead')
                    if thead:
                        headers = [th.get_text(strip=True).lower() for th in thead.find_all('th')]
                        header_text = ' '.join(headers)
                        if ('player' in header_text and 
                            ('min' in header_text or 'goals' in header_text or 'assists' in header_text)):
                            candidate_tables.append(table)
                
                # Filtrar para pegar apenas summary se possível
                summary_candidates = [t for t in candidate_tables if 'summary' in t.get('id', '').lower()]
                if summary_candidates:
                    candidate_tables = summary_candidates
                
                # Home geralmente é primeira tabela, away é segunda
                if candidate_tables:
                    if location == 'home' and len(candidate_tables) > 0:
                        stats_table = candidate_tables[0]
                    elif location == 'away' and len(candidate_tables) > 1:
                        stats_table = candidate_tables[1]
                    elif len(candidate_tables) == 1:
                        stats_table = candidate_tables[0]
            
            if not stats_table:
                print(f"    ❌ Tabela de estatísticas não encontrada para {location} team")
                print(f"    💡 Tabelas disponíveis: {relevant_tables[:10]}")
                # Tentar uma última vez: procurar qualquer tabela com "player" no cabeçalho
                for table in all_tables:
                    thead = table.find('thead')
                    if thead:
                        header_text = ' '.join([th.get_text(strip=True).lower() for th in thead.find_all('th')])
                        if 'player' in header_text:
                            # Verificar se tem colunas de estatísticas
                            if any(word in header_text for word in ['min', 'goals', 'assists', 'xg', 'xa']):
                                print(f"    💡 Tentando usar tabela genérica: {table.get('id', 'N/A')}")
                                stats_table = table
                                break
                
                if not stats_table:
                    # Verificar se o jogo foi realmente jogado (procurar por placar ou resultado)
                    score_elements = soup.find_all(['div', 'span'], string=re.compile(r'\d+\s*-\s*\d+'))
                    if not score_elements:
                        print(f"    ℹ️  Jogo pode não ter sido jogado ainda - sem placar visível")
                    return []
            
            print(f"    ✓ Tabela encontrada ({stats_table.get('id', 'N/A')})")
            
            # Debug apenas se necessário (comentado para produção)
            # header_row = stats_table.find('thead')
            # if header_row:
            #     all_headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            #     all_data_stats = [th.get('data-stat', 'N/A') for th in header_row.find_all('th')]
            #     # Procurar xA/xAG nas colunas
            #     xa_found = False
            #     for i, (header, data_stat) in enumerate(zip(all_headers, all_data_stats)):
            #         if 'xa' in header.lower() or 'xag' in header.lower() or 'xa' in data_stat.lower():
            #             xa_found = True
            #             print(f"    🔍 DEBUG: Coluna {i} - Header: '{header}' | data-stat: '{data_stat}'")
            #     if not xa_found:
            #         print(f"    ⚠️  DEBUG: xA não encontrado nos cabeçalhos. Colunas disponíveis:")
            #         for i, (header, data_stat) in enumerate(zip(all_headers[:15], all_data_stats[:15])):
            #             print(f"        {i}: '{header}' ({data_stat})")
            
            rows = stats_table.find_all('tr')[1:]  # Pular cabeçalho
            
            first_row_processed = False
            for row in rows:
                # Pular linhas de subtotais e cabeçalhos
                row_class = str(row.get('class', []))
                if 'thead' in row_class or 'spacer' in row_class:
                    continue
                
                cells = row.find_all(['td', 'th'])
                if len(cells) < 3:
                    continue
                
                # Extrair dados usando data-stat (método mais confiável no fbref)
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
                            minutes = 0
                    elif data_stat == 'goals':
                        try:
                            goals = int(re.sub(r'[^\d]', '', text) or 0)
                        except:
                            goals = 0
                    elif data_stat == 'assists':
                        try:
                            assists = int(re.sub(r'[^\d]', '', text) or 0)
                        except:
                            assists = 0
                    elif data_stat == 'xg':
                        try:
                            # Converter vírgula para ponto (formato brasileiro/europeu)
                            text_clean = text.replace(',', '.')
                            # Remover tudo exceto dígitos e ponto
                            text_clean = re.sub(r'[^\d.]', '', text_clean)
                            if text_clean:
                                xg = float(text_clean)
                            else:
                                xg = 0.0
                        except (ValueError, AttributeError):
                            xg = 0.0
                    elif data_stat in ['xa', 'xag', 'xg_assist', 'expected_assists', 'x_assisted_goals']:
                        try:
                            # Converter vírgula para ponto (formato brasileiro/europeu)
                            text_clean = text.replace(',', '.')
                            # Remover tudo exceto dígitos e ponto
                            text_clean = re.sub(r'[^\d.]', '', text_clean)
                            if text_clean:
                                xa = float(text_clean)
                            else:
                                xa = 0.0
                        except (ValueError, AttributeError):
                            xa = 0.0
                    # Também verificar se contém "xa" ou "xag" ou "xg_assist" no nome
                    elif ('xa' in data_stat or 'xag' in data_stat or 'xg_assist' in data_stat) and xa == 0.0:
                        # Evitar pegar xG quando procura xA
                        if 'xg' in data_stat and 'assist' not in data_stat and 'xa' not in data_stat:
                            pass
                        else:
                            try:
                                text_clean = text.replace(',', '.')
                                text_clean = re.sub(r'[^\d.]', '', text_clean)
                                if text_clean:
                                    xa = float(text_clean)
                            except (ValueError, AttributeError):
                                pass
                
                # Fallback: se não encontrou por data-stat, tentar por posição
                if not player_name and len(cells) > 0:
                    player_name = cells[0].get_text(strip=True)
                
                # Ignorar linhas sem nome válido ou linhas de subtotal/agregado
                if not player_name or player_name in ['Player', '', 'Reserves', 'Team Total']:
                    continue
                
                # Filtrar linhas de subtotal/agregado
                # Padrões comuns: "16 Players", "15 Players", etc.
                player_name_lower = player_name.lower()
                is_subtotal = False
                
                # Verificar se o nome parece ser um subtotal (ex: "16 Players", "15 Players")
                if 'player' in player_name_lower and any(char.isdigit() for char in player_name):
                    is_subtotal = True
                
                # Verificar se tem minutos anormalmente altos (subtotais)
                # Um jogo tem no máximo ~120 minutos (90 + tempo extra)
                # Subtotais geralmente têm 990 minutos (11 jogadores x 90 minutos)
                if minutes > 120:
                    is_subtotal = True
                
                # Verificar padrões específicos de subtotal
                if re.match(r'^\d+\s+[Pp]layers?$', player_name.strip()):
                    is_subtotal = True
                
                if is_subtotal:
                    continue
                
                # Se não encontrou estatísticas, tentar por índice no cabeçalho
                if minutes == 0 and goals == 0 and assists == 0:
                    header_row = stats_table.find('thead')
                    if header_row:
                        headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
                        try:
                            min_idx = next((i for i, h in enumerate(headers) if 'min' in h.lower()), -1)
                            gls_idx = next((i for i, h in enumerate(headers) if 'gls' in h.lower() or h.lower() == 'g'), -1)
                            ast_idx = next((i for i, h in enumerate(headers) if 'ast' in h.lower() or h.lower() == 'a'), -1)
                            xg_idx = next((i for i, h in enumerate(headers) if 'xg' in h.lower() and 'xag' not in h.lower()), -1)
                            # Tentar múltiplas variações para xA (incluindo xg_assist)
                            xa_idx = -1
                            for i, h in enumerate(headers):
                                h_lower = h.lower()
                                # Buscar por xAG, xA, xg_assist
                                if 'xag' in h_lower or 'xa' in h_lower:
                                    # Mas não pegar xG sozinho
                                    if 'xg_assist' in h_lower or 'xag' in h_lower or ('xa' in h_lower and 'xg' not in h_lower):
                                        xa_idx = i
                                        break
                                elif 'xg_assist' in h_lower:
                                    xa_idx = i
                                    break
                                elif 'expected_assists' in h_lower or 'expected assists' in h_lower:
                                    xa_idx = i
                                    break
                            
                            # Buscar também por data-stat nas células do cabeçalho
                            if xa_idx == -1:
                                header_row = stats_table.find('thead')
                                if header_row:
                                    header_cells = header_row.find_all(['th', 'td'])
                                    for i, header_cell in enumerate(header_cells):
                                        header_data_stat = header_cell.get('data-stat', '').lower()
                                        if header_data_stat in ['xg_assist', 'xag', 'xa'] or 'xg_assist' in header_data_stat:
                                            xa_idx = i
                                            break
                            
                            if min_idx >= 0 and min_idx < len(cells):
                                minutes_str = cells[min_idx].get_text(strip=True)
                                minutes = int(re.sub(r'[^\d]', '', minutes_str) or 0)
                            
                            if gls_idx >= 0 and gls_idx < len(cells):
                                goals = int(re.sub(r'[^\d]', '', cells[gls_idx].get_text(strip=True)) or 0)
                            
                            if ast_idx >= 0 and ast_idx < len(cells):
                                assists = int(re.sub(r'[^\d]', '', cells[ast_idx].get_text(strip=True)) or 0)
                            
                            if xg_idx >= 0 and xg_idx < len(cells):
                                xg_str = cells[xg_idx].get_text(strip=True)
                                try:
                                    # Converter vírgula para ponto (formato brasileiro/europeu)
                                    xg_str_clean = xg_str.replace(',', '.')
                                    xg_str_clean = re.sub(r'[^\d.]', '', xg_str_clean)
                                    if xg_str_clean:
                                        xg = float(xg_str_clean)
                                    else:
                                        xg = 0.0
                                except (ValueError, AttributeError):
                                    xg = 0.0
                            
                            if xa_idx >= 0 and xa_idx < len(cells):
                                xa_str = cells[xa_idx].get_text(strip=True)
                                try:
                                    # Converter vírgula para ponto (formato brasileiro/europeu)
                                    xa_str_clean = xa_str.replace(',', '.')
                                    xa_str_clean = re.sub(r'[^\d.]', '', xa_str_clean)
                                    if xa_str_clean:
                                        xa = float(xa_str_clean)
                                    else:
                                        xa = 0.0
                                except (ValueError, AttributeError):
                                    xa = 0.0
                            # Se ainda não encontrou xA, tentar buscar em todas as células por data-stat
                            if xa == 0.0:
                                for idx, cell in enumerate(cells):
                                    cell_data_stat = cell.get('data-stat', '').lower()
                                    # Buscar variações de xA (xa, xag, expected_assists)
                                    if any(xa_variant in cell_data_stat for xa_variant in ['xa', 'xag', 'expected_assists']) and 'xg' not in cell_data_stat:
                                        try:
                                            xa_text = cell.get_text(strip=True)
                                            if xa_text and xa_text.strip():
                                                xa_text_clean = xa_text.replace(',', '.')
                                                xa_text_clean = re.sub(r'[^\d.]', '', xa_text_clean)
                                                if xa_text_clean:
                                                    xa = float(xa_text_clean)
                                                    break
                                        except (ValueError, AttributeError):
                                            pass
                        except (ValueError, IndexError):
                            pass
                
                # Se ainda não encontrou xA após tudo, tentar métodos alternativos
                if xa == 0.0:
                    # Método 1: Buscar por data-stat em todas as células (incluindo xg_assist)
                    for cell in cells:
                        cell_data_stat = cell.get('data-stat', '').lower()
                        # Buscar por xg_assist, xag, xa
                        if any(xa_variant in cell_data_stat for xa_variant in ['xg_assist', 'xag', 'xa', 'expected_assists', 'assisted_goals']):
                            # Evitar pegar xG quando procura xA
                            if 'xg_assist' in cell_data_stat or 'xag' in cell_data_stat or ('xa' in cell_data_stat and 'xg' not in cell_data_stat):
                                try:
                                    cell_text = cell.get_text(strip=True)
                                    if cell_text and cell_text.strip() and cell_text != '-':
                                        cell_text_clean = cell_text.replace(',', '.')
                                        cell_text_clean = re.sub(r'[^\d.]', '', cell_text_clean)
                                        if cell_text_clean:
                                            xa = float(cell_text_clean)
                                            break
                                except (ValueError, AttributeError):
                                    pass
                    
                    # Método 2: Se xG foi encontrado, xA geralmente está logo depois (próxima coluna)
                    if xa == 0.0 and xg > 0.0:
                        # Encontrar índice de xG e procurar próxima célula
                        for idx, cell in enumerate(cells):
                            cell_data_stat = cell.get('data-stat', '').lower()
                            if 'xg' in cell_data_stat and 'xa' not in cell_data_stat:
                                # Procurar nas próximas 3 células após xG
                                for next_idx in range(idx + 1, min(idx + 4, len(cells))):
                                    next_cell = cells[next_idx]
                                    next_data_stat = next_cell.get('data-stat', '').lower()
                                    next_text = next_cell.get_text(strip=True)
                                    # Se não é numérico válido, pode ser xA
                                    if next_text and next_text != '-':
                                        try:
                                            next_text_clean = next_text.replace(',', '.')
                                            next_text_clean = re.sub(r'[^\d.]', '', next_text_clean)
                                            if next_text_clean:
                                                potential_xa = float(next_text_clean)
                                                # xA geralmente é menor que 1.5, então se for um número pequeno, pode ser xA
                                                if potential_xa < 1.5 and potential_xa >= 0:
                                                    # Verificar se não é outro campo conhecido
                                                    if next_data_stat not in ['xg', 'goals', 'assists', 'minutes', 'player']:
                                                        xa = potential_xa
                                                        break
                                        except (ValueError, AttributeError):
                                            pass
                                if xa > 0.0:
                                    break
                    
                    # Método 3: Buscar por posição relativa (se assists foi encontrado, xA pode estar perto)
                    if xa == 0.0 and assists >= 0:
                        # Buscar células próximas a assists
                        for idx, cell in enumerate(cells):
                            cell_data_stat = cell.get('data-stat', '').lower()
                            if 'assists' in cell_data_stat:
                                # Procurar próxima célula numérica
                                for next_idx in range(idx + 1, min(idx + 3, len(cells))):
                                    next_cell = cells[next_idx]
                                    next_text = next_cell.get_text(strip=True)
                                    next_data_stat = next_cell.get('data-stat', '').lower()
                                    if next_text and next_text != '-':
                                        try:
                                            next_text_clean = next_text.replace(',', '.')
                                            next_text_clean = re.sub(r'[^\d.]', '', next_text_clean)
                                            if next_text_clean:
                                                potential_xa = float(next_text_clean)
                                                if potential_xa < 2.0 and potential_xa >= 0 and 'xa' not in next_data_stat and 'xg' not in next_data_stat:
                                                    # Se parece ser um valor decimal pequeno, pode ser xA
                                                    if '.' in next_text or ',' in next_text:
                                                        xa = potential_xa
                                                        break
                                        except (ValueError, AttributeError):
                                            pass
                                if xa > 0.0:
                                    break
                    
                    # Método 4: Se ainda não encontrou, buscar em todas as células novamente com xg_assist
                    if xa == 0.0:
                        for cell in cells:
                            cell_data_stat = cell.get('data-stat', '').lower()
                            # Buscar especificamente por xg_assist (que é o nome correto no fbref)
                            if cell_data_stat == 'xg_assist':
                                try:
                                    cell_text = cell.get_text(strip=True)
                                    if cell_text and cell_text.strip() and cell_text != '-':
                                        cell_text_clean = cell_text.replace(',', '.')
                                        cell_text_clean = re.sub(r'[^\d.]', '', cell_text_clean)
                                        if cell_text_clean:
                                            xa = float(cell_text_clean)
                                            break
                                except (ValueError, AttributeError):
                                    pass
                    
                    # Debug apenas se necessário (comentado para produção)
                    # if xa == 0.0 and not first_row_processed:
                    #     print(f"    🔍 DEBUG xA: Player={player_name[:20]}, xG={xg}, Assists={assists}")
                    #     print(f"    🔍 DEBUG: Procurando xA em todas as células:")
                    #     for idx, cell in enumerate(cells):  # Todas as células
                    #         cell_stat = cell.get('data-stat', 'N/A')
                    #         cell_text = cell.get_text(strip=True)[:30]
                    #         # Destacar se tem xg_assist
                    #         if 'xg_assist' in cell_stat.lower() or 'xag' in cell_stat.lower():
                    #             print(f"        [{idx}] ⭐ data-stat='{cell_stat}' text='{cell_text}' ⭐")
                    #         else:
                    #             print(f"        [{idx}] data-stat='{cell_stat}' text='{cell_text}'")
                    #     first_row_processed = True
                
                # Format xG com 4 casas decimais
                xg_formatted = round(xg, 4) if xg > 0 else 0.0
                xa_formatted = round(xa, 4) if xa > 0 else 0.0
                
                # Criar registro
                stats = {
                    'Player': player_name,
                    'Team': team,
                    'Date': date,
                    'Opponent': opponent,
                    'Minutes': minutes,
                    'Goals': goals,
                    'Assists': assists,
                    'xG': xg_formatted,
                    'xA': xa_formatted,
                    'Confronto': f"{team}|{opponent}|{date.strftime('%Y-%m-%d')}",
                    'Location': location,
                    'adj': 0,
                    'Year': date.year,
                    'Month': date.month
                }
                player_stats.append(stats)
            
            print(f"    ✓ {len(player_stats)} jogadores processados")
            return player_stats
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"    ⚠️  Rate limit (429)")
                time.sleep(60)
            else:
                print(f"    ❌ Erro HTTP {e.response.status_code}: {e}")
            return []
        except Exception as e:
            print(f"    ❌ Erro ao extrair estatísticas: {e}")
            return []


def process_schedule_table(soup, start_date, end_date, scraper, limit_games=None):
    """
    Processa a tabela de jogos e extrai estatísticas de jogadores
    para jogos dentro do período especificado
    """
    all_player_stats = []
    
    # Encontrar tabela de jogos
    table = soup.find('table', {'id': 'sched_9_1'})
    if not table:
        table = soup.find('table', {'id': re.compile(r'sched.*')})
    if not table:
        tables = soup.find_all('table')
        for t in tables:
            if 'schedule' in str(t.get('id', '')).lower() or 'fixture' in str(t.get('id', '')).lower():
                table = t
                break
    
    if not table:
        print(f"  ⚠️  Tabela de jogos não encontrada")
        return []
    
    rows = table.find_all('tr')[1:]  # Pular cabeçalho
    print(f"  Encontradas {len(rows)} linhas na tabela")
    
    matches_found = 0
    skipped_no_date = 0
    skipped_out_of_range = 0
    skipped_no_teams = 0
    
    for row_idx, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        if len(cells) < 3:
            continue
        
        try:
            # Extrair data
            date_text = ""
            date_cell = None
            
            # Procurar por atributo data-date
            for cell in cells:
                date_attr = cell.get('data-date', '')
                if date_attr and re.match(r'\d{4}-\d{2}-\d{2}', date_attr):
                    date_text = date_attr
                    date_cell = cell
                    break
            
            # Se não encontrou, procurar por texto
            if not date_text:
                for cell in cells[:10]:
                    text = cell.get_text(strip=True)
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', text):
                        date_text = text
                        date_cell = cell
                        break
            
            if not date_text:
                skipped_no_date += 1
                continue
            
            # Converter data
            match_date = pd.to_datetime(date_text, format='%Y-%m-%d', errors='coerce')
            if pd.isna(match_date):
                skipped_no_date += 1
                continue
            
            # Verificar se está no período especificado
            if match_date < start_date or match_date > end_date:
                skipped_out_of_range += 1
                continue
            
            # Extrair times
            home_team = ""
            away_team = ""
            
            # Por data-stat
            for cell in cells:
                data_stat = cell.get('data-stat', '')
                text = cell.get_text(strip=True)
                
                if data_stat == 'home_team':
                    home_team = text
                elif data_stat == 'away_team':
                    away_team = text
            
            # Por posição padrão
            if not home_team and len(cells) > 4:
                home_team = cells[4].get_text(strip=True)
            if not away_team and len(cells) > 5:
                away_team = cells[5].get_text(strip=True)
            
            # Por links
            if not home_team or not away_team:
                team_links = []
                for cell in cells:
                    link = cell.find('a')
                    if link:
                        text = link.get_text(strip=True)
                        href = link.get('href', '')
                        if text and len(text) > 2 and '/squads/' in href:
                            if (not re.match(r'^\d+$', text) and 
                                not re.match(r'\d{4}-\d{2}-\d{2}', text) and
                                not re.match(r'\d{2}:\d{2}', text) and
                                text not in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
                                team_links.append(text)
                
                if team_links:
                    if not home_team and len(team_links) > 0:
                        home_team = team_links[0]
                    if not away_team and len(team_links) > 1:
                        away_team = team_links[1]
            
            if not home_team or not away_team:
                skipped_no_teams += 1
                continue
            
            # Verificar se o jogo foi jogado (tem placar) antes de buscar link
            # Jogos futuros não têm placar e não têm dados disponíveis
            has_score = False
            score_text = ""
            for cell in cells:
                text = cell.get_text(strip=True)
                # Verificar se tem placar (formato XX-XX ou XX:XX)
                if re.match(r'^\d+[\s\-:]\d+$', text) and len(text) <= 10:
                    # Verificar se não é hora (HH:MM)
                    if ':' not in text or (':' in text and int(text.split(':')[0]) > 23):
                        has_score = True
                        score_text = text
                        break
            
            # Se não tem placar, o jogo provavelmente não foi jogado ainda
            if not has_score:
                # Verificar também data-stat para score
                for cell in cells:
                    data_stat = cell.get('data-stat', '')
                    if 'score' in data_stat.lower() and cell.get_text(strip=True):
                        has_score = True
                        score_text = cell.get_text(strip=True)
                        break
                
                if not has_score:
                    print(f"  📅 {match_date.strftime('%Y-%m-%d')}: {home_team} vs {away_team} - ⏳ Jogo ainda não foi jogado (sem placar)")
                    continue
            
            # Buscar link do jogo - procurar em todas as células
            match_link = None
            
            # Primeiro, tentar na célula da data
            if date_cell:
                link_cell = date_cell.find('a')
                if link_cell and link_cell.get('href'):
                    href = link_cell.get('href', '')
                    if '/matches/' in href and '/schedule/' not in href:
                        match_link = urljoin(scraper.base_url, href)
                        if not match_link.startswith('http'):
                            match_link = urljoin(scraper.base_url, href)
            
            # Se não encontrou, procurar em todas as células
            if not match_link:
                for cell in cells:
                    links = cell.find_all('a')
                    for link in links:
                        href = link.get('href', '')
                        if href and '/matches/' in href and '/schedule/' not in href:
                            # Verificar se não é apenas uma data
                            if not re.match(r'^/?en/matches/\d{4}-\d{2}-\d{2}$', href):
                                match_link = urljoin(scraper.base_url, href)
                                if match_link.startswith('http'):
                                    break
                    if match_link:
                        break
            
            # Se ainda não encontrou link, mas tem placar, pode ser problema na extração
            if not match_link:
                print(f"     ⚠️  Link do jogo não encontrado (mas jogo foi jogado - placar: {score_text})")
                # Tentar métodos alternativos de busca de link
                # Às vezes o link está em outra célula ou formato diferente
                for cell in cells:
                    # Procurar todos os links na célula
                    all_links = cell.find_all('a')
                    for link in all_links:
                        href = link.get('href', '')
                        if href and ('/match' in href.lower() or 'match' in href.lower()):
                            if '/schedule' not in href.lower():
                                match_link = urljoin(scraper.base_url, href)
                                if match_link.startswith('http'):
                                    break
                    if match_link:
                        break
                
                if not match_link:
                    print(f"     ❌ Não foi possível encontrar link válido - pulando este jogo")
                    continue
            
            # Validar URL encontrada
            if match_link and not match_link.startswith('http'):
                match_link = urljoin(scraper.base_url, match_link)
            
            # Verificar se URL é válida (deve conter /matches/ e um ID válido)
            if match_link and '/matches/' in match_link:
                # Verificar se não é apenas data (formato inválido)
                if re.match(r'.*/matches/\d{4}-\d{2}-\d{2}$', match_link):
                    print(f"     ⚠️  URL parece inválida (apenas data): {match_link}")
                    print(f"     ℹ️  Tentando encontrar link correto...")
                    # Tentar novamente com método mais agressivo
                    match_link = None
                    for cell in cells:
                        all_links = cell.find_all('a')
                        for link in all_links:
                            href = link.get('href', '')
                            if href and '/matches/' in href:
                                # Verificar se tem ID único (geralmente tem letras/ID após data)
                                if not re.match(r'^/en/matches/\d{4}-\d{2}-\d{2}$', href):
                                    match_link = urljoin(scraper.base_url, href)
                                    if match_link.startswith('http'):
                                        break
                        if match_link:
                            break
                    
                    if not match_link:
                        print(f"     ❌ Não foi possível encontrar link válido - pulando")
                        continue
            
            # Verificar limite
            if limit_games and matches_found >= limit_games:
                print(f"  ⏸️  Limite de {limit_games} jogos atingido")
                break
            
            print(f"  📅 {match_date.strftime('%Y-%m-%d')}: {home_team} vs {away_team} (Placar: {score_text})")
            print(f"     🔗 URL: {match_link}")
            
            # Buscar estatísticas
            stats_home = scraper.get_player_stats_from_match(
                match_link, home_team, away_team, match_date, 'home'
            )
            all_player_stats.extend(stats_home)
            
            stats_away = scraper.get_player_stats_from_match(
                match_link, away_team, home_team, match_date, 'away'
            )
            all_player_stats.extend(stats_away)
            
            matches_found += 1
            print(f"     ✓ {len(stats_home) + len(stats_away)} jogadores processados")
            
            # Se não encontrou dados, pode ser jogo futuro
            if len(stats_home) == 0 and len(stats_away) == 0:
                print(f"     ⚠️  Nenhum dado encontrado - jogo pode não ter sido jogado ainda")
            
            time.sleep(5)  # Delay entre jogos
            
        except Exception as e:
            print(f"     ❌ Erro ao processar linha: {e}")
            continue
    
    print(f"\n  📊 Estatísticas:")
    print(f"     ✓ Jogos processados: {matches_found}")
    print(f"     ⚠️  Sem data: {skipped_no_date}")
    print(f"     ⚠️  Fora do período: {skipped_out_of_range}")
    print(f"     ⚠️  Sem times: {skipped_no_teams}")
    print(f"  ✅ Total: {len(all_player_stats)} registros de jogadores")
    
    return all_player_stats


def get_season_url(year, month):
    """Determina a URL da temporada baseado no mês"""
    # Temporada da Premier League vai de agosto a maio
    # Se o mês é agosto-dezembro, está na temporada atual ano-ano+1
    # Se o mês é janeiro-maio, está na temporada anterior ano-1-ano
    if month >= 8:
        season = f"{year}-{year+1}"
    else:
        season = f"{year-1}-{year}"
    
    return f"https://fbref.com/en/comps/9/{season}/schedule/{season}-Premier-League-Scores-and-Fixtures"


def scrape_period(start_date, end_date, scraper=None, limit_games=None):
    """Busca dados para um período específico"""
    if scraper is None:
        scraper = PremierLeagueScraper()
    
    if not scraper._initialized:
        scraper._ensure_initialized()
    
    all_player_stats = []
    
    # Gerar lista de meses para processar
    current_date = start_date
    months_to_process = []
    
    while current_date <= end_date:
        year_month = (current_date.year, current_date.month)
        if year_month not in months_to_process:
            months_to_process.append(year_month)
        
        # Avançar para o próximo mês
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1, day=1)
    
    print(f"\n📅 Período: {start_date.strftime('%Y-%m-%d')} até {end_date.strftime('%Y-%m-%d')}")
    print(f"📋 Meses a processar: {', '.join([f'{y}-{m:02d}' for y, m in months_to_process])}")
    
    for year, month in months_to_process:
        print(f"\n{'='*60}")
        print(f"Processando {year}-{month:02d}...")
        print(f"{'='*60}")
        
        try:
            url = get_season_url(year, month)
            print(f"  Acessando: {url}")
            
            response = scraper.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Processar tabela filtrando pelo período
            month_stats = process_schedule_table(soup, start_date, end_date, scraper, limit_games)
            all_player_stats.extend(month_stats)
            
            # Delay entre meses
            if (year, month) != months_to_process[-1]:
                print(f"  ⏳ Aguardando 10 segundos antes do próximo mês...")
                time.sleep(10)
                
        except Exception as e:
            print(f"  ❌ Erro ao processar {year}-{month:02d}: {e}")
            continue
    
    return all_player_stats


def get_spreadsheet_template(filepath='premier.xlsx'):
    """Obtém a estrutura de colunas da planilha existente"""
    try:
        df_template = pd.read_excel(filepath, nrows=0)
        return df_template.columns.tolist()
    except:
        # Estrutura padrão baseada na análise
        return [
            'Player', 'Team', 'Date', 'Opponent', 'Minutes', 'Goals', 'Assists',
            'xG', 'xA', 'Confronto', 'Location', 'adj', 'TEAM', 'Chelsea',
            'Unnamed: 14', 'LINHA', '1.5', 'Unnamed: 17', 'FAIR ASS',
            '6.83060124935948', 'Unnamed: 20', 'FAIR GOAL', '5.714158363009968',
            'Unnamed: 23', 'LOCAL TEAM', 'Unnamed: 25', 'Unnamed: 26',
            'LOCAL PLAYER', 'Unnamed: 28', 'Unnamed: 29', 'CONFRONTO',
            'Unnamed: 31', 'Unnamed: 32', 'Unnamed: 33', 'Neto', 'Arsenal',
            'Year', 'Month'
        ]


def main():
    parser = argparse.ArgumentParser(
        description='Busca estatísticas de jogadores da Premier League (MINUTES, GOALS, ASSISTS, XG, XA)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Buscar dados de outubro de 2025
  python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31

  # Buscar dados de outubro a dezembro de 2025
  python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-12-31

  # Modo teste (limita a 5 jogos)
  python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --limit 5 --test

  # Especificar arquivo de saída
  python buscar_estatisticas.py --inicio 2025-10-01 --fim 2025-10-31 --output minha_planilha.xlsx
        """
    )
    
    parser.add_argument(
        '--inicio',
        type=str,
        required=True,
        help='Data de início (formato: YYYY-MM-DD, ex: 2025-10-01)'
    )
    parser.add_argument(
        '--fim',
        type=str,
        required=True,
        help='Data de fim (formato: YYYY-MM-DD, ex: 2025-10-31)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='premier.xlsx',
        help='Arquivo Excel de saída (padrão: premier.xlsx)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limitar número de jogos a processar (útil para testes)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Modo teste - não salva arquivo, apenas mostra resultados'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("BUSCADOR DE ESTATÍSTICAS - PREMIER LEAGUE")
    print("="*60)
    print("\nEstatísticas buscadas: MINUTES, GOALS, ASSISTS, XG, XA")
    
    if args.test:
        print("🧪 MODO TESTE - Nenhuma alteração será salva")
    
    # Parsear datas
    try:
        start_date = pd.to_datetime(args.inicio)
        end_date = pd.to_datetime(args.fim)
    except:
        print("❌ Erro: Formato de data inválido. Use YYYY-MM-DD (ex: 2025-10-01)")
        return
    
    if start_date > end_date:
        print("❌ Erro: Data de início deve ser anterior à data de fim")
        return
    
    print(f"\n📅 Período: {start_date.strftime('%Y-%m-%d')} até {end_date.strftime('%Y-%m-%d')}")
    
    if not args.test:
        resposta = input("\n⚠️  Continuar com a busca? (s/n): ").strip().lower()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            print("Operação cancelada.")
            return
    
    # Inicializar scraper
    print("\n🔧 Inicializando scraper...")
    scraper = PremierLeagueScraper()
    scraper._ensure_initialized()
    
    # Buscar dados
    print("\n🚀 Iniciando busca...")
    all_data = scrape_period(start_date, end_date, scraper, limit_games=args.limit)
    
    if not all_data:
        print("\n⚠️  Nenhum dado foi encontrado.")
        print("\n💡 Possíveis razões:")
        print("   - Os dados ainda não estão disponíveis no site")
        print("   - A estrutura do site mudou")
        print("   - Problemas de conexão ou bloqueio")
        return
    
    # Converter para DataFrame
    print(f"\n📊 Processando {len(all_data)} registros coletados...")
    new_df = pd.DataFrame(all_data)
    
    # Obter estrutura da planilha original
    try:
        template_columns = get_spreadsheet_template(args.output)
        print(f"  📋 Usando estrutura da planilha existente ({len(template_columns)} colunas)")
    except:
        template_columns = get_spreadsheet_template('premier.xlsx')
        print(f"  📋 Usando estrutura padrão ({len(template_columns)} colunas)")
    
    # Garantir que todas as colunas existam
    for col in template_columns:
        if col not in new_df.columns:
            new_df[col] = None
    
    # Reordenar colunas
    new_df = new_df[template_columns]
    
    # Remover duplicatas
    before_dedup = len(new_df)
    new_df = new_df.drop_duplicates(subset=['Player', 'Team', 'Date', 'Opponent'], keep='last')
    duplicates_removed = before_dedup - len(new_df)
    
    if duplicates_removed > 0:
        print(f"  🧹 Removidas {duplicates_removed} duplicatas")
    
    # Ordenar por data
    new_df = new_df.sort_values('Date')
    
    if args.test:
        print(f"\n{'='*60}")
        print("🧪 MODO TESTE - Resultados:")
        print(f"{'='*60}")
        print(f"📈 Total de registros: {len(new_df)}")
        print(f"📅 Data mínima: {new_df['Date'].min().strftime('%Y-%m-%d')}")
        print(f"📅 Data máxima: {new_df['Date'].max().strftime('%Y-%m-%d')}")
        print(f"\nPrimeiras 5 linhas:")
        print(new_df.head(5).to_string())
        print(f"\n💡 Execute sem --test para salvar a planilha")
        print(f"{'='*60}")
    else:
        # Salvar planilha
        import os
        from pathlib import Path
        
        # Criar diretório se não existir
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        new_df.to_excel(args.output, index=False)
        
        print(f"\n{'='*60}")
        print("✅ PLANILHA SALVA COM SUCESSO!")
        print(f"{'='*60}")
        print(f"📈 Total de registros: {len(new_df)}")
        print(f"📅 Data mínima: {new_df['Date'].min().strftime('%Y-%m-%d')}")
        print(f"📅 Data máxima: {new_df['Date'].max().strftime('%Y-%m-%d')}")
        print(f"📁 Arquivo salvo: {os.path.abspath(args.output)}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()

