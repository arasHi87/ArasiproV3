# -*- coding: utf-8 -*-
class Callback(object):

    def __init__(self, callback):
        self.callback = callback

    def PinVerified(self, pin):
        self.callback("輸入此PIN碼 '" + pin + "' 在2分鐘內在您手機的LINE上")

    def QrUrl(self, url, showQr=True):
        if showQr:
            notice='或掃描此QR '
        else:
            notice=''
        self.callback('打開此鏈接 ' + notice + '在2分鐘內在您手機的LINE上\n' + url)
        if showQr:
            try:
                import pyqrcode
                url = pyqrcode.create(url)
                self.callback(url.terminal('green', 'white', 1))
            except:
                pass

    def default(self, str):
        self.callback(str)
