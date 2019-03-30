from django.db import models
from django.core.validators import MinLengthValidator

class State(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "State must be greater than 1 character")]
    )

    def __str__(self):
        return self.name

class City(models.Model):
    nickname = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")]
    )
    population = models.PositiveIntegerField()
    slogan = models.CharField(max_length=300)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.nickname