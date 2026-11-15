from django.test import TestCase
from django.contrib.auth.models import User
from .models import Topic, Entry


class WorkflowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='Test-pass-12345')
        self.other = User.objects.create_user(username='other')
        self.topic = Topic.objects.create(text='Private topic', owner=self.owner)
        self.entry = Entry.objects.create(topic=self.topic, text='Private entry')

    def test_public_home_and_guest_redirect(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertRedirects(self.client.get('/topics/'), '/users/login/?next=/topics/')

    def test_login_redirect_and_next(self):
        data = {'username': 'owner', 'password': 'Test-pass-12345'}
        self.assertRedirects(self.client.post('/users/login/', data), '/')
        self.client.logout()
        self.assertContains(self.client.get('/users/login/?next=/topics/'), 'value="/topics/"')
        self.assertRedirects(self.client.post('/users/login/', dict(data, next='/topics/')), '/topics/')
        self.client.logout()
        self.assertRedirects(self.client.post('/users/login/', dict(data, next='https://evil.example')), '/')

    def test_missing_objects(self):
        self.client.force_login(self.owner)
        for path in ('/topics/99999/', '/new_entry/99999/', '/edit_entry/99999/'):
            for method in (self.client.get, self.client.post):
                self.assertEqual(method(path).status_code, 404)

    def test_create_and_edit(self):
        self.client.force_login(self.owner)
        self.assertRedirects(self.client.post('/new_topic/', {'text': 'New'}), '/topics/')
        topic = Topic.objects.get(text='New')
        self.assertEqual(topic.owner, self.owner)
        self.assertRedirects(self.client.post(f'/new_entry/{topic.pk}/', {'text': 'Created'}), f'/topics/{topic.pk}/')
        entry = topic.entry_set.get()
        self.assertRedirects(self.client.post(f'/edit_entry/{entry.pk}/', {'text': 'Updated'}), f'/topics/{topic.pk}/')
        entry.refresh_from_db()
        self.assertEqual(entry.text, 'Updated')

    def test_foreign_data_is_protected(self):
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get('/topics/'), 'Private topic')
        for path in (f'/topics/{self.topic.pk}/', f'/new_entry/{self.topic.pk}/', f'/edit_entry/{self.entry.pk}/'):
            for method in (self.client.get, self.client.post):
                self.assertEqual(method(path, {'text': 'Hacked'}).status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.text, 'Private entry')
        self.assertEqual(Entry.objects.count(), 1)

    def test_get_logout_preserves_session(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get('/users/logout/').status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)

    def test_empty_entry_is_rejected(self):
        self.client.force_login(self.owner)
        response = self.client.post(f'/new_entry/{self.topic.pk}/', {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entry.objects.count(), 1)
