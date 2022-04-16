from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
import pandas as pd
from telethon.tl.functions.messages import GetDialogsRequest
import re
from html import unescape
import unicodedata


def get_entity_data(entity_id, limit):
    entity = client.get_entity(entity_id)
    posts = client(GetHistoryRequest(
        peer=entity,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))

    messages = []
    for message in posts.messages:
        messages.append(message.message)
    return messages

api_id = ""
api_hash = ""

client = TelegramClient(None, api_id, api_hash) 
client.start()
channel_name = 'https://t.me/it_boooks'

channel_entity = client.get_entity(channel_name)

data = client.get_messages(channel_entity, 2000)
ids = []
links = []
titles = []
descs = []
for post in data:
    if post.id is None or post.message is None:
        continue

    split = post.message.split('\n\n')
    if len(split) == 5:
        ids.append(str(post.id))
        links.append(f'https://t.me/it_boooks/{post.id}')
        title = split[1].replace('\n', ' ')
        desc = split[3].replace('\n', ' ')
        
        titles.append(unicodedata.normalize('NFKC', unescape(title)))
        descs.append(unicodedata.normalize('NFKC', unescape(desc)))


pd_data = pd.DataFrame(list(zip(ids, titles, descs, links)))
pd_data.to_csv('posts.csv', header=False, index=False)
client.log_out()
