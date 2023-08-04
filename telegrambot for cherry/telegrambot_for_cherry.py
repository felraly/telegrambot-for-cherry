import asyncio
import telegram


async def main():
    bot = telegram.Bot("6321575706:AAFdH-lVl5r3Ai0DhFlQHsyt_mK0dpakMnc")
    async with bot:
        print((await bot.get_updates())[0])

if __name__ == '__main__':
    asyncio.run(main())