from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from chessManagement.forms import changePassword
from chessManagement.models import User
from django.contrib.auth import login

class changePasswordTest(TestCase):

    fixtures = ['chessManagement/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {'new_password': 'Wellthen123', 'new_password_confirmation': 'Wellthen123'}
        self.url = reverse('change_password')
        self.client.login(username='johndoe@example.org', password='Password123')

    def test_change_password_url(self):
        self.assertEqual(self.url,'/change_password/')

    def test_get_change_password(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, changePassword))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_change_password(self):
        self.form_input['new_password'] = 'W'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, changePassword))
        self.assertFalse(form.is_bound)
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(check_password("Password123", checkUser.password))

    def test_successful_change_password(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        self.user.is_active = False
        checkUser = User.objects.get(id = self.user.id)
        self.assertTrue(check_password("Wellthen123", checkUser.password))
