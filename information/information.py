import datetime
import discord
from discord.ext import commands
from discord import Spotify



class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.datetime.utcnow()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def serverinfo(self, ctx):
        ''' Displays information about the server. '''

        guild = ctx.guild
        counter, counter1, counter2, counter3 = 0, 0, 0, 0
        for member in ctx.guild.members:
            if member.status == discord.Status.offline:
                counter += 1
            elif member.status == discord.Status.idle:
                counter1 += 1
            elif member.status == discord.Status.do_not_disturb:
                counter2 += 1
            elif member.status == discord.Status.online:
                counter3 += 1

        embed = discord.Embed(
            title=f" Guild Information", colour=self.bot.main_color)

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon_url)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner_url_as(format="png"))

        if len(ctx.guild.roles) <= 20:
            roles = guild.roles[1:][::-1]
        else:
            roles = guild.roles[-20:][::-1]

        emojis = guild.emojis[:20]

        embed.add_field(
            name="Server:", 
            value=f"""
**Guild ID:** `{guild.id}`
**Owner:** `{guild.owner}`
**Members:** `{len(ctx.guild.members)}`
**Server Created:** `{ctx.guild.created_at.strftime('%a, %d %b %Y, %I:%M %p')}`""")
        embed.add_field(
            name=f"Members [{len(ctx.guild.members)}]:",
            value=f"""
**Online:** `{counter3}`
**Idle:** `{counter1}`
**Dnd:** `{counter2}`
**Offline:** `{counter}`""")
        embed.add_field(
            name=f"Channels [{len(ctx.guild.channels)}]:",
            value=f"""
**Categories:** `{len(guild.categories)}`
**Text Channels:** `{len(guild.text_channels)}`
**Voice Channels:** `{len(guild.voice_channels)}`""")
        embed.add_field(
            name=f"Server Settings:",
            value=f"""
**Region:** `{guild.region}`
**Sytem channel:** `{guild.system_channel}`
**Verfication level:** `{guild.verification_level}`
**Boosts:** `{ctx.guild.premium_subscription_count}`""", 
            inline=False)
        if len(roles) == 0:
            pass
        else:
            embed.add_field(name=f"Roles [{len(ctx.guild.roles) - 1}]:",
                            value=" ".join([role.mention for role in roles]))
        if len(emojis) == 0:
            pass
        else:
            embed.add_field(name=f"Emojis [{len(ctx.guild.emojis)- 1}]:", value=" ".join(
                [(f'<:{emoji.name}:{emoji.id}>' if not emoji.animated else f'<a:{emoji.name}:{emoji.id}>') for emoji in emojis]), inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role):
        ''' Displays information about a role. '''

        created = f"{role.created_at.strftime('%a, %d %b')}"
        embed = discord.Embed(
            title=f"Role Information",
            color=self.bot.main_color
        )
        embed.add_field(
            name="Role",
            value=f"{role.mention}"
        )

        embed.add_field(
            name="Role ID",
            value=f"`{role.id}`"
        )

        embed.add_field(
            name="Position",
            value=f"`{role.position}`"
        )

        embed.add_field(
            name="Members",
            value=f"`{len(role.members)}`"
        )

        embed.add_field(
            name="Mentionable",
            value=f"`{role.mentionable}`"
        )

        embed.add_field(
            name="Created",
            value=f"`{created}`"
        )

        embed.add_field(
            name="Color",
            value=f"`#{str(role.color)[1:]}`"
        )

        embed.add_field(
            name="Hoisted",
            value=f"`{role.hoist}`"
        )

        perms_ = ""
        for permission in role.permissions:
            a, b = permission
            a = ' '.join(a.split('_')).title()
            format_ = '+' if b else '-'
            perms_ += format_ + ' ' + a + '\n'
        embed.add_field(
            name="Permissions:",
            value=f"```diff\n{perms_}\n```",
            inline=False
        )
        await ctx.reply(embed=embed)


    @commands.command(aliases=['av'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        ''' Returns the users avatar. '''

        member = member or ctx.author
        if member.is_avatar_animated():
            embed = discord.Embed(
                title=f"{member.name} Avatar", description=f"**Formats:** [PNG]({member.avatar_url_as(format='png', size=1024)}) **|** [JPG]({member.avatar_url_as(format='jpg', size=1024)}) **|** [WEBP]({member.avatar_url_as(format='webp', size=1024)}) **|** [GIF]({member.avatar_url_as(format='gif', size=1024)})", colour=SUCCESS_COLOUR)
        else:
            embed = discord.Embed(
                title=f"{member.name} Avatar", description=f"**Formats:** [PNG]({member.avatar_url_as(format='png', size=1024)}) **|** [JPG]({member.avatar_url_as(format='jpg', size=1024)}) **|** [WEBP]({member.avatar_url_as(format='webp', size=1024)})", colour=SUCCESS_COLOUR)

        embed.set_image(url=member.avatar_url)
        await ctx.reply(embed=embed)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        ''' Displays information about the user. '''

        member = member or ctx.author
        if member.is_on_mobile() == True:
            device = "Mobile"
        else:
            device = "Desktop"
        for activity in member.activities:
            if isinstance(activity, Spotify):
                status = f"listening to **{activity.title}** by **{activity.artist}**"
            else:
                status = member.activity
        if member.activity == None:
            status = "User has no status"
        embed = discord.Embed(
            title=f"User Info",
            description=f"**Custom Status:**\n {status}",
            colour=self.bot.main_color
        )
        embed.add_field(
            name="Mention",
            value=f"{member.mention}"
        )
        embed.add_field(
            name="Discriminator",
            value=f"`#{member.discriminator}`"
        )
        embed.add_field(
            name="ID",
            value=f"`{member.id}`"
        )
        embed.add_field(
            name="Created At",
            value=f"`{member.created_at.strftime('%a, %b %d, %Y, %I:%M %p')}`"
        )
        embed.add_field(
            name="Joined At",
            value=f"`{member.joined_at.strftime('%a, %b %d, %Y, %I:%M %p')}`"
        )
        embed.add_field(
            name="Top Role",
            value=f"{member.top_role.mention}"
        )
        embed.add_field(
            name="Bot",
            value=f"`{member.bot}`"
        )
        embed.add_field(
            name="Status",
            value=f"`{member.status}`"
        )
        embed.add_field(
            name="Boosted",
            value=f"`{bool(member.premium_since)}`"
        )
        embed.add_field(
            name="Device",
            value=f"`{device}`"
        )

        roles = ""

        for role in member.roles[::-1]:
            if len(roles) > 500:
                break
            if str(role) != "@everyone":
                roles += f"{role.mention} "
        if len(roles) == 0:
            roles = "User has no roles."
        embed.add_field(
            name=f"Roles [{len(member.roles)}] ",
            value=roles,
            inline=False
        )
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=embed)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def firstmessage(self, ctx, channel: discord.TextChannel = None):
        ''' Displays first message in a channel. '''

        channel = channel or ctx.channel
        history = await channel.history(limit=1, oldest_first=True).flatten()
        if not history:
            return await ctx.reply("Couldn't find the message!")
        message = history[0]
        embed = discord.Embed(title=f"First Message in {channel.name}",
                              color=self.bot.man_color, description=f"[**Jump To Message**]({message.jump_url})")
        embed.add_field(
            name="Author:", value=f"`{message.author}`", inline=True)
        embed.add_field(name="Message:",
                        value=f"`{message.content}`", inline=True)
        embed.add_field(name="Message Creation Date:",
                        value=f"`{message.created_at.strftime('%a, %d %b %Y, %I:%M %p')}`", inline=True)
        embed.add_field(name="ID:", value=f"`{message.id}`", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def uptime(self, ctx):
        ''' Displays the bot's uptime. '''

        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        embed = discord.Embed(title=f"Bot's Uptime",
                              description=f"```{days} days, {hours} hours, {minutes} minutes, {seconds} seconds```", colour=self.bot.main_color)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)