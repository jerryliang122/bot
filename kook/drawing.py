from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from chat.stable_diffusion import stable_diffusion
import base64
import io

channel_id = None
width = 512
height = 512
steps = 25
stable_diffusions = None


def init(bot: Bot):
    @bot.command(name="sd")
    async def sd(
        msg: Message, args: str, width: int = 512, height: int = 512, steps: int = 25
    ):
        global channel_id, stable_diffusions
        if args == "on":
            channel_id = msg.ctx.channel.id
            await msg.reply("stable diffusion 已开启")
            stable_diffusions = stable_diffusion(
                width=width, height=height, steps=steps
            )
        elif args == "off":
            channel_id = None
            stable_diffusions = None
            await msg.reply("stable diffusion 已关闭")

    @bot.on_message()
    async def sd_message(msg: Message):
        global channel_id, stable_diffusions
        if msg.ctx.channel.id != channel_id:
            return
        elif msg.content == "/sd off":
            return
        text = msg.content
        images, status = await stable_diffusions.txt2img(text)
        if status == False:
            await msg.reply("stable diffusion 失败")
            return
        image = base64.b64decode(images[0])
        image = io.BytesIO(image)
        img_url = await bot.client.create_asset(image)
        await msg.reply(img_url, type=MessageTypes.IMG)
        return
