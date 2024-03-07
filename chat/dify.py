import aiohttp
import json
import sys
import aiohttp_sse_client
import asyncio


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
        # 将session 存储为内部变量
        self.session_id = session_id
        self.user = user
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
                    sse_client = aiohttp_sse_client.Client(resp)  # 创建一个 sse 客户端
                    try:
                        # 迭代 sse 响应的数据
                        async for data in sse_client.events():
                            answer = await self.handle_message(session_id, data.data)
                            if answer is not None:  # 如果answer不为空
                                yield answer
                    except asyncio.CancelledError:
                        # 处理取消异常
                        print("Cancelled")
                    except Exception as e:
                        # 处理其他异常
                        print(e)
                    finally:
                        # 关闭 sse 客户端
                        await sse_client.close()
                else:
                    return "服务器返回了错误的状态码" + str(resp.status)

    async def close(self):
        # 构建请求的URL和头部
        url = self.dify_url + f"/conversations/{self.session_id}"
        headers = {
            "Authorization": f"Bearer {self.dify_token}",  # 使用Bearer Token进行授权
            "Content-Type": "application/json",
        }

        # 准备请求体数据
        data = {
            "user": self.user,  # 指定用户
        }
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers, json=data) as resp:
                # 检查响应状态码
                if resp.status == 200:
                    print("会话已结束")
                else:
                    print("服务器返回了错误的状态码" + str(resp.status))
