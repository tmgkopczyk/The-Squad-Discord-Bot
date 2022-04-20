import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import os
from keep_alive import keep_alive
from datetime import datetime
import requests
import json



client = commands.Bot(command_prefix='-', intents = discord.Intents.all(),help_command=None)


welcome_msg_id = ''
my_secret = os.environ["TOKEN"]
suchatryhard_black = 0x000000

@client.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
  avaliable_commands = ['ban','Bans specifc member from the server that the user mentions','changenick','Changes the specified user\'s server name to that of which they want.','clear',"clears the number of messages from the channel that the user specifies",'help','Shows this message','kick','Kicks a member from the server.','lockdown',"locks down the channel that the user names.",'ping',"Checks the bot's response time to the server.",'poll','Poll command allows for users to either have a good discussion of certain topics (or engage in heated debates/arguments with reasons why their opinion is better).','socials','Displays the socials of SuchATryHard','unban','Unbans the mentioned user from the server.','unlock','Unlocks the channel that was previously locked.']
  commands_list = discord.Embed(
    title = 'Administrator Commands List',
    description = "{}".format('\n'.join(avaliable_commands)),
    timestamp = datetime.now(),
    color = suchatryhard_black
  )
  await ctx.send(embed=commands_list)
    
@help.error
async def help(ctx, error):
  avaliable_commands = ['changenick','Changes the specified user\'s server name to that of which they want.','help','Shows this message','ping',"Checks the bot's response time to the server.",'poll','Poll command allows for users to either have a good discussion of certain topics (or engage in heated debates/arguments with reasons why their opinion is better).','socials','Displays the socials of SuchATryHard']
  if isinstance(error, CheckFailure):
    commands_list = discord.Embed(
      title = 'Member Commands List',
      description = "{}".format('\n'.join(avaliable_commands)),
      timestamp = datetime.now(),
      color = suchatryhard_black
    )
    await ctx.send(embed=commands_list)
    
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send("Kicked {0} for reason {1} ".format(member.mention, reason))


@client.event
async def on_raw_reaction_add(payload):
    msg_id = welcome_msg_id
    if msg_id == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '👍':
            role = discord.utils.get(guild.roles, name="Subscribers")
        await member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):
    msg_id = welcome_msg_id
    if msg_id == payload.message_id:
        guild = await (client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '👍':
            role = discord.utils.get(guild.roles, name="Subscribers")
        member = await (guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found")


@client.command(pass_context=True)
async def bye(ctx):
    welcome_msg = discord.Embed(
        title='Welcome to the official Server of SuchATryHard!',
        description='React to this mesage to gain access to the server!',
        color=suchatryhard_black,
        timestamp = datetime.now()
    )
    msg = await ctx.channel.send(embed=welcome_msg)
    await msg.add_reaction('👍')


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send("Banned {0} for reason {1} ".format(member.mention, reason))


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    unban = discord.Embed(
        title="Success!",
        description="{} has been successfully unbanned.".format(user.mention))
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=unban)
        await guild.unban(user=user)


@client.command()
async def poll(ctx, message, *options):
  indicator_list = ['🇦','🇧','🇨','🇩']
  close_ended_question_responder = ['👍','👎']
  poll = discord.Embed(
    title = message,
    description = "{}".format('\n'.join(options)),
    color=suchatryhard_black,
    timestamp = datetime.now(),
  )
  msg = await ctx.channel.send(embed=poll)
  if len(options) > 1:
    for i in range(len(options)):
      await msg.add_reaction(indicator_list[i])
  elif len(options) == 1:
    for i in range(len(close_ended_question_responder)):
      await msg.add_reaction(close_ended_question_responder[i])
   
    
  

    
@client.command()
async def socials(ctx):   
  socials_list = ["YouTube","https://www.youtube.com/channel/UCHMXHaWoFTa4FRsm7aLaUbQ","Twitter","https://twitter.com/SuchATryHard","Twitch","https://www.twitch.tv/SuchATryHard"]
  linktree = discord.Embed(
    title='Socials',
    description="\n".join(socials_list),
    color=suchatryhard_black,
    timestamp = datetime.now()
  )
  await ctx.channel.send(embed=linktree)


@client.command()
async def ping(ctx):
    ping = discord.Embed(
        title='Pong!',
        description="Your ping to the client is {}ms!".format(
            round(client.latency * 1000)),
        color=suchatryhard_black,
        timestamp=datetime.now(),
    )
    await ctx.channel.send(embed=ping)


@client.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=False)
    await ctx.send('{} is now in lockdown'.format(ctx.channel.mention))


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=True)
    await ctx.send('{} has been unlocked'.format(ctx.channel.mention))


@client.command(pass_context=True)
async def changenick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send('Nickname was changed for {}'.format(member.mention))


@client.command()
@commands.has_permissions(manage_channels=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)



keep_alive()
client.run(my_secret)