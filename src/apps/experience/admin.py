from django.contrib import admin
from apps.experience.models import (
    Experience, Project, ProjectAssets, ReferencePeople,
    PersonalProject, PersonalProjectAssets
)

admin.site.register(Experience)
admin.site.register(Project)
admin.site.register(ProjectAssets)
admin.site.register(ReferencePeople)
admin.site.register(PersonalProject)
admin.site.register(PersonalProjectAssets)
