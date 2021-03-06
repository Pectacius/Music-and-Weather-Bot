import random
import os

from discord.ext import commands
from discord import Embed, File, Member

from custom_errors import NoMemberError
import utils


class GeneralMessageCog(commands.Cog):
    SPIDER_PATH = os.path.join(utils.IMAGE_DIR, 'spider.jpg')
    OOF_PATH = os.path.join(utils.IMAGE_DIR, 'oof.jpg')

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.previous_member = None
        self.member_name = None

    @commands.command()
    async def about(self, ctx: commands.Context) -> None:
        """Sends a message on the who the bot is and the bot's maker"""
        cool_image_path = os.path.join(utils.IMAGE_DIR, 'special.jpg')
        cool_image_file = File(fp=cool_image_path, filename='special.jpg')

        # create and format embed
        about_embed = Embed(title="About",
                            description=f"Info on {self.bot.user.name}",
                            color=0xffa500)
        about_embed.add_field(name=f"Who I Am:",
                              value='I am A Spiritual Lyrical Miracle Individual',
                              inline=False)
        about_embed.add_field(name='Maker:', value="Made by Pectacius" + '\u1d48' + '\u1d49' + '\u1d5b')
        about_embed.set_image(url="attachment://special.jpg")
        await ctx.send(file=cool_image_file, embed=about_embed)

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        """Sends a message to greet the user, sends special message if member says hi more than once in a row"""
        author = ctx.author
        if self.previous_member is None or self.previous_member.id != author.id:
            await ctx.send(f'Greetings {author.name}')
            self.previous_member = author
        else:
            await ctx.send(f'Greeting {author.name}, this does seem familiar...')

    @commands.command()
    async def roast(self, ctx: commands.Context, member: Member) -> None:
        """Pings <member> with a random roast"""
        guild_members = self.bot.get_all_members()

        roasts = {'roblox': (('stop being having autism', "go commit breathn't", 'you were born out of your dad',
                              'you think you funny but look at ya hairline be looking like the macdondald symble',
                              'do you are have stupid', 'yeetus yeetus commit self deletus'),
                             self.SPIDER_PATH),
                  'weirdness': (('ur a trophy{}\n a catas..trophy'.format('\n...' * 3),
                                 'ur pretty{}\n pretty ugly'.format('\n...' * 3)),
                                self.OOF_PATH)}

        roast = random.choice(list(roasts.items()))
        roast_msg = random.choice(roast[1][0])
        roast_img = roast[1][1]

        if member in guild_members:
            # create embed message
            roast_file = File(fp=roast_img, filename='roast_img.jpg')
            roast_embed = Embed(title=self.bot.user.name + " says:", description=roast_msg)
            roast_embed.set_image(url='attachment://roast_img.jpg')
            await ctx.send(member.mention)
            await ctx.send(file=roast_file, embed=roast_embed)
        else:
            raise NoMemberError

    @commands.command()
    async def flip_coin(self, ctx: commands.Context, number: int) -> None:
        """Flips a coin <number> amount of times and sends result in chat"""
        for times in range(number):
            result = random.choice(['Heads', 'Tails'])
            await ctx.send(result)

    @commands.command()
    async def roll_dice(self, ctx: commands.Context, sides: int, number: int) -> None:
        """Rolls a <sides> sided die <number> amount of times and sends result in chat"""
        for times in range(number):
            result = random.choice(range(1, sides + 1))
            await ctx.send(f'{result}')


def setup(bot: commands.Bot) -> None:
    """Loads GeneralMessageCog"""
    bot.add_cog(GeneralMessageCog(bot))
