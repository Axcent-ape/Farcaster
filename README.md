# Farcaster
Farcaster automatizer

automatizer for https://www.farcaster.xyz

More crypto themes and softs in telegram: [ApeCryptor](https://t.me/+_xCNXumUNWJkYjAy "ApeCryptor") 🦧
Additional soft information: https://t.me/ApeCryptorSoft/85

## Functionality
| Functional                                                                                                                           | Supported |
|--------------------------------------------------------------------------------------------------------------------------------------|:---------:|
| Multithreading                                                                                                                       |     ✅    |
| Binding a proxy to accounts in data/proxy.txt                                                                                        |     ✅    |
| Write posts from data/posts.txt                                                                                                      |     ✅    |
| Write comments from data/comments.txt                                                                                                |     ✅    |
| Put likes, recasts, make subscribes, back subscribe                                                                                  |     ✅    |
| Random sleep time between accounts, write posts, seerch feeds, suggested users, likes, subscribes, recasts, back subscribes          |     ✅    |
| Get statistics for all accounts                                                                                                      |     ✅    |

## Settings data/config.py
| Setting                      | Description                                                               |
|------------------------------|---------------------------------------------------------------------------|
| **DELAYS**                   | Delays between actions                                                    |
| **LIMITS**                   | Limits of actions (likes, subscribes, comments, recasts, back subscribes) |
| **FEED_KEY**                 | section to search feeds (home, trending, trending frames, all channels)   |


## Requirements
- Python 3.9 (you can install it [here](https://www.python.org/downloads/release/python-390/)) 
- Add Warpcast mnemonics to data/mnemonics.txt
- Add proxys in format login:password@ip:port to data/proxys.txt

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage
1. Run the bot:
   ```bash
   python main.py
   ```
