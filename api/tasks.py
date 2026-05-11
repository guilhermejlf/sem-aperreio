try:
    from celery import shared_task
except ImportError:
    # Dummy decorator for local dev without Celery installed
    def shared_task(func=None, **kwargs):
        if func:
            return func
        return lambda f: f

from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.conf import settings
from .models import Gasto, MetaGasto
from datetime import timedelta
from decimal import Decimal


@shared_task
def send_weekly_reminder():
    """
    Envia email semanal com resumo dos gastos da semana anterior.
    """
    hoje = timezone.now().date()
    # Semana anterior (segunda a domingo)
    inicio_semana = hoje - timedelta(days=hoje.weekday() + 7)
    fim_semana = inicio_semana + timedelta(days=6)

    email_messages = []

    for user in User.objects.filter(gastos__data__range=(inicio_semana, fim_semana)).distinct():
        # Total gasto na semana
        total = Gasto.objects.filter(
            user=user,
            data__range=(inicio_semana, fim_semana)
        ).aggregate(total=Sum('valor'))['total'] or 0

        # Categoria mais gasta
        cat_mais_gasta = Gasto.objects.filter(
            user=user,
            data__range=(inicio_semana, fim_semana)
        ).values('categoria').annotate(
            total=Sum('valor')
        ).order_by('-total').first()

        # Meta mais próxima do limite
        mes_atual = hoje.month
        ano_atual = hoje.year
        metas = MetaGasto.objects.filter(user=user, mes=mes_atual, ano=ano_atual)
        meta_alerta = None
        for meta in metas:
            if meta.valor_meta and meta.valor_meta > 0:
                pct = (meta.gasto_realizado / float(meta.valor_meta)) * 100
                if pct > 80:
                    meta_alerta = meta
                    break

        # Renderizar email
        cat_nome = dict(Gasto.CATEGORIAS_CHOICES).get(cat_mais_gasta['categoria'], 'Outros') if cat_mais_gasta else 'Nenhuma'
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')

        message = f"""Olá {user.first_name or user.username}!

Aqui está o resumo da semana passada:

Total gasto: R$ {total:.2f}
Categoria mais gasta: {cat_nome}
{'Meta próxima do limite: ' + meta_alerta.categoria_nome if meta_alerta else 'Nenhuma meta próxima do limite.'}

Acesse o app: {frontend_url}"""

        email_messages.append((
            'Sem Aperreio — Resumo Semanal',
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@semaperreio.app'),
            [user.email],
        ))

    if email_messages:
        send_mass_mail(email_messages, fail_silently=True)

    return f"Lembretes enviados para {len(email_messages)} usuário(s)."


@shared_task
def check_monthly_average():
    """
    Verifica se gasto do mês atual ultrapassa média dos últimos 6 meses + 20%.
    Envia email de alerta se sim.
    """
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    # Período dos últimos 6 meses completos
    meses_anteriores = []
    for i in range(1, 7):
        mes = mes_atual - i
        ano = ano_atual
        if mes <= 0:
            mes += 12
            ano -= 1
        meses_anteriores.append((mes, ano))

    email_messages = []

    for user in User.objects.all():
        # Calcular média dos últimos 6 meses
        totais_meses = []
        for mes, ano in meses_anteriores:
            total = Gasto.objects.filter(
                user=user,
                data__month=mes,
                data__year=ano
            ).aggregate(total=Sum('valor'))['total'] or 0
            totais_meses.append(total)

        if not totais_meses or all(t == 0 for t in totais_meses):
            continue

        media = sum(totais_meses) / len(totais_meses)
        if media == 0:
            continue

        # Gasto do mês atual
        gasto_atual = Gasto.objects.filter(
            user=user,
            data__month=mes_atual,
            data__year=ano_atual
        ).aggregate(total=Sum('valor'))['total'] or 0

        # Verificar se ultrapassou 120% da média
        if gasto_atual > media * Decimal('1.2'):
            pct_acima = ((gasto_atual - media) / media) * 100

            # Identificar categoria que mais subiu
            cat_mais_gasta = Gasto.objects.filter(
                user=user,
                data__month=mes_atual,
                data__year=ano_atual
            ).values('categoria').annotate(
                total=Sum('valor')
            ).order_by('-total').first()
            cat_nome = dict(Gasto.CATEGORIAS_CHOICES).get(cat_mais_gasta['categoria'], 'Outros') if cat_mais_gasta else 'Geral'

            message = f"""Olá {user.first_name or user.username}!

⚠️ Alerta: seu gasto este mês está {pct_acima:.0f}% acima da média histórica.

Valores:
- Este mês: R$ {gasto_atual:.2f}
- Média dos últimos 6 meses: R$ {media:.2f}

Categoria que mais contribuiu: {cat_nome}

Acesse o dashboard para ver detalhes: {getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')}"""

            email_messages.append((
                'Sem Aperreio — Alerta de Gastos',
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@semaperreio.app'),
                [user.email],
            ))

    if email_messages:
        send_mass_mail(email_messages, fail_silently=True)

    return f"Verificação concluída. {len(email_messages)} alerta(s) enviado(s)."


@shared_task
def send_email(subject, to_email, template_name, context=None):
    """
    Envia email usando template HTML.
    """
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags

    html_message = render_to_string(f'emails/{template_name}.html', context or {})
    plain_message = strip_tags(html_message)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@semaperreio.app'),
        recipient_list=[to_email],
        html_message=html_message,
        fail_silently=True,
    )
