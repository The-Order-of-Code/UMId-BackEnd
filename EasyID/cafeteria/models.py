from django.db import models
from general.models import User


class Profile(models.Model):
	name = models.CharField(unique=True, max_length=45)

	def __str__(self):
		return self.name


class TicketType(models.Model):
	profiles = models.ManyToManyField(Profile)
	name = models.CharField(max_length=45, unique=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.name


class Ticket(models.Model):
	type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='owner')  # Set null, for finding lost tickets, either this or do nothing, but finding student-less tickets becomes more taxing
	code = models.CharField(max_length=45, blank=True)
	date = models.DateField(null=True, blank=True)
	hash = models.CharField(max_length=45, blank=True)

	def __str__(self):
		return f"{self.user.username}'s {self.type.name} ticket"

	class Meta:
		ordering = ['user', 'type']


class TicketLog(models.Model):
	#same 5 lines as ticket, working around some django stuff with inheritance
	type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='log_owner')
	code = models.CharField(max_length=45, blank=True)
	date = models.DateField(null=True, blank=True)
	hash = models.CharField(max_length=45, blank=True)

	employee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='validator')  # do nothing, so we can keep track of employees
	consumed = models.DateTimeField(auto_now_add=True)
	operation = models.CharField(max_length=45)

	@staticmethod
	def fromTicket(ticket, employee, operation):
		return TicketLog(type=ticket.type, user=ticket.user, code=ticket.code, date=ticket.date, hash=ticket.hash, employee=employee, operation=operation)

	def __str__(self):
		return f"<TicketLog {self.id}: logged on {self.consumed}>"
