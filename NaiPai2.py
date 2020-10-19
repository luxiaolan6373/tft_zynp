import os
import time
import threading
from win32com.client import Dispatch
import win32con, win32api, copy
import win32com.client
# 注册大漠到系统中.
def regDM():
    '''
    注册大漠插件,需要把文件dm.dll放在根目录
    :return: 返回大漠对象
    '''
    path = os.getcwd()
    print('dm.dll路径=', path)
    try:
        dm = Dispatch('dm.dmsoft')
    except:
        os.system(F'regsvr32 {path}/dm.dll')
        dm = Dispatch('dm.dmsoft')
    return dm


# 从系统中卸载大漠
def unRegDM():
    '''
    从系统中卸载大漠插件
    :return:
    '''
    os.system('regsvr32 dm.dll /u')


class AutoOPlayingChess():
    '''
    自动购买棋子,后台鼠标,不占用前台用户的鼠标体验
    '''

    def __init__(self):
        self.dm = regDM()
        self.hwnd = 0
        self.chess = []
        self.chess_bn = []

    def __del__(self):
        self.dm.UnBindWindow()

    def dmReg(self, reg_code, ver_info=''):
        '''
        登录大漠.就是身份验证一下,从而使用插件的高级功能,如果你的是3.xx的免费版本,就不需要这步
        :param reg_code: 大漠后台的注册码
        :param ver_info: 附加信息,主要用于查询消费情况 填了更好查询,不填也无所谓
        :return: 返回1表示成功,其它值请查接口说明
        '''
        value = self.dm.reg(reg_code, ver_info)
        return value

    def SetDict(self, path, errorMsg=0):
        '''
        设置字库,顺便关掉错误提示
        :param path: 字库路径
        :param errorMsg: 默认为关闭错误提示,如果要设置请填1
        :return:0失败,1成功!
        '''
        self.dm.SetShowErrorMsg(errorMsg)
        return self.dm.SetDict(0, path)

    def checkHwnd(self, processName='League of Legends.exe'):
        '''
        循环寻找窗口,直到成功才返回
        :param processName: 进程名
        :return: 返回目标窗口句柄
        '''

        while self.hwnd == 0:
            self.hwnd = self.dm.FindWindowByProcess(processName, 'RiotWindowClass', '')
            time.sleep(5)

    def hwnd_is_True(self, processName='League of Legends.exe'):
        '''
        循环寻找游戏窗口是否存在,如果不存在就结束进程
        :param processName: 进程名
        :return:
        '''
        while self.hwnd != 0:
            self.hwnd = self.dm.FindWindowByProcess(processName, 'RiotWindowClass', '')
            time.sleep(20)

    def chessAdd(self, chessName):
        '''
        将名为chessName的棋子添加进购买库
        :param chessName: 棋子名
        :return:
        '''
        if chessName not in self.chess:
            self.chess.append(chessName)

    def delChess(self, i):
        '''
        删除序号为i的购买池中的棋子
        :param i: 序号
        :return:
        '''
        try:
            del self.chess[i]
            print(self.chess)
        except:
            pass

    def removeChess(self, chessName):
        '''
        删除名字为chessName的购买池中的棋子
        :param chessName: 棋子名
        :return:
        '''

        try:
            self.chess.remove(chessName)
        except:
            pass

    def delChess_bn(self, i):
        '''
        根据所给的chess索引删除不拿列表chess_bn的某个英雄
        :param i: chess索引
        :return:
        '''
        self.chess_bn.remove(self.chess[i])

    def Chess_bn_Add(self, i):
        '''
        根据所给的chess索引将英雄名添加进不拿列表chess_bn
        :param i: chess索引
        :return:
        '''
        try:

            self.chess_bn.append(self.chess[i])
        except:
            pass

    def startAuto(self, starX=200, starY=100, color_format="ffffff-060606", sim=0.95):
        '''
        启动自动购买棋子程序,默认1920*1080分辨率不需要改东西,,如果是更高的分辨率贼需要自己量参数
        :param starX: 识别开始的x坐标 商店1号棋子的名字 的x坐标.,可以小,但是不能大
        :param starY: 商店棋子名字距离屏幕最下方的距离 可以大 不能小
        :param color_format: 颜色格式串
        :param sim:相似度,取值范围0.1-1.0
        :return:如果返回False说明绑定失败.运行失败!
        '''
        speaker = win32com.client.Dispatch("SAPI.SpVoice")

        while True:  # 主循环,用来判断游戏开始和结束然后重新绑定窗口的
            print('正在寻找游戏,等待开始!')
            self.checkHwnd()
            for s in range(5):  # 尝试五次
                # 这个为后台鼠标,,很不稳定经常点击失效所以弃用了
                #dm_ret = self.dm.BindWindowEx(self.hwnd, "dx2","dx.mouse.position.lock.api|dx.mouse.api","normal", "dx.public.active.api", 0)
                dm_ret = self.dm.BindWindow(self.hwnd, "dx2", 'normal', "normal",0)
                if dm_ret == 1:
                    print('绑定成功!', self.hwnd)
                    print('---仅支持1920*1080分辨率,并且游戏要设置无边框模式---')
                    print('---注意了,本程序只会在你[每次按D键刷新商店时]开始智能帮拿!其它时候是保持静默的!---')
                    break
                print(f'第{s + 1}次绑定失败正在尝试!', self.hwnd)
                time.sleep(5)
                self.checkHwnd()
            if dm_ret == 0:
                win32api.MessageBox(0, "绑定失败!请重新运行", "警告!", win32con.MB_ICONWARNING)
                return False
            ret, ScreenWidth, ScreenHeight = self.dm.GetClientSize(self.hwnd)
            lScreenHeight = ScreenHeight - starY
            # 启动每10秒检测一下游戏窗口是否存在..如果不存在则跳出循环,重新等待游戏,,然后重新绑定窗口
            t1 = threading.Thread(target=self.hwnd_is_True)
            t1.setDaemon(True)
            t1.start()
            #循环,直到窗口不见了
            while self.hwnd != 0:
                time.sleep(0.03)
                # 判断用户是否有在按d键,按了之后就启动一次,直到帮忙拿了一轮牌之后(一次商店的牌)
                #281,1010,455,1069

                sss,sbX,sbY=self.dm.GetCursorPos()
                sbDD=self.dm.GetKeyState(1) == 1 and sbX>=281 and sbX<=455 and sbY>=1010 and sbY<=1069
                if self.dm.GetKeyState(68) == 1 or sbDD:
                    is_dianTrue =False
                    print('按了一次D键')
                    if len(self.chess) > 0:  # 判断自动购买棋子池是否有需要购买的棋子,有需要才有必要运行下面的代码
                        while is_dianTrue==False:#开始循环判断是否有需要点击的棋子,直到帮忙点过一轮后退出循环
                            # 返回的是5个当前商店棋子名以及坐标
                            time.sleep(0.1)
                            sls = self.dm.OcrEx(starX, lScreenHeight, ScreenWidth, ScreenHeight, color_format, sim).split('|')
                            #记录下来,好用来念
                            SpeakNames=[]
                            for item in sls:#分别判断
                                s = item.split('$')
                                # 对比是否是设置了自动购买的棋子

                                if s[0] in self.chess:
                                    #判断是否有暂时不买的棋子
                                    if s[0] in self.chess_bn:
                                        break
                                    #加入需要念的英雄
                                    SpeakNames.append(s[0])
                                    x=int(s[1]) + 40
                                    y=int(s[2]) - 30
                                    ret1=self.dm.MoveTo(x, y)
                                    ret2=self.dm.LeftClick()
                                    print(s[0], x, y,ret1,ret2)
                                    is_dianTrue = True#说明点了
                                    time.sleep(0.2)
                            #五个都判断完了,之后看要不要念
                            length=len(SpeakNames)
                            if length>0:
                                text='发现 '
                                for i, item in enumerate(SpeakNames):
                                    if i ==length-1:
                                        text=text+item
                                    else:
                                        text = text + item + ' 和 '
                                #语音播报
                                speaker.Speak(text)

            self.dm.UnBindWindow()
            print('游戏结束或者退出了!')