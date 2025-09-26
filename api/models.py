from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from .lib.qr_code_generator import generate_qr_code

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
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("O email é obrigatório.")
        if not name:
            raise ValueError("O nome completo é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, is_active=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_user(self, email):
        try:
            return User.objects.get(email=email).id
        except User.DoesNotExist:
            return None

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
