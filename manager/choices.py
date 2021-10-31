RM_CHOICES = (
    ('1', '1ª RM'),
    ('2', '2ª RM'),
    ('3', '3ª RM'),
    ('4', '4ª RM'),
    ('5', '5ª RM'),
    ('6', '6ª RM'),
    ('7', '7ª RM'),
    ('8', '8ª RM'),
    ('9', '9ª RM'),
    ('10', '10ª RM'),
    ('11', '11ª RM'),
    ('12', '12ª RM'),
)

SERVICE_CHOICES = (
    ('cr_concession', "Concessão de CR"),
    ('purchase_authorization', "Autorização de Compra"),
    ('craf', "CRAF"),
    ('gt', "Guia de Trânsito"),
    ('register', "Apostilamento"),
)

STATUS_CHOICES = (
    ('deferred', "Deferido"),
    ('in_analysis', "Em Análise"),
    ('pending', "Pendente"),
    ('rejected', "Indeferido"),
    ('refunded', "Restituído"),
    ('other', "Outro"),
)

GRU_STATUS_CHOICES = (
    ('pending', "Pendente"),
    ('payed', "Paga"),
    ('other', "Outro")
)

PCE_TYPE_CHOICES = (
    ('firearm', "Arma de Fogo"),
    ('ammo', "Munição"),
    ('reloading_tool', "Máquina de Recarga"),
    ('dies', "Dies"),
    ('other', "Outro")
)
