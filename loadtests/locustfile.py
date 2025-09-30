import json
from locust import HttpUser, task, between

class SymcompUser(HttpUser):
    wait_time = between(1, 3) 
    
    def on_start(self):
        self.login()
    
    def login(self):
        usuario_dados = {
            "email": "joao@example.com",
            "password": "SenhaSegura123",
            "name": "João Vitor Fernandes Domingues"
        }

        self.client.post("/api/register/", json=usuario_dados)
    
    @task(2)
    def view_activities(self):
        self.client.get("/api/atividade/")
    
    @task(1)
    def view_speakers(self):
        self.client.get("/api/palestrante/")
    
    @task(1)
    def get_certificates(self):
        self.client.get("/api/certificado/")
