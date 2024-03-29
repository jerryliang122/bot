from khl import Bot, Message, EventTypes
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from chat.dify import dify

dify_channel_id = None
dify_conversation_id = None
author_id = None


def init(bot: Bot):
    @bot.command(name="dify")
    async def dify_chat(msg: Message, ages: str):
        global dify_channel_id, author_id, dify_conversation_id
        if ages == "on":
            # 启动dify
            # 获取频道ID
            dify_channel_id = msg.ctx.channel.id
            await msg.reply("已开启dify知识库的AI 聊天功能", use_quote=False)
        elif ages == "off":
            # 关闭dify
            dify_channel_id = None
            chat_dify = dify()
            await chat_dify.close(dify_conversation_id, author_id)
            dify_conversation_id = None
            author_id = None
            await msg.reply("已关闭dify知识库的AI 聊天功能", use_quote=False)
        elif ages == "restart":
            # 重启dify
            chat_dify = dify()
            await chat_dify.close(dify_conversation_id, author_id)
            dify_conversation_id = None
            await msg.reply("已重启dify知识库的AI 聊天功能", use_quote=False)
        else:
            # 未指定参数
            await msg.reply("未指定参数", use_quote=False)

    # 监听该频道事件
    @bot.on_message()
    async def chat(msg: Message):
        global dify_channel_id, dify_conversation_id, author_id
        if msg.content.startswith("/"):
            return
        if msg.ctx.channel.id != dify_channel_id:
            return
        # 实例化dify
        chat_dify = dify()
        if msg.content == "":
            return
        reply_list = []
        reply = chat_dify.ask(dify_conversation_id, msg.author.id, msg.content)
        author_id = msg.author.id
        # 缓存reply 生成器的结果直到结束
        async for i, id in reply:
            reply_list.append(i)
            dify_conversation_id = id
        # 将reply_list 转换成字符串
        reply = "".join(reply_list)
        await msg.reply(reply, use_quote=False)
