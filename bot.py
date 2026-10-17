
import discord
from discord.ext import commands
import requests
import pyttsx3

TOKEN = "TOKEN  HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as error:
        print("Seslendirme hatasi: {}".format(error))


@bot.event
async def on_ready():
    print("Bot aktif: {}".format(bot.user))


@bot.command()
async def start(ctx):
    await ctx.send(
        "Merhaba {}! Botuma hos geldin".format(ctx.author.mention)
    )


@bot.command()
async def fact(ctx):
    await ctx.send("Bir ilginç bilgi buluyorum")

    try:
        response = requests.get(
            "https://uselessfacts.jsph.pl/api/v2/facts/random",
            timeout=15
        )

        print(response.json() if response.status_code == 200
              else "HTTP durum kodu: {}".format(response.status_code))

        if response.status_code != 200:
            await ctx.send(
                "API hata verdi. HTTP kodu: {}".format(
                    response.status_code
                )
            )
            return

        data = response.json()
        fact_text = data.get("text", "").strip()

        if not fact_text:
            await ctx.send("API'den bilgi alınamadı. Tekrar dene.")
            return

        await ctx.send("📚 **İlginç Bilgi:**\n" + fact_text)

        # Seslendirmeyi ayrı bir thread'de çalıştır.
        import asyncio
        await asyncio.to_thread(speak, fact_text)

    except requests.exceptions.RequestException as error:
        print("API bağlantı hatası:", error)
        await ctx.send("API'ye bağlanamadım. İnternetini kontrol et.")

    except (ValueError, KeyError) as error:
        print("JSON hatası:", error)
        await ctx.send("API yanıtı okunamadı. Tekrar dene.")


bot.run(TOKEN)
