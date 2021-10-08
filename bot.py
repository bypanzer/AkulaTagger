import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**Mən Akula Tagger Bot**, Mən qrup və kanaldakı bütün userləri tag edə bilərəm 👻\nDaha çox məlumat üçün  **/help** toxun__\n\n",
                    buttons=(
                      [Button.url('📣 Support', 'https://t.me/EpicProjects'),
                      Button.url('📦 Mənbə', 'https://github.com/EpicPr0jects/AkulaTagger')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Akula Tagger'in kömək menyusu**\n\nƏmr: /mentionall\n__Bu əmr vasitəsilə başqalarını 1 mətnlə tag edə bilərsən.__\n`Nümunə: /mentionall Akulalar oyaqdılar!`\n__Həmçinin 1 mesaja cavab verərək /mentionall əmrini işlədə bilərsən. Bot userləri həmin mesaja tag edəcək__."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('📣 Kanal', 'https://t.me/EpicProjects'),
                      Button.url('📦 Mənbə', 'https://github.com/EpicPr0jects/AkulaTagger')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__Bu əmr yalnız kanal və qruplarda istifadə edilə bilər!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnız akulalar hərkəsi tag edə bilər!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə 1 mesaja üzvləri tag edə bilmərəm! (Mən qrupa əlavə edilmədən öncə yazılan mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__1 mesaja cavab ver və ya üzvləri tag etmək üçün 1 mesaj ver!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> Akula Oyaqdı 🦈<<")
client.run_until_disconnected()
