from django.contrib import admin

from .models import *

admin.site.register(TestSeries),
admin.site.register(Question),
admin.site.register(Option),
admin.site.register(TestAttempt),
admin.site.register(QuizResponse),

