from django.contrib import admin

# Register your models here.

from .models import PoshanFormInformation, UploadPictureModel, UploadWellPictureModel, CensusTable, AhmedSchoolForm
admin.site.register(UploadPictureModel)
admin.site.register(UploadWellPictureModel)
admin.site.register(PoshanFormInformation)
admin.site.register(CensusTable)
admin.site.register(AhmedSchoolForm)