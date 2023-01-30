from rest_framework import serializers
from .models import CV,Language,Certificate,Project,Link,Skill,Education,Work


class CertificateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields ='__all__'


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields ='__all__'


class LinkSerializers(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields ='__all__'


class WorkSerializers(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields ='__all__'


class EducationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields ='__all__'


class SkillSerializers(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields ='__all__'


class LanguageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields ='__all__'


class CvSerializers(serializers.ModelSerializer):
    languages = LanguageSerializers(many=True,required=False)
    works = WorkSerializers(many=True,required=False)
    skills = SkillSerializers(many=True,required=False)
    educations = EducationSerializers(many=True,required=False)
    certificates = CertificateSerializers(many=True,required=False)
    links = LinkSerializers(many=True,required=False)
    projects = ProjectSerializers(many=True,required=False)
    avatar =serializers.ImageField(required=False)

    class Meta:
        model = CV
        fields ='__all__'