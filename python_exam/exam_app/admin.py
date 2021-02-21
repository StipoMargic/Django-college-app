from django.contrib import admin

from .models import Upisi, Korisnik, Predmet

admin.site.register(Korisnik)
admin.site.register(Predmet)
admin.site.register(Upisi)