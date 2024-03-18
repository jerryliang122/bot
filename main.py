from khl import Message, Bot
import os
import logging
import kook.chat_dify as chat_dify
import kook.help as helps

logging.basicConfig(level="INFO")

## websocket
bot = Bot(token=os.environ.get("kook_token"))


# 在机器人启动的时候执行此函数
@bot.on_startup
async def bot_init(bot: Bot):
    helps.init(bot)
    chat_dify.init(bot)  # 调用支线文件test.py中的init函数来注册命令


bot.run()
