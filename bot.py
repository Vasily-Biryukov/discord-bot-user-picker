import os
import gettext
import random
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

from bot_config import BOT_NAME, BOT_PREFIX, BOT_LANGUAGE, BOT_ENV_TOKEN


# Localization things
translation = gettext.translation('userpicker', localedir='./locale', languages=[BOT_LANGUAGE])
translation.install()

class LocalizedHelpCommand(commands.DefaultHelpCommand):
    """Overridden for localization purposes."""

    def __init__(self):
        super().__init__(
            # [LOC] Used in ;help group message.
            # commands_heading=_('Commands:'),

            # [LOC] Used in ;help message as default command group.
            no_category=_('No category'),

            # [LOC] Not used at this moment.
            # aliases_heading=_('Aliases:'),

            # [LOC] Brief description for ;help command.
            command_attrs=dict(help=_('Shows this message.'))
        )

    def command_not_found(self, command):
        # [LOC] Message for ;help <command> output when command is unknown.
        return _('No command called "{}" found').format(command)

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            # [LOC] Message for ;help <group> <subcommand> when subcommand is unknown.
            return _('Command "{0.qualified_name}" has no subcommand named {1}').format(command, string)

        # [LOC] Message for ;help <group> <subcommand> when group is a command, not a group.
        return _('Command "{0.qualified_name}" has no subcommands.').format(command)

    # Not used by default
    # def get_opening_note(self):
    #    command_name = self.invoked_with
    #    return _(
    #       'Use `{0}{1} [command]` for more info on a command.\n'
    #       'You can also use `{0}{1} [category]` for more info on a category.'
    #    ).format(self.clean_prefix, command_name)

    def get_ending_note(self):
        command_name = self.invoked_with
        # [LOC] Used as a footprint for ;help command.
        return _('Type {0}{1} command for more info on a command.').format(self.clean_prefix, command_name)

localized_help_command = LocalizedHelpCommand()


# Implementation
def pick_impl(ctx, count):
    if count < 1:
        # [LOC] Used with ;pick <n> when n < 1.
        return _('You must pick at least one member.')

    author = ctx.author
    if not(hasattr(author, 'voice') and author.voice and author.voice.channel):
        # [LOC] Used with ;pick when user not in voice channel.
        return _(
            'You must be in a voice channel :loudspeaker: '
            'and {} must have access to this channel.'
        ).format(BOT_NAME)

    members = author.voice.channel.members
    if len(members) < 2:
        # [LOC] Used with ;pick when user is alone in voice channel.
        return _(
            'You are alone in this channel :thinking: Call some friends!\n'
            'Do you have friends, are you?'
        )

    if len(members) < count:
        # [LOC] Used with ;pick <n> when n greater than number of members in voice channel.
        return _('Too few members in this channel')

    sample = random.sample(members, count)
    return ', '.join([user.mention for user in sample])


# Create bot and add bot commands
bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    # [LOC] Bot description. First line in the ;help command output.
    description=_('User picker.'),
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'{BOT_PREFIX}help',
    )
)

# ;help
bot.help_command = localized_help_command

# ;pick
@bot.command(
    # [LOC] Brief description of ;pick command, used in ;help message.
    brief=_('Pick random member.'),

    # [LOC] Detailed description of ;pick command, used in ;help pick message.
    help=_(
        'Randomly pick specified number of members from your voice channel (including you) and print their names.\n'
        'For example:\n'
        '{0}pick - prints random member name from your voice channel.\n'
        '{0}pick 2 - prints two random members names from your voice channel.'
    ).format(BOT_PREFIX),

    # [LOC] Brief description of ;pick command, used in ;help pick message.
    description=_('Pick random member(s) from your voice channel.'),
)
async def pick(ctx, count=1):
    await ctx.send(pick_impl(ctx, count))


# Add slash commands
class ApplicationCommandOptionType:
    SUB_COMMAND=1
    SUB_COMMAND_GROUP=2
    STRING=3
    INTEGER=4
    BOOLEAN=5
    USER=6
    CHANNEL=7
    ROLE=8

slash = SlashCommand(bot, auto_register=True)

# /pick-user
@slash.slash(
    name='pick-user',
    description=_('Pick random member(s) from your voice channel.'),
    options=[manage_commands.create_option(
        name='count',
        description=_('members count (1 by default)'),
        option_type=ApplicationCommandOptionType.INTEGER,
        required=False
    )]
)
async def pick_user(ctx, count=1):
    await ctx.send(content=pick_impl(ctx, count))


# Run bot
token = os.environ[f'{BOT_ENV_TOKEN}']
bot.run(token)
