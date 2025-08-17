from .noreply_email import NoreplyEmail
from ..models import EmailVerificationCode, User
from .user_validation_code_generator import UserValidationCodeGenerator

class UserValidationCodeEmail:
    ASSUNTO: str = "SYMCOMP - Código de verificação"
    

    def __init__(self, user: User) -> None:
        self.user = user
        self.code = UserValidationCodeGenerator().generate()
    
    def send(self) -> None:
        EmailVerificationCode.objects.create(user=self.user, code=self.code)

        conteudo = f"Seu código de verificação é {self.code}"
        destinatarios = [self.user.email]

        noreply_email = NoreplyEmail(
            assunto=self.ASSUNTO,
            conteudo=conteudo,
            destinatarios=destinatarios
        )

        noreply_email.send()