# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [] - yyyy-mm-dd

### Added

### Changed

### Fixed

## [0.6.3] - 2022-20-08

Maintenance Release

## 0.6.2 - 2023/07/20

## Added

- `RELAYS_APP_BRANDNAME`, used in message titles
- More DM Handling, Private and Group channels should have titles and messages should relay properly. More testing required.

## Fixed

- Some blank translate strings breaking admin panes
- make tests happy with changed strings
- hard skip edits where the content remains the same to prevent non user initiated edit-spam, discord tends to send edit events enthusiastically.

## Changed

- Dropped testing support for pypy, its performance was incredibly underwhelming in our scenarios

## 0.5.0 - 2023/06/27

- Embed handling
- Threads not having parents/parents are channels not categories
- moar tests
- admin panel fixed and some exceptions edge cases
- Bump googletrans version to fix some issues

## 0.5.0 - 2023/06/19

## Added

- Ingest of Events, Threads and more

## Changed

- User is now a Model, created off the author_id, hopefully this migrates cleanly.
- Embeds now relay cleanly as new signals
- Translations

## 0.5.0 - 2023/06/14

## Added

- on_disconnect() event status update

## Changed

- Moved Message Processing and Relays out of Ingest
- use nice generated embeds for relay outputs

## 0.4.3 - 2023/06/13

## Changed

- Admin view improvements

## Fixed

- Admin view improvements
- tests pass lmao
- adds headers to discordbot messages. These have literally _never_ been in the code so i have no idea how they were working...?

## 0.4.2 - 2023/06/13

## Fixed

- Python 3.8,3.9 compat <https://peps.python.org/pep-0604/>

## 0.4.1 - 2023/06/13

## Fixed

- Added Missing admin Views

## 0.4.0 - 2023/06/13

## Added

- Basic discordbot cog, more is planned
- Web views for servers and messages
- DM/Threads/Events/ and more ingest, relay planned.

## Changed

- Relayconfigs are decoupled from tokens
- Massively rewrote the ingest side of the discord runner, moving code into the relays app itself
- Uses our own logging config, readme for more
- All messages are DB logged by default,
- added discordbot as a dependency, webhooks are less good at scale
- added django-solo for singleton models

## Fixed

- tokens now autoupdate their valid servers on connect
- exceptions _everywhere_

## 0.3.0 - 2023/06/12

Unreleased, Significant refactors

## 0.2.1 - 2022/09/18

Temporarily move back to git deployments, pypi gets mad im using selfcord from git, which isnt published to pypi

## 0.2.0 - 2022/09/18

This is a maintenance update to keep the package operational, I dont actively manage any relays anymore and probably wont notice the next time this fails. ymmv.

Make sure to pull a new `runner_discord.py`

### Changed

- Now uses Discord.py-self library, <https://github.com/dolfies/discord.py-self> imported as selfcord to not clash with existing libraries.
- Re-did package, precommit, setup.cfg etc to modernize whole project

### Fixed

- Updated to Django 4.0, AA3.x

## 0.1.0 - 2020/11/13

Public Release, many thanks to those who tested AA-Relays and reported issues

## Fixed

- Corrected Channel and Server Filtering
- Relay Configurations are now easier to setup with Horizontal filtering, especially relevant with making channels searchable in the Relay Configurations admin panel
- Readme made clearer based on feedback and corrected some venv issues

## 0.0.1a2 - 2020/10/23

### Changed

It is now possible to define multiple relay configurations for a single token.

## [0.0.1a1] - 2020/10/22

Public Beta Release

### Added

### Changed

### Fixed
