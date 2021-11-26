#!/usr/bin/python3.8
import config
import logging, re

from stateMachine import Order
from aiogram import Bot, Dispatcher, executor, types

# установка уровня логирования
logging.basicConfig(level = logging.INFO)

# инициализация в API телеграма
def bot_auth() :

    if config.TG_API_TOKEN != '' :
        bot = Bot(token = config.TG_API_TOKEN)
        dp = Dispatcher(bot)
        
        if config.Vk_API_TOKEN != '' :
            vk_session = vk_api.VkApi(token = config.VK_API_TOKEN)
            longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID) 
            vk_session._auth_token()

            vk = vk_session.get_api()
            return dp, vk

        else : return dp

bot = bot_auth()
order = Order()

# приветствие нового пользователя
@bot.message_handler(commands = ['start', 'help'])
async def greet(message : types.Message) :
    
    await message.answer("Здравствуйте!")
    await message.answer("Какую вы хотите пиццу? Большую или маленькую?")
    order.reset_order()
    order.create_order()

@bot.message_handler(content_types = ['text'])
async def orderTaking(message : types.Message) :
    print(order.state)
    
    if order.state == 'orderCreated' :
        if re.fullmatch("большую.*", message.text.lower()) :
            order.select_size("большую")
            await message.answer("Как вы будете платить?")

        elif re.fullmatch("маленькую.*", message.text.lower()) :
            order.select_size("маленькую")
            await message.answer("Как вы будете платить?")

        else : await message.answer("Пожалуйста, повторите выбор.\n" +
                                    "Какую вы хотите пиццу? Большую или маленькую?")

    elif order.state == 'pizzaSizeSelected' :
        order.select_payment_method(message.text.lower())
        await message.answer("Вы хотите " + order.pizzaSize + " пиццу, " + 
                             "оплата - " + order.paymentMethod + "?")

    elif order.state == 'paymentMethodSelected' :
        if message.text.lower() == "да" :
            order.confirm_order()
            await message.answer("Спасибо за заказ")

        if message.text.lower() == "нет" :
            order.order_mistake()
            await message.answer("Хотите отменить заказ?")

    elif order.state == 'dataMistake' :
        if message.text.lower() == "да" :
            order.reset_order()
            await message.answer("Заказ отменён")

        if message.text.lower() == "нет" :
            order.order_mistake_is_fine()
            await message.answer("Вы хотите " + order.pizzaSize + " пиццу, " + 
                                 "оплата - " + order.paymentMethod + "?")

# запуск long-polling
if __name__ == '__main__' :
    executor.start_polling(bot, skip_updates = True)