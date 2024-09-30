from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin


admin.site.register(Member, ImportExportActionModelAdmin)


admin.site.register(MemberFee, ImportExportActionModelAdmin)

