from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Gasto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gastos')
    CATEGORIAS_CHOICES = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('moradia', 'Moradia'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('lazer', 'Lazer'),
        ('outros', 'Outros'),
    ]

    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="O valor deve ser maior que zero")]
    )
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS_CHOICES,
        validators=[MaxLengthValidator(50, message="Categoria muito longa")]
    )
    descricao = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        validators=[MaxLengthValidator(200, message="Descrição muito longa")]
    )
    data = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data', '-criado_em']
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'

    def __str__(self):
        return f"{self.get_categoria_display()} - R$ {self.valor}"

    def clean(self):
        # Permitir datas futuras para planejamento
        # Apenas validar se a data não é muito antiga
        um_ano_atras = timezone.now().date().replace(year=timezone.now().date().year - 1)
        if self.data < um_ano_atras:
            raise models.ValidationError("A data não pode ser anterior a um ano")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)