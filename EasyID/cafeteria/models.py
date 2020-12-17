from django.db import models
from general.models import User


class Profile(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name


class TicketType(models.Model):
    profiles = models.ManyToManyField(Profile)
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=45, null=True)
    date = models.DateField(null=True)
    hash = models.CharField(max_length=45, null=True)

    def __str__(self):
        return f"{self.user.username}'s {self.type.name} ticket"

    class Meta:
        ordering = ['user', 'type']
