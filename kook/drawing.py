from khl import Bot, Message, EventTypes
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from chat.stable_diffusion import stable_diffusion

channel_id = None
width = 512
height = 512
steps = 25


def init(bot: Bot):
    @bot.command(name="sd")
    async def sd(
        msg: Message, args: str, width: int = 512, height: int = 512, steps: int = 25
    ):
        global channel_id
        if args == "on":
            channel_id = msg.ctx.channel.id
            await msg.reply("stable diffusion 已开启")
