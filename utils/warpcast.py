import asyncio
import random

import aiohttp
import time
from fake_useragent import UserAgent
from eth_account import Account
import canonicaljson
from eth_account.messages import encode_defunct
import base64
from data.config import DELAYS, FEED_KEY


class Warpcast:
    def __init__(self, thread: int, mnemonic: str, proxy: [str, None]):
        Account.enable_unaudited_hdwallet_features()
        self.account = Account.from_mnemonic(mnemonic)

        self.proxy = f"http://{proxy}" if proxy is not None else None
        self.thread = thread

        headers = {'User-Agent': UserAgent(os='android').random}

        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False))

    async def logout(self):
        await self.session.close()

    async def login(self):
        await asyncio.sleep(random.uniform(*DELAYS['ACCOUNTS']))
        timestamp = int(time.time()) * 1000

        payload = {"method": "generateToken", "params": {"timestamp": timestamp, "expires_at": 86400000 + timestamp}}
        signed_message = self.account.sign_message(encode_defunct(primitive=canonicaljson.encode_canonical_json(payload)))
        self.session.headers['Authorization'] = "Bearer eip191:" + base64.b64encode(signed_message.signature).decode()

        resp = await self.session.put("https://api.warpcast.com/v2/auth", json=payload, proxy=self.proxy)
        self.session.headers['Authorization'] = "Bearer " + (await resp.json())['result']['token']['secret']

    async def me(self):
        resp = await self.session.get('https://api.warpcast.com/v2/me', proxy=self.proxy)
        return (await resp.json())['result']['user']

    async def statistics(self):
        await self.login()
        user = await self.me()
        await self.logout()

        fid = user['fid']
        username = user['username']
        display_name = user['displayName']
        verified = "✅" if user['pfp']['verified'] else "❌"
        followers = user['followerCount']
        following = user['followingCount']

        return fid, username, display_name, verified, str(followers), str(following)

    async def write_post(self, text: str, parent_hash: str = ''):
        await asyncio.sleep(random.uniform(*DELAYS['WRITE_POST']))
        json_data = {'embeds': [], 'text': text}

        if parent_hash:
            json_data['parent'] = {'hash': parent_hash}

        resp = await self.session.post('https://client.warpcast.com/v2/casts', json=json_data, proxy=self.proxy)
        resp_json = await resp.json()

        return resp_json.get('result').get('cast').get('hash')[:10], resp_json.get('result').get('cast').get('author').get("username")

    async def get_feed_items(self, viewed_cast_hashes: str = '', latest_main_cast_timestamp: int = 0,
                             exclude_item_id_prefixes=None):
        exclude_item_id_prefixes = [] if exclude_item_id_prefixes is None else exclude_item_id_prefixes

        await asyncio.sleep(random.uniform(*DELAYS['FEED']))
        json_data = {"feedKey": FEED_KEY, "feedType": "default", "viewedCastHashes": viewed_cast_hashes, "updateState": True}

        if latest_main_cast_timestamp:
            json_data['latestMainCastTimestamp'] = latest_main_cast_timestamp
            json_data['olderThan'] = latest_main_cast_timestamp
            json_data['excludeItemIdPrefixes'] = exclude_item_id_prefixes

        resp = await self.session.post('https://client.warpcast.com/v2/feed-items', json=json_data, proxy=self.proxy)
        resp_json = await resp.json()

        items = []
        for item in resp_json.get("result").get("items"):
            items.append((item['cast']['hash'], item['cast']['author']['fid']))

        return items, resp_json.get('result').get('latestMainCastTimestamp')

    async def like(self, cast_hash: str):
        await asyncio.sleep(random.uniform(*DELAYS['PUT_LIKE']))
        json_data = {"castHash": cast_hash}
        resp = await self.session.put('https://client.warpcast.com/v2/cast-likes', json=json_data, proxy=self.proxy)

        resp_json = await resp.json()
        if resp_json.get('result') is not None:
            return resp_json.get('result').get("like").get("reactor").get("username"), True
        else:
            return resp_json.get('errors')[0]['message'], False

    async def get_suggested_users(self, cursor: str = ''):
        await asyncio.sleep(random.uniform(*DELAYS['SUGGESTED_USERS']))

        url = 'https://client.warpcast.com/v2/suggested-users?limit=100&randomized=false'

        if cursor:
            url += "&cursor=" + cursor

        resp = await self.session.get(url, proxy=self.proxy)
        resp_json = await resp.json()

        fids = []
        for user in resp_json.get('result').get("users"):
            if user['fid'] not in fids: fids.append(user['fid'])

        return fids, resp_json.get("next").get('cursor')

    async def follow(self, fid: int):
        await asyncio.sleep(random.uniform(*DELAYS['SUBSCRIBE']))
        json_data = {"targetFid": fid}
        resp = await self.session.put('https://client.warpcast.com/v2/follows', json=json_data, proxy=self.proxy)
        resp_json = await resp.json()

        if resp_json.get('result'):
            return resp_json.get('result').get("success"), True
        else:
            return resp_json.get('errors')[0]['message'], False

    async def recast(self, cast_hash: str):
        await asyncio.sleep(random.uniform(*DELAYS['RECAST']))
        json_data = {"castHash": cast_hash}
        resp = await self.session.put('https://client.warpcast.com/v2/recasts', json=json_data, proxy=self.proxy)

        resp_json = await resp.json()
        if resp_json.get('result') is not None:
            return resp_json.get('result').get("castHash"), True
        else:
            return resp_json.get('errors')[0]['message'], False

    async def get_notification_follows(self, cursor: str):
        url = 'https://client.warpcast.com/v1/notifications-for-tab?tab=follows&limit=100'

        if cursor:
            url += "&cursor=" + cursor

        resp = await self.session.get(url, proxy=self.proxy)
        resp_json = await resp.json()

        if not resp_json.get('result').get("notifications"):
            return None, None

        cursor = resp_json.get('next').get('cursor')

        fids = []
        for notification_tab in resp_json.get('result').get('notifications'):
            for notification in notification_tab['previewItems']:
                fids.append(notification['actor']['fid'])

        return fids, cursor

    async def get_user(self, fid: int):
        resp = await self.session.get(f"https://client.warpcast.com/v2/user?fid={fid}", proxy=self.proxy)
        return (await resp.json()).get('result').get('user')
