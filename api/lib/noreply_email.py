from django.core.mail import send_mail

class NoreplyEmail:
    REMETENTE = "noreply@symcomp.ime.usp.br"

    def __init__(self, assunto: str, conteudo: str, destinatarios: list[str]):
        self.assunto = assunto
        self.conteudo = conteudo
        self.destinatarios = destinatarios

    def send(self):
        send_mail(subject=self.assunto, message=self.conteudo, from_email=self.REMETENTE, recipient_list=self.destinatarios, fail_silently=False)