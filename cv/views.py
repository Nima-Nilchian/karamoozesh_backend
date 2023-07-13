from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from cv.permissions import IsOwner
from rest_framework.response import Response
from custom_lib.permissions import IsStaffOrReadOnly
from .models import CV, Link, Project, Certificate,\
    Skill, Education, Work, Language
from .serializers import CvSerializers, LinkSerializers,\
    ProjectSerializers, CertificateSerializers,\
    SkillSerializers, EducationSerializers,\
    WorkSerializers, LanguageSerializers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

# CV views

class CvList(generics.ListCreateAPIView):
    queryset = CV.objects.all()
    serializer_class = CvSerializers
    filterset_fields = (
        'gender', 'duty_system', 'martial_status',
        'character', 'is_active', 'city',
    )
    search_fields = ('about_me', 'phone_number', 'address')
    ordering_fields = ["created_time", "updated_time"]
    ordering = ["-created_time"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)


class CvDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CV.objects.all()
    serializer_class = CvSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)


#  CV bank

class CvBankView(generics.ListAPIView):
    queryset = CV.objects.filter(is_active=True)
    serializer_class = CvSerializers
    filterset_fields = (
        'gender', 'duty_system', 'martial_status',
        'character', 'is_active', 'city',
    )
    search_fields = ('about_me', 'phone_number', 'address')
    ordering_fields = ["created_time", "updated_time"]
    ordering = ["-created_time"]


# Link views

class LinkListView(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializers
    search_fields = ('title',)
    ordering_fields = ["created_time", "updated_time"]
    ordering = ["-created_time"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class LinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('link_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('link_id'))


# Project views

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    search_fields = ('title', 'description')
    ordering_fields = ["created_time", "updated_time"]
    ordering = ["-created_time"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('project_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('project_id'))


# Certificate views

class CertificateListView(generics.ListCreateAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializers
    search_fields = ('title', 'institute', 'description')
    ordering_fields = ["created_time", "updated_time"]
    ordering = ["-created_time"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class CertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializers
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('certificate_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('certificate_id'))


# Skill views

class SkillListView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializers
    filterset_fields = ('level',)
    search_fields = ('title',)
    ordering_fields = ["level"]
    ordering = ["-level"]
    # permission_classes = (IsStaffOrReadOnly,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializers
    filterset_fields = ('level',)
    search_fields = ('title',)
    ordering_fields = ["level"]
    ordering = ["-level"]
    # permission_classes = (IsStaffOrReadOnly,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('skill_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('skill_id'))


# Education views

class EducationListView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializers
    filterset_fields = ('field_of_study', 'university')
    search_fields = ('university', 'field_of_study', 'description')
    ordering_fields = ["start_date"]
    ordering = ["+start_date"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializers
    ordering_fields = ["start_date"]
    ordering = ["+start_date"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('education_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('education_id'))


# Work views

class WorkListView(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializers
    search_fields = ('title', 'company', 'description', 'industry')
    ordering_fields = ["start_date"]
    ordering = ["-start_date"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class WorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializers
    ordering_fields = ["start_date"]
    ordering = ["-start_date"]
    # permission_classes = (IsAdminUser,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('work_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('work_id'))


# Language views

class LanguageListView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers
    filterset_fields = ('level',)
    search_fields = ('title',)
    ordering_fields = ["level"]
    ordering = ["-level"]
    # permission_classes = (IsStaffOrReadOnly,)
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.kwargs.get('cv_id'):
            return self.queryset.filter(cv_id=self.kwargs.get('cv_id'))
        return self.queryset.all()


class LanguageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializers
    filterset_fields = ('level',)
    search_fields = ('title',)
    ordering_fields = ["level"]
    ordering = ["-level"]
    # permission_classes = (IsStaffOrReadOnly,)
    permission_classes = (IsOwner,)

    def get_object(self):
        if self.kwargs.get('cv_id'):
            return get_object_or_404(
                self.get_queryset(), cv_id=self.kwargs.get('cv_id'),
                pk=self.kwargs.get('language_id')
            )
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('language_id'))


@api_view(['GET', ])
def cv_id_getter(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        user_id = Token.objects.filter(key=token)
        if user_id:
            user_id = user_id.first().user_id
            cv_id = CV.objects.filter(user_id=user_id)
            if cv_id:
                cv_id = cv_id.first().id
                return Response({"cv_id": cv_id}, status=status.HTTP_200_OK)

            return Response({"message": "CV not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)



class CvImageView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, cv_id, format=None):
        uploaded_image = request.FILES['image']
        cv = CV.objects.get(id=cv_id)
        cv.avatar = uploaded_image
        cv.save()

        return Response('Photo uploaded successfully',status=status.HTTP_200_OK)