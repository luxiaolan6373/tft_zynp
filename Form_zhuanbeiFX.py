from PyQt5.QtWidgets import QLabel,QVBoxLayout,QDialog,QFrame,QHBoxLayout
from PyQt5.QtGui import QPixmap
from goneng import *
from setting import *
class ZhuangGeiFX(QDialog):
    def __init__(self,data,chess,job,race,equip):
        super().__init__()
        self.data=data
        self.chess=chess
        self.job = job
        self.race = race
        self.equip = equip
        self.initshow()
    def initshow(self):
        self.setMinimumWidth(504)
        self.setObjectName('ZhuangbeiFX')
        self.spTitle=QLabel('装备分析')
        self.spTitle.setObjectName('Title')
        self.spDoc = QLabel(self.data['equipment_info'].replace('&amp;nbsp;',''))
        self.spDoc.setObjectName('Doc')
        self.spDoc.setWordWrap(True)
        self.vbox=QVBoxLayout()
        self.vbox.addWidget(self.spTitle)
        self.vbox.addWidget(self.spDoc)
        #装备推荐框架
        self.zbTJFrame=QFrame()
        self.zbTJVbox=QVBoxLayout()

        #遍历站位数据,看有没有装备,有装备的就加入zbTJHbox
        self.zbtj_YLH=[]
        self.xjzb_Vbox=[]
        #初始化羁绊和职业容器
        job_list=[]
        race_list=[]

        txData =None
        for item in self.data['hero_location']:
            # 将羁绊和职业数据存进容器
            chessData = chessId_get_data(self.chess, item['hero_id'])
            for job_item in chessData['jobIds'].split(','):
                job_list.append(job_item)
            for race_item in chessData['raceIds'].split(','):
                race_list.append(race_item)
            zwpath = Path_chess + chessData['name']
            if item['equipment_id']!='':
                #英雄头像
                self.zbtj_YLH.append(QHBoxLayout())
                self.zbTJVbox.addLayout(self.zbtj_YLH[-1])
                if chessData["price"] == '1':
                    color = '#989898'
                elif chessData["price"] == '2':
                    color = '#58B137'
                elif chessData["price"] == '3':
                    color = '#3678C8'
                elif chessData["price"] == '4':
                    color = '#C81FC8'
                else:
                    color = '#FDBC03'
                tp_yx = QLabel()
                # 让图像适应标签
                tp_yx.setScaledContents(True)
                tp_yx.setPixmap(QPixmap(zwpath))
                tp_yx.setMaximumSize(50, 50)
                tp_yx.setMinimumSize(50, 50)
                tp_yx.setObjectName('tp_yx')
                tp_yx.setStyleSheet('''#tp_yx{border: 1px solid %s;border-radius: 10px;  }
                                                               ''' % color)

                tp_yx.setToolTip(tanChudataForm(chessData, self.job, self.race))
                self.zbtj_YLH[-1].addWidget(tp_yx)
                jtbt=QLabel('>')
                jtbt.setObjectName('Title')
                self.zbtj_YLH[-1].addWidget(jtbt)


                for equi in item['equipment_id'].split(','):

                    djzb=equipId_get_data(self.equip,equi)
                    # 将羁绊和职业数据存进容器
                    try:
                        if djzb['jobId']!='0' and djzb['jobId']!=None:
                            job_list.append(djzb['jobId'])
                    except:
                        pass
                    try:
                        if djzb['raceId'] != '0' and djzb['raceId']!=None:
                            race_list.append(djzb['raceId'])
                    except:
                        pass


                    zbpath = Path_equip+djzb['imagePath'].split('/')[-1]

                    #print('大装备', zbpath)

                    tp_djzb=QLabel()
                    # 让图像适应标签
                    tp_djzb.setScaledContents(True)
                    tp_djzb.setPixmap(QPixmap(zbpath))
                    tp_djzb.setMaximumSize(40, 40)
                    tp_djzb.setMinimumSize(40, 40)
                    self.zbtj_YLH[-1].addWidget(tp_djzb)
                    #取小装备的id
                    self.xjzb_Vbox.append(QVBoxLayout())
                    self.xjzb_Vbox[-1].addStretch()
                    self.zbtj_YLH[-1].addLayout(self.xjzb_Vbox[-1])
                    for itemXJ in djzb['formula'].split(','):
                        xjzb = equipId_get_data(self.equip, itemXJ)
                        xjzbpath = Path_equip+xjzb['imagePath'].split('/')[-1]
                        #print('小装备', zbpath)

                        tp_xjzb = QLabel()
                        # 让图像适应标签
                        tp_xjzb.setScaledContents(True)
                        tp_xjzb.setPixmap(QPixmap(xjzbpath))
                        tp_xjzb.setMaximumSize(20, 20)
                        tp_xjzb.setMinimumSize(20, 20)
                        self.xjzb_Vbox[-1].addWidget(tp_xjzb)
                    #一个弹簧..用来控制位置的
                    self.xjzb_Vbox[-1].addStretch()

                self.zbtj_YLH[-1].addStretch()
            # 天选羁绊和职业存入
            if 'isChosenHero' in item:

                if item['isChosenHero'] != None:
                    txData = item['isChosenHero']
                    # 天选羁绊id
                    sss = ''
                    for key in txData.keys():
                        sss = key
                    if sss == 'race':
                        race_list.append(txData['race'])
                    else:
                        job_list.append(txData['job'])
                else:
                    pass

        #职业分析组件---------------------------------------------
        self.from_job =QFrame()
        self.from_jobHBox=QHBoxLayout()
        #统计总职业数,并且将底图和图标获取
        jb_ss={}.fromkeys(job_list ).keys()
        for ss in jb_ss:
            num=job_list.count(ss)

            if txData != None:
                if sss == 'job' and txData['job']==ss :
                    test_job=job_get_background_sf(self.job,ss,num,True)
                else:
                    test_job=job_get_background_sf(self.job, ss, num, False)
            else:
                test_job=job_get_background_sf(self.job, ss, num, False)
            if test_job != None:
                #将每一个小组件渲染
                tp_hbox=QHBoxLayout()
                #羁绊背景
                tp_jb_bj=QLabel()
                tp_jb_bj.setScaledContents(True)
                tp_jb_bj.setPixmap(QPixmap(test_job[0]))
                tp_jb_bj.setMaximumSize(30, 34)
                tp_jb_bj.setMinimumSize(30, 34)
                tp_jb_bj.setToolTip(
                    f'''<b style='color:#FFFFFF;'>{test_job[2]['introduce']}<br>{str(test_job[2]['level']).replace('{', '').replace('}', '').replace(',', '<br>')}</b>''')

                #tp_jb_bj上方显示图标
                tp_jb = QLabel(tp_jb_bj)
                tp_jb.move(5,7)
                tp_jb.setScaledContents(True)
                tp_jb.setPixmap(QPixmap(test_job[1]))
                tp_jb.setMaximumSize(20, 20)
                tp_jb.setMinimumSize(20, 20)
                #羁绊名 文字
                tp_text=QLabel(tp_jb_bj)
                tp_text.setObjectName('JB')
                tp_text.setText(f"{num} "+test_job[2]['name'])


                #将数据加入到每一列的布局中
                tp_hbox.addWidget(tp_jb_bj)
                tp_hbox.addWidget(tp_text)
                self.from_jobHBox.addLayout(tp_hbox)

        self.from_jobHBox.addStretch()

        # 羁绊分析组件---------------------------------------------
        self.from_race = QFrame()
        self.from_raceHBox = QHBoxLayout()
        # 统计总羁绊数,并且将底图和图标获取
        race_ss = {}.fromkeys(race_list).keys()
        for ss in race_ss:
            num = race_list.count(ss)


            if txData != None:
                if sss == 'race' and txData['race']==ss :
                    test_race = race_get_background_sf(self.race, ss, num, True)
                else:
                    test_race = race_get_background_sf(self.race, ss, num, False)
            else:
                test_race = race_get_background_sf(self.race, ss, num, False)
            if test_race!=None:
                # 将每一个小组件渲染
                print(test_race)
                tp_hbox = QHBoxLayout()
                # 羁绊背景
                tp_jb_bj = QLabel()
                tp_jb_bj.setScaledContents(True)
                tp_jb_bj.setPixmap(QPixmap(test_race[0]))
                tp_jb_bj.setMaximumSize(30, 34)
                tp_jb_bj.setMinimumSize(30, 34)
                tp_jb_bj.setToolTip(
                    f'''<b style='color:#FFFFFF;'>{test_race[2]['introduce']}<br>{str(test_race[2]['level']).replace('{', '').replace('}', '').replace(',', '<br>')}</b>''')

                # tp_jb_bj上方显示图标
                tp_jb = QLabel(tp_jb_bj)
                tp_jb.move(5,7)
                tp_jb.setScaledContents(True)
                tp_jb.setPixmap(QPixmap(test_race[1]))
                tp_jb.setMaximumSize(20, 20)
                tp_jb.setMinimumSize(20, 20)
                # 羁绊名 文字
                tp_text = QLabel(tp_jb_bj)
                tp_text.setObjectName('JB')
                tp_text.setText(f"{num} "+test_race[2]['name'])

                # 将数据加入到每一列的布局中
                tp_hbox.addWidget(tp_jb_bj)
                tp_hbox.addWidget(tp_text)
                self.from_raceHBox.addLayout(tp_hbox)
        self.from_raceHBox.addStretch()

        self.zbTJFrame.setLayout(self.zbTJVbox)
        self.from_job.setLayout(self.from_jobHBox)
        self.from_race.setLayout(self.from_raceHBox)
        self.vbox.addWidget(self.zbTJFrame)
        self.vbox.addWidget(self.from_job)
        self.vbox.addWidget(self.from_race)


        self.vbox.setSpacing(2)
        self.setLayout(self.vbox)
        self.setStyleSheet('''
        #ZhuangbeiFX{
        border: 1px solid rgb(185, 185, 185);  
        
    	background-color: rgb(22,26,32);
    	border-right-style:none;
        border-top-style:none;
        }
        #Title{
	    color: #FFFFFF;
	    background: rgba(22,26,32, 200);   
	    font: 75 12pt "微软雅黑";}
	    
	    #Doc{
	    color: #7E807D;
	    border-left-style: 1px solid rgb(185, 185, 185);  
	    background: rgba(22,26,32, 200) ;  
	    font: 75 10pt "微软雅黑";}
	    #JB{
	    color: #FFFFFF;
	    background: rgba(22,26,32, 200);   
	    font: 75 10pt "微软雅黑";}
	    QToolTip{
            border: 2px solid qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));   
	        background-color: rgb(22,26,32);
	        ridge:ridge;
	        padding: 4px;
	        border-radius:10px;
        }
        ''')




