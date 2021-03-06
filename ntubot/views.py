from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import F
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
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
        if user_info.part == 0:
            if event.message.text == "遊戲開始":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("剛下課又餓又累的我，在尋找腳踏車的時候，卻怎麼樣也找不到我的腳踏車，只剩下大笨鳥週的車宣掉在地上。突然，我聽到一個奇怪的聲音……"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：我….我只是想吃蚯蚓而已….為什麼要這樣對我？什麼？你說你也不知道我在說什麼？但那明明就是你的腳踏車啊！！你真的不知道嗎？"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/ra4iTVO.jpg",preview_image_url="https://i.imgur.com/ra4iTVO.jpg"))
                #reply.append(TextSendMessage("（你如果不知道請輸入: 「我不知道」；如果假裝知道則輸入「我知道」）"))
                reply.append(TemplateSendMessage(alt_text='Buttons template',
                                                 template=ButtonsTemplate(
                                                    title='請回答是否知道',
                                                    text='你如果不知道請輸入：我不知道」；如果假裝知道則輸入「我知道」',
                                                    actions=[
                                                        MessageTemplateAction(
                                                            label='我知道',
                                                            text='我知道'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='我不知道',
                                                            text='我不知道'
                                                        )])))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入：「遊戲開始」"))
        elif user_info.part == 1:
            if event.message.text == "我不知道":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那好吧，我就姑且相信你。但你要陪我一起找到兇手以及真相！"))
                reply.append(TextSendMessage("\U0001F469我：「但我肚子有點餓，我可以先吃飯嗎？」"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那就去大一女餐廳吧！快點吃一吃，幫我找到兇手！！！"))
                reply.append(TextSendMessage("到大一女餐廳後，請輸入：「我到大一女餐廳了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=1)
            elif event.message.text == "我知道":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：你看起來就是一臉不知道，還說什麼知道，快點啦一起幫我找到兇手！"))
                reply.append(TextSendMessage("\U0001F469我：「但我肚子有點餓，我可以先吃飯嗎？」"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那就去大一女餐廳吧！快點吃一吃，幫我找到兇手！！！"))
                reply.append(TextSendMessage("到大一女餐廳後，請輸入：「我到大一女餐廳了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：你到底知不知道啦！"))

def section1(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到大一女餐廳了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F963路人Ａ：同學，我看你骨骼驚奇，是百年難得一見的解謎奇才，我看你八成正在為腳踏車不見而煩惱吧？"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/bjTA4bQ.jpg",preview_image_url="https://i.imgur.com/bjTA4bQ.jpg"))
                #reply.append(TextSendMessage("是的話，請回答：「大概是吧」"))
                reply.append(TemplateSendMessage(alt_text='Buttons template',
                                                 template=ButtonsTemplate(
                                                    title='請回答',
                                                    text='是的話，請回答：「大概是吧」',
                                                    actions=[
                                                        MessageTemplateAction(
                                                            label='大概是吧',
                                                            text='大概是吧'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='大概不是',
                                                            text='大概不是'
                                                        )])))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：快去大一女餐廳！"))
        elif user_info.part == 1:
            if event.message.text == "大概是吧":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F963路人Ａ：我的腳踏車已經被拖吊好多次，水源阿伯的電話我已經倒背如流！我現在出一道謎題，如果你猜中，我就告訴你阿伯的電話！"))
                #reply.append(TextSendMessage("願意接受挑戰，請輸入「好吧」"))
                reply.append(TemplateSendMessage(alt_text='Buttons template',
                                                 template=ButtonsTemplate(
                                                    title='請回答',
                                                    text='願意接受挑戰，請輸入「好吧」',
                                                    actions=[
                                                        MessageTemplateAction(
                                                            label='好吧',
                                                            text='好吧'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='不好',
                                                            text='不好'
                                                        )])))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=2)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答：「大概是吧」"))
        elif user_info.part == 2:
            if event.message.text == "好吧":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F963路人Ａ：阿伯的電話號碼就是大一女生宿舍B棟一樓的滅火器數量"))
                reply.append(TextSendMessage("解出謎底後，請輸入二碼："))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=3)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答：「好吧」"))
        elif user_info.part == 3:
            #max_hint = 1
            if event.message.text == "11":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("註: 此號碼為虛構，請勿因為覺得好玩就去打擾水源阿伯"))
                reply.append(TextSendMessage("\U0001F469我(打電話給水源阿伯)：阿伯你好，我找不到我的腳踏車，想請問我的腳踏車是不是被拖到水源去了？"))
                reply.append(TextSendMessage("\U0001F474水源阿伯：沒有啊，你的腳踏車不在我們這裡，你去駐警隊問問看？"))
                reply.append(TextSendMessage("到駐警隊後，請輸入：「我到駐警隊了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=2)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("可以找找看餐廳裡的大一女生宿舍B棟一樓平面圖"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section2(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到駐警隊了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F46E警衛: 同學請問有什麼事嗎?"))
                reply.append(TextSendMessage("\U0001F469我: 我的腳踏車不見了，想請你們幫忙調閱監視器!"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/5KjQVSp.jpg",preview_image_url="https://i.imgur.com/5KjQVSp.jpg"))
                reply.append(TextSendMessage("\U0001F46E警衛(一邊查監視器)：喔對了同學，最近一直有人來抱怨這附近有一棵「看起來很危險，會壓到兩個人」的樹，叫駐警隊處理，雖然維護校園安全是我們的工作範圍啦，可是講這麼模糊誰知道阿？你可以幫我調查一下是怎麼回事嗎？\n\n請你輸入「是什麼樹」看起來快要壓到兩個人了？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我現在應該要去駐警隊問吧? 請輸入：「我到駐警隊了」"))
        elif user_info.part == 1:
            if event.message.text == "朴樹":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F46E警衛：太感謝你了！剛好我這邊也調到影像了，你來看看是不是你的車子"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/F2FqVCe.jpg",preview_image_url="https://i.imgur.com/F2FqVCe.jpg"))
                reply.append(TextSendMessage("\U0001F469我：原來案發現場在舟山路水車附近！"))
                reply.append(TextSendMessage("到舟山路後，請輸入「我到案發現場了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=3)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("駐警隊前有棵樹有金屬支撐，下方有兩尊雕像，請輸入該樹品種俗名"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section3(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到案發現場了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那裏有人在拍照！我們去問他有沒有看到是誰壓到我的！"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/hbZ9Shh.jpg",preview_image_url="https://i.imgur.com/hbZ9Shh.jpg"))
                reply.append(TextSendMessage("\U0001F9D0學生:明明這裡都有動物穿越減速慢行的路牌，那個人車還是騎得很快，結果撞死大笨鳥後就跑了，這已經不是第一次了。"))
                reply.append(TextSendMessage("\U0001F469我：那你有看到犯人壓到大笨鳥後去了哪裡嗎？\n\n\U0001F9D0學生:好像有看到往哪裡去......，不過我在進行科普閱讀的推廣與實踐，你看起來是個聰明人，我把答案包裝成謎題，你自己去找尋答案吧，相信難不倒你。"))
                reply.append(TextSendMessage("「犯人的去向，路牌會『合力』告訴你。」\n\n請你輸入犯人是往哪棟建築物去了？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("這些圖片的最後應該就是案發現場吧? 請輸入「我到案發現場了」"))
        elif user_info.part == 1:
            if event.message.text == "圖書館" or event.message.text == "總圖" or event.message.text == "台大圖書館":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：原來往圖書館去了！！我們趕快追過去"))
                reply.append(TextSendMessage("到圖書館後，請輸入「我到圖書館了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=4)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("以兩路牌指向為兩力方向，正解即是兩力合力所指向的最醒目建築物"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/FXp9sgi.jpg",preview_image_url="https://i.imgur.com/FXp9sgi.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section4(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到圖書館了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/n14fdXZ.jpg",preview_image_url="https://i.imgur.com/n14fdXZ.jpg"))
                reply.append(TextSendMessage("\U0001F469我：請問你剛剛有看到什麼可疑、匆忙的人衝進圖書館嗎？\n\n\U0001F4DA館員：沒有耶，我們的讀者都是很文雅的，沒有什麼人會用衝的進來，而且圖書館也不能奔跑喔！\n\n\U0001F469我：嗯…好吧"))
                reply.append(TextSendMessage("\U0001F4DA館員：啊，是說我好像有印象，有一個人整張臉皺成一團，看起來很緊張，褲子上沾滿一些紅色的汙漬。我就覺得很討厭呀！感覺就是剛去棒球場比完棒球或壘球，打輸了，但是好歹也把褲子上的紅土清理乾淨再進來吧？"))
                reply.append(TextSendMessage("\U0001F469我：那個人後來往哪邊走了？\n\n\U0001F4DA館員：他朝我方向走過來啊！他給我一張紙條，我拿來看，上面是一堆文字跟數字，他叫我幫他查這張紙代表的東西，我就罵他啊，我說這不是我要提供的服務\n\n\U0001F469我：所以那是什麼？\n\n\U0001F4DA館員：我可以直接把紙條送給你\n\n請你進圖書館翻書，輸入那位讀者要找的答案是什麼？"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/t64NOqo.jpg",preview_image_url="https://i.imgur.com/t64NOqo.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                #紙條圖片
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：我們去圖書館! 請輸入「我到圖書館了」"))
        elif user_info.part == 1:
            if event.message.text == "報廢":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("(你不小心把書摔在地上，似乎有什麼東西掉出來…？)"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/LAnXc2K.jpg",preview_image_url="https://i.imgur.com/LAnXc2K.jpg"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/iclQMeN.jpg",preview_image_url="https://i.imgur.com/iclQMeN.jpg"))
                reply.append(TextSendMessage("撿起學生證後，發現他穿著某學院的領巾，於是我跑到兇手的系館找人。"))
                reply.append(TextSendMessage("到目的地後，請輸入「我到XX系系館了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=5)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("紙條上半部是一本書的索書號，下半部則是書內名詞的編號，請輸入該名詞"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section5(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到資工系系館了" or event.message.text == "我到德田館了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F469我：我發現德田館外面的地上掉了一張紙，我觀察了一下，發現紙上的格子對應著資工系館的窗戶格子。"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/1dweGIW.jpg",preview_image_url="https://i.imgur.com/1dweGIW.jpg"))
                reply.append(TextSendMessage("請你輸入謎底是什麼？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            elif event.message.text == "我到電機系系館了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("葉秉宸：年輕人，不好意思啊，我在家裡養了六隻黑冠麻鷺好久了，大概三年了吧，現在他們都已長大成熟，發展出各自的興趣，該去讀大學了，能不能請你..."))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/s2xc2fc.jpg",preview_image_url="https://i.imgur.com/s2xc2fc.jpg"))
                reply.append(TextSendMessage("\U0001F469我：等等，黑冠麻鷺是什麼啊？\n\n葉秉宸：黑冠麻鷺就是大家俗稱的大笨鳥啊！不過我養的這幾隻才不笨，他們是大聰鳥。回到正題，可不可以麻煩你帶他們到不同的學院，讓她們進去就讀。他們分別要去：文學院、社科院、管理學院、理學院、工學院、生農學院。\n\n\U0001F469我：等等，這是什麼奇怪的要求？我才不要！\n\n（老人把六隻笨鳥的牽繩塞在你手上後，一溜煙跑走了）\n\n\U0001F469我：我...，什麼鬼啊？這下怎麼辦\n\n（六隻笨鳥眾目睽睽看著你）"))
                reply.append(TextSendMessage("（支線劇情觸發！請你帶這六隻笨鳥分別到文學院、社科院、管理學院、理學院、工學院、生農學院吧！當你準備好要送他們到該學院時，請你輸入「笨鳥來去XX院讀書囉」）\n\n如果要繼續主線請輸入「回到主線」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(is_side=True)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入「我到XX系系館了」"))
        elif user_info.part == 1:
            if event.message.text == "KC":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("我從第六排的窗戶內側拿到一本冊子，是紀錄兇手在資工系的生活"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/XcBW7NA.jpg",preview_image_url="https://i.imgur.com/XcBW7NA.jpg"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/rOiz7E8.jpg",preview_image_url="https://i.imgur.com/rOiz7E8.jpg"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那麼接下來去註冊組問問看，誰是這張學生證的主人吧！"))
                reply.append(TextSendMessage("請輸入換發學生證要去哪棟大樓"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=6)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("「非赤為灰」對應到要看灰色橫條的部份\n\n「由天而地」代表要從上往下數\n\n「家中兄弟我名子叔」從伯仲叔季推出排第三\n\n(第一條灰色橫條在建築物最上方)"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section6(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "行政大樓":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("到行政大樓後，我前往註冊組詢問"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/0n3Gch7.jpg",preview_image_url="https://i.imgur.com/0n3Gch7.jpg"))
                reply.append(TextSendMessage("\U0001F469我: 不好意思，我想問這個舊的學生證是誰的，後來換到哪個系了? 我強烈懷疑他偷了我的腳踏車，還輾過大笨鳥!\n\n\U0001F170職員A: 這個資訊涉及個人隱私，不能隨便洩漏\n\n\U0001F469我: 可是我已經去駐警隊報案了耶"))
                reply.append(TextSendMessage("\U0001F170職員A: 在警衛來確認之前都不行\n\n\U0001F469我: 大笨鳥，我們在學校跑來跑去還是得不到答案，還是乾脆去外面警察局報案算了...?\n\n\U0001F171職員B: (偷偷地)同學你看起來這麼聰明，一定知道傅鐘的歷史在「哪邊」。那個A齁，常常找人問這些問題，裝的自己什麼都知道一樣，這次一定要剉剉他的銳氣。只要告訴我答案，我就去幫你查學生證。\n\n請你輸入傅鐘的歷史靠近哪個方位？"))
                reply.append(TemplateSendMessage(alt_text='Buttons template',
                                                 template=ButtonsTemplate(
                                                    title='傅鐘的歷史靠近哪個方位',
                                                    text='請走入傅鐘內部，尋找記載歷史的文字靠近哪一方位?',
                                                    actions=[
                                                        MessageTemplateAction(
                                                            label='東',
                                                            text='東'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='南',
                                                            text='南'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='西',
                                                            text='西'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='北',
                                                            text='北'
                                                        )])))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("如果真的不知道可以上網查喔"))
        elif user_info.part == 1:
            if event.message.text == "西":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("註: 若真的撿到遺失的學生證請交給駐警隊失物招領\n\n職員B告訴我兇手姓名以及他後來轉到社科院，我接著在FB查詢，發現10分鐘前兇手在醉月湖打卡"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/uxjGueM.jpg",preview_image_url="https://i.imgur.com/uxjGueM.jpg"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：他在醉月湖！我們快追上去！"))
                reply.append(TextSendMessage("到醉月湖後，輸入「我到醉月湖了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=7)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("請觀察腳邊哪一方位有記載傅鐘的歷史?"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section7(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到醉月湖了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/CnNWgXE.jpg",preview_image_url="https://i.imgur.com/CnNWgXE.jpg"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：你看！那台是你的腳踏車對吧?"))
                reply.append(TextSendMessage("(我發現腳踏車被丟進湖中，在裏頭載浮載沉。想要跳下湖中把腳踏車拿回來，但是湖邊的水深危險等標語迫使我打消念頭。這個時候發現湖旁有救生圈可以使用，拋救生圈套住腳踏車把它撈起來，但自己一個人實在很吃力)"))
                reply.append(TextSendMessage("此時，醉月湖中突然出現一隻鵝"))
                #reply.append(TextSendMessage("\U0001F9A2鵝：請問你掉的腳踏車是哪一台腳踏車呢？「金色的」？「銀色的」？還是「被偷走的腳踏車」？"))
                reply.append(TemplateSendMessage(alt_text='Buttons template',
                                                 template=ButtonsTemplate(
                                                    title='請回答',
                                                    text='\U0001F9A2鵝：請問你掉的腳踏車是哪一台腳踏車呢？「金色的」？「銀色的」？還是「被偷走的腳踏車」？',
                                                    actions=[
                                                        MessageTemplateAction(
                                                            label='金色的腳踏車',
                                                            text='金色的腳踏車'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='銀色的腳踏車',
                                                            text='銀色的腳踏車'
                                                        ),
                                                        MessageTemplateAction(
                                                            label='被偷走的腳踏車',
                                                            text='被偷走的腳踏車'
                                                        )])))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：我們快去醉月湖找他!"))
        elif user_info.part == 1:
            if event.message.text == "被偷走的腳踏車":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F9A2鵝：好，看在你這麼誠實的份上，我就請小動物們都一起來幫助你！但是你要先記得醉月湖的「緊急數字」才能確保這次行動的安全！\n\n請你輸入緊急電話上的號碼是多少？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=2)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F9A2鵝: 你確定嗎？ 誠實才會有好報喔！"))
        elif user_info.part == 2:
            if event.message.text == "27":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("（在小動物們的協助下，腳踏車成功被打撈出來，我開心的手舞足蹈，跟著動物一起跳I like to move it）"))
                reply.append(TextSendMessage("\U0001F9A2鵝：腳踏車之外，這是你誠實相告的額外獎勵！(拿出一張金色的紙條)"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/xjd0lV0.jpg",preview_image_url="https://i.imgur.com/xjd0lV0.jpg"))
                reply.append(TextSendMessage("犯人其實覺得很對不起，希望到只有文字的學院之樹找他"))
                reply.append(TextSendMessage("\U0001F469我：雖然拿到腳踏車了，但我們還是有必要知道真相！對吧大笨鳥？\n\n\U0001F426大笨鳥的靈魂：沒錯沒錯，走吧，學院之樹在社科院詩牆。\n\n據說社科院詩牆有這麼一首詩存在，到社科院詩牆後請輸入「我到詩牆了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=8)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("在醉月湖畔緊急電話上的數字是什麼呢？"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/c0Gjwh1.jpg",preview_image_url="https://i.imgur.com/c0Gjwh1.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section8(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到詩牆了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F469我：犯人居然把我的腳踏車丟到湖裡，想要毀屍滅跡，又給我這個紙條到底在想什麼？"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/ANcWWML.jpg",preview_image_url="https://i.imgur.com/ANcWWML.jpg"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：可能是某個讓犯人心神不寧的句子吧？\n\n請你輸入是什麼樣的句子讓犯人焦慮？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我應該是要去充滿文字的地方找犯人 請輸入「我到詩牆了」"))
        elif user_info.part == 1:
            if event.message.text == "「那時我是老人了，」我說：「然而我會永遠認得你」":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("犯人從社科圖走了出來，對我說了許多事，也向我道歉，最後他給我一個臉書連結叫我上去看看"))
                reply.append(TextSendMessage("https://www.facebook.com/%E6%87%BA%E6%82%94%E4%B9%8B%E7%89%86-102158875809508"))
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：謝謝你陪我找到犯人了，我可以安心的成佛了！希望你跟你之後的腳踏車一生平安"))
                #總使用提示數決定結局
                total = user_info.total_hint
                if(total <= 2): #困難
                    reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/mRQfJxX.jpg",preview_image_url="https://i.imgur.com/mRQfJxX.jpg"))
                elif(total > 2 and total <=5): #普通
                    reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/q8YsK2b.jpg",preview_image_url="https://i.imgur.com/q8YsK2b.jpg"))
                else: #簡單
                    reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/i4tXQkr.jpg",preview_image_url="https://i.imgur.com/i4tXQkr.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=0) #玩完重置進度
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=0)
                User_Info.objects.filter(uid=event.source.user_id).update(is_side=False)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "大笨鳥救救我":
                User_Info.objects.filter(uid=event.source.user_id).update(total_hint=F('total_hint')+1)
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("數字為詩牆每行的字數，「/」為分段，圖片中玻璃也有分段。三個數字希望玩家能找到該段落"))
                line_bot_api.reply_message(event.reply_token, reply)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def side_quest(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        if user_info.side_part == 0:
            if event.message.text == "笨鳥來去文學院讀書囉":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥：（喃喃自語）「那棵樹正悲壯地脫落高舉的葉子，這時我們都是老人了...」\n\n我：你在唸什麼啊？\n\n笨鳥：這是楊牧的詩，叫〈學院之樹〉，聽說文學院有一棵將近百年的老樹，這首詩寫的就是它，但最近因為生病而被移除了，真的太悲壯、太讓人惋惜了。你知道是哪棵樹嗎？\n\n（請你告訴笨鳥這棵樹是什麼樹）"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=1)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=1)
            elif event.message.text == "笨鳥來去社科院讀書囉":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥：欸欸，在鳥界裡其實一直有一個傳說，就是社科院三樓聽說有個空中花園，裡面有一棵非常巨大的樹矗立，並直竄不同的樓層，甚至在裡面還能聽課、聽演講...，你能告訴我是什麼神祕的地方嗎？好好奇！\n\n（請你告訴笨鳥這個地方是哪裡）"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=1)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=2)
            elif event.message.text == "笨鳥來去管理學院讀書囉":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥：聽說理工學院的學生們為了避免設備壞掉，會放乖乖，那如果是管院哩？\n\n我：管院管人的，可能只能拜拜求神保佑能遇到好人吧...（？）\n\n笨鳥：喔喔！這是我聽說的那個嘛？聽說在管院附近有一間很靈驗的廟，藏在小徑之中，告訴我是哪！帶我去！\n\n（請你告訴大本鳥那間廟叫什麼名字？）"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=1)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=3)
            elif event.message.text == "笨鳥來去理學院讀書囉":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥:理學院歷史淵遠流長，聽說早在日治時期便製作出亞洲第一台直線加速器，也進行了第一次的人工撞擊原子核實驗。這麼厲害的歷史文物，好像在校內物理文物廳還可以看到ㄟ!不過文物廳是幾號館來著?\n\n(請告訴大笨鳥文物廳是幾號館)"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=1)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=4)
            elif event.message.text == "笨鳥來去工學院讀書囉":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥:工學院有土木、化工、材料、醫療工程等各式各樣的系所，感覺都在跟複雜的點線面搏鬥，不過聽說有個系的系服竟然是極簡主義，令人「哭笑不得」?\n\n(請告訴大笨鳥這是哪個系的系服)"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=1)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=5)
            elif event.message.text == "笨鳥來去生農學院讀書囉":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥:生農學院是我很常去的地方，我都去找我的動物好朋友玩，不像你們的Customer都去買牛奶。不過說到農業，台大好像有個地方跟稻米有很深的淵源，甚至有座紀念小屋，那麼愛吃飯的你應該知道是誰吧?\n\n(請告訴大笨鳥小屋是紀念誰的?)"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=1)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=6)
            elif event.message.text == "回到主線":
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=-1) #退出支線
                return 0 
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請你帶這六隻笨鳥分別到文學院、社科院、管理學院、理學院、工學院、生農學院吧！當你準備好要送他們到該學院時，請你輸入「笨鳥來去XX院讀書囉」）\n\n如果要繼續主線請輸入「回到主線」"))
        elif user_info.side_part == 1:
            if (event.message.text == "印度黃檀樹" or event.message.text == "印度黃檀") and user_info.side_ques == 1:
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥：原來是印度黃檀。我後來去打聽，大棵的被移除了，但好像有他的分枝，小棵的長在前面，希望他能快快長大。也希望我能在文學院好好長大！"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/XZ9olPs.jpg",preview_image_url="https://i.imgur.com/XZ9olPs.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "梁國樹會議廳" and user_info.side_ques == 2:
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥：哇！竟然是個會議廳，我好喜歡這邊，希望之後趕快來修課！"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/EKkl7jL.jpg",preview_image_url="https://i.imgur.com/EKkl7jL.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "伯公亭" and user_info.side_ques == 3:
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥：土地公！土地公！請你保佑我接下來都能遇到好組員、好老師，不要遇到雷包。"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/iBq94OH.jpg",preview_image_url="https://i.imgur.com/iBq94OH.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "二號館" and user_info.side_ques == 4:
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥:不知道直線加速器能不能讓我飛得更快一點......"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/7U92dsK.jpg",preview_image_url="https://i.imgur.com/7U92dsK.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "機械系" and user_info.side_ques == 5:
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥: (阿這邊是要講什麼)"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/Xd3Sc3o.jpg",preview_image_url="https://i.imgur.com/Xd3Sc3o.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            elif event.message.text == "磯永吉" and user_info.side_ques == 6:
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("笨鳥:對對對就是他!我吃米雖不知道米價，但總要記得誰種出好吃的米。"))
                reply.append(ImageSendMessage(original_content_url="https://i.imgur.com/PRYHgM7.jpg",preview_image_url="https://i.imgur.com/PRYHgM7.jpg"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(side_part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(side_ques=0)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請你仔細觀察周邊環境，有必要時可以上網查詢"))

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
            elif user_info.section == 2:
                section2(event, User_Info)
            elif user_info.section == 3:
                section3(event, User_Info)
            elif user_info.section == 4:
                section4(event, User_Info)
            elif user_info.section == 5:
                if user_info.is_side and user_info.side_ques >= 0:
                    side_quest(event, User_Info)
                section5(event, User_Info)
            elif user_info.section == 6:
                if user_info.is_side and user_info.side_ques >= 0:
                    side_quest(event, User_Info)
                section6(event, User_Info)
            elif user_info.section == 7:
                if user_info.is_side and user_info.side_ques >= 0:
                    side_quest(event, User_Info)
                section7(event, User_Info)
            elif user_info.section == 8:
                if user_info.is_side and user_info.side_ques >= 0:
                    side_quest(event, User_Info)
                section8(event, User_Info)
        # print(user)
        file = open("ntubot/user.json", "w")
        json.dump(user, file)
        file.close()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
