#!/usr/bin/env python3
"""
Script de validação para testar todas as ligas disponíveis
Testa apenas 1 jogo de cada liga para validar que está funcionando
"""

import subprocess
import sys
from datetime import datetime, timedelta

LEAGUES = {
    'laliga': 'La Liga (Espanha)',
    'bundesliga': 'Bundesliga (Alemanha)',
    'seriea': 'Serie A (Itália)',
    'portugal': 'Primeira Liga (Portugal)',
    'ligue1': 'Ligue 1 (França)',
    'championship': 'Championship (Inglaterra - Série B)',
}

def test_league(league):
    """Testa uma liga específica com 1 jogo"""
    print(f"\n{'='*70}")
    print(f"🧪 TESTANDO: {LEAGUES[league]}")
    print(f"{'='*70}")
    
    # Usar período recente (últimos 30 dias)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    cmd = [
        sys.executable,
        'buscar_estatisticas_multi_liga.py',
        '--liga', league,
        '--inicio', start_date.strftime('%Y-%m-%d'),
        '--fim', end_date.strftime('%Y-%m-%d'),
        '--limit', '1',
        '--test'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Verificar se encontrou dados
            if 'registros de jogadores' in result.stdout:
                # Extrair número de registros
                for line in result.stdout.split('\n'):
                    if 'Total:' in line and 'registros' in line:
                        print(f"✅ SUCESSO: {line.strip()}")
                        return True
            print("⚠️  AVISO: Comando executou mas não encontrou dados")
            print(result.stdout[-500:])  # Últimas 500 chars
            return False
        else:
            print(f"❌ ERRO: Código de saída {result.returncode}")
            print("STDOUT:")
            print(result.stdout[-500:])
            print("\nSTDERR:")
            print(result.stderr[-500:])
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  TIMEOUT: Comando demorou mais de 5 minutos")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def main():
    print("="*70)
    print("🚀 VALIDAÇÃO DE TODAS AS LIGAS")
    print("="*70)
    print("\nEste script testa cada liga com 1 jogo para validar funcionamento.")
    print("Aguarde... isso pode levar alguns minutos.\n")
    
    results = {}
    
    for league in LEAGUES.keys():
        success = test_league(league)
        results[league] = success
    
    # Resumo final
    print(f"\n{'='*70}")
    print("📊 RESUMO FINAL")
    print(f"{'='*70}")
    
    for league, success in results.items():
        status = "✅ OK" if success else "❌ FALHOU"
        print(f"{status} - {LEAGUES[league]}")
    
    total = len(results)
    passed = sum(1 for s in results.values() if s)
    
    print(f"\n✅ Passou: {passed}/{total}")
    print(f"❌ Falhou: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TODAS AS LIGAS ESTÃO FUNCIONANDO!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} liga(s) falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

