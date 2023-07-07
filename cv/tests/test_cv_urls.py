from django.test import SimpleTestCase
from django.urls import reverse,resolve
from cv.views import *


class TestUrls(SimpleTestCase):

    def test_CvList_url_resolves(self):
        url = reverse('resume_list')
        self.assertEquals(resolve(url).func.view_class,CvList)

    def test_CvDetail_url_resolves(self):
        url = reverse('resume_detail',args=[1])
        self.assertEquals(resolve(url).func.view_class, CvDetail)

    def test_LinkList_url_resolves(self):
        url = reverse('link_list',args=[1])
        self.assertEquals(resolve(url).func.view_class, LinkListView)

    def test_LinkDetail_url_resolves(self):
        url = reverse('link_detail', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, LinkDetailView)

    def test_ProjectList_url_resolves(self):
        url = reverse('project_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, ProjectListView)

    def test_ProjectDetail_url_resolves(self):
        url = reverse('project_detail', args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, ProjectDetailView)

    def test_CertificateList_url_resolves(self):
        url = reverse('certificate_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, CertificateListView)

    def test_CertificateDetail_url_resolves(self):
        url = reverse('certificate_detail', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, CertificateDetailView)

    def test_SkillList_url_resolves(self):
        url = reverse('skill_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, SkillListView)

    def test_SkillDetail_url_resolves(self):
        url = reverse('skill_detail', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, SkillDetailView)

    def test_EducationList_url_resolves(self):
        url = reverse('education_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, EducationListView)

    def test_EducationDetail_url_resolves(self):
        url = reverse('education_detail', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, EducationDetailView)

    def test_WorkList_url_resolves(self):
        url = reverse('work_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, WorkListView)

    def test_WorkDetail_url_resolves(self):
        url = reverse('work_detail', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, WorkDetailView)

    def test_LanguageList_url_resolves(self):
        url = reverse('language_list', args=[1])
        self.assertEquals(resolve(url).func.view_class, LanguageListView)

    def test_LanguageDetail_url_resolves(self):
        url = reverse('language_detail', args=[1,1])
        self.assertEquals(resolve(url).func.view_class, LanguageDetailView)

    def test_cv_id_getter_url_resolves(self):
        url = reverse('get_cv-id')
        self.assertEquals(resolve(url).func,cv_id_getter)