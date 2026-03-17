from django.contrib import admin
from defectsapp.models import defects_mod,developer,tester,defect_screenshot

# Register your models here.
admin.site.register(defects_mod)        
admin.site.register(developer)
admin.site.register(tester)
admin.site.register(defect_screenshot)