import json
import requests  # 这个需要自己 pip install requests 安装
class TFT():#云顶攻略类
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
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
        # 访问攻略详情接口
        res = requests.get("https://lol.qq.com/act/a2016Activity/data/ProdDetail_66_"+listID+".js", headers=self.headers)
        text=take_middle_text(res.text,"var ProdDetail_66_"+listID+"=","}]}};")+"}]}}"
        text =TFT.lol_unescape(self,text)
        #转义成中文
        j=json.loads(text)
        #提取需要的数据
        text=j['msg']['detail']['sProdDetail']
        #这里单引号要替换成双引号,不然json不支持
        text= text.replace("\'", "\"")
        j=json.loads(text)
        lineup_name=j['lineup_name']#卡组名
        author_name=j['author_name']#作者名
        #英雄站位 字典  'location'=站位坐标  'hero_id'=英雄id 'equipment_id'=装备 列表 天选羁绊isChosenHero
        hero_location=j['hero_location']
        if 'early_heros' in str(j):
            early_heros=j['early_heros']#前期 列表
        else:
            early_heros = ''  # 前期 列表
        if 'metaphase_heros' in str(j):
            metaphase_heros=j['metaphase_heros']#中期 列表
        else:
            metaphase_heros = ''  # 中期 列表
        if 'level_3_heros' in str(j):
            level_3_heros = j['level_3_heros']  # 追3星英雄 列表
        else:
            level_3_heros =""

        if 'early_chosen_heros'  in str(j):
            early_chosen_heros = j['early_chosen_heros']  # 天选英雄
        else:
            early_chosen_heros =''
        if 'replace_chosen_heros' in str(j):
            replace_chosen_heros = j['replace_chosen_heros']  # 天选备选英雄
        else:
            replace_chosen_heros = ''

        if 'hero_replace' in str(j):
            hero_replace=j['hero_replace']#备选英雄 字典  'hero_id':英雄id,'replace_heros':英雄id
        else:
            hero_replace=""#备选英雄 字典  'hero_id':英雄id,'replace_heros':英雄id
        #攻略文档
        early_info=j['early_info']#早期过渡
        d_time = j['d_time']#搜牌节奏
        if 'equipment_info' in str(j):
            equipment_info = j['equipment_info']  #装备分析
        else:
            equipment_info =''
        if 'location_info' in str(j):
            location_info = j['location_info']  # 阵容站位
        else:
            location_info =''
        if 'enemy_info' in str(j):
            enemy_info = j['enemy_info']  # 克制分析
        else:
            enemy_info =''
        _time = j['_time']  # 更新时间
        strategy = {'lineup_name':lineup_name,
                    'author_name':author_name,
                    'hero_location':hero_location,
                    'early_heros':early_heros,
                    "metaphase_heros":metaphase_heros,
                    'level_3_heros':level_3_heros,
                    'hero_replace':hero_replace,
                    'early_chosen_heros':early_chosen_heros,
                    'replace_chosen_heros':replace_chosen_heros,
                    'early_info':early_info,
                    'd_time':d_time,
                    'equipment_info':equipment_info,
                    'location_info':location_info,
                    'enemy_info':enemy_info,
                    "_time":_time}


        return strategy
    def get_lineName(self,setID):#获取卡组标题列表
        res = requests.get("https://lol.qq.com/act/AutoCMS/publish/LOLAct/TFTLineup_set4/TFTLineup_set4_"+setID+".js",headers=self.headers)
        text = take_middle_text(res.text,"{return ",";});/")
        j = json.loads(text)
        return j['line_name']
    def get_linelist(self):#返回最新卡组列表
        res =requests.get("https://lol.qq.com/act/AutoCMS/publish/LOLAct/TFTlinelist_set4/TFTlinelist_set4.js", headers=self.headers)
        text=take_middle_text(res.text,"{return",";});/*")
        j=json.loads(text)
        linelist =[]
        for i in j:
            #创建一个字典
            d=dict.fromkeys(('season', 'edition', 'quality', 'pub_time', "sortID", 'line_id', 'line_name'))
            d['season'] = j[str(i)]["season"]  # 赛季
            d['edition']=j[str(i)]["edition"]#版本号
            d['quality']= j[str(i)]["quality"]  # 评级
            d['pub_time']= j[str(i)]["pub_time"]  # 日期
            d['sortID']= j[str(i)]["sortID"]  # 排序位置
            d['line_id']=j[str(i)]["line_id"]#ID
            d['extend'] = j[str(i)]["extend"]  # 是否上架
            d['line_name']=TFT.get_lineName(self,i)#标题
            #排除删除的卡组
            if d['sortID'] != '' and d['extend'] =='1':
                linelist.append(d)  # 存起来
        return TFT.maopao(self,linelist)
    def get_chess(self):#f获取所以棋子的资料，返回一个列表
        res=requests.get("https://game.gtimg.cn/images/lol/act/img/tft/js/10.19-2020.S4/chess.js",headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        chess=[]
        for i in j:
            d=dict.fromkeys(('chessId', 'title', 'name', 'displayName',
                             "raceIds", 'raceIds', 'jobIds', 'price',
                             'skillName', 'skillType', 'skillIntroduce',
                             'skillDetail', 'magic', 'startMagic', 'armor',
                             'spellBlock', 'attackMag', 'attackSpeed', 'attackRange', 'crit',
                             'TFTID', 'recEquip', 'proStatus', 'races', 'jobs', 'attackData', 'lifeData'))
            d['chessId'] = i['chessId']#棋子ID
            d['title'] = i['title']#称呼
            d['name'] = i['name']#头像图片编号
            d['displayName'] = i['displayName']#名字
            d['raceIds'] = i['raceIds']#种族
            d['jobIds'] = i['jobIds']#职业
            d['price'] = i['price']#费用
            d['skillName'] = i['skillName']#技能名称
            d['skillType'] = i['skillType']#技能类型
            d['skillImage'] = i['skillImage']#技能图标
            d['skillIntroduce'] = i['skillIntroduce']#技能简介
            d['skillDetail'] = i['skillDetail']#技能细节
            d['magic'] = i['magic']#法力值
            d['startMagic'] = i['startMagic']#初始法力值
            d['armor'] = i['armor']#护甲
            d['spellBlock'] = i['spellBlock']#魔抗
            d['attackMag'] = i['attackMag']#
            d['attackSpeed'] = i['attackSpeed']#攻击速度
            d['attackRange'] = i['attackRange']#攻击范围
            d['crit'] = i['crit']#暴击
            d['TFTID'] = i['TFTID']
            d['recEquip'] = i['recEquip']#推荐装备
            d['proStatus'] = i['proStatus']#最近状态 无 加强 虚弱
            d['races'] = i['races']#种族
            d['jobs'] = i['jobs']#职业
            d['attackData'] = i['attackData']#攻击力
            d['lifeData'] = i['lifeData']#生命值
            chess.append(d)
        return chess
    def get_equip(self):#获取装资料返回一个列表
        res=requests.get("https://game.gtimg.cn/images/lol/act/img/tft/js/10.19-2020.S4/equip.js",headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        equip=[]
        # 排除项
        excludeIds = ['201', '202', '203', '204', '205', '206', '207', '208', '209','210', '211',
                      '212', '317', '324','331','333','337','340','342','346','349','352','355']
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
                equip.append(d)
        return equip
    def get_job(self):#获取所有的职业 返回一个列表
        res=requests.get('https://game.gtimg.cn/images/lol/act/img/tft/js/10.19-2020.S4/job.js',headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        job=[]
        for i in j:
            d=dict.fromkeys(('jobId','name','introduce','alias','level','TFTID','imagePath'))
            d['jobId'] = i['jobId']#职业id
            d['name'] = i['name']#名称
            d['introduce'] = i['introduce']
            d['alias'] = i['alias']
            d['level'] = i['level']
            d['TFTID'] = i['TFTID']
            d['imagePath'] = i['imagePath']
            job.append(d)
        return job
    def get_race(self):#获取所有的羁绊种族 返回一个列表
        res=requests.get('https://game.gtimg.cn/images/lol/act/img/tft/js/10.19-2020.S4/race.js',headers=self.headers)
        j=json.loads(res.text)
        j=j['data']
        race=[]
        for i in j:
            d=dict.fromkeys(('raceId','name','introduce','alias','level','TFTID','imagePath'))
            d['raceId'] = i['raceId']#职业id
            d['name'] = i['name']#名称
            d['introduce'] = i['introduce']
            d['alias'] = i['alias']
            d['level'] = i['level']
            d['TFTID'] = i['TFTID']
            d['imagePath'] = i['imagePath']
            race.append(d)
        return race



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
    list = tft.get_linelist()
    #演示推荐列表
    for i in list:
        #一个一个获取攻略数据
        # 具体的调用字典的哪个key.请自己看函数里面的备注说明.要显示出来就需要自己写一个界面了.饭已做好,要自己拿筷子吃了 举一反三
        strategy=tft.get_strategy(i['line_id'])
        #这里演示的一些数据 还有N多数据,反正都已经获取到了
        print(i['line_name'],strategy['author_name'],strategy['early_info'])

if __name__=="__main__":
    main()


