from django.db import models

class RobotsCode(models.Model):
    code = models.CharField(max_length=50)

