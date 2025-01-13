from django.db import models


class runningServers(models.Model):
    serverID = models.CharField(max_length=300)
# Create your models here.
