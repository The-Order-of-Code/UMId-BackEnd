from cafeteria.models import *
from library.models import *
from general.models import *

def insertStudent(User,Student):

    User.save();
    Student.user_id = User.id;
    Student.save();

def updateStudent(NewUser,NewStudent):

    olduser = User.objects.get(pk=NewUser.id);
    olduser.password = NewUser.password;
    olduser.is_superuser = NewUser.is_superuser;
    olduser.username = NewUser.username;
    olduser.first_name = NewUser.first_name;
    olduser.last_name = NewUser.last_name;
    olduser.email = NewUser.email;
    olduser.is_staff = NewUser.is_staff;
    olduser.is_active = NewUser.is_active;
    olduser.date_joined = NewUser.date_joined;
    olduser.fullName = NewUser.fullName;
    olduser.birthDate = NewUser.birthDate;
    olduser.birthParish = NewUser.birthParish;
    olduser.birthMunicipality = NewUser.birthMunicipality;
    olduser.birthDistrict = NewUser.birthDistrict;
    olduser.birthCountry = NewUser.birthCountry;
    olduser.save();

    oldstudent = Student.objects.get(pk=NewUser.id);
    oldstudent.number = NewStudent.number;
    oldstudent.year = NewStudent.year;
    oldstudent.academicYear = NewStudent.academicYear;
    oldstudent.edition = NewStudent.edition;
    oldstudent.specialStatuses = NewStudent.specialStatuses;
    oldstudent.studyPlan = NewStudent.studyPlan;
    oldstudent.course_id = NewStudent.course_id;
    oldstudent.save();


def insertEmployee(User,Employee):

    User.save();
    Employee.user_id = User.id;
    Employee.save();

def updateEmployee(NewUser,NewEmployee):

    olduser = User.objects.get(pk=NewUser.id);
    olduser.password = NewUser.password;
    olduser.is_superuser = NewUser.is_superuser;
    olduser.username = NewUser.username;
    olduser.first_name = NewUser.first_name;
    olduser.last_name = NewUser.last_name;
    olduser.email = NewUser.email;
    olduser.is_staff = NewUser.is_staff;
    olduser.is_active = NewUser.is_active;
    olduser.date_joined = NewUser.date_joined;
    olduser.fullName = NewUser.fullName;
    olduser.birthDate = NewUser.birthDate;
    olduser.birthParish = NewUser.birthParish;
    olduser.birthMunicipality = NewUser.birthMunicipality;
    olduser.birthDistrict = NewUser.birthDistrict;
    olduser.birthCountry = NewUser.birthCountry;
    olduser.save();

    oldemployee = Employee.objects.get(pk=NewUser.id);
    oldemployee.save();


def insertTicketWallet(TicketWallet,Student,Ticket):

    TicketWallet.student_id=Student.id;
    TicketWallet.ticket_id=Ticket.id;
    TicketWallet.save();

def updateTicketWallet(NewTicketWallet):

    oldticketwallet = TicketWallet.objects.get(student_id=NewTicketWallet.student_id, ticket_id=NewTicketWallet.ticket_id);
    oldticketwallet.amount = NewTicketWallet.amount;
    oldticketwallet.save();


def insertReservation(Reservation,Room,User):

    Reservation.user_id=User.id;
    Reservation.room_id=Room.id;
    Reservation.save();

def updateReservation(NewReservation):

    oldreservation = Reservation.objects.get(room_id=NewReservation.room_id, user_id=NewReservation.user_id);
    oldreservation.start=NewReservation.start;
    oldreservation.end=NewReservation.end;
    oldreservation.save();