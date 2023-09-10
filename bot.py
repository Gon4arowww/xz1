# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

import logging
import subprocess
import shutil

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, LabeledPrice
from telegram.ext import (
    Application
    , CallbackQueryHandler
    , CommandHandler
    , ContextTypes
    , PreCheckoutQueryHandler
    , MessageHandler
    , filters
)

gv_token = '6169575085:AAGhabHohTffKnJrW9vVzTN3RO5FfenWTwk'
PAYMENT_PROVIDER_TOKEN = "381764678:TEST:65950"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Инструкция по настройке", callback_data='manual')],
        [InlineKeyboardButton("Оплатить VPN", callback_data='pay')],
        [InlineKeyboardButton("Статус", callback_data='status')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    lv_user = query.from_user

    # print(query)

    if query.data == 'manual':
        lv_kbManual = [
            [InlineKeyboardButton("Инструкция IOS", callback_data='manual_ios')],
            [InlineKeyboardButton("Инструкция Android", callback_data='manual_android')],
            [InlineKeyboardButton("Главное меню", callback_data='main')],
        ]

        reply_markup = InlineKeyboardMarkup(lv_kbManual)
        # await query.edit_message_text(text='Как пользоваться ботом')
        await query.edit_message_text(
            text="Инструкция по настройке VPN", reply_markup=reply_markup
        )
    elif query.data == 'pay':
        keyboard = [
            [InlineKeyboardButton("1 месяц", callback_data='pay_1')],
            [InlineKeyboardButton("3 месяца", callback_data='pay_3')],
            [InlineKeyboardButton("6 месяцев", callback_data='pay_6')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Выберите период для оплаты", reply_markup=reply_markup
        )
    elif query.data == 'status':
        # Здесь можно выполнить логику отображения статуса пользователя
        keyboard = [
            [InlineKeyboardButton("Главное меню", callback_data='main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f'Статус VPN для пользователя {lv_user.username} искать по ID: {lv_user.id}', reply_markup=reply_markup
        )
    elif query.data == 'main':

        keyboard = [
            [InlineKeyboardButton("Инструкция по настройке", callback_data='manual')],
            [InlineKeyboardButton("Оплатить VPN", callback_data='pay')],
            [InlineKeyboardButton("Статус", callback_data='status')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Главное меню", reply_markup=reply_markup
        )
    elif query.data == 'manual_ios':
        keyboard = [
            [InlineKeyboardButton("Главное меню", callback_data='main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Инструкция по настройке IOS", reply_markup=reply_markup
        )
    elif query.data == 'manual_android':
        keyboard = [
            [InlineKeyboardButton("Главное меню", callback_data='main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Инструкция по настройке Android", reply_markup=reply_markup
        )
    elif query.data == 'pay_1':
        # keyboard = [
        #     [InlineKeyboardButton("Главное меню", callback_data='main')]
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # await query.edit_message_text(
        #     text="Оплата за 1 месяц", reply_markup=reply_markup
        # )
        """Sends an invoice without shipping-payment."""
        chat_id = update.callback_query.message.chat.id #update.message.chat_id
        title = "Оплата VPN"
        description = "Оплата за 1 месяц"
        # select a payload just for you to recognize its the donation from your bot
        payload = "Custom-Payload"
        # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
        currency = "RUB"
        # price in dollars
        price = 100
        # price * 100 so as to include 2 decimal points
        prices = [LabeledPrice("Руб", price*100)]

        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        await context.bot.send_invoice(
            chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
        )
    elif query.data == 'pay_3':
        """Sends an invoice without shipping-payment."""
        chat_id = update.callback_query.message.chat.id #update.message.chat_id
        title = "Оплата VPN"
        description = "Оплата за 3 месяца"
        # select a payload just for you to recognize its the donation from your bot
        payload = "Custom-Payload"
        # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
        currency = "RUB"
        # price in dollars
        price = 200
        # price * 100 so as to include 2 decimal points
        prices = [LabeledPrice("Руб", price * 100)]

        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        await context.bot.send_invoice(
            chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
        )
    elif query.data == 'pay_6':
        """Sends an invoice without shipping-payment."""
        chat_id = update.callback_query.message.chat.id #update.message.chat_id
        title = "Оплата VPN"
        description = "Оплата за 6 месяцев"
        # select a payload just for you to recognize its the donation from your bot
        payload = "Custom-Payload"
        # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
        currency = "RUB"
        # price in dollars
        price = 350
        # price * 100 so as to include 2 decimal points
        prices = [LabeledPrice("Руб", price * 100)]

        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        await context.bot.send_invoice(
            chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")

# after (optional) shipping, it's the pre-checkout
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Что-то пошло не так...Попробуйте еще раз")
    else:
        await query.answer(ok=True)


# finally, after contacting the payment provider...
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""

    chat_id = update.message.chat_id
    # query = update.callback_query
    print(update)


    lv_userObj = update.message.from_user

    # уникальное имя пользователя
    lv_user = f"{lv_userObj.username}_{lv_userObj.id}"
    ###

    # генерируем ключ клиента в папке /root/easy-rsa
    subprocess.run(["./easyrsa", "gen-req", lv_user, "nopass"], cwd="/root/easy-rsa", input=b"\n")

    # переносим сгенерированный ключ в папку /root/client-configs/keys
    shutil.copy2('/root/easy-rsa/pki/private/' + lv_user + '.key', '/root/client-configs/keys')

    # подписываем ключ и создаем сертификат в папке /root/easy-rsa
    subprocess.run(["./easyrsa", "sign-req", "client", lv_user], cwd="/root/easy-rsa", input=b"yes")

    # переносим сгенерированный сертификат в папку /root/client-configs/keys
    shutil.copy2('/root/easy-rsa/pki/issued/' + lv_user + '.crt', '/root/client-configs/keys')

    # запускаем скрипт make_config.sh, передавая параметр "имя клиента". Скрипт создает конфигурационный файл
    "Имя клиента".ovpn
    subprocess.run(["./make_config.sh", lv_user], cwd="/root/client-configs")

    # создаем пустой файл в root/client-configs/ccd_files с именем пользователя, без разрешения
    open('/root/client-configs/ccd_files/' + lv_user, 'a').close()

    # возвращаем файл .ovpn
    file_path = f"/root/client-configs/{lv_user}.ovpn"
    # file_path = r"D:\avg\test.ovpn"
    with open(file_path, "rb") as f:
        await context.bot.send_document(
            chat_id, document=f, filename=f"{lv_user}.ovpn"
        )
    ###

    # do something after successfully receiving payment?
    keyboard = [
        [InlineKeyboardButton("Главное меню", callback_data='main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # await query.edit_message_text(
    #     text="Оплата за 3 месяца", reply_markup=reply_markup
    # )

    # lv_user.username lv_user.id

    await update.message.reply_text("Оплата проведена!", reply_markup=reply_markup)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(gv_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    application.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
