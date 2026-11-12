from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from learning_logs.models import Topic, Entry

class TopicModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(text='Test Topic', owner=self.user)

    def test_topic_creation(self):
        self.assertEqual(self.topic.text, 'Test Topic')
        self.assertEqual(self.topic.owner, self.user)

class EntryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(text='Test Topic', owner=self.user)
        self.entry = Entry.objects.create(topic=self.topic, text='Test Entry')

    def test_entry_creation(self):
        self.assertEqual(self.entry.text, 'Test Entry')
        self.assertEqual(self.entry.topic, self.topic)

class TopicViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(text='Test Topic', owner=self.user)
        self.client.login(username='testuser', password='testpass')

    def test_topic_list_view(self):
        response = self.client.get(reverse('learning_logs:topics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Topic')

    def test_topic_detail_view(self):
        response = self.client.get(reverse('learning_logs:topic', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Topic')

class EntryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.topic = Topic.objects.create(text='Test Topic', owner=self.user)
        self.entry = Entry.objects.create(topic=self.topic, text='Test Entry')
        self.client.login(username='testuser', password='testpass')

    def test_entry_edit_view(self):
        response = self.client.get(reverse('learning_logs:edit_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Entry')

class AuthTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.topic1 = Topic.objects.create(text='Topic 1', owner=self.user1)
        self.topic2 = Topic.objects.create(text='Topic 2', owner=self.user2)
        self.entry1 = Entry.objects.create(topic=self.topic1, text='Entry 1')
        self.entry2 = Entry.objects.create(topic=self.topic2, text='Entry 2')

    def test_user_isolation(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.get(reverse('learning_logs:topic', args=[self.topic2.id]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('learning_logs:edit_entry', args=[self.entry2.id]))
        self.assertEqual(response.status_code, 404)

        self.client.login(username='user2', password='testpass')
        response = self.client.get(reverse('learning_logs:topic', args=[self.topic1.id]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('learning_logs:edit_entry', args=[self.entry1.id]))
        self.assertEqual(response.status_code, 404)



class AdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='admin-test-pass-123')
        self.client.login(username='admin', password='admin-test-pass-123')

    def test_admin_requires_login(self):
        self.client.logout()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_models_registered(self):
        response = self.client.get('/admin/')
        self.assertContains(response, 'Topics')
        self.assertContains(response, 'Entries')

    def test_create_topic_and_entry_via_admin(self):
        response = self.client.post('/admin/learning_logs/topic/add/', {
            'text': 'Admin topic',
            'owner': self.admin.id,
            'entry_set-TOTAL_FORMS': '0',
            'entry_set-INITIAL_FORMS': '0',
        })
        self.assertEqual(response.status_code, 302)
        topic = Topic.objects.get(text='Admin topic')
        response = self.client.post('/admin/learning_logs/entry/add/', {
            'topic': topic.id,
            'text': 'Admin entry',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(topic=topic, text='Admin entry').exists())
