from django.db import models
from django.contrib.auth.models import User


class Tema(models.Model) :
    titulo = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.CharField(max_length=700)
    
    def __str__(self):
        return f"{self.titulo}"
    
class Sala(models.Model) :
    STATUS_ESCOLHA = [
        ('aberta', 'Inscrições Abertas'),
        ('sorteio', 'Sorteio Realizado'),
        ('andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
    ]
    
    nome = models.CharField(max_length=100, blank=False, null=False)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_ESCOLHA, default='aberta')
    participantes = models.ManyToManyField(User, related_name='salas_inscritas', blank=True)
    valor_premiacao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)
    duracao_horas = models.IntegerField(default=24)
    inicio_atividades = models.DateTimeField(null=True, blank=True)
    temas = models.ManyToManyField(Tema, related_name='salas', blank=True)
    
    def __str__(self):
        return self.nome


    
class Grupo(models.Model) :
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='grupos')
    nome = models.CharField(max_length=100, null=False, blank=False)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, blank=True)
    membros = models.ManyToManyField(User, related_name='meus_grupos')
    lider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liderando', verbose_name="Cabeça de Chave")
    pontuacao_total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.nome} ({self.sala.nome})"

class Avaliacao(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='avaliacoes')
    jurado = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    comentario = models.TextField(blank=True)

    class Meta:
        unique_together = ['grupo', 'jurado']

    def __str__(self):
        return f"Nota {self.nota} - {self.grupo.nome}"
    

class Entrega(models.Model) :
    grupo = models.OneToOneField(Grupo, on_delete=models.CASCADE, related_name='entrega')
    link_projeto = models.URLField(max_length=1000)
    comentarios = models.TextField(blank=True, null=True)
    data_entrega = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entrega do Grupo: {self.grupo.nome}"