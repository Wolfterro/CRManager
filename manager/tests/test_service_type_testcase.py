from django.test import TestCase

from manager.utils import get_service_type_list


# Create your tests here.
# =======================
class ServiceTypeTestCase(TestCase):
    def test_get_activity_from_api(self):
        response = self.client.get('/service_type/')

        self.assertEquals(response.status_code, 200, 'Lista de serviços retornou outro status!')
        service_type_list = get_service_type_list()
        self.assertEquals(response.json(), service_type_list, 'Lista de serviços diferente dos dados do banco!')
