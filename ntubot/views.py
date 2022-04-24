from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from ntubot.models import *
import json
from pathlib import Path
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
def section0(event, User_Info):
    # line_bot_api.push_message('Uc33f69ade360a9d6517282418d213b34', TextSendMessage(text='你可以開始了'))
    # print(event)
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):  # 如果有訊息事件
        if event.message.text == "遊戲開始":
            reply = [] #一次可傳多對話，至多五句
            reply.append(TextSendMessage("剛下課又餓又累的我，在尋找腳踏車的時候，卻怎麼樣也找不到我的腳踏車，只剩下大笨鳥週的車宣掉在地上。突然，我聽到一個奇怪的聲音……"))
            reply.append(TextSendMessage("大笨鳥的靈魂：我….我只是想吃蚯蚓而已….為什麼要這樣對我？什麼？你說你也不知道我在說什麼？但那明明就是你的腳踏車啊！！你真的不知道嗎？"))
            reply.append(TextSendMessage("（你如果不知道請輸入: 「我不知道」；如果假裝知道則輸入「我知道」）"))
            line_bot_api.reply_message(  # 回復傳入的訊息文字
                event.reply_token, reply)
        elif event.message.text == "我不知道":
            reply = [] #一次可傳多對話，至多五句
            reply.append(TextSendMessage("大笨鳥的靈魂：那好吧，我就姑且相信你。但你要陪我一起找到兇手以及真相！"))
            reply.append(TextSendMessage("我：「但我肚子有點餓，我可以先吃飯嗎？」"))
            reply.append(TextSendMessage("大笨鳥的靈魂：那就去大一女餐廳吧！快點吃一吃，幫我找到兇手！！！"))
            reply.append(TextSendMessage("到大一女餐廳後，請輸入：「我到大一女餐廳了」"))
            line_bot_api.reply_message(event.reply_token, reply)
            User_Info.objects.filter(uid=event.source.user_id).update(section=1)
        elif event.message.text == "我知道":
            reply = [] #一次可傳多對話，至多五句
            reply.append(TextSendMessage("你看起來就是一臉不知道，還說什麼知道，快點啦一起幫我找到兇手！"))
            reply.append(TextSendMessage("我：「但我肚子有點餓，我可以先吃飯嗎？」"))
            reply.append(TextSendMessage("大笨鳥的靈魂：那就去大一女餐廳吧！快點吃一吃，幫我找到兇手！！！"))
            reply.append(TextSendMessage("到大一女餐廳後，請輸入：「我到大一女餐廳了」"))
            line_bot_api.reply_message(event.reply_token, reply)
            User_Info.objects.filter(uid=event.source.user_id).update(section=1)
def section1(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到大一女餐廳了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("路人Ａ：同學，我看你骨骼驚奇，是百年難得一見的解謎奇才，我看你八成正在為腳踏車不見而煩惱吧？"))
                reply.append(TextSendMessage("是的話，請回答：「大概是吧」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("大笨鳥的靈魂：快去大一女餐廳！"))
        elif user_info.part == 1:
            if event.message.text == "大概是吧":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("路人Ａ：我的腳踏車已經被拖吊好多次，水源阿伯的電話我已經倒背如流！我現在出一道謎題，如果你猜中，我就告訴你阿伯的電話！"))
                reply.append(TextSendMessage("願意接受挑戰，請輸入「好吧」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=2)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答：「大概是吧」"))
        elif user_info.part == 2:
            if event.message.text == "好吧":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("路人Ａ：這是厚宅的菜單，其中我最喜歡吃咖喱，仔細看裡面五道菜餚的價錢，每道菜的價錢對應到一個號碼，第一位跟最後一位號碼是１跟２，總共有五碼，然後這五碼就是水源阿伯的電話。ex: 111 -> 0, 104 -> 2"))
                reply.append(TextSendMessage("解出謎底後，請輸入五碼："))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=3)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答：「好吧」"))
        elif user_info.part == 3:
            if event.message.text == "12222":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("我(打電話給水源阿伯)：阿伯你好，我找不到我的腳踏車，想請問我的腳踏車是不是被拖到水源去了？"))
                reply.append(TextSendMessage("水源阿伯：沒有啊，你的腳踏車不在我們這裡，你去駐警隊問問看？"))
                reply.append(TextSendMessage("到駐警隊後，請輸入：「我到駐警隊了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=2)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section2(event, User_Info):
    pass

def section3(event, User_Info):
    pass
 
@csrf_exempt
def callback(request):
    user = json.loads(Path("ntubot/user.json").read_text())
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if User_Info.objects.filter(uid=event.source.user_id).exists()==False:
                User_Info.objects.create(uid=event.source.user_id,
                                         name=line_bot_api.get_profile(event.source.user_id).display_name, section=0)
            if(event.source.user_id not in user): user[event.source.user_id] = 0
            
            user_info = User_Info.objects.get(uid=event.source.user_id)
            print(user_info.section)
            if user_info.section == 0:
                section0(event, User_Info)
            elif user_info.section == 1:
                section1(event, User_Info)
        # print(user)
        file = open("ntubot/user.json", "w")
        json.dump(user, file)
        file.close()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
