import re
import time
from uuid import UUID

from aiohttp import ClientResponse
from graia.amnesia.builtins.aiohttp import AiohttpClientInterface
from launart import Launart


def format_time(timestamp: int) -> str:
    """
    格式化时间戳

    :return: 当前时间，格式1970-01-01 12:00:00
    """
    time_local = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_local)


async def is_mc_id(mc_id: str) -> bool:
    """
    判断是否为合法的正版ID

    :param mc_id: 正版用户名（id）
    :return: `True`为是，`False`为否
    """
    return bool(1 <= len(mc_id) <= 16 and re.match(r'^[0-9a-zA-Z_]+$', mc_id))


async def is_uuid(mc_uuid: str) -> bool:
    """
    判断是否为合法uuid
    """
    try:
        UUID(mc_uuid)
    except ValueError:
        return False
    else:
        return True


async def get_uuid(mc_id: str) -> tuple[str | ClientResponse, str]:
    """
    通过 id 从 Mojang 获取 uuid

    :param mc_id: 正版用户名（id）
    """
    launart = Launart.current()
    session = launart.get_interface(AiohttpClientInterface).service.session

    async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{mc_id}') as resp:
        if resp.status != 200:
            return resp, ''
        resp_json = await resp.json()
        return resp_json['name'], resp_json['id']


async def get_mc_id(mc_uuid: str | UUID) -> str | ClientResponse:
    """
    通过 uuid 从 Mojang 获取正版 id

    :param mc_uuid: 输入一个uuid
    """
    launart = Launart.current()
    session = launart.get_interface(AiohttpClientInterface).service.session

    async with session.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{mc_uuid}') as resp:
        if resp.status != 200:
            return resp
        resp_json = await resp.json()
        return resp_json['name']
