from .noreply_email import NoreplyEmail

class ParticipantCertificateEmail:
    ASSUNTO = "Certificado de Participação"
    CONTEUDO = "Segue o certificado em anexo."

    def __init__(self, destinatario: str, certificado_path: str):
        self.destinario = [destinatario]
        self.certificado_path = [certificado_path]
    
    def send(self):
        noreply_email = NoreplyEmail(self.ASSUNTO, self.CONTEUDO, self.destinario, self.certificado_path)

        noreply_email.send()