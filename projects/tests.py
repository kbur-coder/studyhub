import shutil
import tempfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Profile, Project

User = get_user_model()
MEDIA = tempfile.mkdtemp()


def make_png(width, height):
    buffer = BytesIO()
    Image.new('RGB', (width, height), 'orange').save(buffer, format='PNG')
    return SimpleUploadedFile('big.png', buffer.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA)
class StudyHubTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user('alice', 'alice@example.com', 'Zq!8vLm2xPw')
        self.other = User.objects.create_user('bob', 'bob@example.com', 'Zq!8vLm2xPw')

    def test_no_default_admin_account(self):
        self.assertFalse(User.objects.filter(username='admin').exists())

    def test_anonymous_user_is_sent_to_login(self):
        response = self.client.get(reverse('project_list'))
        self.assertRedirects(response, '/login/?next=/')

    def test_registration_creates_profile_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'carol',
            'email': 'carol@example.com',
            'password1': 'Zq!8vLm2xPw',
            'password2': 'Zq!8vLm2xPw',
        })
        self.assertRedirects(response, reverse('project_list'))
        self.assertTrue(Profile.objects.filter(user__username='carol').exists())
        self.assertEqual(self.client.get(reverse('project_list')).status_code, 200)

    def test_create_project_sets_author_and_shrinks_image(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_project'), {
            'title': 'Demo',
            'description': 'Text',
            'technologies': 'Python, Django',
            'image': make_png(1200, 800),
        })
        self.assertRedirects(response, reverse('project_list'))
        project = Project.objects.get()
        self.assertEqual(project.author, self.user)
        with Image.open(project.image.path) as saved:
            self.assertLessEqual(saved.size[0], 600)
            self.assertLessEqual(saved.size[1], 400)

    def test_small_image_is_kept_as_is(self):
        self.client.force_login(self.user)
        self.client.post(reverse('create_project'), {
            'title': 'Small',
            'description': 'Text',
            'technologies': 'Python',
            'image': make_png(100, 80),
        })
        with Image.open(Project.objects.get().image.path) as saved:
            self.assertEqual(saved.size, (100, 80))

    def test_only_author_can_edit_project(self):
        project = Project.objects.create(title='Mine', description='d', technologies='x', author=self.user)
        self.client.force_login(self.other)
        response = self.client.post(reverse('edit_project', args=[project.id]), {
            'title': 'Hacked',
            'description': 'd',
            'technologies': 'x',
        })
        self.assertRedirects(response, reverse('project_list'))
        project.refresh_from_db()
        self.assertEqual(project.title, 'Mine')

    def test_profile_edit_page_is_reachable(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_pages(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)
        self.assertEqual(self.client.get(reverse('profile', args=['bob'])).status_code, 200)
        self.assertRedirects(self.client.get(reverse('profile', args=['nobody'])), reverse('project_list'))

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        self.client.get(reverse('logout'))
        self.assertEqual(self.client.get(reverse('project_list')).status_code, 200)
        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(reverse('project_list')).status_code, 302)
