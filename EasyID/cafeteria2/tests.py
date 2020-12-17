from django.test import TestCase
from cafeteria2.models import *

# Create your tests here.

p1 = Profile(name='Student')
p1.save()
p2 = Profile(name='Teacher')
p2.save()
p3 = Profile(name='Worker')
p3.save()

tt = TicketType()
tt.save()

tt.profiles.add(p1, p3)
for t in tt.profiles.all():
    print(t.name())


