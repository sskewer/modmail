import discord
from discord.ext import commands
from discord.ext.commands import group
import re
from core import checks
from core.models import PermissionLevel

class SlowMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @group(name="slowmode", invoke_without_command=True)
    @commands.has_any_role(454262524955852800, 454268394464870401)
    async def slowmode(self, ctx, time):
        """
        Impostare la slowmode del canale specificato
        Non è possibile impostare una slowmode superiore alle 6 ore
        """     
        units = {
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1
        }
        seconds = 0
        match = re.findall("([0-9]+[smhd])", time)
        if not match:
            embed = discord.Embed(description="⚠ Il formato tempo utilizzato non è corretto!",color = discord.Color.orange())
            return await ctx.send(embed=embed)
        for item in match:
            seconds += int(item[:-1]) * units[item[-1]]
        if seconds > 21600:
            embed = discord.Embed(description="⚠ Non puoi impostare una slowmode superiore alle 6 ore!", color=discord.Color.orange())
            return await ctx.send(embed=embed)
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
        except discord.errors.Forbidden:
            embed = discord.Embed(description="⚠ Non ho i permessi necessari per fare questo!", color=discord.Color.orange())
            return await ctx.send(embed=embed)
        embed=discord.Embed(description=f"La slowmode per questo canale è ora **{time}**", color=discord.Color.red())
        embed.set_author(name="Modifica Slowmode")
        await ctx.send(embed=embed)


    @slowmode.command(name="off")
    @commands.has_any_role(454262524955852800, 454268394464870401)
    async def off(self, ctx):
        """Disattivare la slowmode in un canale"""
        if not channel:
            channel = ctx.channel
            
        seconds_off = 0
        await ctx.channel.edit(slowmode_delay=seconds_off)
        embed=discord.Embed(description=f"La slowmode per questo canale è ora disattivata", color=discord.Color.red())
        embed.set_author(name="Modifica Slowmode")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SlowMode(bot))
