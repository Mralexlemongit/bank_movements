from django.db import models
from users.models import NewUser

class Link(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)

class Institution(models.Model):
    display = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    logo = models.CharField(max_length=100)