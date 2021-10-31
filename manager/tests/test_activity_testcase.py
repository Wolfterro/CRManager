from django.test import TestCase

from manager.models import Activity
from manager.serializers import ActivitySerializer


# Create your tests here.
# =======================
class ActivityTestCase(TestCase):
    def test_get_activity_from_api(self):
        response = self.client.get('/activity/')

        self.assertEquals(response.status_code, 200, 'Lista de atividades retornou outro status!')
        qs = Activity.objects.all()

        serializer = ActivitySerializer(qs, many=True)
        self.assertEquals(response.json(), serializer.data, 'Lista de atividades diferente dos dados do banco!')

    def test_get_activity_instance_from_api(self):
        for id in range(1, 4):
            response = self.client.get('/activity/{}/'.format(id))
            self.assertEquals(response.status_code, 200, 'Detalhe de atividade retornou outro status!')
            instance = Activity.objects.get(id=id)

            serializer = ActivitySerializer(instance)
            self.assertEquals(response.json(), serializer.data, 'Detalhe de atividade diferente dos dados do banco!')
