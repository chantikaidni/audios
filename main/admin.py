from django.contrib import admin
from .models import user_details, Recording, user_work, profession, company, followers

admin.site.register(user_details)
admin.site.register(Recording)
admin.site.register(user_work)
admin.site.register(profession)
admin.site.register(company)
admin.site.register(followers)