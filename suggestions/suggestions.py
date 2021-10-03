
import datetime
import typing
from logging import getLogger
from json import JSONDecodeError

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

logger = getLogger('Modmail')


class Suggestion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.command(name="setsuggestchannel", aliases=['setsuggestionchannel'])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def set_suggestion_channel(self, ctx, channel: discord.TextChannel):
        logger.info('Setting channel.id for suggestions.')
        await self.db.find_one_and_update(
            {'_id': 'suggestions'},
            {'$set': {'channel_id': channel.id}},
            upsert=True
        )
        await ctx.send(f'Successfully set the suggestion channel to {channel.mention}.')



    async def get_suggestion_channel(self, ctx):
        logger.debug('Retrieving channel_id for logger from config.')
        data = await self.db.find_one({'_id': 'suggestions'})
        if data is None:
            raise ValueError(f'I was unable to find a suggestion channel. Try `{self.bot.prefix}setsuggestchannel #channel` to set one.')
        channel_id = data.get('channel_id')
        if channel_id is None:
            raise ValueError(f'I was unable to find a suggestion channel. Try `{self.bot.prefix}setsuggestchannel #channel` to set one.')
        channel = self.bot.guild.get_channel(channel_id) or self.bot.modmail_guild.get_channel(channel_id)
        if channel is None:
            logger.error(f'Suggestion channel with the id: `{channel_id}` could not be found.')
            raise ValueError(f'Suggestion channel with the id: `{channel_id}` could not be found.')

        return channel

    @commands.command(name="suggest")
    @commands.cooldown(1, 300, commands.BucketType.channel)
    async def _suggest(self, ctx, *, suggestion):
        if len(suggestion) <= 10 or len(suggestion) >= 1500:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("Suggestion must be between 10 and 1500 characters.")

        channel = await self.get_suggestion_channel(ctx)
        msg_ = await channel.send(embed=discord.Embed(
            title="New Suggestion!",
            description=suggestion,
            color=self.bot.main_color
        ).set_thumbnail(url=ctx.author.avatar_url).set_footer(text=f"Submitted by: {ctx.author}")
        )
        await msg_.add_reaction('\N{THUMBS UP SIGN}')
        await msg_.add_reaction('\N{THUMBS DOWN SIGN}')

        await ctx.reply("Successfully submitted your suggestion.")




def setup(bot):
    bot.add_cog(Suggestion(bot))