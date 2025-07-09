import os
import asyncio
import logging
from aiohttp import web
from handlers import router as rtr
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
WEB_SERVER_HOST = '0.0.0.0'
WEB_SERVER_PORT = '8000'
WEBHOOK_PATH = '/webhook'
BASE_WEBHOOK_URL = 'https://domain.com'


async def on_startup(bot: Bot) -> None:
    webhook_url = f'{BASE_WEBHOOK_URL}{WEBHOOK_PATH}'
    await bot.set_webhook(webhook_url)
    logging.info('БОТ ВКЛЮЧИЛСЯ. СВЯЗЬ УСТАНОВЛЕНА.')


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    logging.info('БОТ ОТКЛЮЧИЛСЯ. СВЯЗЬ ОБОРВАНА.')


async def main() -> None:
    load_dotenv(find_dotenv())
    bot = Bot(token=os.getenv('TG_KEY'))
    dp = Dispatcher()
    dp.include_router(rtr)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    await site.start()
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('БОТ ОСТАНОВЛЕН ВРУЧНУЮ.')
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}", exc_info=True)
