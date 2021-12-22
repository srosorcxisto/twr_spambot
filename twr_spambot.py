#!/usr/bin/env python3

""" Short description of this Python module.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "S-ro Sorcxisto"
__email__ =  = "srosorcxisto@protonmail.ch"
__credits__ = ["Moiss ROse Bot dev team", "Python Telegram Bot "]
__date__ = "2020/12/22"
__license__ = "GPLv3"
__version__ = "0.0.1"



import logging
import os
import re
import io

from telegram import *
from telegram.ext import *

from datetime import datetime

import os
print(os.environ['HOME'])
CHAT_ID = os.environ['CHAT_ID']
API_TOKEN = os.environ['API_TOKEN']



blocklist_persist = 'blocklist.txt'

if not os.path.exists(blocklist_persist):
    open(blocklist_persist, 'w').close()

block_list = [line.rstrip() for line in open(blocklist_persist)]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def is_user_admin(user_id: int, update: Update, bot) -> bool:
    return bot.get_chat_member(chat_id=CHAT_ID, user_id=user_id).status in ['administrator', 'creator']


def persist_update():
    blocklist_file = open(blocklist_persist, 'w')
    block_list_formatted = map(lambda x: x + '\r', block_list)
    blocklist_file.writelines(block_list_formatted)
    blocklist_file.close()


def list(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        chunked_list = []

        for i in range(0, len(block_list), 80):
            chunked_list.append(block_list[i:i + 80])

        for chunk in chunked_list:
            update.message.reply_text('\n'.join(chunk), disable_web_page_preview=True)

    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def tail(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        if len(context.args) == 0:
            lines = 10

        elif type(int(context.args[0])) == int:
            lines = int(context.args[0])

        else:
            # print(context.args[0])
            update.message.reply_text('Please enter a number')
            return

        tail_text = f'Here are the last  {lines} entries in the blocklist:\n'

        for i in block_list[len(block_list) - lines:len(block_list)]:
            tail_text = tail_text + '     ' + i + '\n'

        update.message.reply_text(tail_text, disable_web_page_preview=True)
    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def status(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        update.message.reply_text('I am alive and well.\n')

    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def kill(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        update.message.reply_text('Killing process.\n')
        with io.open('log.txt', 'a', encoding="utf-8") as f:
            f.write('Kill:\n   User: {}\n   UTime: {}'.format(
                update.message.from_user.username, datetime.now()))
        exit()

    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def debug(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        update.message.reply_document(document=open('debug_log.txt', 'rb'))

    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def log(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        update.message.reply_document(document=open('log.txt', 'rb'))

    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def export(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        update.message.reply_document(document=open('blocklist.txt', 'rb'))

    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.'
                                  , disable_web_page_preview=True)


def add(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):
        if context.args[0]:
            string_to_add = ' '.join(context.args)
            if string_to_add == ' ':
                update.message.reply_text('I can\'t add a blank filter...',
                                          disable_web_page_preview=True,
                                          disable_notification=True)
            else:
                if string_to_add in block_list:
                    update.message.reply_text(f'{string_to_add} is already in the blocklist...',
                                              disable_web_page_preview=True,
                                              disable_notification=True)
                else:
                    block_list.append(string_to_add)
                    persist_update()
                    update.message.reply_text(f'Added {string_to_add} to blocklist',
                                              disable_web_page_preview=True,
                                              disable_notification=True)
                    with io.open('log.txt', 'a', encoding="utf-8") as f:
                        f.write(f'Add: \n'
                                f'   User: {update.message.from_user.full_name}\n'
                                f'   Filter: {string_to_add}\n'
                                f'   Time: {datetime.now()}\n')
    else:
        update.message.reply_text('Sorry, only admins can use this function')


def delete(update: Update, context: CallbackContext) -> None:
    if is_user_admin(update.message.from_user.id, update, context.bot):

        string_to_del = ' '.join(context.args)
        block_list.remove(string_to_del)
        persist_update()
        update.message.reply_text(f'Removed {string_to_del} from blocklist',
                                  disable_web_page_preview=True,
                                  disable_notification=True)
        with io.open('log.txt', 'a', encoding="utf-8") as f:
            f.write(f'Rem: \n'
                    f'   User: {update.message.from_user.full_name}\n'
                    f'   Filter: {string_to_del}\n'
                    f'   Time: {datetime.now()}\n')
    else:
        update.message.reply_text('Sorry, only admins from the main White Rose chat can use this function.')


def message(update: Update, context: CallbackContext) -> None:

    message_text = 'Another one bites the dust...!\n' \
                   'Banned: {}.\n' \
                   'Reason: \n' \
                   '     Automated blocklist action, due to a match on: {} \n\n' \
                   '@admin, Feel free to delete this message if no further action is warranted. Contact @srosorcxisto in ' \
                   'the admin chat if the bot is misbehaving. '

    if update.message:
        for s in block_list:

            if re.search(re.escape(s), '{}'.format(update.message.text)):

                update.message.reply_text(message_text.format(update.message.from_user.full_name, s),
                                          disable_web_page_preview=True)
                user_id_to_ban = update.message.from_user.id
                try:

                    with io.open('log.txt', 'a', encoding="utf-8") as f:
                        f.write(f'Ban: \n'
                                f'   User: {update.message.from_user.full_name} ({user_id_to_ban})\n'
                                f'   Chat:{update.effective_chat.title}({update.effective_chat.username}: {update.effective_chat.id})\n'
                                f'   Match: {s}\n'
                                f'   Time: {datetime.now()}\n'
                                f'   result: Success\n')
                    update.effective_chat.ban_member(user_id_to_ban)
                    update.message.delete()
                    break

                except:
                    with io.open('log.txt', 'a', encoding="utf-8") as f:
                        f.write(f'Ban: \n'
                                f'   User: {update.message.from_user.full_name} ({user_id_to_ban})\n'
                                f'   Chat:{update.effective_chat.title}({update.effective_chat.username}: {update.effective_chat.id})\n'
                                f'   Match: {s}\n'
                                f'   Time: {datetime.now()}\n'
                                f'   result: Fail\n')
                    update.message.reply_text('I am unable to ban the user/delete the spam. Am I an admin?',
                                              allow_sending_without_reply=True)
                    break

    if update.edited_message:
        for s in block_list:
            if re.search(re.escape(s), '{}'.format(update.edited_message.text)):
                update.edited_message.reply_text(message_text.format(update.edited_message.from_user.username, s),
                                                 disable_web_page_preview=True)
                user_id_to_ban = update.edited_message.from_user.id
                try:

                    with io.open('log.txt', 'a', encoding="utf-8") as f:
                        f.write(f'Ban: \n'
                                f'   User: {update.edited_message.from_user.full_name} ({user_id_to_ban})\n'
                                f'   Chat:{update.effective_chat.title}({update.effective_chat.username}: {update.effective_chat.id})\n'
                                f'   Match: {s}\n'
                                f'   Time: {datetime.now()}\n'
                                f'   result: Success\n')

                    update.effective_chat.ban_member(user_id_to_ban)
                    update.edited_message.delete()
                    break
                except:
                    with io.open('log.txt', 'a', encoding="utf-8") as f:
                        f.write(f'Ban: \n'
                                f'   User: {update.edited_message.from_user.full_name} ({user_id_to_ban})\n'
                                f'   Chat:{update.effective_chat.title}({update.effective_chat.username}: {update.effective_chat.id})\n'
                                f'   Match: {s}\n'
                                f'   Time: {datetime.now()}\n'
                                f'   result: Fail\n')
                    update.edited_message.reply_text('I am unable to ban the user/delete the spam. Am I an admin?',
                                                     allow_sending_without_reply=True)
                    break
            else:
                pass


def main() -> None:
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    # dispatchers
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('rem', delete))
    dispatcher.add_handler(CommandHandler('list', list))
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(CommandHandler('debug', debug))
    dispatcher.add_handler(CommandHandler('kill', kill))
    dispatcher.add_handler(CommandHandler('tail', tail))
    dispatcher.add_handler(CommandHandler('log', log))
    dispatcher.add_handler(CommandHandler('export', export))

    dispatcher.add_handler(MessageHandler(Filters.text, message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    with io.open('log.txt', 'a', encoding="utf-8") as f:
        f.write(f'Started session at {datetime.now()}\n')
    main()
