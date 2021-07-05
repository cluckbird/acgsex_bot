# coding:utf-8
# pip install python-telegram-bot --upgrade
import os, logging, requests, time, psutil, datetime, re
from telegram.ext import *
from telegram import *

updater = Updater(token='在這裡填入你的BotToken', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
def start(update, context):
    keyboard = [[InlineKeyboardButton("錯誤反饋", callback_data='fk')],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text='KatoNei 色圖庫！ 開發中', reply_markup=reply_markup)

def sex(update, context):
    ftime = open('st_time','r').read()
    now_time = int("{:.0f}".format(time.time()))
    taginfo = str(update.message.text).replace(" ","").replace("/sex","").replace("@katonei_bot","")
    if now_time - int(ftime) > 5:
        if taginfo == "":
            # 請求隨機API
            img = requests.get('http://127.0.0.1:8080/api/num', allow_redirects = False)
            # 發送加載中訊息
            query = context.bot.send_message(chat_id=update.effective_chat.id, text='載入色圖中 ...', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('無法加載？', callback_data='loadingerror')]]))

            # menu_3 = [[InlineKeyboardButton("不夠色，再來一張", callback_data='bgs'),
            #             InlineKeyboardButton("不好看，刪掉", callback_data='pa')],
            #             [InlineKeyboardButton("圖像鏈接", url="https://pixiv.net/i/"+img.text)],]
            menu_3 = [[InlineKeyboardButton("不夠色，再來一張", callback_data='bgs')],
                        [InlineKeyboardButton("圖像鏈接", url="https://pixiv.net/i/"+img.text)],]
            reply_markup_sex = InlineKeyboardMarkup(menu_3)
            # context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://www.pixiv.net/artworks/"+img.text+"/image.webp", caption="@{} 給！你要的色圖".format(eval(str(update))['message']['from']['username']), reply_markup=reply_markup_sex)
            info = eval(open("/www/wwwroot/bot/webp/"+img.text+"/info.json", "r").read())
            try:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/www/wwwroot/bot/webp/"+img.text+"/image.webp", "rb"), caption="@{} 給！你要的色圖\n作品名: {}\n畫師: #{}\nPixiv ID: {}\n標籤: {}".format(eval(str(update))['message']['from']['username'], info['title'], info['user'], img.text, info['tag'].replace(" ", "  #")), reply_markup=reply_markup_sex)
            except:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/www/wwwroot/bot/webp/"+img.text+"/image.webp", "rb"), caption="給！你要的色圖\n作品名: {}\n畫師: #{}\nPixiv ID: {}\n標籤: {}".format(info['title'], info['user'], img.text, info['tag'].replace(" ", "  #")), reply_markup=reply_markup_sex)
            # 刪除 “加載訊息”
            context.bot.delete_message(chat_id=eval(str(query))['chat']['id'], message_id=eval(str(query))['message_id'])
            # 寫入發送時時間戳
            xr_time = "{:.0f}".format(time.time())
            open('st_time','w').write(xr_time)
        else:
            img = requests.get('http://127.0.0.1:8080/api/num_tag?tag='+taginfo, allow_redirects = False)
            if img.text != "error":
                # 發送加載中訊息
                query = context.bot.send_message(chat_id=update.effective_chat.id, text='載入色圖中 ...', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('無法加載？', callback_data='loadingerror')]]))

                menu_3 = [[InlineKeyboardButton("不夠色，再來一張", callback_data='bgs')],
                            [InlineKeyboardButton("圖像鏈接", url="https://pixiv.net/i/"+img.text)],]
                reply_markup_sex = InlineKeyboardMarkup(menu_3)
                # context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://www.pixiv.net/artworks/"+img.text+"/image.webp", caption="@{} 給！你要的色圖".format(eval(str(update))['message']['from']['username']), reply_markup=reply_markup_sex)
                info = eval(open("/www/wwwroot/bot/webp/"+img.text+"/info.json", "r").read())
                try:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/www/wwwroot/bot/webp/"+img.text+"/image.webp", "rb"), caption="@{} 給！你要的色圖\n作品名: {}\n畫師: #{}\nPixiv ID: {}\n標籤: {}".format(eval(str(update))['message']['from']['username'], info['title'], info['user'], img.text, info['tag'].replace(" ", "  #")), reply_markup=reply_markup_sex)
                except:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/www/wwwroot/bot/webp/"+img.text+"/image.webp", "rb"), caption="給！你要的色圖\n作品名: {}\n畫師: #{}\nPixiv ID: {}\n標籤: {}".format(info['title'], info['user'], img.text, info['tag'].replace(" ", "  #")), reply_markup=reply_markup_sex)
                # 刪除 “加載訊息”
                context.bot.delete_message(chat_id=eval(str(query))['chat']['id'], message_id=eval(str(query))['message_id'])
                # 寫入發送時時間戳
                xr_time = "{:.0f}".format(time.time())
                open('st_time','w').write(xr_time)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=eval(str(update))['message']['message_id'], text="沒有找到這個Tag呢...再試一次吧！")
    else:
        query = context.bot.send_message(chat_id=update.effective_chat.id, text='太快啦！等待五秒再試試吧', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('長時間處於等待狀態？', callback_data='loadingerror2')]]))
        # time.sleep(3)
        # context.bot.delete_message(chat_id=eval(str(query))['chat']['id'], message_id=eval(str(query))['message_id'])   # 刪除提示
    
def ping(update, context):
    cpu = psutil.cpu_percent()
    men = psutil.virtual_memory().percent
    usenum = open("data/use.conf").read()
    imglist = os.listdir(os.getcwd() + "/webp")
    try:
        upnum = open("data/upnum/"+str(datetime.datetime.now().strftime('%Y-%m-%d')), "r").read()
    except:
        upnum = 0

    context.bot.send_message(chat_id=update.effective_chat.id, text="CPU: {}%\nMEN: {}%\n使用量: {}\n今日更新量：{}\n數據庫總量: {}".format(str(cpu), str(men), str(usenum), str(upnum), str(len(imglist))))
    
def bothelp(update, context):
    helptext = '''BOT 使用幫助
`/sex` 隨機發送一張色圖
`/sex 標籤名` 隨機發送一張含該標籤的色圖  
`/ping` 查看伺服器和bot信息'''
    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=eval(str(update))['message']['message_id'], text=helptext, parse_mode="MarkdownV2")

def test(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="測試訊息", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('測試按鈕', callback_data='testb')]]))
    # print(update.message.text)
    pass

def echo(update, context):
    
    # if "投稿" in update.message.text:
    #     context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=eval(str(update))['message']['message_id'], text="點擊這裡 @katonei_push_bot 私訊投稿機器人就可以投稿啦！")
    pass


def menu_actions(update, context):
    query = update.callback_query

    if query.data == 'bgs':
        ftime = open('st_time','r').read()
        now_time = int("{:.0f}".format(time.time()))
        if now_time - int(ftime) > 5:
            img = requests.get('http://127.0.0.1:8080/api/num', allow_redirects = False)
            query_test = context.bot.send_message(chat_id=update.effective_chat.id, text='載入色圖中 ...', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('無法加載？', callback_data='loadingerror')]]))

            menu_4 = [[InlineKeyboardButton("不夠色，再來一張", callback_data='bgs')],
                    [InlineKeyboardButton("圖像鏈接", url="https://pixiv.net/i/"+img.text)],]
            reply_markup_sex = InlineKeyboardMarkup(menu_4)
            info = eval(open("/www/wwwroot/bot/webp/"+img.text+"/info.json", "r").read())
            try:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/www/wwwroot/bot/webp/"+img.text+"/image.webp", "rb"), caption="@{} 給！你要的色圖\n作品名: {}\n畫師: #{}\nPixiv ID: {}\n標籤: {}".format(eval(str(query))['from']['username'], info['title'], info['user'], img.text, info['tag'].replace(" ", "  #")), reply_markup=reply_markup_sex)
            except:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("/www/wwwroot/bot/webp/"+img.text+"/image.webp", "rb"), caption="給！你要的色圖\n作品名: {}\n畫師: #{}\nPixiv ID: {}\n標籤: {}".format(info['title'], info['user'], img.text, info['tag'].replace(" ", "  #")), reply_markup=reply_markup_sex)
            # 删除加载
            context.bot.delete_message(chat_id=eval(str(query_test))['chat']['id'], message_id=eval(str(query_test))['message_id'])
            xr_time = "{:.0f}".format(time.time())
            open('st_time','w').write(xr_time)
            # 鍵盤回調
            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="色圖來啦~")
        else:
            # 鍵盤回調
            context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="太快了，等待五秒後再試試吧！")

    elif query.data == 'pa':
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

        imgid = re.findall(re.compile(r'ID\:([\s\S]*?)\n'), query.message.caption)[0].replace(" ",'')
        try:
            context.bot.send_photo(chat_id=-1001163881018, photo=open("/www/wwwroot/bot/webp/"+imgid+"/image.webp", "rb"), caption="@{} 反饋: {} 不夠色".format(eval(str(query))['from']['username'], imgid), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('刪除', callback_data='delimg'),InlineKeyboardButton('前往組群', url='https://t.me/{}'.format(str(eval(str(query))['message']['chat']['username'])))]]))
        except:
            context.bot.send_photo(chat_id=-1001163881018, photo=open("/www/wwwroot/bot/webp/"+imgid+"/image.webp", "rb"), caption="反饋: {} 不夠色".format(imgid), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('刪除', callback_data='delimg')]]))
        # 鍵盤回調
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="嗚嗚嗚...")
    elif query.data == "delimg":
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        imgid = re.findall(re.compile(r'\反\饋\:([\s\S]*?)\不\夠\色'), query.message.caption)[0].replace(" ",'')
        os.system("rm -rf webp/"+imgid)
        # 鍵盤回調
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="已刪除 "+imgid)
    elif query.data == "fk":
        context.bot.send_message(chat_id=-1001163881018, text="@{} 反饋訊息，清入群查看問題".format(eval(str(query))['from']['username']), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('已解決', callback_data='pa'),InlineKeyboardButton('前往組群', url='https://t.me/{}'.format(str(eval(str(query))['message']['chat']['username'])))]]))
        query_test = context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='已通知管理員，等待處理')
        # 鍵盤回調
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="反饋成功！")
        time.sleep(5)
        # 删除反饋輸出
        context.bot.delete_message(chat_id=eval(str(query_test))['chat']['id'], message_id=eval(str(query_test))['message_id'])

    elif query.data == "loadingerror":
        context.bot.send_message(chat_id=-1001163881018, text="@{} 反饋: 伺服器圖像加載有問題".format(eval(str(query))['from']['username']), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('已解決', callback_data='pa'),InlineKeyboardButton('前往組群', url='https://t.me/{}'.format(str(eval(str(query))['message']['chat']['username'])))]]))
        query_test = context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='加載錯誤已反饋')
        # 鍵盤回調
        context.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text="反饋成功！")
        time.sleep(5)
        # 删除反饋輸出
        context.bot.delete_message(chat_id=eval(str(query_test))['chat']['id'], message_id=eval(str(query_test))['message_id'])
        
# /start
dispatcher.add_handler(CommandHandler('start', start))
# start 鍵盤回調
dispatcher.add_handler(CallbackQueryHandler(menu_actions))
# /sex
dispatcher.add_handler(CommandHandler('sex', sex))
# /ping
dispatcher.add_handler(CommandHandler('ping',ping))
# Help
dispatcher.add_handler(CommandHandler('help',bothelp))
# /test
dispatcher.add_handler(CommandHandler('test',test))

# 匹配所有
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()