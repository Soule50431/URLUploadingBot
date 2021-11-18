import random

from bs4 import BeautifulSoup
import discord

from notion_api import *

# 自分のBotのアクセストークンに置き換えてください
DISCORD_TOKEN = os.getenv("DiscordToken")
NOTION_TOKEN = os.getenv("NotionToken")

channel_ids = list(map(int, os.getenv("ChannelIDs").split(",")))
database_ids = os.getenv("DatabaseIDs").split(",")

# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('logged in')


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # ignore when sender is bot
    if message.author.bot:
        return

    if message.content == "/hootle":
        rand = random.random()
        if rand < 0.3:
            await message.channel.send("フルー!")
        elif 0.3 <= rand < 0.6:
            await message.channel.send("フルッフ!")
        else:
            await message.channel.send("フルル!")

    if "https://" in message.content:

        for channel_id, database_id in zip(channel_ids, database_ids):
            if message.channel.id == channel_id:
                # get url and its title
                url = message.content

                stop_words = ["youtube", "twitter", "nicovideo", "github"]
                if not any([stop_word in url for stop_word in stop_words]):
                    html = requests.get(url).text

                    soup = BeautifulSoup(html, "html.parser")
                    title = soup.title.string
                else:
                    title = url

                if url not in get_page_urls(database_id):
                    post_new_pages(database_id, title, url)
                    print(f"create new page of {title}")
                else:
                    print(f"{title} already exists")

# Botの起動とDiscordサーバーへの接続
client.run(DISCORD_TOKEN)
