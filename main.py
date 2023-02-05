#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.10

import asyncio
import logging
import os.path
import sys
import coloredlogs
from json import loads

import aiohttp
from dotenv import load_dotenv

FORMAT = '[%(asctime)s] [%(filename)s] [%(levelname)s] [%(lineno)d]: %(' \
         'message)s '
formatter = logging.Formatter(FORMAT)
formatter_color = coloredlogs.ColoredFormatter(FORMAT)
LOG_LEVEL = logging.DEBUG

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter_color)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)


async def check_if_existed_env() -> bool:
    """
    Check if the .env file exists
    :return: boolean value, True - if the .env file exists, False - otherwise
    """

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        logger.debug(f'Found.env file at {dotenv_path}')
        return True
    else:
        logger.critical(f'{dotenv_path} does not exist, please add .env to this directory.')
        return False


async def get_videos(session: aiohttp.ClientSession) -> list:
    """
    Get videos from VK
    :param session: aiohttp session, used to make requests
    :return: list of videos
    """

    url = "https://api.vk.com/method/video.get"
    params = {'access_token': os.environ.get('token'), 'v': '5.131', 'count': '200'}

    async with session.post(url, data=params) as resp:
        videos = loads(await resp.text())['response']['items']

    logger.debug(f'Got {len(videos)} videos')

    if len(videos) == 0:
        logger.critical('No videos found')

    return videos


async def video_delete(session: aiohttp.ClientSession) -> bool:
    """
    Delete videos from VK
    :param session: aiohttp session, used to make requests
    :return: boolean value, True - if the deletion was successful, False - otherwise
    """

    videos = await get_videos(session)
    flag: bool = True

    for video in videos:
        params = {'access_token': os.environ.get('token'), 'v': '5.131', 'target_id': os.environ.get('target_id'),
                  'owner_id': video['owner_id'], 'video_id': video['id']}
        async with session.post("https://api.vk.com/method/video.delete", data=params) as resp:
            result = loads(await resp.text())

        if result['response'] != 1:
            logger.critical("Video wasn't deleted")
            logger.debug(result)
            flag = False
            continue

        logger.debug(f'Response: {result}')
        logger.info(f'Deleted video {video["id"]}')

        await asyncio.sleep(2)

    await session.close()

    return flag


async def main() -> None:
    """
    Main function, starts the script
    :return: None
    """

    connect = aiohttp.ClientSession()
    await check_if_existed_env()

    result = await video_delete(connect)
    if result is False:
        logger.critical('Something went wrong.')
        return None

if __name__ == '__main__':
    asyncio.run(main())
