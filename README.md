# AA Relays

This is an Alliance Auth App for forwarding, collating and filtering of messages from various chat services to defined outputs including Database logging.

![License](https://img.shields.io/badge/license-MIT-green) ![python](https://img.shields.io/badge/python-3.6-informational) ![django](https://img.shields.io/badge/django-3.1-informational)

## Features

- Sources

  - Discord Messages, Embeds

- DB Logging
- Destinations

  - Discord Webhook
  - Discord Channel Message via AA-DiscordBot

- UI (Well... admin interface) for selecting sources and destinations

- Filtering By

  - Server Source
  - Channel Source
  - Mentions AND/OR non mentions
  - Regex on the Message Content

- Web UI
  - Servers, their status and metrics
  - Messages in a server.

## Planned Features

- Discord Events, Threads, PrivateMessages
- Slack Source

## Installation

### Step One - Install

Install the app with your venv active

```bash
pip install git+https://gitlab.com/tactical-supremacy/aa-relays.git
```

Pull the Runners

```bash
wget https://gitlab.com/tactical-supremacy/aa-relays/-/raw/master/relays/runner_discord.py
```

### Step Two - Configure

- Add `relays` to INSTALLED_APPS
- Add the below lines to your `local.py` settings file

```python
## Settings for AA-Relays ##
AARELAYS_TRANSLATION_LANGUAGE = "en" #https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages
LOGGING['handlers']['relays_log_file']= {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/relays.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
        }
LOGGING['loggers']['relays'] = {'handlers': ['relays_log_file'],'level': 'DEBUG'}
```

### Step Three - Update Project

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`

### Step Four - Run Relays

The "Runners" need to be ran on your server separately for this to function. While they have the context of Django and Alliance Auth, Each "Relay" own runner process to operate.

Supervisor is one option, which you should have for allianceauth already, this is a sample configuration for starting a runner for discord for the first AccessToken in the database.

`/etc/supervisord.d/aarelays.conf` or `/etc/supervisord.d/aarelays.ini` depending on OS

```python
[program:runner_1]
command=/home/allianceserver/venv/auth/bin/python runner_discord.py 1
directory=/home/allianceserver/myauth/
user=allianceserver
stdout_logfile=/home/allianceserver/myauth/log/relays.log
stderr_logfile=/home/allianceserver/myauth/log/relays.log
autostart=true
autorestart=true
startsecs=10
priority=900

[group:aarelays]
programs=runner_1
priority=900
```

### Step Four-A - Run Relays Docker

```dockerfile
  allianceauth_relay_1:
    container_name: allianceauth_relay_1
    <<: [*allianceauth-base]
    restart: on-failure:1
    entrypoint: [
      "/opt/venv/bin/python",
      "runner_discord.py",
      "1"
    ]
```

## Settings

| Name                          | Description                                                          | Default |
| ----------------------------- | -------------------------------------------------------------------- | ------- |
| AARELAYS_TRANSLATION_LANGUAGE | When attempting a relay translation, what language do I translate to | "en"    |

## Permissions

| Name                | Purpose                                                | Code                  |
| ------------------- | ------------------------------------------------------ | --------------------- |
| Can Access This App | Allow users to submit Access Tokens from the Front-End | `relays.basic_access` |

## Logic

For every message, looping through each Relay Configuration, Messages are Relayed based on the following logic order

```pseudo
Source Server Matches OR All Servers True/False
AND
Source Channel matches OR All Channels True/False
AND
@here/@everyone True/False OR Non Mentions True/False OR Regex (Default ".^" To not match anything, further below)
```

## Regex

Sometimes distinguishing between Mentions and Chatter isn't enough.

Theoretically the full regex library is supported here, but minimal testing has been done, ymmv.

AA Relays Adds header fields into the message string so these cam be regex-ed upon, like so.

`joined_content_with_headers = f"{message.channel.guild.name}/{message.channel.name}/{message.author}: {joined_content}"`

Examples

```psuedo
*supers*
*red pen*

*<@318309023478972417>* For User mentions
*<@&735881663799623710>* for Role Mentions
*supercarriers/318309023478972417/* For a Channel message by a specific Author
```

## Meta

```psuedocode
Runner ->
selfcord.on_message() event ->
relays.ingest.ingest_discord_message_new() ->
django.object ->
signal ->
queue up process_message()
<---thread--->
process_message() ->
fire webhooks / queue up discordbot tasks
<---thread--->
discordbot task ->
send discordbot message
--fin--
```
