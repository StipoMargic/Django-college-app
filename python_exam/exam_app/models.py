from django.contrib.auth.models import AbstractUser
from django.db import models


class Korisnik(AbstractUser):
    MENTOR = 'MENTOR'
    STUDENT = 'STUDENT'
    ROLES = (
        (MENTOR, 'Mentor'),
        (STUDENT, 'Student'),
    )

    NONE = 'NONE'
    REDOVNI = 'REDOVNI'
    IZVANREDNI = 'IZVANREDNI'
    STATUS = (
        (NONE, 'None'),
        (REDOVNI, 'Redovni'),
        (IZVANREDNI, 'Izvanredni'),
    )
    role = models.CharField(
        max_length=12,
        choices=ROLES,
        default=STUDENT,
        null=False
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default=NONE,
        null=False
    )

    def __str__(self):
        return self.username


class Predmet(models.Model):
    DA = 'DA'
    NE = 'NE'
    IZBORNI = (
        (DA, 'Da'),
        (NE, 'Ne'),
    )
    ime = models.CharField(max_length=100, null=False)
    kod = models.CharField(max_length=6, null=False)
    program = models.TextField(null=False)
    bodovi = models.IntegerField(null=False)
    sem_redovni = models.IntegerField(null=False)
    sem_izvanredni = models.IntegerField(null=False)
    izborni = models.CharField(max_length=2, choices=IZBORNI, null=False)

    def __str__(self):
        return self.ime


class Upisi(models.Model):
    student = models.ForeignKey(Korisnik, on_delete=models.SET_NULL, null=True)
    predmet = models.ForeignKey(Predmet, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=64)
