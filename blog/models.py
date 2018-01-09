from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from itsdangerous import URLSafeTimedSerializer as utsr
import base64


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=True)
    phone_number = models.CharField(
        _('手机号码'),
        unique=True,
        max_length=11,
        error_messages={
            'unique': _("该电话号码已存在"),
        },
    )

    class Meta(AbstractUser.Meta):
        pass
