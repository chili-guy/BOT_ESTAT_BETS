#!/usr/bin/env python3
"""
Script de validação de acesso ao fbref.com
Testa se o acesso está funcionando antes de fazer scraping completo
"""

import requests
import time
import sys

# Tentar importar cloudscraper
try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False
    print("⚠️  cloudscraper não está instalado. Instale com: pip install cloudscraper")

def test_access(league_id, league_name):
    """Testa acesso a uma liga específica"""
    base_url = "https://fbref.com"
    
    # Criar sessão
    if HAS_CLOUDSCRAPER:
        # Usar cloudscraper com configurações otimizadas
        session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            },
            delay=10  # Delay maior entre requisições
        )
        print(f"  ✅ Usando cloudscraper")
    else:
        session = requests.Session()
        print(f"  ⚠️  Usando requests padrão (pode ter problemas)")
    
    # Headers realistas
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.google.com/'
    }
    
    if hasattr(session, 'headers'):
        session.headers.update(headers)
    
    # Teste 1: Acesso à página inicial
    print(f"\n  🔄 Teste 1: Acessando página inicial...")
    try:
        time.sleep(2)
        response = session.get(base_url, timeout=20)
        if response.status_code == 200:
            print(f"  ✅ Página inicial acessível (Status: 200)")
        elif response.status_code == 403:
            print(f"  ❌ ERRO 403: Acesso bloqueado à página inicial")
            return False
        else:
            print(f"  ⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Erro ao acessar página inicial: {e}")
        return False
    
    # Teste 2: Acesso à página da liga
    # Formato: https://fbref.com/en/comps/{league_id}/2025-2026/schedule/2025-2026-Scores-and-Fixtures
    season = "2025-2026"
    url = f"{base_url}/en/comps/{league_id}/{season}/schedule/{season}-Scores-and-Fixtures"
    
    print(f"\n  🔄 Teste 2: Acessando página da liga...")
    print(f"  📍 URL: {url}")
    
    try:
        time.sleep(3)  # Delay entre requisições
        response = session.get(url, timeout=20)
        
        if response.status_code == 200:
            print(f"  ✅ Página da liga acessível (Status: 200)")
            print(f"  📊 Tamanho da resposta: {len(response.content)} bytes")
            
            # Verificar se tem conteúdo útil
            if len(response.content) > 10000:  # Página completa geralmente tem mais de 10KB
                print(f"  ✅ Conteúdo parece válido")
                return True
            else:
                print(f"  ⚠️  Conteúdo muito pequeno, pode estar bloqueado")
                return False
                
        elif response.status_code == 403:
            print(f"  ❌ ERRO 403: Acesso bloqueado à página da liga")
            print(f"  💡 Tentando novamente com delay maior...")
            
            # Tentar novamente com delay maior
            time.sleep(10)
            session.headers.update({
                'Referer': base_url,
                'Origin': base_url
            })
            response = session.get(url, timeout=20)
            
            if response.status_code == 200:
                print(f"  ✅ Segunda tentativa bem-sucedida!")
                return True
            else:
                print(f"  ❌ Ainda bloqueado (Status: {response.status_code})")
                return False
                
        elif response.status_code == 429:
            print(f"  ⚠️  Rate limit (429). Aguardando 30 segundos...")
            time.sleep(30)
            response = session.get(url, timeout=20)
            if response.status_code == 200:
                print(f"  ✅ Acesso após aguardar rate limit")
                return True
            else:
                print(f"  ❌ Ainda com problemas (Status: {response.status_code})")
                return False
        else:
            print(f"  ⚠️  Status inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"  ❌ Timeout ao acessar página da liga")
        return False
    except Exception as e:
        print(f"  ❌ Erro ao acessar página da liga: {e}")
        return False

def main():
    """Testa acesso para todas as ligas"""
    print("="*70)
    print("🔍 VALIDAÇÃO DE ACESSO AO FBREF.COM")
    print("="*70)
    
    leagues = {
        'premier': {'id': 9, 'name': 'Premier League'},
        'laliga': {'id': 12, 'name': 'La Liga'},
        'bundesliga': {'id': 20, 'name': 'Bundesliga'},
        'seriea': {'id': 11, 'name': 'Serie A'},
        'portugal': {'id': 32, 'name': 'Primeira Liga'},
        'ligue1': {'id': 13, 'name': 'Ligue 1'},
        'championship': {'id': 10, 'name': 'Championship'},
    }
    
    # Se passar argumento, testar apenas essa liga
    if len(sys.argv) > 1:
        league_key = sys.argv[1].lower()
        if league_key in leagues:
            league = leagues[league_key]
            print(f"\n🧪 Testando acesso para: {league['name']}")
            result = test_access(league['id'], league['name'])
            if result:
                print(f"\n✅ {league['name']}: ACESSO OK - Pode prosseguir com o scraping")
                sys.exit(0)
            else:
                print(f"\n❌ {league['name']}: ACESSO BLOQUEADO - Verifique antes de fazer scraping")
                sys.exit(1)
        else:
            print(f"❌ Liga '{league_key}' não encontrada")
            print(f"Ligas disponíveis: {', '.join(leagues.keys())}")
            sys.exit(1)
    
    # Testar todas as ligas
    results = {}
    for league_key, league in leagues.items():
        print(f"\n{'='*70}")
        print(f"🧪 Testando: {league['name']}")
        print(f"{'='*70}")
        result = test_access(league['id'], league['name'])
        results[league_key] = result
        
        if (league_key, league) != list(leagues.items())[-1]:
            print(f"\n⏳ Aguardando 5 segundos antes do próximo teste...")
            time.sleep(5)
    
    # Resumo
    print(f"\n{'='*70}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*70}")
    
    success_count = 0
    for league_key, league in leagues.items():
        status = "✅ OK" if results[league_key] else "❌ BLOQUEADO"
        print(f"  {league['name']:20s} {status}")
        if results[league_key]:
            success_count += 1
    
    print(f"\n{'='*70}")
    print(f"✅ Acessíveis: {success_count}/{len(leagues)}")
    print(f"{'='*70}")
    
    if success_count == len(leagues):
        print("\n🎉 TODAS AS LIGAS ESTÃO ACESSÍVEIS! Pode prosseguir com o scraping.")
        sys.exit(0)
    elif success_count > 0:
        print(f"\n⚠️  Algumas ligas estão bloqueadas. Teste novamente mais tarde.")
        sys.exit(1)
    else:
        print("\n❌ TODAS AS LIGAS ESTÃO BLOQUEADAS!")
        print("💡 Possíveis soluções:")
        print("   - Aguarde alguns minutos e tente novamente")
        print("   - Atualize o cloudscraper: pip install --upgrade cloudscraper")
        print("   - Verifique sua conexão com a internet")
        sys.exit(1)

if __name__ == "__main__":
    main()

