import datetime
from rest_framework import serializers
from dateutil.relativedelta import relativedelta
from apps.experience.models import (
    Experience, Project, ProjectAssets,
    PersonalProject, PersonalProjectAssets,
    ReferencePeople, Blog
)


class ExperienceSerializer(serializers.ModelSerializer):
    sum_work = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Experience
        exclude = ('user', 'created', 'updated')

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
                return "%s %s- %s %s - %d mos" % (
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
