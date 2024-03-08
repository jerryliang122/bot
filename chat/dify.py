import aiohttp
import json
import os
import asyncio


class dify:
    def __init__(self):
        self.dify_url = os.environ.get("dify_url")
        # 检查环境变量中是否有dify_token
        self.dify_token = os.environ.get("dify_token")

    async def handle_message(self, data):
        # 将data 转为字典
        data = json.loads(data)
        # 检查该字典中的conversation_id 的值是否为session_id
        # if data["conversation_id"] != session_id:
        #    return
        # 读取data中的event
        event = data["event"]
        if event == "agent_message" or event == "message":
            return (data["answer"], data["conversation_id"])
        else:
            return (None, None)

    async def ask(self, session_id: str, user: str, query: str):
        """
        异步发送查询请求并处理响应。

        参数:
        - session_id: 会话ID，用于标识特定的会话。
        - user: 用户标识，表示发起查询的用户。
        - query: 查询字符串，用户的问题或指令。

        返回值:
        无返回值，但会异步处理接收到的服务器发送事件（SSE）。
        """
        # 将session 存储为内部变量
        self.session_id = session_id
        self.user = user
        # 如果没有配置环境变量直接返回一段消息
        if self.dify_url == None or self.dify_token == None:
            yield "请检查dify环境变量是否配置正确"
        # 构建请求的URL和头部
        url = self.dify_url + "/chat-messages"
        headers = {
            "Authorization": f"Bearer {self.dify_token}",  # 使用Bearer Token进行授权
            "Content-Type": "application/json",
        }

        # 准备请求体数据
        data = {
            "inputs": {},
            "query": query,  # 用户的查询
            "response_mode": "streaming",  # 使用流式响应模式
            "conversation_id": session_id,  # 指定会话ID
            "user": user,  # 指定用户
        }

        # 使用aiohttp发送异步POST请求
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                # 检查响应状态码
                if resp.status == 200:
                    buffer = ""  # 用于累积响应数据的缓冲区
                    async for chunk in resp.content.iter_any():
                        buffer += chunk.decode("utf-8")  # 解码响应内容
                        parts = buffer.split("\n\n")
                        for part in parts[:-1]:
                            if part.startswith("data: ") and len(part) > len("data: "):
                                part = part.replace("data: ", "")
                                data = part.strip()
                                answer, conversation_id = await self.handle_message(
                                    data
                                )
                                if answer != None:  # 如果answer不为空
                                    yield (answer, conversation_id)
                else:
                    yield "服务器返回了错误的状态码" + str(resp.status)

    async def close(self, session_id, user):
        """
        异步关闭当前会话。

        该方法会向服务器发送一个请求，以结束当前用户的会话。

        参数:
        - self: 对象自身的引用。

        返回值:
        - 无返回值。
        """
        # 构建请求的URL和头部
        url = self.dify_url + f"/conversations/{session_id}"
        headers = {
            "Authorization": f"Bearer {self.dify_token}",  # 使用Bearer Token进行授权
            "Content-Type": "application/json",
        }

        # 准备请求体数据
        data = {
            "user": user,  # 指定用户
        }
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers, json=data) as resp:
                # 检查响应状态码
                if resp.status == 200:
                    print("会话已结束")
                else:
                    print("服务器返回了错误的状态码" + str(resp.status))
