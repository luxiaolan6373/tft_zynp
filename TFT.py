import json
import requests  # 这个需要自己 pip install requests 安装
class TFT():#云顶攻略类
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        self.dataList=[]
        self.get_linelist()
    def lol_unescape(self,t):  # "去掉转义字符这很蛋疼,研究了很久..如果还碰到其它的转义字符可以加上去
        t = t.replace("&amp;#39;", "\'")
        t = t.replace("&lt;/p&gt;", "}")
        t = t.replace("&lt;p&gt;", "")
        t = t.replace("&lt;\/p&gt;", "")
        return t
    def maopao(self,list):  # 冒泡排序
        length = len(list)
        for i in range(length - 1):
            for j in range(length - i - 1):
                if int(list[j]['sortID']) > int(list[j + 1]['sortID']):
                    list[j], list[j + 1] = list[j + 1], list[j]
        return list
    def get_strategy(self,listID):#提取攻略 返回一个字典
        strategy=json.loads(self.dataList[listID]['detail'],strict=False)
        return strategy
    def get_linelist(self):#返回最新卡组列表包括攻略详情
        '''
        返回所有最新卡组的数据列表
        :return:
        '''
        res =requests.get("https://game.gtimg.cn/images/lol/act/tftzlkauto/json/lineupJson/s4/6/lineup_detail_total.json",
                          headers=self.headers)
        self.dataList=self.maopao(json.loads(res.text)['lineup_list'])
    def get_chess(self):#f获取所以棋子的资料，返回一个列表
        res=requests.get("https://game.gtimg.cn/images/lol/act/img/tft/js/chess.js",headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        return j
    def get_equip(self):#获取装资料返回一个列表
        res=requests.get("https://game.gtimg.cn/images/lol/act/img/tft/js/equip.js",headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        equip=[]
        # 排除项
        excludeIds = ['201', '202', '203', '204', '205', '206', '207', '208', '209','210', '211',
                      '212', '317', '324','331','333','337','340','342','346','349','352','355','']
        for i in j:
            #排除之前版本删除的装备
            if i['equipId'] not in excludeIds:
                d=dict.fromkeys(('equipId','type','name','effect','keywords','formula','imagePath','TFTID','jobId'))
                d['equipId'] = i['equipId']#id
                d['type'] = i['type']#类型,大装备=2 小装备=1
                d['name'] = i['name']#名字
                d['effect'] = i['effect']#作用
                d['keywords'] = i['keywords']#简介
                d['formula'] = i['formula']#合成需要
                d['imagePath'] = i['imagePath']#图标地址
                d['TFTID'] = i['TFTID']
                d['jobId'] = i['jobId']#职业 如果是有转职功能的,就会有职业不为0
                d['raceId'] = i['raceId']  # 职业 如果是有转职功能的,就会有职业不为0
                equip.append(d)
        return equip
    def get_job(self):#获取所有的职业 返回一个列表
        res=requests.get('https://game.gtimg.cn/images/lol/act/img/tft/js/job.js',headers=self.headers)
        j=json.loads(res.text)#兼容模式
        j=j['data']
        return j
    def get_race(self):#获取所有的羁绊种族 返回一个列表
        res=requests.get('https://game.gtimg.cn/images/lol/act/img/tft/js/race.js',headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        return j

def take_middle_text(txt,txt_s,txt_e='',seeks=0,seeke=0):#取中间文本函数
    try:
        if txt_e or seeks or seeke:
            pass
        else:
            raise 1
        s_1 = txt.find(txt_s)
        if s_1 == -1:
            raise 1
        l_1 = len(txt_s)
        if txt_e:
            s_2 = txt.find(txt_e,s_1)
            if s_1 == -1 or s_2 == -1:
                return False
            return txt[s_1+l_1:s_2]
        if seeks:
            return txt[s_1-seeks:s_1]
        if seeke:
            return txt[s_1+l_1:s_1+l_1+seeke]
    except:
        return '传参错误或未找到传参文本'

def main():
    tft = TFT()
    #可以使用print(列表名)打印数据
    chess = tft.get_chess()#获取所有的棋子数据 返回一个列表
    equip = tft.get_equip()#获取所有的装备数据 返回一个列表
    job = tft.get_job()#获取所有的职业数据 返回一个列表
    race = tft.get_race()#获取所有的羁绊数据 返回一个列表
    tft.get_linelist()
    #演示推荐列表
    for i in range(len(tft.dataList)):
        #一个一个获取攻略数据
        # 具体的调用字典的哪个key.请自己看函数里面的备注说明.要显示出来就需要自己写一个界面了.饭已做好,要自己拿筷子吃了 举一反三
        #这里演示的一些数据 还有N多数据,反正都已经获取到了
        strategy=tft.get_strategy(i)
        print( strategy)
if __name__=="__main__":
    main()


