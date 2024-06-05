from utils import starter
from utils.core import get_all_lines
from itertools import zip_longest
import asyncio


async def main():
    print("Soft's author: https://t.me/ApeCryptor\n")
    action = int(input("Select action for each Warpcast account:"
                       "\n1. Get statistics"
                       "\n2. Writing random posts from data/posts.txt"
                       "\n3. Put likes on random user posts"
                       "\n4. Subscribe to random users"
                       "\n5. Put recasts on random user posts"
                       "\n6. Back Subscribe"
                       "\n7. Writing random comment from data/posts.txt to random post"
                       "\n\n> "))

    if action == 1:
        await starter.action_1()
        return

    mnemonics = get_all_lines("data/mnemonics.txt")
    proxys = get_all_lines("data/proxy.txt")

    accounts = [[mnemonic, thread, proxy] for thread, (mnemonic, proxy) in enumerate(zip_longest(mnemonics, proxys)) if
                mnemonic]

    tasks = []
    for mnemonic, thread, proxy in accounts:
        if action == 2:
            tasks.append(asyncio.create_task(starter.action_2(mnemonic, thread, proxy)))
        elif action == 3:
            tasks.append(asyncio.create_task(starter.action_3(mnemonic, thread, proxy)))
        elif action == 4:
            tasks.append(asyncio.create_task(starter.action_4(mnemonic, thread, proxy)))
        elif action == 5:
            tasks.append(asyncio.create_task(starter.action_5(mnemonic, thread, proxy)))
        elif action == 6:
            tasks.append(asyncio.create_task(starter.action_6(mnemonic, thread, proxy)))
        elif action == 7:
            tasks.append(asyncio.create_task(starter.action_7(mnemonic, thread, proxy)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
