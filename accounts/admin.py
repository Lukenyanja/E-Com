from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from accounts.models import (
	Account,

    )



class AccountAdmin(UserAdmin):
	list_display = ('username','email')
	search_fields = ('email','username',)
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	

admin.site.register(Account, AccountAdmin)