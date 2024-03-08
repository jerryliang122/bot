from khl import Bot, Message
from chat.dify import dify


def init(bot: Bot):
    @bot.command(name="help")
    async def help(msg: Message, ages: str):
        if bool(ages) == False:
            menu = """
            T.G.超图书馆员♂
            /help chat 查看chat相关说明
            """
        if ages == "chat":
            menu = """
            T.G.超图书馆员♂
            /dify on 将在该频道启动dify知识库的AI 聊天功能
            /dify off 将在该频道关闭dify知识库的AI 聊天功能
            """
        await msg.reply(menu, use_quote=False)

    @bot.command(name="dify")
    async def dify_chat(msg: Message, ages: str):
        global channel_id
        # 获取频道ID
        channel_id = msg.ctx.channel.id
        if ages == "on":
            # 启动dify
            await msg.reply("已开启dify知识库的AI 聊天功能", use_quote=False)
        elif ages == "off":
            # 关闭dify
            await msg.reply("已关闭dify知识库的AI 聊天功能", use_quote=False)
        else:
            # 未指定参数
            await msg.reply("未指定参数", use_quote=False)
