import asyncio
import requests
import random
import string
import pyperclip
import os
from aiohttp import ClientSession
from rgbprint import gradient_print, Color
from plyer import notification

notification.notify(
    title='KoRaider', # ──> Noti Title.
    message='Coded by Koraedn.',
    app_name='KR',#   ^
    timeout=5#        └────── Notification Message.
)#          ^
#           │
# ──────────┘
#  How long the noti lasts.

def lt(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()# <───┬── Collect tokens in file_path var
    vtoke = list(set(tokens))#      <──────────┼── Run vtoke (Verify Tokens) function on tokens of file_path
    return vtoke#                              │
#                                              │
# ─────────────────────────────────────────────┘

def check(token):
    url = "https://discord.com/api/v9/users/@me"# <───┬── Discord api for main page.
    headers = {"Authorization": token}# <─────────────┴───── Authorization: {token variable} for any USER ACCOUNT related scripts
    response = requests.get(url, headers=headers)
    return response.status_code == 200
#                                   ^
#                                   ├── Checks if HTTP response comes back as 'valid'
# ──────────────────────────────────┘

def vt(tokens):
    vtoke = []#   <───────────────┬── Stores verified tokens. (definition of vtoke)
    for token in tokens:#         │
        if check(token):#     <───┼── Calls 'checl' function on each token.
            vtoke.append(token)#  │
    return vtoke#                 │
#                                 │
# ────────────────────────────────┘

async def scrapeuid(session, cid, token):
    headers = {"Authorization": token}
    url = f"https://discord.com/api/v9/channels/{cid}/messages?limit=100"
#                                                                    ^
    async with session.get(url, headers=headers) as response:#       ├── Scrape UID's from past 100 messages. (only change if you know what you are doing)
        uids = set()#                                                │
#                                                             ┌──────┘
        if response.status == 200:#                 <─────────┼── Checks if HTTP response comes back as 'valid'
            messages = await response.json()#                 │
            for message in messages:#                         │
                uids.add(message['author']['id'])#      <─────┼── Collects the UserID (UID) from the author of message (sender)
#                                                             │
    return list(uids)#                                        │
#                                                             │
# ────────────────────────────────────────────────────────────┘

async def get_friends(session, token):
    headers = {"Authorization": token}
    url = "https://discord.com/api/v9/users/@me/relationships"#     <─────────────────────┬── Discord's API channel for friends.
    async with session.get(url, headers=headers) as response:#                            │
        if response.status == 200:#                         <─────────────────────────────┼── Checks if HTTP response comes back as 'valid'
            friends_data = await response.json()#                                         │
            return [friend['id'] for friend in friends_data if friend['type'] == 1]#  <───┼─┬ Collect friend if relationship is type 1.
        return []#                                                                        │ └─────────────── 'Type 1' indications relationship as 'friend'
#                                                                                         │
# ────────────────────────────────────────────────────────────────────────────────────────┘

def randstr():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Generate a random string Numerical and Alphebetical values, 8 chars long.

def randestr(length=5):
    emojis = ['😂', '🔥', '💀', '😎', '😡', '😍', '🤖', '👽', '👾', '🎉', '💥', '🥶', '🥵']
#             └─────────────────────────────────────────────────────────┬─────────────────────┘
#                                                                       ├── All the emojis that can be used during string creation.
#                                                                       └┐
    return ''.join(random.choices(emojis, k=length))#                    │
#  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                     ├── Feel free to add on more emojis by continuing the var.
#  Uses emojis inside of 'emojis' var to create random 5 char string.    │
#  ──────────────────────────────────────────────────────────────────────┘

async def send(session, token, cid, message, uids=None, pc=1, random_string=False, random_emoji=False):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v9/channels/{cid}/messages"#              <───────┬── Discord's API to access the messages of a channel (used to send)
#                                                                                     │
    if random_string:#                                                                │
        message += " - " + randstr()# <───────────────────────────────────────────────┼── IF CHOSEN: Add the random string of chars, seperated by '-'
#                                                                                     │
    if random_emoji:#                                                                 │
        message += " " + randestr()#  <───────────────────────────────────────────────┼── IF CHOSEN: Add the random string of emojis, seperated by '-'
#                                                                                     │
    if uids:#                                                                         │
        pings = ' '.join([f"<@{random.choice(uids)}>" for _ in range(pc)])#           │
        message += " " + pings#     <─────────────────────────────────────────────────┼── ON MESSAGE: Add the chosen amount of pings (scraped) to it.
#                                                                                     │
    payload = {"content": message}# <─────────────────────────────────────────────────┼─┬ The PayLoad to be sent.
#                                                                                     │ └── Basically everything added up to 1 message variable set into a payload.
    try:#                                                                             │
        async with session.post(url, headers=headers, json=payload) as response:#     │
            if response.status == 200:# <─────────────────────────────────────────────┼── Checks if HTTP response comes back as 'valid'
                return True#                                                          │
            else:#                                                                    │
                return False#                                                         │
    except Exception:#                                                                │
        return False#                                                                 │
#                                                                                     │
# ────────────────────────────────────────────────────────────────────────────────────┘

async def leave_guild(session, token, guild_id):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/@me"# <─────────────────────┬── Discord's API for accessing a server.
    headers = {"Authorization": token}#                                                      │
    async with session.delete(url, headers=headers) as response:#                            │
        if response.status == 204:#  <───────────────────────────────────────────────────────┼── Checks if valid HTTP response, yet no content.
            print(f"[{Color.green}Left guild{Color.reset}]: {guild_id}")#                    │
        else:#                                                                               │
            print(f"[{Color.red}Failed to leave guild{Color.reset}]: {response.status}")#    │
#                                                                                            │
#  ──────────────────────────────────────────────────────────────────────────────────────────┘

async def get_guilds(session, token):
    headers = {"Authorization": token}
    url = "https://discord.com/api/v9/users/@me/guilds"#  <───────┬── Discord's API for guild listing (basically)
    async with session.get(url, headers=headers) as response:#    │
        if response.status == 200:#       <───────────────────────┼─┬ Checks if HTTP response comes back as 'valid'
            return await response.json()#                         │ └── In our case: To check if the 'guild' / server exists.
        return []#                                                │
#                                                                 │
#  ───────────────────────────────────────────────────────────────┘

async def leave_servers(session, token):
    guilds = await get_guilds(session, token)
    for guild in guilds:
        guild_id = guild['id']
        await leave_guild(session, token, guild_id)# <─┬── Send a leave request to the 'Guild' / server.
#                                                      │
#  ────────────────────────────────────────────────────┘

def copy(data):
    pyperclip.copy(', '.join(data))
    print(f"[{Color.blue}INFO{Color.reset}] UID's copied to cb.")
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Simple function to copy UID's to the users clipboard.

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   If i have to explain this you are really out of your mind.

def menart():
    ascii_art = r"""
                           ██╗  ██╗ ██████╗ ██████╗  █████╗ ██╗██████╗ ███████╗██████╗ 
                           ██║ ██╔╝██╔═══██╗██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
                           █████╔╝ ██║   ██║██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
                           ██╔═██╗ ██║   ██║██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
                           ██║  ██╗╚██████╔╝██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
                           ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    gradient_print(ascii_art, start_color=Color.red, end_color=Color.yellow)
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   The main menu's ASCII art, + the function to print it with color (using rgbprint)

async def ts(tmtks):
    cls()
    print("[TERMED TOKENS]")
    for token_info in tmtks:
        print(f"Token: {token_info['half_token']}***, Name: {token_info['username']} has possibly been terminated.")# <─┬── Alert user of POSSIBLE token termination. (NOT 100% ACCURATE, FALSLEY CLAIMS ASWELL)
    input(".")#                                                                                                         │
#                                                                                                                       │
#  ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

async def mass_dm(session, token, message):
    friends = await get_friends(session, token)
    tasks = []

    for friend_id in friends:
        channel_id = await get_dm_channel(session, token, friend_id)
        if channel_id:
            tasks.append(send(session, token, channel_id, message))
        else:
            print(f"Failed to DM channel for UID {friend_id}")

    await asyncio.gather(*tasks)
    print(f"[{Color.green}Mass DM sent to{Color.reset}]: {len(friends)} messages sent.")# <──┬── Alert user the operation was complete.
#                                                                                            │
#  ──────────────────────────────────────────────────────────────────────────────────────────┘

async def get_dm_channel(session, token, friend_id):
    url = f"https://discord.com/api/v9/users/{friend_id}/channels"
    async with session.get(url, headers={"Authorization": token}) as response:
        if response.status == 200:
            channels = await response.json()
            for channel in channels:
                if channel['type'] == 1:#         <────────────────────────────────────────────────────┬── Checks if channel is equal to 'type 1' (DM)
                    return channel['id']#                                                              │
    url = f"https://discord.com/api/v9/users/@me/channels"#                                            │
    payload = {"recipient_id": friend_id}#                                                             │
    async with session.post(url, headers={"Authorization": token}, json=payload) as response:#         │
        if response.status == 200:#                      <─────────────────────────────────────────────┼── Checks if HTTP response comes back as 'valid'
            channel_data = await response.json()#                                                      │
            return channel_data['id']#                                                                 │
    return None#                                                                                       │
#                                                                                                      │
#  ────────────────────────────────────────────────────────────────────────────────────────────────────┘

async def load_blacklist():
    if not os.path.exists("blacklist.txt"):
        return set()
    with open("blacklist.txt", 'r') as file:
        return set(line.strip() for line in file.readlines())#  <──────────┬── Read all lines of 'blacklist.txt' for server ID's to NOT send in.
#                                                                          │
#  ────────────────────────────────────────────────────────────────────────┘

async def send_message_to_all_channels(session, token, message, blacklist):
    guilds = await get_guilds(session, token)
    for guild in guilds:
        if guild['id'] in blacklist:
            continue
        channels_url = f"https://discord.com/api/v9/guilds/{guild['id']}/channels"
        headers = {"Authorization": token}
        async with session.get(channels_url, headers=headers) as response:
            if response.status == 200:#             <────────────────────────────────────────┬── Checks if HTTP response comes back as 'valid'
                channels = await response.json()#                                            │
                send_tasks = []#                                                             │
                for channel in channels:#                                                    │
                    if channel['type'] in (0, 5) and channel['type'] != 2:#     <────────────┼─┬  Check if channel is 'type 0-5' (excluding type 2)
                        send_tasks.append(send(session, token, channel['id'], message))#     │ └── 'Type 2' in Discord's API refers to Voice Channels.
                await asyncio.gather(*send_tasks)#                                           │
#                                                                                            │
#  ──────────────────────────────────────────────────────────────────────────────────────────┘

async def gc_spammer(session, vtoke, user_ids, amount):
    tasks = []
    for _ in range(amount):
        token = random.choice(vtoke)
        payload = {
            "recipients": user_ids,
        }
        url = "https://discord.com/api/v9/users/@me/channels"
        
        async with session.post(url, headers={"Authorization": token}, json=payload) as response:
            if response.status == 200:#                                         <─────────────────────┬── Checks if HTTP response comes back as 'valid'
                group_chat_data = await response.json()#                                              │
                print(f"[{Color.red}Created GC{Color.reset}]: {group_chat_data['id']}")#  <───────────┼── Lets you know if GC was successfully created!
                tasks.append(group_chat_data['id'])#                                                  │
            else:#                                                                                    │
                print(f"[{Color.red}Failed to create gc{Color.reset}]: {response.status}")#           │
#                                                                                                     │
#   ──────────────────────────────────────────────────────────────────────────────────────────────────┘

async def main():
    os.system("title KoRaider ^| Koraedn") # Set title using OS.
    tmtks = [] # Termed Tokens.
    while True:
        cls() # Clear the screen using the cls function.
        menart()
        koraedn = "tokens.txt" # Tokens listed in:
        if not os.path.exists(koraedn):
            print(f"[{Color.red}ERROR{Color.reset}] {koraedn} wasn't found.")# Display error if file wasn't found
            return
        
        tokens = lt(koraedn)# List tokens
        vtoke = vt(tokens)# Verify listed tokens
        print(f"                                               [{Color.light_green}INFO{Color.reset}] Valids: {len(vtoke)}")
        if len(vtoke) == 0:# If 'vtoke' (verified tokens) is equal to 0, then display ↓
            print(f"[{Color.red}ERROR{Color.reset}] non valids entered.")#        <<<<<
            return

        print(f"                                                   [{Color.light_green}OPTIONS{Color.reset}]")
        print(f"                                                   [{Color.light_green}1{Color.reset}] Raider")
        print(f"                                                   [{Color.light_green}2{Color.reset}] Scraper")
        print(f"                                                   [{Color.light_green}3{Color.reset}] Mass DM")          # Options!!!!!1!!!
        print(f"                                                   [{Color.light_green}4{Color.reset}] Leave Servers")
        print(f"                                                   [{Color.light_green}5{Color.reset}] DM All servers")
        print(f"                                                   [{Color.light_green}6{Color.reset}] Group Chat Spammer")
        print(f"                                                   [{Color.light_green}7{Color.reset}] Quit")
        choice = input(f"Choose [{Color.orange}>{Color.reset}] ")

        if choice == "7":
            break

        cid = None# Channel ID
        uids = None# User ID
        cuid = None# Custom User ID
        termtr = []# Termed Tokens

        async with ClientSession() as session:
            if choice == "2":
                cid = input(f"Channel ID [{Color.orange}>{Color.reset}] ")
                token = vtoke[0]
                uids = await scrapeuid(session, cid, token)
                if uids:
                    print(f"[{Color.green}SCRAPED{Color.reset}] UID: {uids}")
                    copy(uids)#   <───────────────────────────────────────────────┬── Use our 'copy' function to copy tokens!
                else:#                                                            │
                    print(f"[{Color.red}ERROR{Color.reset}] Couldn't Scrape")#    │
#                                                                                 │
#  ───────────────────────────────────────────────────────────────────────────────┘

            elif choice == "1":
                use_scraper = input(f"Scraper? (y/n) [{Color.orange}>{Color.reset}] ").lower()

                if use_scraper == 'y':
                    cid = input(f"Channel ID [{Color.orange}>{Color.reset}] ")
                    token = vtoke[0]
                    uids = await scrapeuid(session, cid, token)
                    if uids:
                        copy(uids)
                    else:
                        print(f"[{Color.red}ERROR{Color.reset}] Couldn't Scrape")
                        continue
                else:
                    cuid = input(f"Enter custom UID [{Color.orange}>{Color.reset}] ")
                    cid = input(f"Channel ID) [{Color.orange}>{Color.reset}] ")

                message = input(f"Message [{Color.orange}>{Color.reset}] ")#                           ──┐
                rstring = input(f"Random String? (y/n) [{Color.orange}>{Color.reset}] ").lower() == 'y'# │
                remoji = input(f"Emoji String? (y/n) [{Color.orange}>{Color.reset}] ").lower() == 'y'#   │
                mc = int(input(f"Message amount [{Color.orange}>{Color.reset}] "))#                      ├── Yip yap ass questions 
                pc = int(input(f"Pings per message [{Color.orange}>{Color.reset}] "))#                 ──┘

                tasks = []
                for i in range(mc):
                    token_index = i % len(vtoke)
                    token = vtoke[token_index]
                    task = send(session, token, cid, message, uids, pc=pc, random_string=rstring, random_emoji=remoji)
                    tasks.append(task)

                results = await asyncio.gather(*tasks)

                for i, success in enumerate(results):
                    if not success:
                        half_token = vtoke[i % len(vtoke)][:len(vtoke[i % len(vtoke)]) // 2]
                        username = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": vtoke[i % len(vtoke)]}).json().get("username", "Unknown User")# Half a token
                        termtr.append({'half_token': half_token, 'username': username})

                for tmtk in termtr:
                    if tmtk not in tmtks:
                        tmtks.append(tmtk)

            elif choice == "3":
                message = input(f"Message to DM [{Color.orange}>{Color.reset}] ")
                await mass_dm(session, vtoke[0], message)

            elif choice == "4":
                token = vtoke[0]
                await leave_servers(session, token)

            elif choice == "5":
                message = input(f"Enter message to send to all channels [{Color.orange}>{Color.reset}] ")
                blacklist = await load_blacklist()
                for token in vtoke:
                    await send_message_to_all_channels(session, token, message, blacklist)

            elif choice == "6":
                user_ids = input(f"Enter User IDs (comma-separated) [{Color.orange}>{Color.reset}] ").split(',')
                user_ids = [uid.strip() for uid in user_ids]
                amount = int(input(f"Number of Group Chats to create [{Color.orange}>{Color.reset}] "))

                await gc_spammer(session, vtoke, user_ids, amount)

            if termtr:
                await ts(tmtks)

if __name__ == "__main__":
    asyncio.run(main())
