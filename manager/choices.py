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
    ('address_update', "Atualização de Endereço do Acervo"),
    ('doc_update', "Atualização de Documento Pessoal"),
    ('activity_update', "Atualização de Tipo de Atividade"),
    ('cr_cancel', "Cancelamento de CR para Pessoa Física"),
    ('second_address_add', "Inclusão de 2º Endereço de Acervo"),
    ('purchase_authorization', "Autorização de Compra"),
    ('craf', "CRAF"),
    ('gt', "Guia de Trânsito"),
    ('register', "Apostilamento"),
    ('import_authorization', "Autorização de Aquisição de PCE por Importação (CII)"),
    ('procurator_add', "Instituir Procurador para Pessoa Física"),
    ('revalidation', "Revalidação para Pessoa Física")
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
