from khl import Bot, Message, EventTypes
from chat.dify import dify

dify_channel_id == None


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
        global dify_channel_id
        if ages == "on":
            # 启动dify
            # 获取频道ID
            dify_channel_id = msg.ctx.channel.id
            await msg.reply("已开启dify知识库的AI 聊天功能", use_quote=False)
        elif ages == "off":
            # 关闭dify
            dify_channel_id = None
            await msg.reply("已关闭dify知识库的AI 聊天功能", use_quote=False)
        else:
            # 未指定参数
            await msg.reply("未指定参数", use_quote=False)

    # 监听该频道事件
    @bot.on_message()
    async def chat(msg: Message):
        global dify_channel_id
        if msg.ctx.channel.id != dify_channel_id:
            return
        # 实例化dify
        chat_dify = dify()
        if msg.content == "":
            return
        reply_list = []
        reply = await chat_dify.ask(dify_channel_id, msg.author, msg.content)
        # 缓存reply 生成器的结果直到结束
        async for i in reply:
            reply_list.append(i)
        # 将reply_list 转换成字符串
        reply = "".join(reply_list)
        await msg.reply(reply, use_quote=False)
