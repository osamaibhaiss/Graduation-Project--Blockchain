from django.contrib import admin
from .models import Voter, Login, Group, Result, Election

admin.site.register(Voter)
admin.site.register(Login)
admin.site.register(Group)
admin.site.register(Result)
admin.site.register(Election)

