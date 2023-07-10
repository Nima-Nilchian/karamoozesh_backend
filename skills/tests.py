from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Subject, Link


class SubjectTests(APITestCase):
    def setUp(self):
        self.subject1 = Subject.objects.create(name='Subject 1', description='Description 1')
        self.subject2 = Subject.objects.create(name='Subject 2', description='Description 2')

    def test_subject_list(self):
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.subject1.name)
        self.assertContains(response, self.subject2.name)

    def test_subject_detail(self):
        url = reverse('subject-detail', args=[self.subject1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.subject1.name)


class LinkTests(APITestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='Subject', description='Description')
        self.link1 = Link.objects.create(subject_id=self.subject, address='https://example.com')
        self.link2 = Link.objects.create(subject_id=self.subject, address='https://example.org')

    def test_link_list(self):
        url = reverse('link-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.link1.address)
        self.assertContains(response, self.link2.address)

    def test_link_detail(self):
        url = reverse('link-detail', args=[self.link1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], self.link1.address)