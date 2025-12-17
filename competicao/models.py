from django.db import models
from django.contrib.auth.models import User

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
    participantes = models.ManyToManyField(User, related_name='salas_inscritas')
    valor_premiacao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome

class Tema(models.Model) :
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='temas')
    titulo = models.CharField(max_length=200, blank=False, null=False)
    descricao = models.CharField(max_length=700)
    
    def __str__(self):
        return f"{self.titulo} - {self.sala.nome}"
    
class Grupo(models.Model) :
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='grupos')
    nome = models.CharField(max_length=100, null=False, blank=False)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, blank=True)
    membros = models.ManyToManyField(User, related_name='meus_grupos')
    cabeca_de_chave = models.BooleanField(default=False)
    pontuacao_total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.nome} ({self.sala.nome})"

class Avaliacao(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='avaliacoes')
    jurado = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    comentario = models.TextField(blank=True)

    class Meta:
        unique_together = ('grupo', 'jurado')

    def __str__(self):
        return f"Nota {self.nota} - {self.grupo.nome}"