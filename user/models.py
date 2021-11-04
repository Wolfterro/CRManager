from django.db import models
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from user.utils import get_random_hash


# Create your models here.
# ========================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")

    full_name = models.CharField(max_length=150, default=None, verbose_name="Nome completo")
    email = models.EmailField(default=None, verbose_name="E-Mail")
    photo = models.URLField(default=None, blank=True, null=True, verbose_name="Foto")

    birthday = models.DateField(default=None, verbose_name="Data de nascimento")
    cpf = models.CharField(max_length=16, default=None, verbose_name="CPF")
    rg = models.CharField(max_length=20, default=None, verbose_name="RG")

    address = models.ForeignKey('user.Address', on_delete=models.CASCADE, verbose_name="Endereço do Acervo", related_name='user_address')
    second_address = models.ForeignKey('user.Address', default=None, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Segundo Endereço do Acervo", related_name='second_user_address')

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return "{} [{}]".format(self.full_name, self.cpf)

    def save(self, **kwargs):
        super(UserProfile, self).save(**kwargs)

        if not hasattr(self.user, 'auth_token'):
            Token.objects.create(user=self.user)

    def city_and_uf(self):
        return self.address.get_formatted_city_and_uf()

    # Properties
    # ----------
    @property
    def authorization_token(self):
        if hasattr(self.user, 'auth_token'):
            return "Token {}".format(self.user.auth_token.key)

        return None

    @property
    def cr(self):
        cr = self.cr_set.first()
        if not cr:
            return None

        return {
            "number": cr.number,
            "expiration_date": cr.expiration_date,
            "rm": cr.rm,
            "activities": [x.name for x in cr.activities.all()]
        }

    # Static Methods
    # --------------
    @staticmethod
    def create_user(data):
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        email_user = email.split("@")[0]
        random_hash = get_random_hash(8)
        username = "{}.{}".format(email_user, random_hash)

        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )


class Address(models.Model):
    address = models.CharField(max_length=255, default=None, verbose_name="Endereço")
    number = models.CharField(max_length=16, default=None, verbose_name="Número")
    complement = models.CharField(max_length= 150, default=None, blank=True, null=True, verbose_name="Complemento")

    neighborhood = models.CharField(max_length=50, default=None, verbose_name="Bairro")
    zip_code = models.CharField(max_length=12, default=None, verbose_name="CEP")
    city = models.CharField(max_length=100, default=None, verbose_name="Cidade")
    uf = models.CharField(max_length=2, default=None, verbose_name="UF")

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return self.get_formatted_address()

    def get_formatted_address(self):
        complement_and_cep = " ({}) CEP: {}".format(
            self.complement,
            self.zip_code
        ) if self.complement else " CEP: {}".format(self.zip_code)

        return "{}, {}{} - {} - {}, {}".format(
            self.address,
            self.number,
            complement_and_cep,
            self.neighborhood,
            self.city,
            self.uf
        )

    def get_formatted_city_and_uf(self):
        return "{} - {}".format(self.city, self.uf)
