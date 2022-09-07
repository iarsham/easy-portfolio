from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.extensions.models import AbstractTime, AbstractImage, AbstractFile
from apps.portfolio.constants import EMPLOYMENT_STATUS

User = get_user_model()


class Experience(AbstractTime):
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        related_name='experience_user'
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        unique=True,
        editable=False,
        null=True,
        blank=True
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=100,
        null=False,
    )
    Employment_type = models.CharField(
        verbose_name=_("Employment_type"),
        max_length=20,
        choices=EMPLOYMENT_STATUS,
        null=False,
    )
    company_name = models.CharField(
        verbose_name=_("Company Name"),
        max_length=100,
        null=False,
    )
    company_website_link = models.URLField(
        verbose_name=_("Company Website Link"),
        null=True,
        blank=True,
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )
    start_date = models.DateField(
        verbose_name=_("Start Position"),
        null=False,
    )
    end_date = models.DateField(
        verbose_name=_("End Position"),
        default=None,
        null=True,
        blank=True,
    )
    still_working = models.BooleanField(
        verbose_name=_("Still Working?"),
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")
        ordering = ('-updated', '-created')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username} {self.role} {self.company_name}"
            )
        if self.still_working and self.end_date:
            self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        if self.end_date is None:
            return "%s - %s - %s-Present - %s" % (
                self.role, self.user.username,
                self.start_date,
                self.company_website_link
            )
        return "%s - %s - %s-%s - %s" % (
            self.role, self.user.username,
            self.start_date, self.end_date,
            self.company_website_link
        )


class Project(models.Model):
    experience = models.ForeignKey(
        verbose_name=_("Experience"),
        to=Experience,
        on_delete=models.CASCADE,
        related_name='experience_project'
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=150,
        null=False,
    )
    link = models.URLField(
        verbose_name=_("Link"),
        max_length=300,
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=False,
    )
    stacks = models.JSONField(
        verbose_name=_("Stacks"),
        default=list,
        null=False,
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return "%s - %s - %s" % (
            self.experience.user.username,
            self.name,
            self.description[:15],
        )


class ProjectAssets(AbstractFile):
    project = models.ForeignKey(
        verbose_name=_("Project"),
        to=Project,
        on_delete=models.CASCADE,
        related_name="assets_project"
    )

    def __str__(self):
        return f"{self.project}"


class ReferencePeople(AbstractImage):
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        related_name='reference_user'
    )
    full_name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=75,
        null=False,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=150,
        null=False,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"),
        unique=True,
        null=True,
    )
    linkedin = models.URLField(
        verbose_name=_("Linkedin"),
        max_length=150,
        null=False,
    )
    recommendation = models.TextField(
        verbose_name=_("Recommendation Text"),
        null=False,
    )

    class Meta:
        verbose_name = _("Reference People")
        verbose_name_plural = _("Reference Peoples")

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.email}"


class PersonalProject(models.Model):
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        related_name='personal_user'
    )
    name = models.CharField(
        verbose_name=_("Project Name"),
        max_length=200,
        null=False,
    )
    link = models.URLField(
        verbose_name=_("Project Link"),
        max_length=250,
        null=True,
        blank=True
    )
    stacks = models.JSONField(
        verbose_name=_("Project Stacks"),
        default=list,
        null=False,
    )
    description = models.TextField(
        verbose_name=_("Project Description"),
        null=False,
    )

    class Meta:
        verbose_name = _("Personal Project")
        verbose_name_plural = _("Personal Projects")

    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.link}"


class PersonalProjectAssets(AbstractFile):
    personal_project = models.ForeignKey(
        verbose_name=_("Personal Project"),
        to=PersonalProject,
        on_delete=models.CASCADE,
        related_name="personal_assets"
    )

    def __str__(self):
        return f"{self.personal_project}"
