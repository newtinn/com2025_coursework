from django.test import TestCase
from django.urls import reverse

class HomePageTests(TestCase):

    def setUp(self):
        return

    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Home')
        self.assertContains(response, 'Welcome to the home page')

    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
    
        self.assertContains(response, 'Contact')
        #self.assertContains(response, 'Contact Us')
        #self.assertContains(response, 'This is my footer')
