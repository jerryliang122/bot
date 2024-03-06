import aiohttp
import json
import sys


class dify:
    def __init__(self):
        # 先运行检查环境变量
        self.check_status = self.check()
        if self.check_status == True:
            self.dify_url = sys.environ.get("dify_url")
            # 检查环境变量中是否有dify_token
            self.dify_token = sys.environ.get("dify_token")

    # 检查环境变量
    def check(self):
        if "dify_url" not in sys.environ:
            return False
        # 检查环境变量中是否有dify_token
        elif "dify_token" not in sys.environ:
            return False
        else:
            return True

    async def handle_message(session_id, data):
        # 将data 转为字典
        data = json.loads(data)
        # 检查该字典中的conversation_id 的值是否为session_id
        if data["conversation_id"] != session_id:
            return
        # 读取data中的event
        event = data["event"]
        if event == "agent_message":
            return data["answer"]

    async def ask(self, session_id, user, query):
        """
        异步发送查询请求并处理响应。

        参数:
        - session_id: 会话ID，用于标识特定的会话。
        - user: 用户标识，表示发起查询的用户。
        - query: 查询字符串，用户的问题或指令。

        返回值:
        无返回值，但会异步处理接收到的服务器发送事件（SSE）。
        """
        # 如果没有配置环境变量直接返回一段消息
        if self.check_status == False:
            return "请检查dify环境变量是否配置正确"
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
                        parts = buffer.split("\n\n")  # 根据换行符分割响应数据
                        for part in parts[
                            :-1
                        ]:  # 遍历分割后的数据（忽略最后一部分，因为它可能是不完整的）
                            if part.startswith("data: "):  # 找到包含实际数据的部分
                                data = part[len("data: ") :].strip()  # 提取数据
                                answer = await self.handle_message(
                                    session_id, data
                                )  # 异步处理接收到的数据
                                if answer is not None:  # 如果answer不为空
                                    yield answer
                else:
                    return "服务器返回了错误的状态码" + str(resp.status)
