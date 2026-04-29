#!/usr/bin/env python
"""
Script de atualização de dados: copia `data` → `data_competencia`
para todos os Gastos onde data_competencia está vazio.

Uso:
    cd backend && python scripts/migrate_data_competencia.py
"""

import os
import sys
import django

# Garantir que o diretório 'backend' esteja no path ANTES da raiz do projeto
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import Gasto


def run_migration():
    """Copia `data` para `data_competencia` quando este estiver vazio."""
    gastos_para_atualizar = Gasto.objects.filter(data_competencia__isnull=True)
    count = gastos_para_atualizar.count()

    if count == 0:
        print("Nenhum gasto precisa de atualização (todos já possuem data_competencia).")
        return

    print(f"Atualizando {count} gastos: data → data_competencia ...")

    updated = 0
    for gasto in gastos_para_atualizar.iterator():
        gasto.data_competencia = gasto.data
        gasto.save(update_fields=["data_competencia"])
        updated += 1

        if updated % 100 == 0:
            print(f"  → {updated}/{count} processados...")

    print(f"✅ Concluído! {updated} registros atualizados.")


if __name__ == "__main__":
    run_migration()
