from django.core.mail import EmailMessage

class NoreplyEmail:
    REMETENTE = "noreply@symcomp.ime.usp.br"

    def __init__(self, assunto: str, conteudo: str, destinatarios: list[str], anexos_path: list[str] = None):
        self.assunto = assunto
        self.conteudo = conteudo
        self.destinatarios = destinatarios
        self.anexos_path = anexos_path or []

    def send(self):
        email = EmailMessage(subject=self.assunto, body=self.conteudo, from_email=self.REMETENTE, to=self.destinatarios)

        for anexo in self.anexos_path:
            email.attach_file(anexo)
        
        email.send(fail_silently=False)