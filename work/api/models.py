from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    namecategory = models.CharField(max_length=200)


class Parametrs(models.Model):
    сontent = models.FloatField()
    humidity = models.FloatField()
    contentmass = models.FloatField()
    heatmass = models.FloatField()


class Component(models.Model):
    title_categories = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='categorys',
    )
    parametrs = models.OneToOneField(
        Parametrs,
        on_delete=models.CASCADE,
        related_name='parametr',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='components'
    )

    def __str__(self) -> str:
        return self.title_categories