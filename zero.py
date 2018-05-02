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
cl = LINE("EsWGJ7xLifOgpGEuK2F8.HE6aZ7ktwzuq0mf6SLPCMa.4nUnGBGiBOWeljI0IMTYQVY909Zv6TdRQUyBcvrWQ1Q=")
cl.log("Auth Token : " + str(cl.authToken))
kl = LINE("Esp04YSjNlFgduKnWTy9.hsy9DORB3tUFtfgdphXnkq.jV/pDfbBRxnAo8dxUlXNUtzkaPC7sS3z0n2O8z09FsU=")
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
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(param2)
            if settings["autoAdd"] == True:
                cl.sendMessage(op.param1, "你好 {} 謝謝你加本機為好友 :D\n       line.me/ti/p/1MRX_Gjbmv".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 24:
            print ("[ 24 ] 通知離開副本")
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 1:
            print ("[1]更新配置文件")
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if clMID in op.param3:
                print ("進入群組: " + str(group.name))
                cl.acceptGroupInvitation(op.param1)
                cl.sendMessage(op.param1, "歡迎使用由Arasi開發的ArasiproV3!!!\nMy creator:")
                time.sleep(1)
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
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            GS = group.creator.mid
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) +"\n踢人者: " + contact1.displayName + "\nMid: " + contact1.mid + "\n被踢者" + contact2.displayName + "\nMid:" + contact2.mid )
            if settings["protect"] == True:
                if op.param2 in settings['admin'] or op.param2 in settings['bot'] or op.param2 == GS:
                    pass
                else:
                    try:
                        cl.kickoutFromGroup(op.param1,[op.param2])
                    except:
                        try:
                            kl.kickoutFromGroup(op.param1,[op.param2])
                        except:
                            pass
                    if op.param3 in settings['bot']:
                        try:
                            ticket = cl.reissueGroupTicket(op.param1)
                        except:
                            ticket = kl.reissueGroupTicket(op.param1)
                        if group.preventedJoinByTicket == False:
                            pass
                        else:
                            group.preventedJoinByTicket = False
                            try:
                                cl.updateGroup(group)
                            except:
                                kl.updateGroup(group)
                        cl.acceptGroupInvitationByTicket(op.param1, ticket)
                        kl.acceptGroupInvitationByTicket(op.param1, ticket)
                        settings["blacklist"][op.param2] = True
                        with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                                cl.sendMessage(op.param1, "成功新增blacklist\n" + "MID : " + op.param2)
                                time.sleep(1)
                                cl.sendContact(op.param1, op.param2)
                        group.preventedJoinByTicket = True
                        cl.updateGroup(group)
        if op.type == 60:
            if op.param2 in settings['blacklist']:
                cl.sendMessage(op.param1, "[警告]\n此人位於黑名單中! ! !")
            else:
               sendMessageWithMention(op.param1, op.param2)
               cl.sendMessage(op.param1, "歡迎加入群組! ! !")
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
            elif msg.contentType == 16:
                if settings["timeline"] == True:
                    msg.contentType = 0
                    msg.text = "URLat\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendMessage(msg.to,msg.text)
            #if msg.contentType == 0:
            if text is None:
                return
            grp = cl.getGroup(to)
            GS = grp.creator.mid
            if sender in GS or sender in settings['gm'] or sender in settings['admin']:
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
                            settings['gm'][to][ls] = True
                            with open('temp.json', 'w') as fp:
                                json.dump(settings, fp, sort_keys=True, indent=4)
                                cl.sendMessage(to, "成功新增Group Master權限")
                                cl.sendContact(to, ls)
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
                            if ls in settings['gm'][to]:
                                del settings['gm'][to][ls]
                                with open('temp.json', 'w') as fp:
                                    json.dump(settings, fp, sort_keys=True, indent=4)
                                    cl.sendMessage(to, "成功移除Group Master權限")
                                    cl.sendContact(to, ls)
                            else:
                                cl.sendMessage(to, "此人並未擁有Group Master權限")
            if text.lower() == 'speed':
                start = time.time()
                cl.sendMessage(to, "processing......")
                elapsed_time = time.time() - start
                cl.sendMessage(to,format(str(elapsed_time)) + "秒")
            elif text.lower() == 'test':
                cl.sendMessage(to, "運行中")
                kl.sendMessage(to, "運行中")
            elif "botlist" in msg.text:
                if settings["bot"] == {}:
                    cl.sendMessage(to, "沒有機器名單")
                else:
                    try:
                        mc = "[ 機器名單 ]"
                        for mi_d in settings["bot"]:
                            mc += "-> " + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                    except:
                        pass
            elif "adminlist" in msg.text:
                if settings["admin"] == {}:
                    cl.sendMessage(to, "沒有管理員名單")
                else:
                    try:
                        mc = "[ 管理員名單 ]\n"
                        for mi_d in settings["admin"]:
                            mc += "-> " + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                    except:
                        pass
            elif text.lower() == 'rebot':
                cl.sendMessage(to, "重新啟動")
                restartBot()
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
                    ret_ = "[ 利用情報 ]"
                    ret_ += "\n私の名前は : {}".format(contact.displayName)
                    ret_ += "\nグループ名 : {}".format(str(group.name))
                    ret_ += "\n現在のバージョン: alpha v1.0.0"
                    ret_ += "\n作成者 : {}".format(creator.displayName)
                    ret_ += "\nURLを追加 : http://line.naver.jp/ti/p/~ee27676271"
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
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(logError(e))
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
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
                                    cl.sendMessage(to, "？")
                                    sendMessageWithMention(to, contact.mid)
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
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)