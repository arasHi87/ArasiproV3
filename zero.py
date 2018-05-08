#-*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse,timeit,data,atexit
from gtts import gTTS
from googletrans import Translator
botStart = time.time()
cl = LINE("tfcis20@gmail.com", "e27676271")
cl.log("Auth Token : " + str(cl.authToken))
kl = LINE("yukino0038@gmail.com", "e27676271")
kl.log("Auth Token : " + str(kl.authToken))
oepoll = OEPoll(cl)
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
read = json.load(readOpen)
settings = json.load(settingsOpen)
myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}
lineSettings = cl.getSettings()
clProfile = cl.getProfile()
clMID = cl.profile.mid
myProfile["displayName"] = clProfile.displayName
myProfile["statusMessage"] = clProfile.statusMessage
myProfile["pictureStatus"] = clProfile.pictureStatus
msg_dict = {}
bl = [""]
god = ['u85ee80cfb293599510d0c17ab25a5c98']
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def restartBot():
    print ("[ 訊息 ] 機器重啟")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
def logError(text):
    cl.log("[ 錯誤 ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """
    〘God指令〙
    【rebot】重新開機
    【killban】踢出黑單
    【cancel】取消群組邀請
    【tagall】標註全部人

    〘Admin指令〙
    【add_admin @】新增admin
    【del_admin @】刪除admin
    【add_gm @】新增gm
    【del_gm @】刪除gm
    【ban @】黑單某人
    【unban @】解除黑單某人
    【clearban】清空黑名單
    【yukino:bye】讓yukino退出群組
    【Fbc:】好友廣播
    【Gbc:】群組廣播
    【resetgroup】重新設定群組
    
    〘GM指令〙
    【add_wc:(歡迎訊息)】新增群組歡迎訊息
    【renew_wc:(歡迎訊息)】更新群組歡迎訊息
    【del_wc】刪除群組歡迎訊息
    【add on/off】自動加入好友 開/關
    【ar on/off】自動已讀 開/關
    【join on/off】自動入群 開/關
    【leave on /off】自動離開副本 開/關
    【contact on/off】查看好友詳細資料 開/關
    【inviteprotect on/off】邀請保護 開/關
    【protect on/off】群組保護 開/關
    【qr on/off】網址保護 開/關
    【reread on/off】查看收回 開/關
    【dm on/off】標註回復 開/關
    【ck on/off】查看貼圖詳細資料 開/關
    【curl】關閉群組網址
    【ourl】開啟群組網址

    〘Normal指令〙
    【help】查看設定
    【set】查看設定
    【test】查看運行
    【botlist】查看機器清單
    【adminlist】查看管理員清單
    【banlist】查看黑名單
    【reactlist】查看回復列表
    【runtime】查看運行時間
    【about】關於機器
    【MyMid】查看自己系統識別碼
    【MyName】查看自己名字
    【MyBio】查看自己個簽
    【MyPicture】查看自己頭貼網址
    【MyCover】查看自己封面網址
    【Contact @】標註查看好友資料
    【Mid @】標註查看系統識別碼
    【Name @】標註查看名稱
    【Bio @】標註查看狀態消息
    【Picture @】標註查看頭貼
    【Cover @】標注查看封面
    【Gowner】查看群組擁有者
    【Gurl】丟出群組網址
    【ginfo】查看群組詳情
    【gb】查看群組成員
    【lg】查看所有群組
    【status】查看自身狀態
    【add_react:(關鍵字):(回應)】新增關鍵字回應
    【del_react:(關鍵字):(回應)】刪除關鍵字回應
    【renew_react:(關鍵字):(回應)】更新關鍵字回應
    【add_sr:(貼圖id):(貼圖包id)】新增貼圖回應
    【renew_sr:(貼圖id):(貼圖包id))】更新貼圖回應
    【del_sr:(貼圖id):(貼圖包id)】刪除貼圖回應
    【sn】設立以讀點
    【sf】關閉已讀點
    【sr】更新已讀點
    【r】查看當前已讀
    ⇒Credits By.Arasi™⇐"""
    return helpMessage
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(op.param1)
            print ("[ 5 ] 通知添加好友 名字: " + contact.displayName)
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                cl.sendMessage(op.param1, "安安！{} 感謝您加我為好友！".format(str(contact.displayName)))
                cl.sendMessage(op.param1, "咱是由Arasi所開發的ArasiproV3\n歡迎邀請我加入群組喔!!!!\n如有問題請麻煩私訊作者")
                cl.sendContact(op.param1, "u85ee80cfb293599510d0c17ab25a5c98")
        if op.type == 24:
            print ("[ 24 ] 通知離開副本")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 1:
            print ("[1]更新配置文件")
        if op.type == 11:
            group = cl.getGroup(op.param1)
            if op.param1 not in settings["qrprotect"]:
                if op.param2 in settings['admin'] and op.param2 in settings['bot'] and op.param2 not in settings['gm'][op.param1]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
                    invsend = 0
                    cl.sendMessage(op.param1,cl.getContact(op.param2).displayName + "你沒有權限觸碰網址!")
                    try:
                        kl.kickoutFromGroup(op.param1,[op.param2])
                    except:
                        cl.kickoutFromGroup(op.param1,[op.param2])
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            GS = group.creator.mid
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if clMID in op.param3:
                if settings["autoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1, "歡迎使用由Arasi開發的ArasiproV3!!!\nMy creator:")
                    cl.sendContact(op.param1, "u85ee80cfb293599510d0c17ab25a5c98")
                    if group.preventedJoinByTicket == True:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                    else:
                        pass
                    ticket = cl.reissueGroupTicket(op.param1)
                    kl.acceptGroupInvitationByTicket(op.param1, ticket)
                    group.preventedJoinByTicket = True
                    cl.updateGroup(group)
                    try:
                        if op.param1 not in settings['gm']:
                            settings['gm'][op.param1] = {}
                        if GS not in settings['gm'][op.param1]:
                            settings['gm'][op.param1][GS] = GS
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(op.param1, "設置GM權限成功")
                        if GS in settings['gm'][op.param1]:
                            cl.sendMessage(op.param1, "本群GM為:")
                            cl.sendContact(op.param1, GS)
                    except:
                        cl.sendMessage(op.param1, "[ERROR]\n設置GM權限失敗!!!!\n請尋找作者幫忙")
                        cl.sendContact(op.param1, "u85ee80cfb293599510d0c17ab25a5c98")
            elif op.param1 not in settings["inviteprotect"]:
                if op.param2 not in settings['admin'] and op.param2 not in settings['bot'] and op.param2 not in settings['gm'][op.param1]:
                    cl.sendMessage(op.param1, "群組邀請保護開啟中!!!!")
                    kl.cancelGroupInvitation(op.param1, [op.param3])
                    try:
                        settings['blacklist'][op.param2] = True
                        with open('temp.json', 'w') as fp:
                            json.dump(settings, fp, sort_keys=True, indent=4)
                        cl.sendMessage(op.param1, "成功新增黑單")
                        cl.sendContact(op.param1, op.param2)
                    except:
                        cl.sendMessage(op.param1, "[ERROR]\n新增黑單失敗")
            else:
                if op.param3 in settings['blacklist']:
                    kl.cancelGroupInvitation(op.param1, [op.param3])
                    cl.sendMessage(op.param1, "[警告]\n邀請名單位於黑單中")
                    cl.sendContact(op.param1, op.param3)
                elif op.param2 in settings['blacklist']:
                    kl.cancelGroupInvitation(op.param1, [op.param3])
                    cl.sendMessage(op.param1, "[警告]\n你位於黑名單中並不能邀請人員")
                    cl.sendContact(op.param1, op.param3)
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) +"\n踢人者: " + contact1.displayName + "\nMid: " + contact1.mid + "\n被踢者" + contact2.displayName + "\nMid:" + contact2.mid )
            if op.param1 not in settings["protect"]:
                if op.param2 in settings['admin'] or op.param2 in settings['bot'] or op.param2 in settings['gm'][op.param1]:
                    pass
                else:
                    try:
                        kl.kickoutFromGroup(op.param1,[op.param2])
                    except:
                        cl.kickoutFromGroup(op.param1,[op.param2])
                    if op.param3 in settings['bot']:
                        if group.preventedJoinByTicket == True:
                            group.preventedJoinByTicket = False
                        try:
                            ticket = kl.reissueGroupTicket(op.param1)
                            kl.updateGroup(group)
                            cl.acceptGroupInvitationByTicket(op.param1, ticket)
                        except:
                            ticket = cl.reissueGroupTicket(op.param1)
                            cl.updateGroup(group)
                            kl.acceptGroupInvitationByTicket(op.param1, ticket)
                        settings["blacklist"][op.param2] = True
                        with open('temp.json', 'w') as fp:
                            json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(op.param1, "成功新增blacklist\n" + "MID : " + op.param2)
                            cl.sendContact(op.param1, op.param2)
                        group.preventedJoinByTicket = True
                        cl.updateGroup(group)
        if op.type == 60:
            if op.param2 in settings['blacklist']:
                cl.sendMessage(op.param1, "[警告]\n此人位於黑名單中! ! !")
            else:
                if op.param2 not in settings['bot']:
                    if op.param1 not in settings['wel']:
                        try:
                            arrData = ""
                            text = "%s " %('你好~~')
                            arr = []
                            mention = "@x "
                            slen = str(len(text))
                            elen = str(len(text) + len(mention) - 1)
                            arrData = {'S':slen, 'E':elen, 'M':op.param2}
                            arr.append(arrData)
                            text += mention + '!!歡迎加入群組!!!!'
                            cl.sendMessage(op.param1,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                        except Exception as error:
                            print(error)
                    else:
                        cl.sendMessage(op.param1, settings['wel'][op.param1])
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg._from in settings['blacklist']:
                return
            if msg.contentType == 13:
                if settings["contact"] == True:
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[名稱]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[個簽]:\n" + contact.statusMessage + "\n[頭貼網址]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面網址]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                            cl.sendMessage(msg.to,"[名稱]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[個簽]:\n" + contact.statusMessage + "\n[頭貼網址]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面網址]:\n" + str(cu))
            elif msg.contentType == 7:
                stk_id = msg.contentMetadata['STKID']
                stk_ver = msg.contentMetadata['STKVER']
                pkg_id = msg.contentMetadata['STKPKGID']
                number = str(stk_id) + str(pkg_id)
                if sender in settings['limit']:
                    if number in settings['limit'][sender]['stick']:
                        if settings ['limit'][sender]['stick'][number] >= 3:
                            settings ['limit'][sender]['stick']['react'] = False
                        else:
                            settings ['limit'][sender]['stick'][number] += 1
                            settings ['limit'][sender]['stick']['react'] = True
                    else:
                        try:
                            del settings['limit'][sender]['stick']
                        except:
                            pass
                        settings['limit'][sender]['stick'] = {}
                        settings['limit'][sender]['stick'][number] = 1
                        settings['limit'][sender]['stick']['react'] = True
                else:
                    settings['limit'][sender] = {}
                    settings['limit'][sender]['stick'] = {}
                    settings['limit'][sender]['text'] = {}
                    settings['limit'][sender]['stick'][number] = 1
                    settings['limit'][sender]['stick']['react'] = True
                if settings['limit'][sender]['stick']['react'] == False:
                    return
                if to in settings['cc']:
                    command = "->add_sr:" + format(stk_id) + ":" + format(pkg_id) + ":"
                    cl.sendMessage(to, command)
                elif to in settings["checkSticker"]:
                    ret_ = "<<貼圖資料>>"
                    ret_ += "\n[貼圖ID] : {}".format(stk_id)
                    ret_ += "\n[貼圖包ID] : {}".format(pkg_id)
                    ret_ += "\n[貼圖網址] : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n[貼圖圖片網址]：https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png;compress=true".format(stk_id)
                    ret_ += "\n<<完>>"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                    cl.sendMessage(op.param1,ret_)
                    cl.sendMessage(to, command)
                elif number in settings['sr']:
                    react = settings['sr'][number]
                    cl.sendMessage(to, str(react))
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    try:
                        msg.contentType = 0
                        f_mid = msg.contentMetadata["postEndUrl"].split("userMid=")
                        s_mid = f_mid[1].split("&")
                        mid = s_mid[0]
                        try:
                            arrData = ""
                            text = "%s " %("[文章持有者]\n")
                            arr = []
                            mention = "@x "
                            slen = str(len(text))
                            elen = str(len(text) + len(mention) - 1)
                            arrData = {'S':slen, 'E':elen, 'M':mid}
                            arr.append(arrData)
                            text += mention + "\n[文章預覽]\n(僅提供100字內容)\n " + msg.contentMetadata["text"] + "\n[文章網址]\n " + msg.contentMetadata["postEndUrl"]
                            cl.sendMessage(msg.to,text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                        except Exception as error:
                            print(error)
                    except:
                        ret_ = "\n[文章預覽]\n(僅提供100字內容)\n " + msg.contentMetadata["text"]
                        ret_ += "\n[文章網址]\n " + msg.contentMetadata["postEndUrl"]
                        cl.sendMessage(msg.to, ret_)
            if msg.contentType == 0:
                if text is None:
                    return
                if sender in settings['limit']:
                    if msg.text in settings['limit'][sender]['text']:
                        if settings ['limit'][sender]['text'][msg.text] >= 3:
                            settings ['limit'][sender]['text']['react'] = False
                        else:
                            settings ['limit'][sender]['text'][msg.text] += 1
                            settings ['limit'][sender]['text']['react'] = True
                    else:
                        try:
                            del settings['limit'][sender]['text']
                        except:
                            pass
                        settings['limit'][sender]['text'] = {}
                        settings['limit'][sender]['text'][msg.text] = 1
                        settings['limit'][sender]['text']['react'] = True
                else:
                    settings['limit'][sender] = {}
                    settings['limit'][sender]['stick'] = {}
                    settings['limit'][sender]['text'] = {}
                    settings['limit'][sender]['text'][msg.text] = 1
                    settings['limit'][sender]['text']['react'] = True
                if settings['limit'][sender]['text']['react'] == True:
                    if sender in god:
                        if msg.text in ["cancel"]:
                            if msg.toType == 2:
                                X = cl.getGroup(msg.to)
                                if X.invitee is not None:
                                    gInviMids = (contact.mid for contact in X.invitee)
                                    ginfo = cl.getGroup(msg.to)
                                    sinvitee = str(len(ginfo.invitee))
                                    start = time.time()
                                    for cancelmod in gInviMids:
                                        cl.cancelGroupInvitation(msg.to, [cancelmod])
                                    elapsed_time = time.time() - start
                                    cl.sendMessage(to, "已取消完成\n取消時間: %s秒" % (elapsed_time))
                                    cl.sendMessage(to, "取消人數:" + sinvitee)
                        elif msg.text in ["killban"]:
                            if msg.toType == 2:
                                group = cl.getGroup(to)
                                gMembMids = [contact.mid for contact in group.members]
                                matched_list = []
                                for tag in settings["blacklist"]:
                                    matched_list+=filter(lambda str: str == tag, gMembMids)
                                if matched_list == []:
                                    print ("1")
                                    cl.sendMessage(to, "沒有黑名單")
                                    return
                                for jj in matched_list:
                                    cl.kickoutFromGroup(to, [jj])
                                    cl.sendMessage(to, "黑名單以踢除")
                        elif text.lower() == 'tagall':
                            group = cl.getGroup(msg.to)
                            nama = [contact.mid for contact in group.members]
                            k = len(nama)//100
                            for a in range(k+1):
                                txt = u''
                                s=0
                                b=[]
                                for i in group.members[a*100 : (a+1)*100]:
                                    b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                                    s += 7
                                    txt += u'@Alin \n'
                                cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                                cl.sendMessage(to, "總共 {} 個成員".format(str(len(nama))))
                        elif text.lower() == 'rebot':
                            cl.sendMessage(to, "重新啟動中......")
                            restartBot()
                    if sender in settings['admin'] or sender in god:
                        if msg.text.lower().startswith("add_admin "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    if ls not in settings['admin']:
                                        settings['admin'][ls] = True
                                        with open('temp.json', 'w') as fp:
                                            json.dump(settings, fp, sort_keys=True, indent=4)
                                            cl.sendMessage(to, "成功新增Admin權限")
                                            cl.sendContact(to, ls)
                                    else:
                                        cl.sendMessage(to, "此人已擁有Admin權限")
                        elif msg.text.lower().startswith("del_admin "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    if ls in settings['admin']:
                                        del settings['admin'][ls]
                                        with open('temp.json', 'w') as fp:
                                            json.dump(settings, fp, sort_keys=True, indent=4)
                                            cl.sendMessage(to, "成功移除Admin權限")
                                            cl.sendContact(to, ls)
                                    else:
                                        cl.sendMessage(to, "此人並未擁有Admin權限")
                        elif "Ban" in msg.text:
                            if msg.toType == 2:
                                print ("[Ban] 成功")
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                targets = []
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                if targets == []:
                                    pass
                                else:
                                    for target in targets:
                                        try:
                                            settings["blacklist"][target] = True
                                            with open('temp.json', 'w') as fp:
                                                json.dump(settings, fp, sort_keys=True, indent=4)
                                                cl.sendMessage(to, "已加入黑名單")
                                        except:
                                            pass
                        elif "Unban" in msg.text:
                            if msg.toType == 2:
                                print ("[UnBan] 成功")
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                targets = []
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                if targets == []:
                                    pass
                                else:
                                    for target in targets:
                                        try:
                                            del settings["blacklist"][target]
                                            with open('temp.json', 'w') as fp:
                                                json.dump(settings, fp, sort_keys=True, indent=4)
                                                cl.sendMessage(to, "已解除黑名單")
                                        except:
                                            pass
                        elif text.lower() == 'clear ban':
                            for mi_d in settings["blacklist"]:
                                settings["blacklist"] = {}
                                cl.sendMessage(to, "已清空黑名單")
                        elif msg.text.lower().startswith("fbc:"):
                            bctxt = text.replace("fbc:","")
                            t = cl.getAllContactIds()
                            for manusia in t:
                                cl.sendMessage(manusia,"[好友廣播]\n"+bctxt)
                        elif msg.text.lower().startswith("gbc:"):
                            bctxt = text.replace("gbc:","")
                            n = cl.getGroupIdsJoined()
                            for manusia in n:
                                cl.sendMessage(manusia,"[群組廣播]\n"+bctxt)
                        elif msg.text.lower() == 'resetgroup':
                            group = cl.getGroup(to)
                            GS = group.creator.mid
                            cl.sendMessage(to, "[警告]\n開始重新設定群組!!!")
                            try:
                                if to in settings['protect']:
                                    del settings['protect'][to]
                                if to in settings['inviteprotect']:
                                    del settings['inviteprotect'][to]
                                if to in settings['qrprotect']:
                                    del settings['qrprotect'][to]
                                if to in settings['reread']:
                                    del settings['reread'][to]
                                if to in settings['checkSticker']:
                                    del settings['checkSticker'][to]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[警告]\n刪除群組設定成功")
                            except:
                                cl.sendMessage(to, "[ERROR]\n刪除群組設定失敗")
                            try:
                                if to in settings['gm']:
                                    del settings['gm'][to]
                                    with open('temp.json', 'w') as fp:
                                        json.dump(settings, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[警告]\n刪除群組GM成功")
                            except:
                                cl.sendMessage(to, "[ERROR]\n刪除群組GM失敗")
                            cl.sendMessage(to, "[警告]\n開始重新設定群組GM")
                            try:
                                settings['gm'][to] = {}
                                settings['gm'][to][GS] = GS
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "[警告]\n設定群組GM成功\n群組GM為:")
                                cl.sendContact(to, GS)
                            except:
                                cl.sendMessage(to, "[ERROR]\n設定群組GM失敗")
                            cl.sendMessage(to, "重新設定群組完成如有錯誤請私訊作者!!!")
                    if sender in settings['gm'][to] or sender in settings['admin'] or sender in god:
                        if msg.text.lower().startswith("add_gm "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    if to not in settings['gm']:
                                        settigs['gm'][to] = {}
                                    if ls not in settings['gm'][to]:
                                        settings['gm'][to][ls] = ls
                                        with open('temp.json', 'w') as fp:
                                            json.dump(settings, fp, sort_keys=True, indent=4)
                                            cl.sendMessage(to, "成功新增GM權限")
                                            cl.sendContact(to, ls)
                                    else:
                                        cl.sendMessage(to, "此人已擁有GM權限")
                        elif msg.text.lower().startswith("del_gm "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    if ls in settings['gm'][to][ls]:
                                        try:
                                            del settings['gm'][to][ls]
                                            with open('temp.json', 'w') as fp:
                                                json.dump(settings, fp, sort_keys=True, indent=4)
                                                cl.sendMessage(to, "成功刪除Group Master權限")
                                        except:
                                            cl.sendMessage(to, "[ERROR]\n刪除Group Master權限失敗")
                                    else:
                                        cl.sendMessage(to, "[ERROR]\n此人並未擁有Group Master權限")
                        elif msg.text.lower().startswith("add_wc"):
                            list_ = msg.text.split(":")
                            if to not in settings['wel']:
                                try:
                                    settings['wel'][to] = list_[1]
                                    with open('temp.json', 'w') as fp:
                                        json.dump(settings, fp, sort_keys=True, indent=4)
                                        cl.sendMessage(to, "[提示]\n成功設置群組歡迎訊息\n歡迎訊息: " + list_[1])
                                except:
                                    cl.sendMessage(to, "[ERROR]\n設置群組歡迎訊息失敗!!!")
                            else:
                                cl.sendMessage(to, "[ERROR]\n群組歡迎訊息已存在!!!")
                        elif msg.text.lower().startswith("renew_wc"):
                            list_ = msg.text.split(":")
                            if to in settings['wel']:
                                try:
                                    del settings['wel'][to]
                                    settings['wel'][to] = list_[1]
                                    with open('temp.json', 'w') as fp:
                                        json.dump(settings, fp, sort_keys=True, indent=4)
                                        cl.sendMessage(to, "[提示]\n成功更新群組歡迎訊息\n歡迎訊息: " + list_[1])
                                except:
                                    cl.sendMessage(to, "[ERROR]\n更新群組歡迎訊息失敗!!!")
                            else:
                                cl.sendMessage(to, "[ERROR]\n你正在更新不存在的歡迎訊息!!!")
                        elif text.lower() == ("del_wc"):
                            if to in settings['wel']:
                                try:
                                    del settings['wel'][to]
                                    with open('temp.json', 'w') as fp:
                                        json.dump(settings, fp, sort_keys=True, indent=4)
                                        cl.sendMessage(to, "[提示]\n成功刪除群組歡迎訊息")
                                except:
                                    cl.sendMessage(to, "[ERROR]\n刪除群組歡迎訊息失敗!!!")
                            else:
                                cl.sendMessage(to, "[ERROR]\n你正在刪除不存在的歡迎訊息!!!")
                        elif text.lower() == 'wc':
                            if to in settings['wel']:
                                cl.sendMessage(to, settings['wel'][to])
                            else:
                                cl.sendMessage(to, "[提示]\n使用預設群組歡迎訊息中!!!")
                        elif text.lower() == 'yukino:bye':
                            if msg.toType == 2:
                                ginfo = cl.getGroup(to)
                                try:
                                    cl.sendMessage(to, "各位掰掰~")
                                    cl.leaveGroup(to)
                                    kl.leaveGroup(to)
                                    del settings['protect'][op.param1]
                                    del settings['inviteprotect'][op.param1]
                                    del settings['qrprotect'][op.param1]
                                    with open('temp.json', 'w') as fp:
                                        json.dump(settings, fp, sort_keys=True, indent=4)
                                except:
                                    pass
                        elif text.lower() == 'add on':
                            settings["autoAdd"] = True
                            cl.sendMessage(to, "自動加入好友已開啟")
                        elif text.lower() == 'add off':
                            settings["autoAdd"] = False
                            cl.sendMessage(to, "自動加入好友已關閉")
                        elif text.lower() == 'ar on':
                            settings["autoRead"] = True
                            cl.sendMessage(to, "自動已讀已開啟")
                        elif text.lower() == 'ar off':
                            settings["autoRead"] = False
                            cl.sendMessage(to, "自動已讀已關閉")
                        elif text.lower() == 'join on':
                            settings["autoJoin"] = True
                            cl.sendMessage(to, "自動加入群組已開啟")
                        elif text.lower() == 'join off':
                            settings["autoJoin"] = False
                            cl.sendMessage(to, "自動加入群組已關閉")
                        elif text.lower() == 'leave on':
                            settings["autoLeave"] = True
                            cl.sendMessage(to, "自動離開副本已開啟")
                        elif text.lower() == 'leave off':
                            settings["autoLeave"] = False
                            cl.sendMessage(to, "自動離開副本已關閉")
                        elif text.lower() == 'contact on':
                            settings["contact"] = True
                            cl.sendMessage(to, "查看好友資料詳情開啟")
                        elif text.lower() == 'contact off':
                            settings["contact"] = False
                            cl.sendMessage(to, "查看好友資料詳情關閉")
                        elif text.lower() == 'inviteprotect on':
                            if to in settings["inviteprotect"]:
                                del settings["inviteprotect"][to]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "群組邀請保護已開啟")
                        elif text.lower() == 'inviteprotect off':
                            settings["inviteprotect"][to] = to
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "群組邀請保護已關閉")
                        elif text.lower() == 'protect on':
                            if to in settings['protect']:
                                del settings["protect"][to]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "群組保護已開啟")
                        elif text.lower() == 'protect off':
                            settings["protect"][to] = to
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "群組保護已關閉")
                        elif text.lower() == 'qr on':
                            if to in settings['qrprotect']:
                                del settings["qrprotect"][to]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "群組網址保護已開啟")
                        elif text.lower() == 'qr off':
                            settings["qrprotect"][to] = to
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "群組網址保護已關閉")
                        elif text.lower() == 'reread on':
                            if to in settings["reread"][to]:
                                del settings["reread"][to]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "查詢收回開啟")
                        elif text.lower() == 'reread off':
                            settings["reread"][to] = to
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "查詢收回關閉")
                        elif text.lower() == 'dm on':
                            settings["detectMention"] = True
                            cl.sendMessage(to, "自動回應開啟")
                        elif text.lower() == 'dm off':
                            settings["detectMention"] = False
                            cl.sendMessage(to, "自動回應關閉")
                        elif text.lower() == 'ck on':
                            settings["checkSticker"][to] = True
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "確認貼圖開啟")
                        elif text.lower() == 'ck off':
                            del settings["checkSticker"][to]
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                            cl.sendMessage(to, "確認貼圖關閉")
                        elif text.lower() == 'cc on':
                            settings['cc'][to] = True
                            cl.sendMessage(to, "生成貼圖指令開啟")
                        elif text.lower() == 'cc off':
                            del settings['cc'][to]
                            cl.sendMessage(to, "生成貼圖指令關閉")
                        elif text.lower() == 'ourl':
                            if msg.toType == 2:
                                G = cl.getGroup(to)
                                if G.preventedJoinByTicket == False:
                                    cl.sendMessage(to, "群組網址已開啟")
                                else:
                                    G.preventedJoinByTicket = False
                                    cl.updateGroup(G)
                                    cl.sendMessage(to, "成功開啟群組網址")
                        elif text.lower() == 'curl':
                            if msg.toType == 2:
                                G = cl.getGroup(to)
                                if G.preventedJoinByTicket == True:
                                    cl.sendMessage(to, "群組網址已關閉")
                                else:
                                    G.preventedJoinByTicket = True
                                    cl.updateGroup(G)
                                    cl.sendMessage(to, "成功關閉群組網址")
                    if msg.text in settings['react']:
                        cl.sendMessage(to, settings['react'][msg.text])
                    if text.lower() == 'speed':
                        start = time.time()
                        cl.sendMessage(to, "processing......")
                        elapsed_time = time.time() - start
                        cl.sendMessage(to,format(str(elapsed_time)) + "秒")    
                    elif text.lower() == 'set':
                        try:
                            ret_ = "[ 設定 ]"
                            if settings["autoAdd"] == True: ret_ += "\n自動加入好友 [ON]"
                            else: ret_ += "\n自動加入好友 [OFF]"
                            if settings["autoJoin"] == True: ret_ += "\n自動加入群組 [ON]"
                            else: ret_ += "\n自動加入群組 [OFF]"
                            if settings["autoLeave"] == True: ret_ += "\n自動離開副本 [ON]"
                            else: ret_ += "\n自動離開副本 [OFF]"
                            if settings["autoRead"] == True: ret_ += "\n自動已讀 [ON]"
                            else: ret_ += "\n自動已讀 [OFF]"
                            if to not in settings["protect"]: ret_ += "\n群組保護開啟 [ON]"
                            else: ret_ += "\n群組保護關閉 [OFF]"
                            if to not in settings["inviteprotect"]: ret_ += "\n群組邀請保護 [ON]"
                            else: ret_ += "\n群組邀請保護 [OFF]"
                            if to not in settings["qrprotect"]: ret_ += "\n群組網址保護 [ON]"
                            else: ret_ += "\n群組網址保護 [OFF]"
                            if settings["contact"] == True: ret_ += "\n詳細資料 [ON]"
                            else: ret_ += "\n詳細資料 [OFF]"
                            if to not in settings["reread"]: ret_ += "\n查詢收回 [ON]"
                            else: ret_ += "\n查詢收回 [OFF]"
                            if settings["detectMention"] == True: ret_ += "\n標註回覆 [ON]"
                            else: ret_ += "\n標註回覆 [OFF]"
                            if to in  settings["checkSticker"]: ret_ += "\n貼圖資料查詢 [ON]"
                            else: ret_ += "\n貼圖資料查詢 [OFF]"
                            if to in settings['cc']: ret_ += "\n生成貼圖指令 [ON]"
                            else: ret_ += "\n生成貼圖指令 [OFF]"
                            cl.sendMessage(to, str(ret_))
                        except Exception as e:
                            cl.sendMessage(msg.to, str(e))
                    if text.lower() == 'help':
                            helpMessage = helpmessage()
                            cl.sendMessage(to, str(helpMessage))
                            cl.sendMessage(to, "我的作者")
                            cl.sendContact(to, "u85ee80cfb293599510d0c17ab25a5c98")
                    elif text.lower() == 'test':
                        cl.sendMessage(to, "運行中......")
                        kl.sendMessage(to, "運行中......")
                    elif text.lower() == 'botlist':
                        if settings["bot"] == {}:
                            cl.sendMessage(to, "沒有機器名單")
                        else:
                            try:
                                mc = "[ 機器名單 ]\n"
                                for mi_d in settings["bot"]:
                                    mc += "-> " + cl.getContact(mi_d).displayName + "\n"
                                cl.sendMessage(to, mc)
                            except:
                                pass
                    elif text.lower() == 'adminlist':
                        if settings["admin"] == {}:
                            cl.sendMessage(to, "沒有管理員名單")
                        else:
                            try:
                                mc = "[ 管理員名單 ]\n"
                                for mi_d in settings["admin"]:
                                    mc += "-> " + cl.getContact(mi_d).displayName + "\n"
                                cl.sendMessage(to, mc)
                            except:
                                cl.sendMessage(to, "error")
                    elif text.lower() == 'banlist':
                        if settings["blacklist"] == {}:
                            cl.sendMessage(to, "沒有黑名單")
                        else:
                            try:
                                mc = "[ 黑名單 ]\n"
                                for mi_d in settings["blacklist"]:
                                    mc += "-> " + cl.getContact(mi_d).displayName + "\n"
                                cl.sendMessage(to, mc)
                            except:
                                pass
                    elif text.lower() == 'reactlist':
                        ret_ = "[關鍵字列表]\n"
                        for name in settings['react']:
                            ret_ +="->" + name + "\n"
                        cl.sendMessage(to, ret_)
                    elif text.lower() == 'gmlist':
                        if settings["gm"][to] == {}:
                                cl.sendMessage(to, "沒有Group Master名單")
                        else:
                            try:
                                mc = "[ GM名單 ]\n"
                                for mi_d in settings["gm"][to]:
                                    mc += "-> " + cl.getContact(mi_d).displayName + "\n"
                                cl.sendMessage(to, mc)
                            except:
                                pass
                    elif text.lower() == 'runtime':
                        timeNow = time.time()
                        runtime = timeNow - botStart
                        runtime = format_timespan(runtime)
                        cl.sendMessage(to, "機器運行時間 {}".format(str(runtime)))
                    elif text.lower() == 'about':
                        try:
                            arr = []
                            owner = "u85ee80cfb293599510d0c17ab25a5c98"
                            creator = cl.getContact(owner)
                            contact = cl.getContact(clMID)
                            group = cl.getGroup(to)
                            contactlist = cl.getAllContactIds()
                            blockedlist = cl.getBlockedContactIds()
                            ret_ = "<<利用情報>>"
                            ret_ += "\n[私の名前は] : {}".format(contact.displayName)
                            ret_ += "\n[グループ名] : {}".format(str(group.name))
                            ret_ += "\n[現在のバージョン]: alpha v1.0.0"
                            ret_ += "\n[作成者] : {}".format(creator.displayName)
                            ret_ += "\n[URLを追加] : http://line.naver.jp/ti/p/~ee27676271"
                            cl.sendMessage(to, str(ret_))
                        except Exception as e:
                            cl.sendMessage(msg.to, str(e))
                    elif text.lower() == 'mymid':
                        cl.sendMessage(msg.to,"[MID]\n" +  sender)
                    elif text.lower() == 'myname':
                        me = cl.getContact(sender)
                        cl.sendMessage(msg.to,"[顯示名稱]\n" + me.displayName)
                    elif text.lower() == 'mybio':
                        me = cl.getContact(sender)
                        cl.sendMessage(msg.to,"[狀態消息]\n" + me.statusMessage)
                    elif text.lower() == 'mypicture':
                        me = cl.getContact(sender)
                        cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                    elif text.lower() == 'mycover':
                        me = cl.getContact(sender)
                        cover = cl.getProfileCoverURL(sender)
                        cl.sendImageWithURL(msg.to, cover)
                    elif msg.text.lower().startswith("mid "):
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            ret_ = ""
                            for ls in lists:
                                ret_ += "" + ls
                            cl.sendMessage(msg.to, str(ret_))
                    elif msg.text.lower().startswith("bio "):
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                contact = cl.getContact(ls)
                                cl.sendMessage(msg.to, "[ 狀態消息 ]\n{}" + contact.statusMessage)
                    elif msg.text.lower().startswith("picture "):
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = "http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus
                                cl.sendImageWithURL(msg.to, str(path))
                    elif msg.text.lower().startswith("cover "):
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = cl.getProfileCoverURL(ls)
                                    cl.sendImageWithURL(msg.to, str(path))
                    elif text.lower() == 'gowner':
                        group = cl.getGroup(to)
                        GS = group.creator.mid
                        cl.sendContact(to, GS)
                    elif text.lower() == 'gid':
                        gid = cl.getGroup(to)
                        cl.sendMessage(to, "[群組ID : ]\n" + gid.id)
                    elif text.lower() == 'gurl':
                        if msg.toType == 2:
                            group = cl.getGroup(to)
                            if group.preventedJoinByTicket == False:
                                ticket = cl.reissueGroupTicket(to)
                                cl.sendMessage(to, "[ 群組網址 ]\nhttp://line.me/R/ti/g/{}".format(str(ticket)))
                            else:
                                cl.sendMessage(to, "群組網址未開啟".format(str(settings["keyCommand"])))
                    elif text.lower() == 'ginfo':
                        group = cl.getGroup(to)
                        try:
                            gCreator = group.creator.displayName
                        except:
                            gCreator = "未找到"
                        if group.invitee is None:
                            gPending = "0"
                        else:
                            gPending = str(len(group.invitee))
                        if group.preventedJoinByTicket == True:
                            gQr = "關閉"
                            gTicket = "沒有"
                        else:
                            gQr = "開啟"
                            gTicket = "http://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                        path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                        ret_ = "╔══[ 群組資料 ]"
                        ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                        ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                        ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                        ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                        ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                        ret_ += "\n╠ 群組網址 : {}".format(gQr)
                        ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                        ret_ += "\n╚══[ 完 ]"
                        cl.sendMessage(to, str(ret_))
                        cl.sendImageWithURL(to, path)
                    elif text.lower() == 'gb':
                        if msg.toType == 2:
                            group = cl.getGroup(to)
                            ret_ = "╔══[ 成員列表 ]"
                            no = 0 + 1
                            for mem in group.members:
                                ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                                no += 1
                            ret_ += "\n╚══[ 總共： {} ]".format(str(len(group.members)))
                            cl.sendMessage(to, str(ret_))
                    elif text.lower() == 'lg':
                        groups = cl.groups
                        ret_ = "[群組列表]"
                        no = 0 + 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n[總共 {} 個群組]".format(str(len(groups)))
                        cl.sendMessage(to, str(ret_))
                    elif text.lower() == 'status':
                        contact = cl.getContact(sender)
                        ret_ = "[使用者狀態]\n"
                        ret_ += '使用者名稱 => ' + contact.displayName + "\n"
                        if sender in god:
                            ret_ += '使用者權限 => ' + 'God mod\n'
                            ret_ += '使用者限制 => ' + '無限制\n'
                            ret_ += '指令權限 => ' + 'All usefull'
                        elif sender in settings['admin']:
                            ret_ += '使用者權限 => ' + 'Admin\n'
                            ret_ += '使用者限制 => ' + '無限制\n'
                            ret_ += '指令權限 => ' + 'All without revoke'
                        elif sender in settings['blacklist']:
                            ret_ += '使用者權限 => ' + 'Blacklist\n'
                            ret_ += '使用者限制 => ' + '全功能制限\n'
                            ret_ += '指令權限 => ' + 'All useless\n'
                        else:
                            ret_ += '使用者權限 => ' + 'Normal\n'
                            ret_ += '使用者限制 => ' + '普通限制\n'
                            ret_ += '指令權限 => ' + 'Only normal\n'
                        cl.sendMessage(to, ret_)
                    elif msg.text.lower().startswith("add_react"):
                        list_ = msg.text.split(":")
                        if list_[1] not in settings['react']:
                            try:
                                settings['react'][list_[1]] = list_[2]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "[新增回應]\n" + "關鍵字: " + list_[1] + "\n回應: " + list_[2])
                            except:
                                cl.sendMessage(to, "[ERROR]\n" + "新增關鍵字失敗")
                        else:
                            cl.sendMessage(to, "[ERROR]\n" + "關鍵字已存在")
                    elif msg.text.lower().startswith("del_react"):
                        list_ = msg.text.split(":")
                        if list_[1] in settings['react']:
                            try:
                                del settings['react'][list_[1]]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "[刪除關鍵字]\n成功刪除關鍵字!!!\n關鍵字: " + list_[1])
                            except:
                                cl.sendMessage(to, "[ERROR]\n刪除關鍵字失敗!!!")
                        else:
                            cl.sendMessage(to, "[ERROR]\n指定刪除的關鍵字並不在列表中!!!")
                    elif msg.text.lower().startswith("renew_react"):
                        list_ = msg.text.split(":")
                        if list_[1] in settings['react']:
                            try:
                                del settings['react'][list_[1]]
                                settings['react'][list_[1]] = list_[2]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "[更新回應]\n成功更新回應!!!\n關鍵字: " + list_[1] + "\n回應: " + list_[2])
                            except:
                                cl.sendMessage(to, "[ERROR]\n更新關鍵字失敗!!!")
                        else:
                            cl.sendMessage(to, "[ERROR]\n指定更新關鍵字並不在列表中!!!")
                    elif msg.text.lower().startswith("add_sr"):
                        list_ = msg.text.split(":")
                        number = str(list_[1]) + str(list_[2])
                        if number not in settings['sr']:
                            try:
                                settings['sr'][number] = list_[3]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "[新增貼圖回應]\n" + "回應: " + list_[3] + "\n系統辨識碼: " + number)
                            except:
                                cl.sendMessage(to, "[ERROR]\n" + "新增貼圖關鍵字失敗")
                        else:
                            cl.sendMessage(to, "[ERROR]\n" + "貼圖關鍵字已存在")
                    elif msg.text.lower().startswith("del_sr"):
                        list_ = msg.text.split(":")
                        number = str(list_[1]) + str(list_[2])
                        if number in settings['sr']:
                            try:
                                del settings['sr'][number]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "[刪除貼圖關鍵字]\n成功刪除貼圖關鍵字!!!\n系統辨識碼: " + number)
                            except:
                                cl.sendMessage(to, "[ERROR]\n刪除貼圖關鍵字失敗!!!")
                        else:
                            cl.sendMessage(to, "[ERROR]\n指定刪除的貼圖關鍵字並不在列表中!!!")
                    elif msg.text.lower().startswith("renew_sr"):
                        list_ = msg.text.split(":")
                        number = str(list_[1]) + str(list_[2])
                        if number in settings['sr']:
                            try:
                                del settings['sr'][number]
                                settings['sr'][number] = list_[3]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "[更新貼圖回應]\n成功更新貼圖回應!!!\n回應: " + list_[3] + "\n系統辨識碼: " + number)
                            except:
                                cl.sendMessage(to, "[ERROR]\n更新貼圖關鍵字失敗!!!")
                        else:
                            cl.sendMessage(to, "[ERROR]\n指定更新貼圖關鍵字並不在列表中!!!")
                    elif text.lower() == 'sn':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                        hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                        bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                        hr = timeNow.strftime("%A")
                        bln = timeNow.strftime("%m")
                        for i in range(len(day)):
                            if hr == day[i]: hasil = hari[i]
                        for k in range(0, len(bulan)):
                            if bln == str(k): bln = bulan[k-1]
                        readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                        if msg.to in read['readPoint']:
                                try:
                                    del read['readPoint'][msg.to]
                                    del read['readMember'][msg.to]
                                    del read['readTime'][msg.to]
                                except:
                                    pass
                                read['readPoint'][msg.to] = msg.id
                                read['readMember'][msg.to] = ""
                                read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                                read['ROM'][msg.to] = {}
                                with open('read.json', 'w') as fp:
                                    json.dump(read, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(msg.to,"已讀點已開始")
                        else:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                cl.sendMessage(msg.to, "設定已讀點:\n" + readTime)
                    elif text.lower() == 'sf':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                        hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                        bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                        hr = timeNow.strftime("%A")
                        bln = timeNow.strftime("%m")
                        for i in range(len(day)):
                            if hr == day[i]: hasil = hari[i]
                        for k in range(0, len(bulan)):
                            if bln == str(k): bln = bulan[k-1]
                        readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                        if msg.to not in read['readPoint']:
                            cl.sendMessage(msg.to,"已讀點已經關閉")
                        else:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                    pass
                            cl.sendMessage(msg.to, "刪除已讀點:\n" + readTime)
                    elif text.lower() == 'sr':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                        hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                        bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                        hr = timeNow.strftime("%A")
                        bln = timeNow.strftime("%m")
                        for i in range(len(day)):
                            if hr == day[i]: hasil = hari[i]
                        for k in range(0, len(bulan)):
                            if bln == str(k): bln = bulan[k-1]
                        readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                        if msg.to in read["readPoint"]:
                            try:
                                del read["readPoint"][msg.to]
                                del read["readMember"][msg.to]
                                del read["readTime"][msg.to]
                            except:
                                pass
                            cl.sendMessage(msg.to, "重置已讀點:\n" + readTime)
                        else:
                            cl.sendMessage(msg.to, "已讀點未設定")
                    elif text.lower() == 'r':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                        hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                        bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                        hr = timeNow.strftime("%A")
                        bln = timeNow.strftime("%m")
                        for i in range(len(day)):
                            if hr == day[i]: hasil = hari[i]
                        for k in range(0, len(bulan)):
                            if bln == str(k): bln = bulan[k-1]
                        readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                        if receiver in read['readPoint']:
                            if read["ROM"][receiver].items() == []:
                                cl.sendMessage(receiver,"[ 已讀者 ]:\n沒有")
                            else:
                                chiya = []
                                for rom in read["ROM"][receiver].items():
                                    chiya.append(rom[1])
                                cmem = cl.getContacts(chiya)
                                zx = ""
                                zxc = ""
                                zx2 = []
                                xpesan = '[ 已讀者 ]:\n'
                            for x in range(len(cmem)):
                                xname = str(cmem[x].displayName)
                                pesan = ''
                                pesan2 = pesan+"@c\n"
                                xlen = str(len(zxc)+len(xpesan))
                                xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                                zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                                zx2.append(zx)
                                zxc += pesan2
                            text = xpesan+ zxc + "\n[ 已讀時間 ]: \n" + readTime
                            try:
                                cl.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                            except Exception as error:
                                print (error)
                            pass
                        else:
                            cl.sendMessage(receiver,"已讀點未設定")
        if op.type == 26:
            try:
                msg = op.message
                try:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                except:
                    pass
            except Exception as e:
                print(logError(e))
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if at not in settings["reread"]:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            print ["收回訊息"]
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    cl.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                        cl.log()
                if msg.contentType == 0 and sender not in clMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if clMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = cl.getContact(sender)
                                    sendMessageWithMention(to, contact.mid)
                                    cl.sendMessage(to, "安安你好,我是防翻機器人Yukino,有事請找主人")
                                    time.sleep(0.5)
                                    cl.sendContact(op.param1, "u85ee80cfb293599510d0c17ab25a5c98")
                                break
        if op.type == 55:
            print ("[ 55 ] 通知讀取消息")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                    pass
            except:
                pass
    except Exception as e:
        logError(e)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)