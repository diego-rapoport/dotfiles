PHONE =

NOTIFY_CMD = "dunstify -r 7373 -a Telegram -i {icon_path} {title}{subtitle} {msg}"

CHAT_FLAGS = {
    "online": "●",
    "pinned": "車",
    "muted": "婢",
    # chat is marked as unread
    "unread": "",
    # last msg haven't been seen by recipient
    "unseen": "✓",
    "secret": "🔒",
    "seen": "✓✓",  # leave empty if you don't want to see it
}
MSG_FLAGS = {
    "selected": "",
    "forwarded": "",
    "new": "",
    "unseen": "烙",
    "edited": "",
    "pending": "",
    "failed": "💩",
    "seen": "✓✓",  # leave empty if you don't want to see it
}

USERS_COLORS = tuple(range(233))

FILE_PICKER_CMD = "ranger --choosefile={file_path}"
