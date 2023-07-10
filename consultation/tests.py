from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user.models import User
from .models import Consultant, Skill, ConsultantSkills


class ConsultantAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', is_consultant=True)
        self.token = Token.objects.create(user=self.user)
        self.consultant = Consultant.objects.create(user_id=self.user)
        self.skill = Skill.objects.create(name='Programming')
        self.consultant_skill = ConsultantSkills.objects.create(
            consultant_id=self.consultant,
            skill_id=self.skill,
            skill_level='3'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_consultant(self):
        url = reverse('consultant-detail', kwargs={'pk': self.consultant.id})
        data = {
            'phone_number': '09876543210',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '09876543210')

    def test_delete_consultant(self):
        url = reverse('consultant-detail', kwargs={'pk': self.consultant.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Consultant.objects.count(), 0)

    def test_create_consultant_skill(self):
        url = reverse('consultant-skills-list')  # Assuming you have a URL named 'consultant-skill-list' for creating consultant skills
        data = {
            'consultant_id': self.consultant.id,
            'skill_id': self.skill.id,
            'skill_level': '4',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConsultantSkills.objects.count(), 2)  # Assuming there is already one consultant skill created in the setup

    def test_get_consultant_skill(self):
        url = reverse('consultant-skills-detail', kwargs={'pk': self.consultant_skill.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['consultant_id'], self.consultant.id)
        self.assertEqual(response.data['skill_id'], self.skill.id)
        self.assertEqual(response.data['skill_level'], '3')