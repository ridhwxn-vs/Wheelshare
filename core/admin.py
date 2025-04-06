from django.contrib import admin
from .models import UserProfile, Cycle, Rental, UserReview, CycleReview

admin.site.register(UserProfile)
admin.site.register(Cycle)
admin.site.register(Rental)
admin.site.register(UserReview)
admin.site.register(CycleReview)
