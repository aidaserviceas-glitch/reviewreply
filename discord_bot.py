# ReviewReply Discord Bot
# Kjør med: python reviewreply_bot.py
# Krever: pip install discord.py requests
# Sett DISCORD_TOKEN som environment variable

import discord, requests, os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
WORKER_URL = "https://reviewreply-worker.aida-service-as.workers.dev"

@client.event
async def on_ready():
    print(f"ReviewReply Bot logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("/reviewreply "):
        review_text = message.content[13:].strip()
        if len(review_text) < 10:
            await message.reply("Please paste the full review text after /reviewreply")
            return

        await message.reply("Generating professional response...")

        try:
            r = requests.post(f"{WORKER_URL}/optimize",
                json={"text": review_text, "type": "review_reply"},
                timeout=20)
            if r.status_code == 200:
                reply = r.json().get("result","Could not generate response")
                await message.reply(f"**Professional response:**\n\n{reply}\n\n*Powered by ReviewReply — reviewreply.pages.dev*")
            else:
                await message.reply(f"Error generating response. Try at reviewreply.pages.dev")
        except Exception as e:
            await message.reply("Service unavailable. Try at reviewreply.pages.dev")

client.run(os.environ.get("DISCORD_TOKEN",""))
