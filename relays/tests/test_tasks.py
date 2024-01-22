from unittest import TestCase, mock

from relays.models import Channel, Message, RelayConfiguration, Server, User
from relays.tasks import process_message


class YourModuleTests(TestCase):

    def setUp(self):
        Server.objects.all().delete()
        Channel.objects.all().delete()
        User.objects.all().delete()
        Message.objects.all().delete()
        self.server = Server.objects.create(server=1, name="Test Server", protocol="Discord")
        self.channel = Channel.objects.create(channel=1, name="Test Channel", server=self.server)
        self.user = User.objects.create(id=1, name="Test User")
        self.message = Message.objects.create(
            message=1, channel=self.channel, content="Test message", user=self.user)

    @mock.patch("relays.models.Message.objects.get")
    @mock.patch("relays.models.RelayConfiguration.objects.all")
    def test_process_message(self, mock_relay_configs, mock_get_message):
        # Create a mock Message instance
        message_pk = 1
        message = self.message
        mock_get_message.return_value = message

        # Create a mock RelayConfiguration instance
        relay_configuration = RelayConfiguration(id=1)
        relay_configuration.source_servers.all = mock.Mock()
        relay_configuration.source_server_all = True
        relay_configuration.source_channels.all = mock.Mock()
        relay_configuration.source_channel_all = True
        relay_configuration.message_mention = True
        relay_configuration.message_non_mention = False
        relay_configuration.message_regex = "test_regex"
        relay_configuration.destination_webhooks.all = mock.Mock()
        relay_configuration.destination_aadiscordbot.all = mock.Mock()
        mock_relay_configs.return_value = [relay_configuration]

        # Call the process_message task
        process_message(message_pk)

# Assert that the mock objects and methods were called
        mock_get_message.assert_called_once_with(pk=message_pk)

    @mock.patch("relays.models.Message.objects.get")
    @mock.patch("relays.models.RelayConfiguration.objects.all")
    def test_process_message_no_configurations(self, mock_relay_configs, mock_get_message):
        # Create a mock Message instance
        message_pk = 1
        message = self.message
        mock_get_message.return_value = message

        # No RelayConfiguration objects
        mock_relay_configs.return_value = []

        # Call the process_message task
        process_message(message_pk=message_pk)

        # Assert that the mock objects and methods were called
        mock_relay_configs.assert_called_once_with()
