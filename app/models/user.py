from pybald.db import models


class User(models.Model):
    username = models.Column(models.Unicode(40), unique=True, key='username')
    email = models.Column(models.Unicode(255), unique=True, key='email')
    access_token = models.Column(models.Unicode(40), unique=True)
    date_created = models.Column(models.TIMESTAMP,
                                 default=models.func.current_timestamp())
    can_login = True
