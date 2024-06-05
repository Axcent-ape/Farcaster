DELAYS = {
    "ACCOUNTS": [2, 5],           # delay between accounts
    "WRITE_POST": [5, 10],        # delay between write posts
    "FEED": [1, 2],               # delay between search list posts (1 list = 15 posts)
    "SUGGESTED_USERS": [1, 2],    # delay between search list users (1 list = 15 users)
    "PUT_LIKE": [1, 5],           # delay between likes
    "SUBSCRIBE": [1, 2],          # delay between subs
    "RECAST": [1, 2],             # delay between recasts
    "BACK_SUBSCRIBE": [1, 3]      # delay between back subs
}

LIMITS = {
    "LIKES": 100,               # maximum count of likes per session
    "SUBSCRIBES": 200,          # maximum count of subscribe per session
    "COMMENTS": 100,            # maximum count of comments per session
    "RECASTS": 20,              # maximum count of recasts per session
    "BACK_SUBSCRIBES": 200      # maximum count of back subscribes per session
}

# from which section to search. Available 'home', 'trending', 'trending-frames', 'all-channels'.
FEED_KEY = "trending-frames"


