from django.core import mail
from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Book
import unittest
from django.test import Client


# Create your tests here.
# class SimpleTest(unittest.TestCase):
#     def test_details(self):
#         response = self.client.get('/customer/details/')
#         self.assertEqual(response.status_code, 200)
#
#     def test_index(self):
#         response = self.client.get('/customer/index/')
#         self.assertEqual(response.status_code, 200)


# class BookMethodTests(TestCase):
#     def test_recent_pub(self):
#         """
#             recent_publication() should return
#             False for future publication dates.
#         :return: False
#         """
#         futuredate = timezone.now().date() + datetime.timedelta(days=5)
#         future_pub = Book(publication_date=futuredate)
#         self.assertEqual(future_pub.recent_publication(), False)


class EmailTest(TestCase):
    def test_send_email(self):
        # Send Messsage
        mail.send_mail('Subject here', 'Here is the message.',
                       'kdsnop@gmail.com', ['kkwnop@gmail.com'],
                       )

        # Test One Message sent or not
        self.assertEqual(len(mail.outbox), 1)

        # Confirm First Message Subject is correct or not
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
