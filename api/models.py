from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from .lib.qr_code_generator import generate_qr_code
import random

## Para geração de usernames (Nota: é possível passar isso para um arquivo de texto depois)
ADJECTIVES = [
    "Happy", "Sad", "Sleepy", "Hungry", "Thirsty", "Excited", "Curious", "Shy",
    "Brave", "Clever", "Lazy", "Nervous", "Grumpy", "Silly", "Goofy", "Epic",
    "Sneaky", "Spicy", "Salty", "Crispy", "Chunky", "Tiny", "Mega", "Ultra",
    "Electric", "Digital", "Pixel", "Cosmic", "Quantum", "Galactic", "Loud",
    "Silent", "Rusty", "Shiny", "Broken", "Weird", "Random", "Fuzzy", "Sticky",
    "Slimy", "Wobbly", "Bouncy", "Floating", "Melty", "Explosive", "Turbo",
    "Invisible", "Obvious", "Secret", "Illegal", "Confused", "Chaotic"
]

NOUNS = [
    "Potato", "Pickle", "Taco", "Pizza", "Donut", "Burger", "Cookie",
    "Noodle", "Toast", "Pineapple", "Pumpkin", "Cabbage", "Cheese", "Onion",
    "Penguin", "Duck", "Llama", "Cat", "Dog", "Hamster", "Sloth", "Koala",
    "Tiger", "Shark", "Octopus", "Dolphin", "Dragon", "Unicorn", "Wizard",
    "Ninja", "Pirate", "Knight", "Robot", "Alien", "Zombie", "Vampire", "Ghost",
    "Goblin", "Troll", "Gnome", "Witch", "Demon", "Angel", "King", "Queen",
    "Prince", "Princess", "Lord", "Overlord", "Captain", "Doctor", "Professor"
]

class Link(models.Model):
    domain = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.domain
    
class Papel(models.TextChoices):
    PRESIDENTE = 'presidente'
    ORGANIZADOR = 'organizador'
    PALESTRANTE = 'palestrante'
    PARTICIPANTE = 'participante'

class StatusAtividade(models.TextChoices):
    PROVISORIA = 'provisoria'
    CONFIRMADA = 'confirmada'

class TipoAtividade(models.TextChoices):
    PALESTRA = 'palestra'
    ENCERRAMENTO = 'encerramento'
    CONVERSA = 'conversa'
    COFFEE_BREAK = 'coffee_break'

class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    papel = models.CharField(max_length=30, choices=Papel.choices, default=Papel.PARTICIPANTE)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_papel_display()}"
    
class DesignacaoDePapel(models.Model):
    email = models.EmailField(unique=True)
    papel = models.CharField(max_length=30, choices=Papel.choices)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} → {self.get_papel_display()}"

class Palestrante(models.Model):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255)
    ocupacao = models.CharField(max_length=255)
    biografia = models.TextField()
    link_apresentacao = models.URLField()
    foto_url = models.URLField()
    foto_alt = models.CharField(max_length=255)
    links = models.ManyToManyField(Link, related_name="palestrantes")

    def __str__(self):
        return self.nome


class UserManager(BaseUserManager):
    """
    User Manager customizado, onde email é o identificador único.
    Implementa geração de username customizado
    """
    def _generate_unique_username(self):
        """
        Gera um username único da lista de palavras
        """
        while True:
            adjective = random.choice(ADJECTIVES).capitalize()
            noun = random.choice(NOUNS).capitalize()
            number = random.randint(1000, 9999)

            username = f"{adjective}{noun}{number}"
            
            if not User.objects.filter(username=username).exists():
                return username
            
    def create_user(self, email, name, password=None, **kwargs):
        if not email:
            raise ValueError("O email é obrigatório.")
        if not name:
            raise ValueError("O nome completo é obrigatório.")
        email = self.normalize_email(email)

        # Possibilita nomes customizados, indicado apenas para admins/palestrantes/etc
        if 'username' not in kwargs:
            kwargs['username'] = self._generate_unique_username()

        user = self.model(email=email, name=name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **kwargs):
        # Cria superusuário e dá acesso máximo
        user = self.create_user(email, name, password, **kwargs)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.eh_verificado = True
        user.eh_organizador = True
        user.eh_presidente = True
        
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """
    Model de Usuário. Estende o Usuário do Django pelo AbstractUser.
    """
    name = models.CharField("Nome Completo", max_length=255)
    email = models.EmailField("Email", unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True) # Revisar depois
    
    eh_verificado = models.BooleanField(default=False)
    eh_organizador = models.BooleanField(default=False)
    eh_presidente = models.BooleanField(default=False)
    
    def verifica_email():
        pass
    
    USERNAME_FIELD = 'email' # id principal
    REQUIRED_FIELDS = ['name']

    # Linka o manager com o model
    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_user(self, email):
        try:
            return User.objects.get(email=email).id
        except User.DoesNotExist:
            return None

class Jogador(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="jogador"
    )

    pontos = models.IntegerField(default=0)

    def __str__(self):
        return f'Jogador {self.user.username}'
    
    def ganha_pontos(self, valor : int):
        """Adiciona pontos à pontuação do jogador"""
        if valor > 0:
            self.pontos += valor
            self.save()

class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_codes")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Code {self.code} for {self.user.email}"

    class Meta:
        ordering = ['-created_at']

class Atividade(models.Model):
    tipo = models.CharField(max_length=30, choices=TipoAtividade.choices)
    status = models.CharField(max_length=30, choices=StatusAtividade.choices, default=StatusAtividade.PROVISORIA)
    comeca_as = models.DateTimeField(unique=True)
    termina_as = models.DateTimeField(unique=True)
    qr_code = models.ImageField(upload_to='qr_codes', null=True, blank=True)

    def generate_qr_data(self) -> str:
        return (
            f"Atividade: {self.get_tipo_display()}\n"
            f"Status: {self.get_status_display()}\n"
            f"Início: {self.comeca_as.strftime('%d/%m/%Y %H:%M')}\n"
            f"Término: {self.termina_as.strftime('%d/%m/%Y %H:%M')}"
        )

    def generate_qr_code(self):
        if not self.qr_code:
            qr_data = self.generate_qr_data()
            filename, image_file = generate_qr_code(qr_data)
            self.qr_code.save(filename.split('/')[-1], image_file, save=False)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.comeca_as.strftime('%d/%m/%Y %H:%M')}"

class ActivityHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Atividade, on_delete=models.CASCADE)

    @classmethod
    def get_hours(self, name : str):
        hours = (
            ActivityHistory.objects
            .filter(user__name=name)
            .annotate(duracao=F('activity__termina_as') - F('activity__comeca_as'))
            .aggregate(total=Sum('duracao'))
        )
        
        if hours['total'] is None:
            return 0
        return int(hours['total'].total_seconds()/3600)
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
