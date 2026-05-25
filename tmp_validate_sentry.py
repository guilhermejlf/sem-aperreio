import urllib.request
import json

print("=== Validacao Sentry ===\n")

# 1. Healthcheck basico
print("1. Healthcheck basico:")
try:
    req = urllib.request.Request('https://campo-valor-production.up.railway.app/api/health/')
    with urllib.request.urlopen(req, timeout=15) as response:
        body = json.loads(response.read().decode())
        print(f"   Status: {body.get('status')}")
        print(f"   Version: {body.get('version')}")
        print(f"   ✅ OK")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Healthcheck detalhado
print("\n2. Healthcheck detalhado:")
try:
    req = urllib.request.Request('https://campo-valor-production.up.railway.app/api/health/detailed/')
    req.add_header('Origin', 'https://sem-aperreio.vercel.app')
    with urllib.request.urlopen(req, timeout=15) as response:
        body = json.loads(response.read().decode())
        print(f"   Overall: {body.get('status')}")
        print(f"   Version: {body.get('version')}")
        for check, info in body.get('checks', {}).items():
            status = info.get('status', 'unknown')
            icon = '✅' if status in ('ok', 'not_configured') else '❌'
            print(f"   {icon} {check}: {status}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. CORS preflight
print("\n3. CORS preflight:")
try:
    req = urllib.request.Request(
        'https://campo-valor-production.up.railway.app/api/health/',
        method='OPTIONS'
    )
    req.add_header('Origin', 'https://sem-aperreio.vercel.app')
    req.add_header('Access-Control-Request-Method', 'GET')
    with urllib.request.urlopen(req, timeout=15) as response:
        acao = response.getheader('Access-Control-Allow-Origin')
        print(f"   Access-Control-Allow-Origin: {acao}")
        print(f"   {'✅ OK' if acao else '❌ Missing'}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 4. Check frontend
print("\n4. Frontend Vercel:")
try:
    req = urllib.request.Request('https://sem-aperreio.vercel.app/')
    with urllib.request.urlopen(req, timeout=15) as response:
        print(f"   Status: {response.status}")
        print(f"   ✅ OK")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n=== Instrucoes para validar Sentry ===")
print("1. Abra https://sem-aperreio.vercel.app no Chrome")
print("2. Abra DevTools (F12) → Console")
print("3. Procure por: '[Sentry] Initialized'")
print("4. Se nao aparecer, faca logout/login (tokens expiraram)")
print("5. No console do browser, execute: throw new Error('teste sentry')")
print("6. Verifique o dashboard do Sentry em ~30 segundos")
print("7. Para testar backend, acesse: https://campo-valor-production.up.railway.app/api/health/error/")
print("   (se existir um endpoint de teste)")
