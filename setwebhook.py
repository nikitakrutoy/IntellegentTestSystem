import telepot
import environ


bot_token = '326195811:AAFLRPho2ptH6HkNdaJPKszQodGZb67o8yc'
bot = telepot.Bot(bot_token)
bot.setWebhook('https://glacial-hamlet-86113.herokuapp.com/its/bot/{bot_token}/'.format(bot_token=bot_token))
