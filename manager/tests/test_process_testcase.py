from django.test import TestCase

from manager.models import Process

from user.models import UserProfile, Address


# Create your tests here.
# =======================
class ProcessTestCase(TestCase):
    def get_process_from_api(self):
        process_data = {
            "user": 1,
            "protocol": "00123456789",
            "entry_date": "2021-10-31",
            "service": "craf",
            "status": "pending",
            "om": "2º Batalhão de Infantaria Motorizado (Escola)",
            "gru_status": "pending",
            "gru_compensation_date": None,
            "pce": {
                "name": "G2c",
                "manufacturer": "Taurus",
                "pce_type": "firearm",
                "quantity": 1
            }
        }

        return self.client.post(
            "/process/",
            data=process_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.user_profile.authorization_token
        )

    def setUp(self):
        user_data = {
            "email": "fulanus.aleatorius@gmail.com",
            "password": "123456",
            "first_name": "Fulanus",
            "last_name": "Aleatorius",
        }
        user_profile_data = {
            "full_name": "Fulanus Maximus Aleatorius",
            "email": "fulanus.aleatorius@gmail.com",
            "birthday": "1990-01-01",
            "cpf": "123.456.789-00",
            "rg": "1234567890",
        }
        address_data = {
            "address": "Rua Romanus",
            "number": "100",
            "complement": "Casa 01",
            "zip_code": "12345-678",
            "neighborhood": "Vila Romana",
            "city": "Roma",
            "uf": "RJ"
        }

        user = UserProfile.create_user(user_data)
        self.address = Address.objects.create(**address_data)

        self.user_profile = UserProfile.objects.create(
            user=user,
            address=self.address,
            **user_profile_data
        )

    def test_create_process_from_api(self):
        response = self.get_process_from_api()

        self.assertEquals(response.status_code, 201, 'Criação de processos retornou outro status!')
        process = Process.objects.get(id=response.json().get('id'))

        self.assertEquals("craf", process.service, 'Tipo de serviço do processo não está igual!')
        self.assertEquals("pending", process.status, 'Status do processo não está igual!')
        self.assertEquals(process.user, self.user_profile, 'Usuário do processo não é o mesmo!')

    def test_update_process_from_api(self):
        response = self.get_process_from_api()
        process = Process.objects.get(id=response.json().get('id'))

        new_data = {
            "status": "in_analysis",
            "gru_status": "payed",
            "gru_compensation_date": "2021-10-31"
        }
        response = self.client.patch(
            '/process/{}/'.format(process.pk),
            data=new_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.user_profile.authorization_token
        )

        self.assertEquals(response.status_code, 202, 'Atualização de processo retornou outro status!')
        process.refresh_from_db()

        self.assertEquals(new_data.get("status"), process.status, 'Status do processo não foi alterado!')
        self.assertEquals(new_data.get("gru_status"), process.gru_status, 'Status da GRU do processo não foi alterado!')
        self.assertEquals(
            new_data.get("gru_compensation_date"),
            process.gru_compensation_date.strftime("%Y-%m-%d"),
            'Data da compensação da GRU não foi alterada!'
        )

    def test_delete_process_from_api(self):
        response = self.get_process_from_api()
        process = Process.objects.get(id=response.json().get('id'))

        response = self.client.delete(
            '/process/{}/'.format(process.pk),
            HTTP_AUTHORIZATION=self.user_profile.authorization_token
        )
        self.assertEquals(response.status_code, 204, 'Remoção de processo retornou outro status!')

        process_exists = Process.objects.filter(id=process.id).exists()
        self.assertFalse(process_exists, 'Processo não foi removido do sistema!')
