from django.test import TestCase

from manager.models import CR

from user.models import UserProfile, Address


# Create your tests here.
# =======================
class CRTestCase(TestCase):
    def get_user_from_api(self):
        user_profile_data = {
            "user": {
                "email": "fulanus.aleatorius2@gmail.com",
                "password": "123456",
                "first_name": "Fulanus",
                "last_name": "Aleatorius"
            },
            "full_name": "Fulanus Maximus Aleatorius 2",
            "email": "fulanus.aleatorius2@gmail.com",
            "birthday": "1990-01-01",
            "cpf": "123.456.789-00",
            "rg": "1234567890",
            "address": {
                "address": "Rua Romanus",
                "number": "100",
                "complement": "Casa 01",
                "zip_code": "12345-678",
                "neighborhood": "Vila Romana",
                "city": "Roma",
                "uf": "RJ"
            },
            "second_address": {
                "address": "Rua Romanus",
                "number": "100",
                "complement": "Casa 02",
                "zip_code": "12345-678",
                "neighborhood": "Vila Romana",
                "city": "Roma",
                "uf": "RJ"
            },
        }

        return self.client.post(
            '/user_profile/',
            data=user_profile_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=self.user_profile.authorization_token
        )

    def get_cr_from_api(self, user_profile):
        cr_data = {
            "user": user_profile.id,
            "number": "000.999.999-99",
            "expiration_date": "2099-01-01",
            "rm": "1",
            "activities": [
                "Tiro Desportivo",
                "Caça",
                "Colecionamento"
            ]
        }

        return self.client.post(
            '/cr/',
            data=cr_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=user_profile.authorization_token
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

    def test_cr_creation_from_api(self):
        response = self.get_user_from_api()
        user_profile = UserProfile.objects.get(id=response.json().get('id'))

        response = self.get_cr_from_api(user_profile)

        self.assertEquals(response.status_code, 201, 'Criação de CR retornou outro status!')
        user_profile.refresh_from_db()
        cr = user_profile.cr_set.first()

        self.assertIsNotNone(cr, 'CR não está associado ao usuário!')
        self.assertEquals(response.json().get('number'), cr.number, 'Número do CR não está igual ao esperado!')

    def test_cr_update_from_api(self):
        response = self.get_user_from_api()
        user_profile = UserProfile.objects.get(id=response.json().get('id'))

        self.get_cr_from_api(user_profile)
        user_profile.refresh_from_db()
        cr = user_profile.cr_set.first()

        new_data = {
            "number": "000.000.000-00",
            "expiration_date": "2050-01-01"
        }
        response = self.client.patch(
            '/cr/{}/'.format(cr.pk),
            data=new_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=user_profile.authorization_token
        )

        self.assertEquals(response.status_code, 202, 'Atualização de CR retornou outro status!')
        cr.refresh_from_db()

        self.assertEquals(new_data.get("number"), cr.number, 'Número do CR não foi alterado!')
        self.assertEquals(new_data.get("expiration_date"), cr.expiration_date.strftime("%Y-%m-%d"), 'Data de validade do CR não foi alterado!')

    def test_cr_delete_from_api(self):
        response = self.get_user_from_api()
        user_profile = UserProfile.objects.get(id=response.json().get('id'))

        self.get_cr_from_api(user_profile)
        user_profile.refresh_from_db()
        cr = user_profile.cr_set.first()

        response = self.client.delete(
            '/cr/{}/'.format(cr.pk),
            HTTP_AUTHORIZATION=user_profile.authorization_token
        )
        self.assertEquals(response.status_code, 204, 'Remoção de CR retornou outro status!')

        cr_exists = CR.objects.filter(id=cr.id).exists()
        self.assertFalse(cr_exists, 'CR não foi removido do sistema!')
