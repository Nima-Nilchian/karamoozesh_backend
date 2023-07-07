from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from cv.models import *
from user.models import User


class TestViews(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='secret',email="test@gmail.com")
        self.user_2 = User.objects.create_user(username='test_user2', password='secret',email="test2@gmail.com")
        self.cv = CV.objects.create(
            firstname = "test", lastname = "test", gender = "M", user_id = self.user,
         duty_system = "1", martial_status = "1", data_of_birth= "2023-07-01",
        city= "test",
        )
        self.link = Link.objects.create(
            title="test",link="https://www.varzesh3.com/",
            cv_id=self.cv,
        )
        self.project = Project.objects.create(
            title="test",link="https://www.varzesh3.com/",
            description="test test",cv_id=self.cv
        )
        self.certificate = Certificate.objects.create(
            title="test",institute="test",
            issue_date="2023-07-01",cv_id=self.cv
        )
        self.skill = Skill.objects.create(
            title="test",level="2",
            cv_id=self.cv
        )
        self.education = Education.objects.create(
            grade="test",field_of_study="test",university="test",
            cv_id=self.cv
        )
        self.work = Work.objects.create(
            title="test",company="test",
            cv_id=self.cv
        )
        self.language = Language.objects.create(
            title="test",level="1",
            cv_id=self.cv
        )
    # test CVList view

    def test_get_all_cvs(self):
        self.client.force_login(self.user)
        url = reverse('resume_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_cvs_with_no_auth(self):
        url = reverse('resume_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_cv_with_no_auth(self):
        url = reverse('resume_list')
        data = {
            "firstname":"test" , "lastname":"test" , "gender":"M" ,"user_id":self.user.id ,
            "duty_system":"1" , "martial_status":"1" , "data_of_birth": "2023-07-01",
            "city":"test",
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_cv_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('resume_list')
        data = {
            "firstname":"" , "lastname":"test" , "gender":"M" ,"user_id":self.user.id ,
            "duty_system":"1" , "martial_status":"1" , "data_of_birth": "2023-07-01",
            "city":"test",
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_cv(self):
        self.client.force_login(self.user)
        url = reverse('resume_list')
        data = {
            "firstname":"test1" , "lastname":"test1" , "gender":"M" ,"user_id":self.user_2.id ,
            "duty_system":"1" , "martial_status":"1" , "data_of_birth": "2023-07-01",
            "city":"test",
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test CVDetail view

    def test_get_cv_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('resume_detail', args=[self.cv.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_cv_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('resume_detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_cv_detail_with_no_auth(self):
        response = self.client.get(reverse('resume_detail', args=[self.cv.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_cv(self):
        self.client.force_login(self.user)
        data = {
            "firstname":"test_2","lastname":"test_2",
        }
        response = self.client.patch(reverse('resume_detail', args=[self.cv.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_cv_with_no_auth(self):
        data = {
            "firstname":"test_2","lastname":"test_2",
        }
        response = self.client.patch(reverse('resume_detail', args=[self.cv.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_cv_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "firstname":"","lastname":"test_2",
        }
        response = self.client.patch(reverse('resume_detail', args=[self.cv.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_cv(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('resume_detail',args=[self.cv.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CV.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_cv_with_no_auth(self):
        response = self.client.delete(reverse('resume_detail',args=[self.cv.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test LinkList view

    def test_get_all_links(self):
        self.client.force_login(self.user)
        url = reverse('link_list',args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_links_with_no_auth(self):
        url = reverse('link_list',args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_link_with_no_auth(self):
        url = reverse('link_list',args=[self.cv.id])
        data = {
            "title":"test","link":"https://www.varzesh3.com/",
            "cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_link_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('link_list',args=[self.cv.id])
        data = {
            "title": "test", "link": "test",
            "cv_id": self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_link(self):
        self.client.force_login(self.user)
        url = reverse('link_list',args=[self.cv.id])
        data = {
            "title": "test", "link": "https://www.varzesh3.com/",
            "cv_id": self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test LindDetail view

    def test_get_link_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('link_detail', args=[self.cv.id,self.link.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_link_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('link_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_link_detail_with_no_auth(self):
        response = self.client.get(reverse('link_detail', args=[self.cv.id,self.link.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_link(self):
        self.client.force_login(self.user)
        data = {
            "title":"test_2","link":"https://www.varzesh31.com/",
        }
        response = self.client.patch(reverse('link_detail', args=[self.cv.id,self.link.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_link_with_no_auth(self):
        data = {
            "title":"test_2","link":"https://www.varzesh3.com/",
        }
        response = self.client.patch(reverse('link_detail', args=[self.cv.id,self.link.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_link_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "title":"","link":"test_2",
        }
        response = self.client.patch(reverse('link_detail', args=[self.cv.id,self.link.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_link(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('link_detail',args=[self.cv.id,self.link.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Link.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_link_with_no_auth(self):
        response = self.client.delete(reverse('link_detail',args=[self.cv.id,self.link.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test ProjectList view

    def test_get_all_projects(self):
        self.client.force_login(self.user)
        url = reverse('project_list',args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_projects_with_no_auth(self):
        url = reverse('project_list',args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_project_with_no_auth(self):
        url = reverse('project_list',args=[self.cv.id])
        data = {
            "title":"test","link":"https://www.varzesh3.com/",
            "description":"test test","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_project_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('project_list',args=[self.cv.id])
        data = {
            "title":"test","link":"https://www.varzesh3.com/",
            "description":"test test","cv_id":2
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project(self):
        self.client.force_login(self.user)
        url = reverse('link_list',args=[self.cv.id])
        data = {
            "title":"test","link":"https://www.varzesh3.com/",
            "description":"test test","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test ProjectDetail view

    def test_get_project_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('project_detail', args=[self.cv.id,self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_project_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('project_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_project_detail_with_no_auth(self):
        response = self.client.get(reverse('project_detail', args=[self.cv.id,self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project(self):
        self.client.force_login(self.user)
        data = {
            "title":"test_2","link":"https://www.varzesh31.com/",
        }
        response = self.client.patch(reverse('project_detail', args=[self.cv.id,self.project.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_project_with_no_auth(self):
        data = {
            "title":"test_2","link":"https://www.varzesh3.com/",
        }
        response = self.client.patch(reverse('project_detail', args=[self.cv.id,self.project.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_project_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "title":"","link":"test_2",
        }
        response = self.client.patch(reverse('project_detail', args=[self.cv.id,self.project.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('project_detail',args=[self.cv.id,self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_project_with_no_auth(self):
        response = self.client.delete(reverse('project_detail',args=[self.cv.id,self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test CertificateList view

    def test_get_all_certificates(self):
        self.client.force_login(self.user)
        url = reverse('certificate_list',args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_certificates_with_no_auth(self):
        url = reverse('certificate_list',args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_certificate_with_no_auth(self):
        url = reverse('certificate_list',args=[self.cv.id])
        data = {
            "title":"test","institute":"test",
            "issue_date":"2023-07-01","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_certificate_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('certificate_list',args=[self.cv.id])
        data = {
            "title":"test","institute":"test",
            "issue_date":"test","cv_id":2
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_certificate(self):
        self.client.force_login(self.user)
        url = reverse('certificate_list',args=[self.cv.id])
        data = {
            "title":"test","institute":"test",
            "issue_date":"2023-07-01","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test CertificateDetail view

    def test_get_certificate_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('certificate_detail', args=[self.cv.id,self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_certificate_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('certificate_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_certificate_detail_with_no_auth(self):
        response = self.client.get(reverse('certificate_detail', args=[self.cv.id,self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_certificate(self):
        self.client.force_login(self.user)
        data = {
            "title":"test_2","issue_date":"2022-07-01"
        }
        response = self.client.patch(reverse('certificate_detail', args=[self.cv.id,self.certificate.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_certificate_with_no_auth(self):
        data = {
            "title":"test_2","issue_date":"2022-07-01"
        }
        response = self.client.patch(reverse('certificate_detail', args=[self.cv.id,self.certificate.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_certificate_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "title":"","issue_date":"test"
        }
        response = self.client.patch(reverse('certificate_detail', args=[self.cv.id,self.certificate.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_certificate(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('certificate_detail',args=[self.cv.id,self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Certificate.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_certificate_with_no_auth(self):
        response = self.client.delete(reverse('certificate_detail',args=[self.cv.id,self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test SkillList view

    def test_get_all_skills(self):
        self.client.force_login(self.user)
        url = reverse('skill_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_skills_with_no_auth(self):
        url = reverse('skill_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_skill_with_no_auth(self):
        url = reverse('skill_list', args=[self.cv.id])
        data = {
            "title": "test", "level":"2",
            "cv_id":self.cv.id,
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_skill_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('skill_list', args=[self.cv.id])
        data = {
            "title": "test", "level":"6",
            "cv_id":2
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_skill(self):
        self.client.force_login(self.user)
        url = reverse('skill_list', args=[self.cv.id])
        data = {
            "title": "test", "level":"2",
            "cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test SkillDetail view

    def test_get_skill_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('skill_detail', args=[self.cv.id,self.skill.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_skill_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('skill_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_skill_detail_with_no_auth(self):
        response = self.client.get(reverse('skill_detail', args=[self.cv.id,self.skill.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_skill(self):
        self.client.force_login(self.user)
        data = {
            "title":"test","level":"4"
        }
        response = self.client.patch(reverse('skill_detail', args=[self.cv.id,self.skill.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_skill_with_no_auth(self):
        data = {
            "title":"test","level":"4"
        }
        response = self.client.patch(reverse('skill_detail', args=[self.cv.id,self.skill.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_skill_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "title":"test","level":"6"
        }
        response = self.client.patch(reverse('skill_detail', args=[self.cv.id,self.skill.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_skill(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('skill_detail',args=[self.cv.id,self.skill.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_skill_with_no_auth(self):
        response = self.client.delete(reverse('skill_detail',args=[self.cv.id,self.skill.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test EducationList view

    def test_get_all_educations(self):
        self.client.force_login(self.user)
        url = reverse('education_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_educations_with_no_auth(self):
        url = reverse('education_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_education_with_no_auth(self):
        url = reverse('education_list', args=[self.cv.id])
        data = {
            "grade":"test","field_of_study":"test",
            "university":"test","cv_id":self.cv.id,
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_education_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('education_list', args=[self.cv.id])
        data = {
            "grade":"test","field_of_study":"test",
            "university":"test","cv_id":2
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_education(self):
        self.client.force_login(self.user)
        url = reverse('education_list', args=[self.cv.id])
        data = {
            "grade":"test","field_of_study":"test",
            "university":"test","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test EducationDetail view

    def test_get_education_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('education_detail', args=[self.cv.id,self.education.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_education_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('education_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_education_detail_with_no_auth(self):
        response = self.client.get(reverse('education_detail', args=[self.cv.id,self.education.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_education(self):
        self.client.force_login(self.user)
        data = {
            "grade":"test_1","university":"test3"
        }
        response = self.client.patch(reverse('education_detail', args=[self.cv.id,self.education.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_education_with_no_auth(self):
        data = {
            "grade":"test_1","university":"test3"
        }
        response = self.client.patch(reverse('education_detail', args=[self.cv.id,self.education.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_education_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "grade":"","university":"test3"
        }
        response = self.client.patch(reverse('education_detail', args=[self.cv.id,self.education.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_education(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('education_detail',args=[self.cv.id,self.education.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_education_with_no_auth(self):
        response = self.client.delete(reverse('education_detail',args=[self.cv.id,self.education.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test WorkList view

    def test_get_all_works(self):
        self.client.force_login(self.user)
        url = reverse('work_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_works_with_no_auth(self):
        url = reverse('work_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_work_with_no_auth(self):
        url = reverse('work_list', args=[self.cv.id])
        data = {
            "title": "test", "company": "test", "cv_id": self.cv.id,
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_work_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('work_list', args=[self.cv.id])
        data = {
            "title": "test", "company": "test", "cv_id": 2
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_work(self):
        self.client.force_login(self.user)
        url = reverse('work_list', args=[self.cv.id])
        data = {
            "title":"test","company":"test","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test WorkDetail view

    def test_get_work_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('work_detail', args=[self.cv.id,self.work.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_work_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('work_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_work_detail_with_no_auth(self):
        response = self.client.get(reverse('work_detail', args=[self.cv.id,self.work.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_work(self):
        self.client.force_login(self.user)
        data = {
            "title":"test_1","company":"test3"
        }
        response = self.client.patch(reverse('work_detail', args=[self.cv.id,self.work.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_work_with_no_auth(self):
        data = {
            "title":"test_1","company":"test3"
        }
        response = self.client.patch(reverse('work_detail', args=[self.cv.id,self.work.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_work_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "title":"","company":"test3"
        }
        response = self.client.patch(reverse('work_detail', args=[self.cv.id,self.work.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_work(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('work_detail',args=[self.cv.id,self.work.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Work.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_work_with_no_auth(self):
        response = self.client.delete(reverse('work_detail',args=[self.cv.id,self.work.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test LanguageList view

    def test_get_all_languages(self):
        self.client.force_login(self.user)
        url = reverse('language_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_languages_with_no_auth(self):
        url = reverse('language_list', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_language_with_no_auth(self):
        url = reverse('work_list', args=[self.cv.id])
        data = {
            "title": "test", "level": "1", "cv_id": self.cv.id,
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_create_language_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse('language_list', args=[self.cv.id])
        data = {
            "title": "test", "level": "7", "cv_id": 2
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_language(self):
        self.client.force_login(self.user)
        url = reverse('language_list', args=[self.cv.id])
        data = {
            "title":"test","level":"2","cv_id":self.cv.id
        }
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test LanguageDetail view

    def test_get_language_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('language_detail', args=[self.cv.id,self.language.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_get_language_detail_with_incorrect_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('language_detail', args=[self.cv.id,2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_get_language_detail_with_no_auth(self):
        response = self.client.get(reverse('language_detail', args=[self.cv.id,self.language.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_language(self):
        self.client.force_login(self.user)
        data = {
            "title":"test_1","level":"2"
        }
        response = self.client.patch(reverse('language_detail', args=[self.cv.id,self.language.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_update_language_with_no_auth(self):
        data = {
            "title":"test_1","level":"test3"
        }
        response = self.client.patch(reverse('language_detail', args=[self.cv.id,self.language.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_update_language_with_incorrect_data(self):
        self.client.force_login(self.user)
        data = {
            "title":"","level":"test3"
        }
        response = self.client.patch(reverse('language_detail', args=[self.cv.id,self.language.id]), data=data , format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_language(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('language_detail',args=[self.cv.id,self.language.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Language.objects.filter(pk=self.cv.pk).exists())

    def test_not_delete_language_with_no_auth(self):
        response = self.client.delete(reverse('language_detail',args=[self.cv.id,self.language.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
