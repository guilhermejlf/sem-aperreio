"""
Script de migração de dados: copia `data` → `data_competencia` quando vazio.

Uso:
    python manage.py shell < scripts/migrate_data_competencia.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Gasto


def migrar_data_competencia():
    gastos_sem_competencia = Gasto.objects.filter(data_competencia__isnull=True)
    total = gastos_sem_competencia.count()

    if total == 0:
        print("Nenhum gasto precisa de migração. Todos já possuem data_competencia.")
        return

    print(f"Migrando {total} gasto(s): data → data_competencia...")

    atualizados = 0
    for gasto in gastos_sem_competencia.iterator():
        gasto.data_competencia = gasto.data
        gasto.save(update_fields=['data_competencia'])
        atualizados += 1
        if atualizados % 100 == 0:
            print(f"  ...{atualizados}/{total} concluídos")

    print(f"Concluído! {atualizados} registro(s) atualizado(s).")


if __name__ == '__main__':
    migrar_data_competencia()
