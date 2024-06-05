import asyncio
from utils import Warpcast
from utils.core import logger, get_all_lines, random_line
from itertools import zip_longest
import datetime
import pandas as pd
import os
from data.config import LIMITS


async def action_1():
    mnemonics = get_all_lines("data/mnemonics.txt")
    proxys = get_all_lines("data/proxy.txt")

    tasks = []
    for thread, (mnemonic, proxy) in enumerate(zip_longest(mnemonics, proxys)):
        if not mnemonic: break
        tasks.append(Warpcast(thread, mnemonic, proxy).statistics())

    data = await asyncio.gather(*tasks)

    if not os.path.exists('statistics'): os.mkdir('statistics')
    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['FID', 'Username', 'Display name', 'verified', 'Followers', 'Following']

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    logger.success(f"Saved statistics to {path}")


async def action_2(mnemonic: str, thread: int, proxy: [str, None]):
    warpcast = Warpcast(thread, mnemonic, proxy)
    await warpcast.login()
    logger.info(f"Thread {thread} | Start work")

    random_post = random_line("data/posts.txt", True)
    if random_post:
        hash_, username = await warpcast.write_post(random_post.replace('\\n', '\n'))
        logger.success(f"Thread {thread} | @{username} | Write post https://warpcast.com/{username}/{hash_} :{random_post}")
    else:
        logger.warning(f"Thread {thread} | No posts in data/posts.txt")

    await warpcast.logout()


async def action_3(mnemonic: str, thread: int, proxy: [str, None]):
    warpcast = Warpcast(thread, mnemonic, proxy)
    await warpcast.login()
    logger.info(f"Thread {thread} | Start work")

    exclude_item_id_prefixes = []
    latest_main_cast_timestamp = 0

    while len(exclude_item_id_prefixes) < LIMITS['LIKES']:
        items, latest_main_cast_timestamp = await warpcast.get_feed_items(
            latest_main_cast_timestamp=latest_main_cast_timestamp,
            exclude_item_id_prefixes=exclude_item_id_prefixes
        )

        for item in items:
            item_id, author_fid = item
            username, status = await warpcast.like(item_id)
            if not status:
                logger.error(f"Thread {thread} | {username}")
                break
            exclude_item_id_prefixes.append(item_id[:10][2:])
            logger.success(f"Thread {thread} | @{username} | Put like {len(exclude_item_id_prefixes)}/{LIMITS['LIKES']} to {item_id}")

        if not status: break

    logger.warning(f"Thread {thread} | Has reached limit of likes!")
    await warpcast.logout()


async def action_4(mnemonic: str, thread: int, proxy: [str, None]):
    warpcast = Warpcast(thread, mnemonic, proxy)
    await warpcast.login()
    logger.info(f"Thread {thread} | Start work")

    fids_l = []
    cursor = ''
    while len(fids_l) < LIMITS['SUBSCRIBES']:
        fids, cursor = await warpcast.get_suggested_users(cursor)

        for fid in fids:
            msg, status = await warpcast.follow(fid)
            if not status:
                logger.error(f"Thread {thread} | {msg}")
                break
            fids_l.append(fid)
            logger.success(f"Thread {thread} | Subscribe {len(fids_l)}/{LIMITS['SUBSCRIBES']} to {fid}")

        if not status: break

    logger.warning(f"Thread {thread} | Has reached limit of subscribes!")
    await warpcast.logout()


async def action_5(mnemonic: str, thread: int, proxy: [str, None]):
    warpcast = Warpcast(thread, mnemonic, proxy)
    await warpcast.login()
    logger.info(f"Thread {thread} | Start work")

    exclude_item_id_prefixes = []
    latest_main_cast_timestamp = 0

    while len(exclude_item_id_prefixes) < LIMITS['RECASTS']:
        items, latest_main_cast_timestamp = await warpcast.get_feed_items(
            latest_main_cast_timestamp=latest_main_cast_timestamp,
            exclude_item_id_prefixes=exclude_item_id_prefixes
        )

        for item in items:
            item_id, author_fid = item
            msg, status = await warpcast.recast(item_id)
            if not status:
                logger.error(f"Thread {thread} | {msg}")
                break
            exclude_item_id_prefixes.append(item_id[:10][2:])
            logger.success(f"Thread {thread} | Put recast {len(exclude_item_id_prefixes)}/{LIMITS['RECASTS']} to {item_id}")

        if not status: break

    logger.warning(f"Thread {thread} | Has reached limit of recasts!")
    await warpcast.logout()


async def action_6(mnemonic: str, thread: int, proxy: [str, None]):
    warpcast = Warpcast(thread, mnemonic, proxy)
    await warpcast.login()
    logger.info(f"Thread {thread} | Start work")

    fids_l = []
    cursor = ''
    while len(fids_l) < LIMITS['BACK_SUBSCRIBES']:
        fids, cursor = await warpcast.get_notification_follows(cursor)
        if fids is None and cursor is None:
            break

        for fid in fids:
            user = await warpcast.get_user(fid)
            if not user['viewerContext']['following']:
                msg, status = await warpcast.follow(fid)
                if status:
                    logger.success(f"Thread {thread} | Back follow to {fid}")

                await asyncio.sleep(2)

    logger.success(f"Thread {thread} | Finish back subscribe")
    await warpcast.logout()


async def action_7(mnemonic: str, thread: int, proxy: [str, None]):
    warpcast = Warpcast(thread, mnemonic, proxy)
    await warpcast.login()
    logger.info(f"Thread {thread} | Start work")

    exclude_item_id_prefixes = []
    latest_main_cast_timestamp = 0

    while len(exclude_item_id_prefixes) < LIMITS['COMMENTS']:
        items, latest_main_cast_timestamp = await warpcast.get_feed_items(
            latest_main_cast_timestamp=latest_main_cast_timestamp,
            exclude_item_id_prefixes=exclude_item_id_prefixes
        )

        for item in items:
            item_id, author_fid = item

            random_comment = random_line("data/comments.txt", True)
            if random_comment:
                hash_, username = await warpcast.write_post(random_comment.replace('\\n', '\n'), item_id)

                exclude_item_id_prefixes.append(item_id[:10][2:])
                logger.success(f"Thread {thread} | @{username} | {username} | Write comment {len(exclude_item_id_prefixes)}/{LIMITS['COMMENTS']} https://warpcast.com/{username}/{hash_} :{random_comment}")
            else:
                logger.warning(f"Thread {thread} | No posts in data/comments.txt")
                break
        if not random_line("data/comments.txt", True):
            break
    logger.warning(f"Thread {thread} | Has reached limit of comments!")
    await warpcast.logout()
