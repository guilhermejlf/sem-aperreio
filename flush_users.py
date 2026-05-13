import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.production')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

count = User.objects.count()
print(f"Usuarios encontrados: {count}")

if count > 0:
    User.objects.all().delete()
    print("Todos os usuarios foram excluidos.")
else:
    print("Nenhum usuario para excluir.")
