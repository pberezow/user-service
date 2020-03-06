from django.db import models

# Create your models here.


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    licence_id = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=30, blank=False)

    class Meta:
        unique_together = ('licence_id', 'name')
