import re

from telegram import Update, InputMediaPhoto
from telegram.ext import Handler, BaseFilter, MessageHandler, Filters, CallbackContext

handlers = []


def handler(handler: Handler, arg: str = None, **kw):
    def decorater(func):
        if arg == None:
            func_handler = handler(func, **kw)
        else:
            func_handler = handler(arg, func, **kw)
        handlers.append(func_handler)
        return func
    return decorater


def message(filters: BaseFilter, **kw):
    return handler(MessageHandler, filters, **kw)


def isSignature(signature: str):
    def decorater(func):
        def wrapper(update: Update, context: CallbackContext):
            if update.channel_post.author_signature == signature:
                return func(update, context)
            else:
                def _pass(update: Update, context: CallbackContext):
                    return
                return _pass(update, context)
        return wrapper
    return decorater


def enntities_parser(text, entities):  # 假定：没有嵌套；只有超链接
    text_with_link = text
    entities.reverse()  # 从后往前替换
    for entity in entities:
        start = entity.offset
        end = start + entity.length
        text_with_link = text_with_link[:start] + '<a href="{}">'.format(entity.url) + text_with_link[start:end] + '</a>' + text_with_link[end:]
    return text_with_link


@message(filters=Filters.text & Filters.update.channel_post)
@isSignature('IFTTT')
def parser_bot(update: Update, context: CallbackContext):
    try:
        text = update.channel_post.text
        entities = update.channel_post.entities
        if not re.findall(r'Media\n\n', text):
            return
        text_without_media = re.sub(r'Media\n\n', '', text)
        media = []
        entities_without_media = []
        for entity in entities:
            if entity.type == 'text_link':
                if re.match(r'https?://wx\d\.sinaimg\.cn', entity.url):
                    media.append(InputMediaPhoto(entity.url))
                else:
                    entities_without_media.append(entity)
        text_with_link = enntities_parser(
            text_without_media, entities_without_media)
        msg = update.effective_message.reply_text(
            text=text_with_link, quote=False, disable_web_page_preview=True, parse_mode='HTML')
        if media:
            if len(media) > 9:
                media2 = media[9:]
                media1 = media[:9]
                msg.reply_media_group(media=media1, quote=True)
                msg.reply_media_group(media=media2, quote=True)
            else:
                msg.reply_media_group(media=media, quote=True)
        update.effective_message.delete()
        return
    except Exception as e:
        print(repr(e))
        return
