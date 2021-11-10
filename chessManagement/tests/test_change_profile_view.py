from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import changeProfile
from chessManagement.models import User

class changeProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            experience='Beginner',
            personal_statement='Hi I would like to apply ',
            bio='Hello, I am John Doe.',
            password='Password123',
        )
        self.form_input = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'experience': '',
            'bio': '',
            'personal_statement': '',
        }
        self.url = reverse('change_profile', kwargs={'user_id': self.user.id})

    def test_change_password_url(self):
        self.assertEqual(self.url,f'/change_profile/{self.user.id}')

    def test_get_change_password(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, changeProfile))
        self.assertFalse(form.is_bound)

    def test_successful_change_only_first_name(self):
        self.form_input['first_name'] = 'Jane'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.first_name == "Jane")
        self.assertTrue(checkUser.last_name == "Doe")

    def test_successful_change_only_last_name(self):
        self.form_input['last_name'] = 'Bob'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.first_name == "John")
        self.assertTrue(checkUser.last_name == "Bob")

    def test_successful_change_both_first_and_last_name(self):
        self.form_input['last_name'] = 'Bob'
        self.form_input['first_name']= 'Jane'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.first_name == "Jane")
        self.assertTrue(checkUser.last_name == "Bob")

    def test_successful_change_only_email(self):
        self.form_input['email'] = 'jane@example.com'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.email == "jane@example.com")
        self.assertTrue(checkUser.username == "jane@example.com")

    def test_successful_change_only_experience(self):
        self.form_input['experience'] = 'Master'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.experience == "Master")

    def test_successful_change_only_bio(self):
        self.form_input['bio'] = 'Hi this is a new bio'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.bio == "Hi this is a new bio")

    def test_successful_change_only_personal_statement(self):
        self.form_input['personal_statement'] = 'Hi this is a new personal statement'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.personal_statement == "Hi this is a new personal statement")

    def test_successful_change_all_details(self):
        self.form_input['first_name'] = 'Jane'
        self.form_input['last_name'] = 'Bob'
        self.form_input['email'] = 'jane@example.com'
        self.form_input['experience'] = 'Master'
        self.form_input['bio'] = 'Hi this is a new bio'
        self.form_input['personal_statement'] = 'Hi this is a new personal statement'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('profile', kwargs={'user_id': self.user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        checkUser = User.objects.get(id=self.user.id)
        self.assertTrue(checkUser.first_name == "Jane")
        self.assertTrue(checkUser.last_name == "Bob")
        self.assertTrue(checkUser.bio == "Hi this is a new bio")
        self.assertTrue(checkUser.experience == "Master")
        self.assertTrue(checkUser.email == "jane@example.com")
        self.assertTrue(checkUser.username == "jane@example.com")
        self.assertTrue(checkUser.personal_statement == "Hi this is a new personal statement")

    # def test_successful_change_password(self):
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     response_url = reverse('profile', kwargs={'user_id': self.user.id})
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'profile.html')
    #     self.user.is_active = False
    #     checkUser = User.objects.get(id = self.user.id)
    #     self.assertTrue(check_password("Wellthen123", checkUser.password))

    # def test_get_change_password_with_invalid_id(self):
    #     url = reverse('profile', kwargs={'user_id': self.user.id+1})
    #     response = self.client.get(url, follow=True)
    #     response_url = reverse('user_list')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'user_list.html')
