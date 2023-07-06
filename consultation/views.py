from rest_framework import generics
from .models import Consultant, Skill, ConsultantSkills
from .serializers import ConsultantSerializers, SkillSerializers, ConsultantSkillsSerializers
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class ConsultantList(generics.ListCreateAPIView):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializers
    search_fields = ('phone_number',)
    ordering_fields = ["created_time"]
    ordering = ["-created_time"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsAuthenticated,)


class ConsultantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsAuthenticated,)


class SkillList(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsAuthenticated,)


class SkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsAuthenticated,)


class ConsultantSkillsList(generics.ListCreateAPIView):
    queryset = ConsultantSkills.objects.all()
    serializer_class = ConsultantSkillsSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsAuthenticated,)


class ConsultantSkillsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConsultantSkills.objects.all()
    serializer_class = ConsultantSkillsSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsAuthenticated,)
