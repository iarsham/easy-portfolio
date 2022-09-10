from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from apps.extensions.utils import upload_file_path
from apps.extensions.utils import validate_file_size
from apps.portfolio.constants import PROFICIENCY_STATUS
from apps.extensions.models import (
    AbstractTime, AbstractImage, AbstractCertificate
)

User = get_user_model()


class AboutMe(AbstractTime):
    user = models.OneToOneField(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        related_name='user_aboutme'
    )
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=150,
        null=True,
        blank=True,
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=150,
        null=True,
        blank=True,
    )
    job_title = models.CharField(
        verbose_name=_("Job Title"),
        max_length=150,
        null=True,
        blank=True,
    )
    summery = models.TextField(
        verbose_name=_("Summery"),
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"),
        unique=True,
        null=True,
        blank=True,
    )
    resume = models.FileField(
        verbose_name=_("Resume"),
        null=True,
        blank=True,
        upload_to=upload_file_path,
        validators=[
            validate_file_size,
            FileExtensionValidator(
                allowed_extensions=['pdf', 'docs'],
            )
        ]
    )
    social_accounts = models.JSONField(
        verbose_name=_("Social Account"),
        default=list,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("About Me")
        verbose_name_plural = _("About Me")
        ordering = ('-updated',)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"


class AboutMeProfile(AbstractImage):
    about_me = models.ForeignKey(
        verbose_name=_("About Me"),
        to=AboutMe,
        on_delete=models.CASCADE,
        related_name="aboutme_profile"
    )

    def __str__(self):
        return f"{self.about_me.user.username} - profiles"


class Education(models.Model):
    about_me = models.OneToOneField(
        verbose_name=_("About Me"),
        to=AboutMe,
        on_delete=models.CASCADE,
        related_name='about_education'
    )
    institute = models.CharField(
        verbose_name=_("Institute"),
        max_length=150,
        null=True,
        blank=True,
    )
    field_study = models.CharField(
        verbose_name=_("Field of study"),
        max_length=100,
        null=True,
        blank=True,
    )
    degree = models.CharField(
        verbose_name=_("Degree"),
        max_length=150,
        null=True,
        blank=True,
    )
    grade = models.PositiveSmallIntegerField(
        verbose_name=_("Grade"),
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )
    start_time = models.DateField(
        verbose_name=_("Start learing"),
        null=True,
        blank=True,
    )
    finish_time = models.DateField(
        verbose_name=_("Finish learing"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Educations")

    def __str__(self):
        return "%s - %s" % (
            self.about_me.user.username,
            self.field_study
        )


class Skill(models.Model):
    name = models.CharField(
        verbose_name=_("Skill Name"),
        max_length=150,
        null=False,
    )
    about_me = models.ForeignKey(
        verbose_name=_("About Me"),
        to=AboutMe,
        on_delete=models.CASCADE,
        related_name='about_skill'
    )

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self):
        return f"{self.about_me.user.username} - {self.name}"


class SkillCertificate(AbstractCertificate):
    skill = models.ForeignKey(
        verbose_name=_("Skill"),
        to=Skill,
        on_delete=models.CASCADE,
        related_name="skill_certificate"
    )

    def __str__(self):
        return f"{self.skill.about_me.user.username} - certificates"


class Language(models.Model):
    about_me = models.ForeignKey(
        to=AboutMe,
        on_delete=models.CASCADE,
        related_name='about_language'
    )
    name = models.CharField(
        max_length=100,
        null=False,
    )
    proficiency = models.CharField(
        max_length=75,
        choices=PROFICIENCY_STATUS,
        null=False,
    )

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return "%s - %s - %s" % (
            self.about_me.user.username,
            self.name,
            self.proficiency
        )


class LanguageCertificate(AbstractCertificate):
    language = models.ForeignKey(
        verbose_name=_("Language"),
        to=Language,
        on_delete=models.CASCADE,
        related_name="language_certificate"
    )

    def __str__(self):
        return f"{self.language.about_me.user.username} - certificates"


class Achievement(models.Model):
    about_me = models.ForeignKey(
        AboutMe,
        models.CASCADE,
        related_name='about_achieve'
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=250,
        null=False,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=False,
    )

    def __str__(self):
        return f"{self.about_me.user.username} - {self.title}"

    class Meta:
        verbose_name = _("Achievement")
        verbose_name_plural = _("Achievements")


class AchievementCertificate(AbstractCertificate):
    achievement = models.ForeignKey(
        verbose_name=_("Achievement"),
        to=Achievement,
        on_delete=models.CASCADE,
        related_name="achievement_certificate"
    )

    def __str__(self):
        return f"{self.achievement.about_me.user.username} - certificates"


class ContactMe(AbstractTime):
    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        related_name='user_contact_me'
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=150,
        null=False
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        null=False
    )
    subject = models.CharField(
        verbose_name=_("Subject"),
        max_length=300,
        null=False
    )
    message = models.TextField(
        verbose_name=_("Message"),
        null=False
    )

    class Meta:
        verbose_name = _("ContactMe")
        verbose_name_plural = _("ContactMe")

    def __str__(self):
        return f"{self.user.username} - {self.email}"
