from django.test import TestCase
from django.urls import reverse


class HealthTest(TestCase):

    def test_website_is_healthy(self):
        response = self.client.get(reverse('health:index'))
        self.assertContains(response, "I'm healthy")
