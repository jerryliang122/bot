import aiohttp
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import logging


class GenerateImage(BaseModel):
    prompt: str
    negative_prompt: str = Field("", title="负提示")
    seed: int = Field(-1, title="种子")
    subseed: int = Field(-1, title="子种子")
    subseed_strength: float = Field(0, title="子种子强度")
    seed_resize_from_h: int = Field(-1, title="种子高度调整")
    seed_resize_from_w: int = Field(-1, title="种子宽度调整")
    sampler_name: str = Field("DPM++ 2M Karras", title="采样器名称")
    batch_size: int = Field(1, title="批次大小")
    n_iter: int = Field(1, title="迭代次数")
    steps: int = Field(25, title="步骤")
    cfg_scale: int = Field(7, title="CFG 规模")
    width: int = Field(512, title="宽度")
    height: int = Field(512, title="高度")


class stable_diffusion:
    def __init__(
        self,
        negative_prompt: str = "",
        seed: int = -1,
        subseed: int = -1,
        subseed_strength: float = 0,
        seed_resize_from_h: int = -1,
        seed_resize_from_w: int = -1,
        sampler_name: str = "DPM++ 2M Karras",
        batch_size: int = 1,
        n_iter: int = 1,
        steps: int = 25,
        cfg_scale: int = 7,
        width: int = 512,
        height: int = 512,
    ):
        # 读取地址在env环境
        self.url = os.environ.get("stable_diffusion_url")
        self.params = {
            "negative_prompt": negative_prompt,
            "seed": seed,
            "subseed": subseed,
            "subseed_strength": subseed_strength,
            "seed_resize_from_h": seed_resize_from_h,
            "seed_resize_from_w": seed_resize_from_w,
            "sampler_name": sampler_name,
            "batch_size": batch_size,
            "n_iter": n_iter,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
        }

    async def txt2img(self, txt: str):
        # 拼接URL
        url = self.url + "/sdapi/v1/txt2img"
        # 在self.params中添加新的参数
        self.params["prompt"] = txt
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=self.params) as response:
                if response.status == 200:
                    r = response.json()
                    # 将json中的images的列表中的值取出
                    return (r["images"], True)
                else:
                    logging.error(
                        f"服务器错误,返回的状态是:{response.status}", exc_info=True
                    )
                    return ("出现问题,服务器错误", False)
