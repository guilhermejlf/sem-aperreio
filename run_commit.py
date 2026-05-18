import subprocess
import os
import glob

os.chdir(r'C:\Users\guilherme.freire\Desktop\projeto-ia')

# Clean up temporary files
for temp_file in ['run_tests.py', 'run_build.py', 'build_frontend.py',
                   'test_results.txt', 'test_output.txt', 'pytest_output.txt',
                   'build_status.txt']:
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f'Removed {temp_file}')

# Add all changes
subprocess.run(['git', 'add', '-A'], check=True)

# Commit
result = subprocess.run(
    ['git', 'commit', '-m', 'feat(cache): implementa Redis cache com fallback LocMem\n\n- Configura CACHES no settings com Redis em prod e LocMem em dev\n- Adiciona cache_utils.py com cached_view, invalidate_gastos, invalidate_receitas\n- Aplica cache nos endpoints dashboard, gastos, receitas, extrato\n- Invalida cache automaticamente em mutacoes POST/PUT/DELETE\n- Corrige serializacao de DRF Response para evitar erros de pickle\n- Usa hash MD5 para chaves de cache seguras\n- Adiciona django-redis e Faker ao requirements.txt'],
    capture_output=True, text=True
)

print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr)
print(f'Commit return code: {result.returncode}')
