from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, PerfilUsuario, DesignacaoDePapel, Papel

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        try:
            designacao = DesignacaoDePapel.objects.get(email=instance.email)
            papel = designacao.papel
        except DesignacaoDePapel.DoesNotExist:
            papel = Papel.PARTICIPANTE
        
        PerfilUsuario.objects.create(user=instance, papel=papel)

@receiver(post_save, sender=User)
def aplicar_designacao_ao_registrar_usuario(sender, instance, created, **kwargs):
    if created:
        try:
            designacao = DesignacaoDePapel.objects.get(email=instance.email)
            PerfilUsuario.objects.create(user=instance, papel=designacao.papel)
            designacao.delete()
        except DesignacaoDePapel.DoesNotExist:
            PerfilUsuario.objects.create(user=instance)
