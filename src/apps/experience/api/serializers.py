import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from apps.experience.models import (
    Experience, Project, ProjectAssets, PersonalProject,
    PersonalProjectAssets, ReferencePeople, Blog
)


class ExperienceSerializer(serializers.ModelSerializer):
    sum_work = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Experience
        exclude = ('user', 'created', 'updated')

    def validate(self, attrs):
        end_date = attrs.get('end_date', None)
        if attrs['still_working'] is False and end_date is None:
            raise serializers.ValidationError(
                _("Your work experience has ended. Enter the end date")
            )
        if attrs['still_working'] is True and end_date:
            raise serializers.ValidationError(
                _("Your working now, dont need to end_date")
            )
        if end_date is not None and end_date <= attrs['start_date']:
            raise serializers.ValidationError(
                _("The end date cannot be less than the start date")
            )
        return attrs

    def get_sum_work(self, obj):
        if obj.still_working:
            date = relativedelta(datetime.date.today(), obj.start_date)
            if not date.years:
                return "%s %s Present %s mos" % (
                    obj.start_date.strftime('%B')[:3],
                    obj.start_date.year,
                    date.months
                )
            return "%s %s Present %s yr %s mos" % (
                obj.start_date.strftime('%B')[:3],
                obj.start_date.year, date.years, date.months
            )
        else:
            date = relativedelta(obj.end_date, obj.start_date)
            if not date.years:
                return "%s %s- %s %s - %s mos" % (
                    obj.start_date.strftime('%B')[:3], obj.start_date.year,
                    obj.end_date.strftime('%B')[:3], obj.end_date.year,
                    date.months
                )
            return "%s %s - %s %s - %s yr %s mos" % (
                obj.start_date.strftime('%B')[:3], obj.start_date.year,
                obj.end_date.strftime('%B')[:3],
                obj.end_date.year, date.years, date.months
            )


class ProjectAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssets
        fields = ('id', 'file')


class ProjectSerializer(serializers.ModelSerializer):
    assets = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = ('experience',)
        extra_kwargs = {'stacks': {'required': True}}

    def validate(self, attrs):
        request = self.context['request']
        if request.method == "POST" and Project.objects.filter(
                experience__user=request.user,
                name__icontains=attrs['name']
        ).exists():
            raise serializers.ValidationError('project with this name exists.')
        return attrs

    def get_assets(self, obj):
        return ProjectAssetsSerializer(
            instance=obj.assets_project.all(),
            many=True,
            context={"request": self.context['request']}
        ).data

    def create(self, validated_data):
        new_obj = Project.objects.create(**validated_data)
        uploaded_files = self.context['request'].FILES
        assets_obj_list = []
        for file in uploaded_files.getlist('file'):
            assets_obj_list.append(ProjectAssets(project=new_obj, file=file))
        ProjectAssets.objects.bulk_create(assets_obj_list)
        return new_obj

    def update(self, instance, validated_data):
        uploaded_files = self.context['request'].FILES
        assets_obj_list = []
        for file in uploaded_files.getlist('file'):
            assets_obj_list.append(ProjectAssets(project=instance, file=file))
        ProjectAssets.objects.bulk_create(assets_obj_list)
        return super().update(instance, validated_data)


class ReferencePeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferencePeople
        exclude = ('user',)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == "POST" and ReferencePeople.objects.filter(
                full_name__icontains=attrs['full_name'],
                email__icontains=attrs['email'],
        ).exists():
            raise serializers.ValidationError(
                'someone with this full_name and email exists.'
            )
        return attrs


class PersonalProjectAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssets
        fields = ('id', 'file')


class PersonalProjectSerializer(serializers.ModelSerializer):
    assets = serializers.SerializerMethodField()

    class Meta:
        model = PersonalProject
        exclude = ('user',)
        extra_kwargs = {'stacks': {'required': True}}

    def get_assets(self, obj):
        return ProjectAssetsSerializer(
            instance=obj.personal_assets.all(),
            many=True,
            context={'request': self.context['request']}
        ).data

    def validate(self, attrs):
        request = self.context['request']
        if request.method == "POST" and PersonalProject.objects.filter(
                user=request.user,
                name__icontains=attrs['name']
        ).exists():
            raise serializers.ValidationError('project with this name exists.')
        return attrs

    def create(self, validated_data):
        new_obj = PersonalProject.objects.create(**validated_data)
        uploaded_files = self.context['request'].FILES
        assets_obj_list = []
        for file in uploaded_files.getlist('file'):
            assets_obj_list.append(
                PersonalProjectAssets(personal_project=new_obj, file=file)
            )
        PersonalProjectAssets.objects.bulk_create(assets_obj_list)
        return new_obj

    def update(self, instance, validated_data):
        uploaded_files = self.context['request'].FILES
        assets_obj_list = []
        for file in uploaded_files.getlist('file'):
            assets_obj_list.append(
                PersonalProjectAssets(personal_project=instance, file=file)
            )
        PersonalProjectAssets.objects.bulk_create(assets_obj_list)
        return super().update(instance, validated_data)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ("user",)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == "POST" and Blog.objects.filter(
                user=request.user,
                title__icontains=attrs['title']
        ).exists():
            raise serializers.ValidationError('blog with this title exists.')
        return attrs
