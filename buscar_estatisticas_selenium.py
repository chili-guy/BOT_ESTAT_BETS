#!/usr/bin/env python3
"""
Script usando Selenium para buscar estatísticas do FBref
Selenium simula navegador real e pode contornar Cloudflare
"""

import sys
import argparse
from datetime import datetime
import pandas as pd
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False
    print("❌ Selenium não está instalado")
    print("💡 Instale com: pip install selenium")
    print("💡 Também precisa instalar ChromeDriver")
    sys.exit(1)

LEAGUE_IDS = {
    'premier': {'id': 9, 'name': 'Premier League'},
    'laliga': {'id': 12, 'name': 'La Liga'},
    'bundesliga': {'id': 20, 'name': 'Bundesliga'},
    'seriea': {'id': 11, 'name': 'Serie A'},
    'portugal': {'id': 32, 'name': 'Primeira Liga'},
    'ligue1': {'id': 13, 'name': 'Ligue 1'},
    'championship': {'id': 10, 'name': 'Championship'},
}

class SeleniumFBrefScraper:
    """Scraper usando Selenium para contornar Cloudflare"""
    
    def __init__(self, headless=True):
        self.base_url = "https://fbref.com"
        self.headless = headless
        self.driver = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Configura o driver do Chrome"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("  ✅ ChromeDriver inicializado")
        except Exception as e:
            print(f"  ❌ Erro ao inicializar ChromeDriver: {e}")
            print("  💡 Certifique-se de que o ChromeDriver está instalado")
            print("  💡 Ou instale: sudo apt-get install chromium-chromedriver")
            raise
    
    def get_page(self, url, wait_time=10):
        """Acessa uma página e aguarda carregar"""
        try:
            print(f"  🔄 Acessando: {url}")
            self.driver.get(url)
            
            # Aguardar a página carregar (especialmente para Cloudflare)
            time.sleep(5)  # Aguardar desafio Cloudflare
            
            # Aguardar até que a página esteja carregada
            WebDriverWait(self.driver, wait_time).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Verificar se passou do desafio Cloudflare
            if "Just a moment" in self.driver.page_source[:1000]:
                print("  ⏳ Aguardando resolução do desafio Cloudflare...")
                time.sleep(10)  # Aguardar mais tempo
            
            if "Just a moment" in self.driver.page_source[:1000]:
                print("  ⚠️  Ainda na página de desafio")
                return False
            
            print("  ✅ Página carregada")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao carregar página: {e}")
            return False
    
    def get_schedule_page(self, league_id, season):
        """Acessa página de schedule de uma liga"""
        url = f"{self.base_url}/en/comps/{league_id}/{season}/schedule/{season}-Scores-and-Fixtures"
        return self.get_page(url)
    
    def extract_match_data(self, soup):
        """Extrai dados dos jogos da página"""
        # Similar ao código original, mas usando BeautifulSoup do HTML do Selenium
        matches = []
        # Implementação similar ao buscar_estatisticas_multi_liga.py
        return matches
    
    def close(self):
        """Fecha o driver"""
        if self.driver:
            self.driver.quit()
            print("  ✅ Driver fechado")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Busca estatísticas usando Selenium (contorna Cloudflare)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument('--liga', type=str, required=True,
                       choices=list(LEAGUE_IDS.keys()),
                       help='Liga a buscar')
    parser.add_argument('--season', type=str, default='2025-2026',
                       help='Temporada (ex: 2025-2026)')
    parser.add_argument('--test', action='store_true',
                       help='Modo teste')
    parser.add_argument('--visible', action='store_true',
                       help='Mostrar navegador (não headless)')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🔍 BUSCADOR DE ESTATÍSTICAS - SELENIUM")
    print("="*70)
    print(f"Liga: {LEAGUE_IDS[args.liga]['name']}")
    print(f"Temporada: {args.season}")
    print(f"Modo: {'VISÍVEL' if args.visible else 'HEADLESS'}")
    print("="*70)
    
    scraper = None
    
    try:
        print("\n🔧 Inicializando Selenium...")
        scraper = SeleniumFBrefScraper(headless=not args.visible)
        
        print(f"\n📊 Acessando página da liga...")
        success = scraper.get_schedule_page(LEAGUE_IDS[args.liga]['id'], args.season)
        
        if success:
            print("✅ Página acessada com sucesso!")
            
            if args.test:
                print("\n🧪 MODO TESTE - HTML da página:")
                print(scraper.driver.page_source[:500])
            else:
                # Extrair dados
                soup = BeautifulSoup(scraper.driver.page_source, 'html.parser')
                matches = scraper.extract_match_data(soup)
                print(f"✅ Extraídos {len(matches)} jogos")
        else:
            print("❌ Não foi possível acessar a página")
            
    except KeyboardInterrupt:
        print("\n⚠️  Interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()

