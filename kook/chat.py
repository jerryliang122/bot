from khl import Bot, Message


def init(bot: Bot):
    @bot.command()
    async def help(msg: Message):
        menu = """
T.G.超图书馆员♂
/help chat 查看chat相关说明
"""
        await msg.reply(menu, use_quote=False)

    @bot.command(name="help chat")
    async def help_chat(msg: Message):
        menu = """
        T.G.超图书馆员♂
        /dify on 将在该频道启动dify知识库的AI 聊天功能
        /dify off 将在该频道关闭dify知识库的AI 聊天功能
        """
