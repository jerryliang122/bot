from khl import Bot, Message, EventTypes
from khl.card import Card, CardMessage, Module, Types, Element, Struct


def init(bot: Bot):
    @bot.command(name="help")
    async def help(msg: Message, ages: str = None):
        cm = CardMessage()
        if bool(ages) == False:
            c = Card(
                Module.Header("T.G.超图书馆员♂"),
                Module.Context("正在开发意想不到的功能"),
                Module.Section(
                    "/help chat 查看chat相关说明\n" + "/help sd 查看stable 相关说明"
                ),
            )
        if ages == "chat":
            c = Card(
                Module.Header("T.G.超图书馆员♂"),
                Module.Context("dify知识库的AI 聊天功能"),
                Module.Section(
                    "使用方法：\n"
                    + "/dify on 开启dify知识库的AI 聊天功能\n"
                    + "/dify off 关闭dify知识库的AI 聊天功能\n "
                    + "/dify restart 重启dify知识库的AI 聊天功能\n"
                ),
            )
        if ages == "sd":
            c = Card(
                Module.Header("T.G.超图书馆员♂"),
                Module.Context("stable diffusion 的AI画图"),
                Module.Section(
                    "无法调整模型。需要联系腐竹调整使用的模型。\n"
                    + "使用方法：\n "
                    + "/sd on 在频道中开启，在后面追加参数 即可设置图像输出参数,示例如下\n"
                    + "/sd on (宽度，像素默认512) (高度，像素默认512) (步骤，默认25)\n"
                    + "/sd off 在频道中关闭\n"
                ),
            )
        cm.append(c)
        await msg.reply(cm, use_quote=False)
