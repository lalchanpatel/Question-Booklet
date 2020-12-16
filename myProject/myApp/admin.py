from django.contrib import admin

# Register your models here.

# class cart_table_admin(admin.ModelAdmin):
#     # a list of displayed columns name.
#     list_display = ['user', 'seller', 'product_id', 'count']

from .models import User, Question, Topictag, Question_topic, Subject

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Question_topic)
admin.site.register(Topictag)
