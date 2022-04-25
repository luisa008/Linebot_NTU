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
            reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：我….我只是想吃蚯蚓而已….為什麼要這樣對我？什麼？你說你也不知道我在說什麼？但那明明就是你的腳踏車啊！！你真的不知道嗎？"))
            reply.append(TextSendMessage("（你如果不知道請輸入: 「我不知道」；如果假裝知道則輸入「我知道」）"))
            line_bot_api.reply_message(  # 回復傳入的訊息文字
                event.reply_token, reply)
        elif event.message.text == "我不知道":
            reply = [] #一次可傳多對話，至多五句
            reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那好吧，我就姑且相信你。但你要陪我一起找到兇手以及真相！"))
            reply.append(TextSendMessage("\U0001F469我：「但我肚子有點餓，我可以先吃飯嗎？」"))
            reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那就去大一女餐廳吧！快點吃一吃，幫我找到兇手！！！"))
            reply.append(TextSendMessage("到大一女餐廳後，請輸入：「我到大一女餐廳了」"))
            line_bot_api.reply_message(event.reply_token, reply)
            User_Info.objects.filter(uid=event.source.user_id).update(section=1)
        elif event.message.text == "我知道":
            reply = [] #一次可傳多對話，至多五句
            reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：你看起來就是一臉不知道，還說什麼知道，快點啦一起幫我找到兇手！"))
            reply.append(TextSendMessage("\U0001F469我：「但我肚子有點餓，我可以先吃飯嗎？」"))
            reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那就去大一女餐廳吧！快點吃一吃，幫我找到兇手！！！"))
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
                reply.append(TextSendMessage("\U0001F963路人Ａ：同學，我看你骨骼驚奇，是百年難得一見的解謎奇才，我看你八成正在為腳踏車不見而煩惱吧？"))
                reply.append(TextSendMessage("是的話，請回答：「大概是吧」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：快去大一女餐廳！"))
        elif user_info.part == 1:
            if event.message.text == "大概是吧":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F963路人Ａ：我的腳踏車已經被拖吊好多次，水源阿伯的電話我已經倒背如流！我現在出一道謎題，如果你猜中，我就告訴你阿伯的電話！"))
                reply.append(TextSendMessage("願意接受挑戰，請輸入「好吧」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=2)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答：「大概是吧」"))
        elif user_info.part == 2:
            if event.message.text == "好吧":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F963路人Ａ：這是厚宅的菜單，其中我最喜歡吃咖喱，仔細看裡面五道菜餚的價錢，每道菜的價錢對應到一個號碼，第一位跟最後一位號碼是１跟２，總共有五碼，然後這五碼就是水源阿伯的電話。ex: 111 -> 0, 104 -> 2"))
                reply.append(TextSendMessage("解出謎底後，請輸入五碼："))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=3)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請回答：「好吧」"))
        elif user_info.part == 3:
            if event.message.text == "12222":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F469我(打電話給水源阿伯)：阿伯你好，我找不到我的腳踏車，想請問我的腳踏車是不是被拖到水源去了？"))
                reply.append(TextSendMessage("\U0001F474水源阿伯：沒有啊，你的腳踏車不在我們這裡，你去駐警隊問問看？"))
                reply.append(TextSendMessage("到駐警隊後，請輸入：「我到駐警隊了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=2)
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
                reply.append(TextSendMessage("\U0001F46E警衛(一邊查監視器)：喔對了同學，最近一直有人來抱怨這附近有一棵「看起來很危險，會壓到兩個人」的樹，叫駐警隊處理，雖然維護校園安全是我們的工作範圍啦，可是講這麼模糊誰知道阿？你可以幫我調查一下是怎麼回事嗎？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("我現在應該要去駐警隊問吧? 請輸入：「我到駐警隊了」"))
        elif user_info.part == 1:
            if event.message.text == "朴樹":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F46E警衛：太感謝你了！剛好我這邊也調到影像了，你來看看是不是你的車子"))
                #放監視器圖片
                reply.append(TextSendMessage("\U0001F469我：原來舟山路是案發現場！"))
                reply.append(TextSendMessage("到舟山路後，請輸入「我到案發現場了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=3)
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
                reply.append(TextSendMessage("\U0001F9D0學生:明明這裡都有動物穿越減速慢行的路牌，那個人車還是騎得很快，結果撞死大笨鳥後就跑了，這已經不是第一次了。"))
                reply.append(TextSendMessage("\U0001F469我：那你有看到犯人壓到大笨鳥後去了哪裡嗎？"))
                reply.append(TextSendMessage("\U0001F9D0學生:好像有看到往哪裡去......，不過我在進行科普閱讀的推廣與實踐，你看起來是個聰明人，我把答案包裝成謎題，你自己去找尋答案吧，相信難不倒你。"))
                reply.append(TextSendMessage("「犯人的去向，路牌會『合力』告訴你。」"))
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
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section4(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到圖書館了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F469我：請問你剛剛有看到什麼可疑、匆忙的人衝進圖書館嗎？\n\U0001F4DA館員：沒有耶，我們的讀者都是很文雅的，沒有什麼人會用衝的進來，而且圖書館也不能奔跑喔！\n\U0001F469我：嗯…好吧"))
                reply.append(TextSendMessage("\U0001F4DA館員：啊，是說我好像有印象，有一個人整張臉皺成一團，看起來很緊張，褲子上沾滿一些紅色的汙漬。我就覺得很討厭呀！感覺就是剛去棒球場比完棒球或壘球，打輸了，但是好歹也把褲子上的紅土清理乾淨再進來吧？"))
                reply.append(TextSendMessage("\U0001F469我：那個人後來往哪邊走了？\n\U0001F4DA館員：他朝我方向走過來啊！他給我一張紙條，我拿來看，上面是一堆文字跟數字，他叫我幫他查這張紙代表的東西，我就罵他啊，我說這不是我要提供的服務\n\U0001F469我：所以那是什麼？\n\U0001F4DA館員：我可以直接把紙條送給你"))
                line_bot_api.reply_message(event.reply_token, reply)
                #紙條圖片
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：我們去圖書館! 請輸入「我到圖書館了」"))
        elif user_info.part == 1:
            if event.message.text == "報廢":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("(你不小心把書摔在地上，似乎有什麼東西掉出來…？)"))
                #書打開圖片
                #學生證圖片
                reply.append(TextSendMessage("撿起學生證後，發現他穿著某學院的領巾，於是我跑到兇手的系館找人。"))
                reply.append(TextSendMessage("到目的地後，請輸入「我到XX系系館了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=5)
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
                #資工系謎題圖片
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入「我到XX系系館了」"))
        elif user_info.part == 1:
            if event.message.text == "KC":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("我從第六排的窗戶內側拿到一本冊子，是紀錄兇手在資工系的生活"))
                #日記照片
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：那麼接下來去註冊組問問看，誰是這張學生證的主人吧！"))
                reply.append(TextSendMessage("請輸入換發學生證要去哪棟大樓"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=6)
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
                reply.append(TextSendMessage("\U0001F469我: 不好意思，我想問這個舊的學生證是誰的，後來換到哪個系了? 我強烈懷疑他偷了我的腳踏車，還輾過大笨鳥!"))
                reply.append(TextSendMessage("\U0001F170職員A: 這個資訊涉及個人隱私，不能隨便洩漏"))
                reply.append(TextSendMessage("\U0001F469我: 可是我已經去駐警隊報案了耶"))
                reply.append(TextSendMessage("\U0001F170職員A: 在警衛來確認之前都不行\n\U0001F469我: 大笨鳥，我們在學校跑來跑去還是得不到答案，還是乾脆去外面警察局報案算了...?\n\U0001F171職員B: (偷偷地)同學你看起來這麼聰明，一定知道傅鐘的歷史在「幾度」。那個A齁，常常找人問這些問題，裝的自己什麼都知道一樣，這次一定要剉剉他的銳氣。只要告訴我答案，我就去幫你查學生證。"))
                #資工系謎題圖片
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("如果真的不知道可以上網查喔"))
        elif user_info.part == 1:
            if event.message.text == "150" or event.message.text == "150度":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("職員B告訴我兇手姓名以及他後來轉到社科院，我接著在FB查詢，發現10分鐘前兇手在醉月湖打卡"))
                #打卡畫面
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：他在醉月湖！我們快追上去！"))
                reply.append(TextSendMessage("到醉月湖後，輸入「我到醉月湖了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=7)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

def section7(event, User_Info):
    user_info = User_Info.objects.get(uid=event.source.user_id)
    if isinstance(event, MessageEvent):
        #print(user_info.part)
        if user_info.part == 0:
            if event.message.text == "我到醉月湖了":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：你看！那台是你的腳踏車對吧?"))
                reply.append(TextSendMessage("(我發現腳踏車被丟進湖中，在裏頭載浮載沉。想要跳下湖中把腳踏車拿回來，但是湖邊的水深危險等標語迫使我打消念頭。這個時候發現湖旁有救生圈可以使用，拋救生圈套住腳踏車把它撈起來，但自己一個人實在很吃力)"))
                reply.append(TextSendMessage("此時，醉月湖中突然出現一隻鵝"))
                reply.append(TextSendMessage("\U0001F9A2鵝：請問你掉的腳踏車是哪一台腳踏車呢？「金色的」？「銀色的」？還是「被偷走的腳踏車」？"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=1)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F426大笨鳥的靈魂：我們快去醉月湖找他!"))
        elif user_info.part == 1:
            if event.message.text == "被偷走的腳踏車":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("\U0001F9A2鵝：好，看在你這麼誠實的份上，我就請小動物們都一起來幫助你！但是你要先記得醉月湖的「緊急數字」才能確保這次行動的安全！"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=2)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("\U0001F9A2鵝: 你確定嗎？ 誠實才會有好報喔！"))
        elif user_info.part == 2:
            if event.message.text == "27":
                reply = [] #一次可傳多對話，至多五句
                reply.append(TextSendMessage("（在小動物們的協助下，腳踏車成功被打撈出來）"))
                reply.append(TextSendMessage("（我開心的手舞足蹈，跟著動物一起跳I like to move it）"))
                reply.append(TextSendMessage("\U0001F9A2鵝：腳踏車之外，這是你誠實相告的額外獎勵！(拿出一張金色的紙條)"))
                #金色紙條圖片
                reply.append(TextSendMessage("犯人其實覺得很對不起，希望到只有文字的學院之樹找他"))
                reply.append(TextSendMessage("\U0001F469我：雖然拿到腳踏車了，但我們還是有必要知道真相！對吧大笨鳥？\n\U0001F426大笨鳥的靈魂：沒錯沒錯，走吧，學院之樹在社科院詩牆。\n據說社科院詩牆有這麼一首詩存在，到社科院詩牆後請輸入「我到詩牆了」"))
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=8)
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
                reply.append(TextSendMessage("\U0001F426大笨鳥的靈魂：可能是某個讓犯人心神不寧的句子吧？"))
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
                line_bot_api.reply_message(event.reply_token, reply)
                User_Info.objects.filter(uid=event.source.user_id).update(part=0)
                User_Info.objects.filter(uid=event.source.user_id).update(section=0) #玩完要重置嗎?
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage("想不出來可以請大笨鳥幫忙 請輸入「大笨鳥救救我」"))

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
                section5(event, User_Info)
            elif user_info.section == 6:
                section6(event, User_Info)
            elif user_info.section == 7:
                section7(event, User_Info)
            elif user_info.section == 8:
                section8(event, User_Info)
        # print(user)
        file = open("ntubot/user.json", "w")
        json.dump(user, file)
        file.close()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
