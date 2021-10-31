from django.test import TestCase

from user.models import UserProfile, Address


# Create your tests here.
# =======================
class UserTestCase(TestCase):
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

    def test_user_profile_has_token(self):
        self.assertIsNotNone(self.user_profile.authorization_token, 'Token não existe!')

    def test_user_profile_contains_at_least_one_address(self):
        self.assertIsNotNone(
            self.user_profile.address or self.user_profile.second_address,
            'Usuário não possui ao menos um endereço de acervo!'
        )

    def test_formatted_address(self):
        self.assertIsNotNone(self.address.get_formatted_address(), 'Endereço não possui formatação!')

    def test_formatted_address_city_and_uf(self):
        city_and_uf = self.address.get_formatted_city_and_uf()

        self.assertIsNotNone(city_and_uf, 'Cidade e Estado não existe para o usuário!')
        self.assertEquals(city_and_uf, "Roma - RJ", 'Cidade e Estado são diferentes!')

    def test_user_creation(self):
        user_data = {
            "email": "john.doe@gmail.com",
            "password": "123456",
            "first_name": "John",
            "last_name": "Doe"
        }

        user = UserProfile.create_user(user_data)

        self.assertIsNotNone(user, 'Usuário não foi criado!')
        self.assertEquals(user.email, user_data.get('email'), 'E-Mail do usuário criado é diferente do esperado!')

        username = user.username
        self.assertIn("john.doe", username, 'Username não contém nome do e-mail!')

    def test_user_profile_creation_via_api(self):
        response = self.get_user_from_api()

        self.assertEquals(response.status_code, 201, 'Criação de UserProfile retornou outro status!')
        self.assertIn('token', response.json(), 'A chave de autorização não está presente na resposta de criação!')

    def test_user_profile_patch_via_api(self):
        response = self.get_user_from_api()
        user_profile = UserProfile.objects.get(id=response.json().get('id'))

        new_data = {
            "cpf": "000.000.000-00",
            "rg": "000000000"
        }
        response = self.client.patch(
            '/user_profile/{}/'.format(user_profile.pk),
            data=new_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=user_profile.authorization_token
        )

        self.assertEquals(response.status_code, 202, 'Atualização de UserProfile retornou outro status!')
        user_profile.refresh_from_db()

        self.assertEquals(new_data.get("cpf"), user_profile.cpf, 'CPF do Usuário não foi alterado!')
        self.assertEquals(new_data.get("rg"), user_profile.rg, 'RG do Usuário não foi alterado!')

    def test_user_profile_delete_via_api(self):
        response = self.get_user_from_api()
        user_profile = UserProfile.objects.get(id=response.json().get('id'))

        response = self.client.delete(
            '/user_profile/{}/'.format(user_profile.pk),
            HTTP_AUTHORIZATION=user_profile.authorization_token
        )

        self.assertEquals(response.status_code, 204, 'Remoção de UserProfile retornou outro status!')

        user_profile_exists = UserProfile.objects.filter(id=user_profile.id).exists()
        self.assertFalse(user_profile_exists, 'Usuário não foi removido do sistema!')
