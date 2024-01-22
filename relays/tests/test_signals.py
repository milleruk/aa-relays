from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.test import TestCase

from relays.models import Channel, Message, Server, User
from relays.signals import message_new


class SignalTestCase(TestCase):
    def setUp(self):
        self.server = Server.objects.create(server=2, name="Test Server", protocol="Discord")
        self.channel = Channel.objects.create(channel=1, name="Test Channel", server=self.server)
        self.user = User.objects.create(id=1, name="Test User")
        self.message = Message.objects.create(message=1, channel=self.channel, content="Test message", user=self.user)

    def test_message_new_signal(self):
        # Connect the signal handler to the post_save signal
        post_save.connect(message_new, sender=Message)

        # Emit the post_save signal by saving the Message instance
        self.message.save()

        # Perform assertions based on the expected behavior of the signal handler
        # For example, check if the process_message task was triggered or not
        # You can mock the task function and check if it was called or not

        # Example assertion: Check if process_message task was called
        with self.assertRaises(ObjectDoesNotExist):
            # Attempt to fetch the Message instance created by the signal handler
            Message.objects.get(content='Processed message')
