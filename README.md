# User Picker
![logo](/icon/userpicker.svg)

Is a Discord bot which helps you to answer a complicated questions
like:
* Who's failed the game?
* Who is the most useless player?
* Whose momma is fatter?

And so on.

In other words it randomly picks member(s) from your voice channel.

# Bot commands

#### ;help
Show list of available commands and brief description.

You can type `;help <command>` for detailed description about `<command>`.

#### ;pick
Randomly choose one member from your voice channel (including you) and print his or her name.

#### ;pick n
*n* must be a number from 1 to your voice channel members count.

Randomly choose *n* members from your voice channel (including you) and print their names.

# Installation
* Go to [Discord application page](https://discord.com/developers/applications)
and press **New Application** button.
* Enter the name of your application and press **Create**.
* Change the application icon if you want.
* Go to the **Bot** page and press button **Add Bot**.
* Copy *token* from the bot page.
* Add environment variable *USERPICKERTOKEN* and set your *token* as variable value.
`set USERPICKERTOKEN=<your token>`
* Execute bot.py (if you want logging redirect output to file)
`bot.py >bot.log 2>&1`
* Generate bot invitation link on the **OAuth2** page of your application:
  * In the **scopes** section check *bot* and *applications.commands* options;
  * In the **bot permissions** section check *View Channels* and *Send Messages* options;
  * Copy link from the bottom of the **scopes** section and paste it to your browser.
* In your discord text channel type `;help` for list of commands.
* You can also use `/pick-user` command.

You can change some bot constants before launch in bot_config.py:
* `BOT_NAME` - name of the bot. Used in some messages.
* `BOT_PREFIX` - prefix for all commands. Default is `;`.
Change if default prefix is in conflict with other bots on your Discord server.
* `BOT_ENV_TOKEN` - environment variable with your application token.
Default is *USERPICKERTOKEN*.
* `BOT_LANGUAGE` - used localization.

----
Bot uses [discord.py](https://discordpy.readthedocs.io/en/latest/index.html) package and
[discord-py-slash-command](https://discord-py-slash-command.readthedocs.io/en/latest/index.html) extension.
