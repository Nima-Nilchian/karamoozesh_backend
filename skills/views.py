from rest_framework import generics
from custom_permissions.permissions import IsStaffOrReadOnly
from .models import Subject, Link
from .serializers import SubjectSerializer, LinkSerializer


class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsStaffOrReadOnly,)
    search_fields = ('name', 'description')


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsStaffOrReadOnly,)
    lookup_field = 'pk'


class LinkList(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsStaffOrReadOnly,)
    search_fields = ('subject_id', 'address')


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsStaffOrReadOnly,)
    lookup_field = 'pk'

