from rest_framework import serializers
from .models import Subject, Link


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ('created_time', 'updated_time')


class LinkSerializer(serializers.ModelSerializer):
    subject_id = serializers.HyperlinkedRelatedField(
        queryset=Subject.objects.all(),
        view_name='subject-detail'
    )

    class Meta:
        model = Link
        exclude = ('created_time', 'updated_time')
