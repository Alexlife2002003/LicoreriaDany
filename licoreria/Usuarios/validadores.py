from django.core.validators import RegexValidator

rfc_validador = RegexValidator(
    regex='^([A-ZÑ&]{3,4})?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$',
    message='El RFC no tiene un formato válido',
    code='rfc_invalido'
)

nomapellido_validador= RegexValidator(
    regex='^[a-zA-Z]+[a-zA-Z]+$',
    message='no tiene formato valido el nombre',
    code='nom_app_invalido'

)


