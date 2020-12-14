from django.db import models
from general.models import User


class Ticket(models.Model):
    type = models.CharField(max_length=45, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.type


class TicketWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.user} has {self.amount} of {self.ticket.type}'

    class Meta:
        ordering = ['user', 'ticket']  # For the admin page
        unique_together = ['user', 'ticket']
