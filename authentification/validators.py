# authentification/validators.py

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                _("Le mot de passe doit contenir au moins 10 caractères."),
                code='password_too_short',
            )
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une lettre majuscule."),
                code='password_no_upper',
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins une lettre minuscule."),
                code='password_no_lower',
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un chiffre."),
                code='password_no_digit',
            )
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(
                _("Le mot de passe doit contenir au moins un symbole."),
                code='password_no_symbol',
            )
        # Liste des symboles interdits pour éviter les injections
        forbidden_symbols = ['<','>',',', '--', '/*', '*/', '@@', 'char', 'nchar', 'varchar', 'nvarchar', 'alter', 'begin', 'cast', 'create', 'cursor', 'declare', 'delete', 'drop', 'end', 'exec', 'fetch', 'insert', 'kill', 'select', 'sys', 'sysobjects', 'syscolumns', 'table', 'update']

        for symbol in forbidden_symbols:
            if symbol in password:
                raise ValidationError(
                    _("Le mot de passe contient un symbole interdit."),
                    code='password_forbidden_symbol',
                )

    def get_help_text(self):
        return _(
            "Votre mot de passe doit contenir au moins 10 caractères, une lettre majuscule, "
            "une lettre minuscule, un chiffre et un symbole. Il ne doit pas contenir de symboles interdits."
        )
