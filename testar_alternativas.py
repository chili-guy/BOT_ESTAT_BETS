#!/usr/bin/env python3
"""
Script para testar diferentes rotas de extração de dados
Alternativas ao fbref.com quando estiver bloqueado
"""

import requests
import time
import sys

def test_alternative_1_understat():
    """Teste 1: Understat - Site alternativo com dados xG"""
    print("\n" + "="*70)
    print("🧪 TESTE 1: Understat (understat.com)")
    print("="*70)
    print("Understat fornece dados xG/xA para várias ligas")
    
    base_url = "https://understat.com"
    
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        session.headers.update(headers)
        
        print(f"  🔄 Testando acesso a {base_url}...")
        response = session.get(base_url, timeout=15)
        
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Understat está acessível!")
            print("  💡 Pode ser usado como alternativa para dados xG/xA")
            return True
        else:
            print(f"  ❌ Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_alternative_2_fotmob():
    """Teste 2: FotMob - API/Mobile app com dados"""
    print("\n" + "="*70)
    print("🧪 TESTE 2: FotMob API (fotmob.com)")
    print("="*70)
    print("FotMob tem API pública para alguns dados")
    
    try:
        # API endpoint público do FotMob
        api_url = "https://www.fotmob.com/api/leagues?id=47"  # Premier League
        
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        session.headers.update(headers)
        
        print(f"  🔄 Testando API do FotMob...")
        response = session.get(api_url, timeout=15)
        
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print("  ✅ FotMob API está acessível!")
            print("  💡 Pode fornecer dados básicos de jogos")
            return True
        else:
            print(f"  ❌ Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return False

def test_alternative_3_fbref_alternative_urls():
    """Teste 3: Tentar URLs alternativas do fbref"""
    print("\n" + "="*70)
    print("🧪 TESTE 3: URLs alternativas do FBref")
    print("="*70)
    print("Testando diferentes endpoints que podem ter menos proteção")
    
    # Tentar importar cloudscraper
    try:
        import cloudscraper
        session = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
            delay=10
        )
        print("  ✅ Usando cloudscraper")
    except:
        session = requests.Session()
        print("  ⚠️  Usando requests padrão")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    session.headers.update(headers)
    
    # URLs alternativas para testar
    alternative_urls = [
        {
            'name': 'Página inicial',
            'url': 'https://fbref.com',
        },
        {
            'name': 'Premier League - Temporada atual',
            'url': 'https://fbref.com/en/comps/9/Premier-League-Stats',
        },
        {
            'name': 'Bundesliga - Temporada atual',
            'url': 'https://fbref.com/en/comps/20/Bundesliga-Stats',
        },
    ]
    
    results = {}
    for alt in alternative_urls:
        try:
            print(f"\n  🔄 Testando: {alt['name']}")
            time.sleep(5)  # Delay entre testes
            
            response = session.get(alt['url'], timeout=20)
            
            if response.status_code == 200 and 'Just a moment' not in response.text[:500]:
                print(f"  ✅ Acessível! (Status: 200)")
                results[alt['name']] = True
            elif response.status_code == 403:
                print(f"  ❌ Bloqueado (Status: 403)")
                results[alt['name']] = False
            else:
                print(f"  ⚠️  Status: {response.status_code}")
                results[alt['name']] = False
                
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            results[alt['name']] = False
    
    return results

def test_alternative_4_selenium():
    """Teste 4: Verificar se Selenium está disponível"""
    print("\n" + "="*70)
    print("🧪 TESTE 4: Selenium (simulação de navegador)")
    print("="*70)
    print("Selenium pode contornar bloqueios Cloudflare")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        print("  ✅ Selenium está instalado!")
        print("  💡 Pode ser usado como alternativa para contornar Cloudflare")
        print("  📝 Instalação: pip install selenium")
        print("  📝 Também precisa do ChromeDriver")
        return True
        
    except ImportError:
        print("  ⚠️  Selenium não está instalado")
        print("  💡 Instale com: pip install selenium")
        print("  💡 Selenium pode ser melhor que cloudscraper para Cloudflare")
        return False

def test_alternative_5_soccerdata_lib():
    """Teste 5: Verificar biblioteca soccerdata"""
    print("\n" + "="*70)
    print("🧪 TESTE 5: Biblioteca SoccerData")
    print("="*70)
    print("Biblioteca Python especializada em dados de futebol")
    
    try:
        import soccerdata as sd
        print("  ✅ SoccerData está instalado!")
        print("  💡 Pode ser usado para extrair dados do FBref")
        print("  📚 Documentação: https://github.com/probberechts/soccerdata")
        return True
        
    except ImportError:
        print("  ⚠️  SoccerData não está instalado")
        print("  💡 Instale com: pip install soccerdata")
        print("  💡 Biblioteca especializada que já lida com FBref")
        return False

def main():
    """Testa todas as alternativas"""
    print("="*70)
    print("🔍 TESTANDO ROTAS ALTERNATIVAS DE EXTRAÇÃO")
    print("="*70)
    print("\nEste script testa diferentes formas de obter dados de futebol")
    print("quando o fbref.com está bloqueado.\n")
    
    results = {}
    
    # Testar alternativas
    results['Understat'] = test_alternative_1_understat()
    time.sleep(2)
    
    results['FotMob'] = test_alternative_2_fotmob()
    time.sleep(2)
    
    fbref_results = test_alternative_3_fbref_alternative_urls()
    results['FBref URLs'] = fbref_results
    time.sleep(2)
    
    results['Selenium'] = test_alternative_4_selenium()
    results['SoccerData'] = test_alternative_5_soccerdata_lib()
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    print("\n✅ Alternativas funcionais:")
    for name, result in results.items():
        if isinstance(result, dict):
            for sub_name, sub_result in result.items():
                if sub_result:
                    print(f"  ✅ {name} - {sub_name}")
        elif result:
            print(f"  ✅ {name}")
    
    print("\n❌ Alternativas não funcionais:")
    for name, result in results.items():
        if isinstance(result, dict):
            for sub_name, sub_result in result.items():
                if not sub_result:
                    print(f"  ❌ {name} - {sub_name}")
        elif not result:
            print(f"  ❌ {name}")
    
    print("\n" + "="*70)
    print("💡 RECOMENDAÇÕES")
    print("="*70)
    
    if results.get('SoccerData'):
        print("\n1. ✅ USE SOCCERDATA - Biblioteca especializada que já lida com FBref")
        print("   Instale: pip install soccerdata")
        print("   Vantagem: Já tem lógica para contornar bloqueios")
    
    if results.get('Selenium'):
        print("\n2. ✅ USE SELENIUM - Melhor para contornar Cloudflare")
        print("   Instale: pip install selenium")
        print("   Vantagem: Simula navegador real, difícil de detectar")
    
    if results.get('Understat'):
        print("\n3. ✅ USE UNDERSTAT - Para dados xG/xA")
        print("   Vantagem: Especializado em dados avançados (xG, xA)")
    
    if results.get('FotMob'):
        print("\n4. ✅ USE FOTMOB API - Para dados básicos")
        print("   Vantagem: API pública, fácil de usar")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()

