import sys,MainWindow,requests,os,Form_SquadList,Form_strategy,Form_souPaiJieZou,Form_zhengrongZW,Form_zaoqiGD,Form_zhuanbeiFX,Form_hero
import Form_zdlist,Form_zb
from PyQt5.QtWidgets import QCheckBox,QApplication,QMessageBox,QHeaderView,QGridLayout,QPushButton,QMainWindow,QVBoxLayout,QLabel,QFrame,QAbstractItemView,QTableWidgetItem,QDialog,QRadioButton,QHBoxLayout,QSpacerItem,QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QImage,QCursor,QPalette,QBrush
from TFT import TFT
from NaiPai import AutoOPlayingChess
from goneng import *
from setting import *
import threading,copy

#功能
def updataAutoChess():
    global atpc,chess
    chessList = []  # 选中的棋子池
    if  dangqianData!='':
        hero_location=dangqianData['hero_location']

        for item in hero_location:
            #print(item)
            #获取棋子名称
            try:
                chessDATA= chessId_get_data(chess,item['hero_id'])
                chessList.append(chessDATA['displayName'])
            except:
                pass
        if len(chess)>0:
            # 将需要购买的棋子放入池子中
            atpc.chess=chessList
            zdlistLoading(chessList)
            print('目前的自动列表:',atpc.chess)
def downSJ():
    '''
    下载官网的图片数据
    :return:
    '''
    '棋子图片'
    if len(os.listdir(Path_chess))< len(chess):
        for item in chess:
            name=item['name']
            url = f"https://game.gtimg.cn/images/lol/act/img/tft/champions/{name}"
            res = requests.get(url)
            Path_1 = f"{Path_chess}/{name}"
            with open(Path_1, 'wb')as f:
                f.write(res.content)

    '棋子大图'
    if len(os.listdir(Path_chess_D))< len(chess):
        for item in chess:
            name=item['name'].split('.')[0]
            url = f"https://game.gtimg.cn/images/lol/tft/cham-icons/624x318/{name}.jpg"
            res = requests.get(url)
            Path_1 = f"{Path_chess_D}/{name}.jpg"
            with open(Path_1, 'wb')as f:
                f.write(res.content)


    '装备图片'
    if len(os.listdir(Path_equip)) < len(equip):
        for item in equip:
            name = item['imagePath'].split('/')[-1]
            url = item['imagePath']
            res = requests.get(url)
            Path_1 = f"{Path_equip}/{name}"
            with open(Path_1, 'wb')as f:
                f.write(res.content)
    '职业图片'
    if len(os.listdir(Path_job)) < len(job):
        for item in job:
            name = item['imagePath'].split('/')[-1]
            url = item['imagePath']
            res = requests.get(url)
            Path_1 = f"{Path_job}/{name}"
            Path_2 = f"{Path_job2}/{name}"
            with open(Path_2, 'wb')as f:
                f.write(res.content)
            #将图片的颜色转换成白色
            CreateNewImage(Path_2,Path_1,[255,255,255])
    '羁绊图片'
    if len(os.listdir(Path_race)) < len(race):
        for item in race:
            name = item['imagePath'].split('/')[-1]
            url = item['imagePath']
            res = requests.get(url)
            Path_1 = f"{Path_race}/{name}"
            Path_2 = f"{Path_race2}/{name}"
            with open(Path_2, 'wb')as f:
                f.write(res.content)
            # 将图片的颜色转换成白色
            CreateNewImage(Path_2, Path_1, [255, 255, 255])
#事件槽
def buttonClick():
    '''
    按钮事件都绑定在这里了
    :return:
    '''
    global t_squadList,zdlistForm,clist
    #取出对象mainWindow.sender()
    mainWindow.sender().setEnabled(False)
    if mainWindow.sender().text()=='官方阵容':
        if squadList.isVisible():
            squadList.setVisible(False)
        else:
            squadList.setVisible(True)
            if squadListUI.tabZhengR.rowCount() ==0:
                loadingList()
            if zdlistForm.isVisible():
                squadList.move(0,mainWindow.geometry().height()+zdlistForm.geometry().height()-18)
            else:
                squadList.move(0, mainWindow.geometry().height() )
            try:
                heroForm.setVisible(False)
            except:
                pass
            try:
                equipForm.setVisible(False)
            except:
                pass
    if mainWindow.sender().text()=='自动列表':
        if zdlistForm.isVisible():#如果自动列表已经显示了,则关闭显示
            zdlistForm.setVisible(False)
            if squadList.isVisible():
                squadList.move(0, mainWindow.geometry().height() )
            if heroForm.isVisible():
                heroForm.move(0, mainWindow.geometry().height() )
            if equipForm.isVisible():
                equipForm.move(0, mainWindow.geometry().height())

        else:
            heroForm.move(0, mainWindow.geometry().height()+zdlistForm.geometry().height()-18)
            squadList.move(0, mainWindow.geometry().height() + zdlistForm.geometry().height()-18)
            equipForm.move(0, mainWindow.geometry().height() + zdlistForm.geometry().height()-18)
            zdlistForm.setVisible(True)
    if mainWindow.sender().text()=='英雄':
        if heroForm.isVisible():
            heroForm.setVisible(False)
        else:
            if heroFormUI.tabHero.rowCount()==0:
                Hero_loadingList(chess)
            heroForm.move(0, mainWindow.geometry().height() + zdlistForm.geometry().height() - 18)
            try:
                squadList.setVisible(False)
            except:
                pass
            try:
                equipForm.setVisible(False)
            except:
                pass


            zdlistForm.setVisible(True)
            heroForm.setVisible(True)
    if mainWindow.sender().text()=='装备':
        if equipForm.isVisible():
            equipForm.setVisible(False)
        else:
            if zdlistForm.isVisible():
                equipForm.move(0, mainWindow.geometry().height() + zdlistForm.geometry().height() - 18)
            else:
                equipForm.move(0, mainWindow.geometry().height() )
            try:
                squadList.setVisible(False)
            except:
                pass
            try:
                heroForm.setVisible(False)
            except:
                pass
            equipForm.setVisible(True)
    if mainWindow.sender().text()=='关闭':
        text=''
        try:
            if len(atpc.chess) > 0:
                with open('data/zdlist.ini', 'w') as f:
                    for item in atpc.chess:
                        text=text+item+" "
                    f.write(text)
        except:
            pass

        app.quit()
    print('单击了',mainWindow.sender().text())
    mainWindow.sender().setEnabled(True)
def tablistClick():
    '''
    官方阵容鼠标选中时
    :return:
    '''
    global dangqianData,spjzFrom,zrzwFrom
    #取当前选中项
    row = squadListUI.tabZhengR.selectedItems()[0].row()
    #记录当前的阵容数据,让下面的界面各自分析
    dangqianData=strategyS[row]
    #同时展开 早期过渡和装备分析
    showZaoQiGD(True)
    showZhuangBeiFX(True)
def checkBoxStateChanged(a):
    '''
    复选框选中与不选中事件,用来标记暂时不点的棋子
    :param a:
    :return:
    '''
    global zdlistForm,zdlistUI
    try:
        i=int(zdlistForm.sender().text()) # 获取当前列索引
        if a==2:#选中
           atpc.delChess_bn(i)
        else:
            atpc.Chess_bn_Add(i)
        print('标记不点列表',atpc.chess_bn)
    except:
        pass
def double_click_Hero_remove(index):
    '''
    删除数据支持多选
    :return:
    '''
    global zdlistForm, zdlistUI
    try:
        column = index.column()  # 获取当前列索引
        zdlistUI.tabZDlist.removeColumn(column)  # 从自动列表tab中删除
        atpc.delChess(column)  # 删除指定位置的
    except:
        pass
def double_click_Hero_Add(index):
    '''双击增加一个自动列表的棋子'''
    global atpc,heroItems
    try:
        i = index.column() + (index.row() * 4)
        if heroItems[i]['displayName'] not in atpc.chess:
            column = zdlistUI.tabZDlist.columnCount() + 1
            zdlistUI.tabZDlist.setColumnCount(column)
            zidong_kuanjia(heroItems[i], zdlistUI.tabZDlist.columnCount() - 1)  # 加入一个数据
            atpc.chessAdd(heroItems[i]['displayName'])  # 加入
            print('目前的自动列表:', atpc.chess)

    except:
        pass

def keyReleaseEvent_zd(event):
    if event.key()==16777223:
        #当前选中列
        sc_ls=[]#被选中的
        for item in zdlistUI.tabZDlist.selectedIndexes():
            column=item.column()
            #找到名字然后存进去
            sc_ls.append(atpc.chess[column])
        for name in sc_ls:
            if name in atpc.chess_bn:#不拿列表如果有也要清空,,不然就没法办法取消了
                atpc.chess_bn.remove(name)  # 删除指定的棋子
            atpc.removeChess(name)  # 删除指定的棋子
        print('当前自动列表:',atpc.chess)
        zdlistLoading(atpc.chess)


#英雄相关功能
def rb_click(biaoji):
    '''
    单选框的选中事件
    :param biaoji: 标记
    :return:
    '''
    global tj_chess
    text=heroForm.sender().text()
    print(text, biaoji)
    #根据标识然后把条件加入条件列表tj_chess中
    if biaoji=='price':
        if text=='全部':
            tj_chess[0] ='0'
        else:
            tj_chess[0] = text.replace('金币', '')
    if biaoji=='job':
        if text == '全部':
            tj_chess[1]='0'
        else:
            print('text',text)
            #根据职业名取id
            tj_chess[1] = jobName_get_data(job,text)['jobId']
    if biaoji=='race':
        if text == '全部':
            tj_chess[2] = '0'
        else:
            # 根据羁绊名取id
            tj_chess[2]=raceName_get_data(race,text)['raceId']
    print('条件列表',tj_chess)
    Hero_loadingList(Hero_filter(chess,tj_chess[0],tj_chess[1],tj_chess[2],tj_chess[3]))
def bjk_editing(led_keyword):
    '''
    编辑框内容被改变,更新数据
    :return:
    '''
    global tj_chess
    tj=led_keyword.text()
    tj_chess[3] = tj
    print(tj_chess[3])


#载入和初始化
def zidong_kuanjia(chessData,i):
    xzFrame = QFrame()  # 框架

    zwpath = Path_chess + chessData['name']
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
    tp_qlb = QLabel(xzFrame)
    # 让图像适应标签
    tp_qlb.setScaledContents(True)
    tp_qlb.setPixmap(QPixmap(zwpath))
    tp_qlb.setMaximumSize(50, 50)
    tp_qlb.setMinimumSize(50, 50)
    tp_qlb.setObjectName('tp_qlb')
    tp_qlb.setToolTip(tanChudataForm(chessData, job, race))
    tp_qlb.setStyleSheet('''#tp_qlb{padding: 1px;  border: 1px solid %s;border-radius: 12px;  }''' % color)
    qkBts = QCheckBox(xzFrame)
    qkBts.setObjectName('qkBts')
    if chessData['displayName'] in atpc.chess_bn:
        qkBts.setChecked(False)
    else:
        qkBts.setChecked(True)

    qkBts.setText("          " + str(i))
    qkBts.setStyleSheet('''#qkBts{
            Color:red;
            }''')

    qkBts.stateChanged[int].connect(checkBoxStateChanged)

    zdlistUI.tabZDlist.setCellWidget(0, i, xzFrame)
    zdlistUI.tabZDlist.setColumnWidth(i, 52)  # 设置某列的宽度
def loadingList():
    '''
    载入官方列表
    :return:
    '''
    squadListUI.tabZhengR.setRowCount(len(line_list))
    squadListUI.tabZhengR.setColumnCount(11)

    for i,item in enumerate(line_list):

        strategy = tft.get_strategy(item['line_id'])
        strategyS.append(strategy)
        # 设置阵容强度
        tphot = QLabel()

        tphot.setAlignment(Qt.AlignCenter)
        tphot.setStyleSheet(f'''
                 background-image: url({Path_img}hot.png);
                 color: #98794C;
                 font-size:28px;
                 font:微软雅黑;
                 padding: 1px;  
                 background-position:center;
             ''')
        tphot.setText(item['quality'])
        tphot.setAlignment(Qt.AlignCenter)
        squadListUI.tabZhengR.setCellWidget(i, 0, tphot)
        # 设置阵容名
        tabItem = QTableWidgetItem(item['line_name'])
        squadListUI.tabZhengR.setItem(i, 1, tabItem)


        hero_location=strategy['hero_location']
        level_3_heros=strategy['level_3_heros']
        k=0
        for j,heroitem in enumerate(hero_location):
            try:
                chessData = chessId_get_data(chess, heroitem['hero_id'])
            except:
                #错误偏移
                k+=1
                continue
            tpgFrame= QFrame()
            #天选英雄
            if 'isChosenHero' in heroitem:
                if heroitem['isChosenHero']!=None:

                    tpgFrame.setObjectName('tpgFrame')
                    tpgFrame.setStyleSheet('''
                    #tpgFrame{
                        border: 1px solid #DF8AE7; 
                        border-radius: 5px; 
                          }''')
            vbox = QVBoxLayout()

            tp = QLabel(tpgFrame)
            if heroitem['hero_id'] in level_3_heros:
                tp.setText('★★★')
            tphot.setAlignment(Qt.AlignCenter)
            tp.setStyleSheet('''
                margin: 1px;               
                color: #FDBC03;
                font-size:12px;
                font:微软雅黑;
            ''')
            tp.setMaximumSize(42, 12)
            tp.setMinimumSize(42, 12)
            #居中
            tphot.setAlignment(Qt.AlignCenter)

            tp1 = QLabel(tpgFrame)
            tp1.setMaximumSize(42, 42)
            tp1.setMinimumSize(42, 42)
            #让图像适应标签
            tp1.setScaledContents(True)
            tp1.setToolTip(tanChudataForm(chessData,job,race))


            if chessData["price"] =='1':
                color = '#989898'
            elif chessData["price"] =='2':
                color = '#58B137'
            elif chessData["price"] =='3':
                color = '#3678C8'
            elif chessData["price"] =='4':
                color = '#C81FC8'
            else:
                color = '#FDBC03'


            tp1.setStyleSheet(f'''
                    margin: 1px;
                    border: 1px solid {color}; 
                    border-radius: 10px;  
                    ''')

            chessPath =Path_chess +chessData['name']

            tp1.setPixmap(QPixmap(chessPath))

            vbox.addWidget(tp)
            vbox.addWidget(tp1)
            vbox.setContentsMargins(1,0,1,1)
            #控件间距
            vbox.setSpacing(1)
            tpgFrame.setLayout(vbox)
            squadListUI.tabZhengR.setCellWidget(i, 2 + j-k, tpgFrame)

    # 行列大小根据内容调整大小

    squadListUI.tabZhengR.resizeRowsToContents()
    squadListUI.tabZhengR.resizeColumnsToContents()
def zdlistLoading(clist):
    '''
    初始化自动列表
    :param clist:
    :return:
    '''

    zdlistUI.tabZDlist.setColumnCount(len(clist))
    zdlistUI.tabZDlist.setRowCount(1)
    for i, item in enumerate(clist):
        chessData = chessName_get_data(chess, item)
        zidong_kuanjia(chessData,i)
    zdlistUI.tabZDlist.setRowHeight(0, 52)  # 设置某行的高度


    #zdlistUI.tabZDlist.setRowHeight(20,20)

    # 行列大小根据内容调整大小
    #zdlistUI.tabZDlist.resizeRowsToContents()
    #zdlistUI.tabZDlist.resizeColumnsToContents()
def Hero_loadingList(hero_list):
    '''
    根据所提供的数据把列表在tabw中显示出来
    :param hero_list: 列表字典数据
    :return:
    '''
    global job,race,heroItems
    heroFormUI.tabHero.clear()
    length=len(hero_list)
    fy=4#每4个为一行
    y=0#纵向位置

    if length%fy==0:
        heroFormUI.tabHero.setRowCount(length//fy)
    else:
        heroFormUI.tabHero.setRowCount(length//fy+1)
    heroFormUI.tabHero.setColumnCount(fy)
    heroItems=copy.deepcopy(hero_list)

    for i,item in enumerate(hero_list):
        x=i%4#求出x位置,0123 每次保持这个顺序
        if x==0 and i>0:#求出y的位置
            y+=1

        # 英雄框架,代表每一个英雄
        hero_frame=QFrame()
        # 表格布局
        gbox=QGridLayout()
        #英雄海报
        tp1 = QLabel()
        chessPath = Path_chess_D + item['name'].split('.')[0] + '.jpg'
        # 让图像适应标签
        tp1.setScaledContents(True)
        tp1.setPixmap(QPixmap(chessPath))
        tp1.setMaximumSize(208, 106)
        tp1.setMinimumSize(208, 106)
        tp1.setToolTip(tanChudataForm(item, job, race))
        #边框颜色
        if item["price"] == '1':
            color = '#989898'
        elif item["price"] == '2':
            color = '#58B137'
        elif item["price"] == '3':
            color = '#3678C8'
        elif item["price"] == '4':
            color = '#C81FC8'
        else:
            color = '#FDBC03'

        tp1.setStyleSheet(f'''
                            margin: 1px;
                            border: 1px solid {color}; 
                            border-radius: 10px;  
                            ''')
        #羁绊职业布局
        vbox_jobRace = QVBoxLayout()
        #上面加弹簧
        vbox_jobRace.addStretch()
        #职业job
        jobIds = item['jobIds'].split(',')
        for item_job in jobIds:
            #职业图标
            tp_jb=QLabel()
            # 每一个的布局
            hbox_job = QHBoxLayout()#横向布局
            job_data=jobId_get_data(job, item_job)
            jbPath = Path_job+job_data['alias']
            # 让图像适应标签
            tp_jb.setStyleSheet('tp_jb')
            tp_jb.setScaledContents(True)
            tp_jb.setPixmap(QPixmap(jbPath))
            tp_jb.setMaximumSize(20, 20)
            tp_jb.setMinimumSize(20, 20)
            tp_jb.setToolTip(f'''<b style='color:#FFFFFF;'>{job_data['introduce']}<br>{str(job_data['level']).replace('{','').replace('}','').replace(',','<br>')}</b>''' )

            hbox_job.addWidget(tp_jb)#将图标放入布局中
            name = QLabel(job_data['name'])
            name.setToolTip(
                f'''<b style='color:#FFFFFF;'>{job_data['introduce']}<br>{str(job_data['level']).replace('{', '').replace('}', '').replace(',', '<br>')}</b>''')

            hbox_job.addWidget(name)#然后把羁绊名字放入布局
            # 尾部加上弹簧让羁绊靠左显示
            hbox_job.addStretch()
            #每一行数据放入总职业羁绊布局中
            vbox_jobRace.addLayout(hbox_job)
        #尾部加上弹簧让羁绊靠左显示
        hbox_job.addStretch()

        # 羁绊特质race
        raceIds = item['raceIds'].split(',')
        for item_race in raceIds:
            # 职业图标
            tp_race = QLabel()
            # 每一个的布局
            hbox_race = QHBoxLayout()  # 横向布局
            race_data = raceId_get_data(race, item_race)
            racePath = Path_race + race_data['alias']
            # 让图像适应标签
            tp_race.setStyleSheet('tp_race')
            tp_race.setScaledContents(True)
            tp_race.setPixmap(QPixmap(racePath))
            tp_race.setMaximumSize(20, 20)
            tp_race.setMinimumSize(20, 20)
            tp_race.setToolTip(
                f'''<b style='color:#FFFFFF;'>{race_data['introduce']}<br>{str(race_data['level']).replace('{', '').replace('}', '').replace(',', '<br>')}</b>''')


            hbox_race.addWidget(tp_race)  # 将图标放入布局中
            name = QLabel(race_data['name'])
            name.setToolTip(
                f'''<b style='color:#FFFFFF;'>{race_data['introduce']}<br>{str(race_data['level']).replace('{', '').replace('}', '').replace(',', '<br>')}</b>''')

            hbox_race.addWidget(name)  # 然后把羁绊名字放入布局
            # 尾部加上弹簧让羁绊靠左显示
            hbox_race.addStretch()
            # 每一行数据放入总职业羁绊布局中
            vbox_jobRace.addLayout(hbox_race)



        #将总布局设置在英雄背景上方
        tp1.setLayout(vbox_jobRace)


        #名称和名字以及金币
        title=QLabel(item['title'])
        title.setObjectName('title')
        displayName = QLabel(item['displayName'])
        displayName.setObjectName('displayName')
        price = QLabel(item['price']+'金币')
        price.setObjectName('price')
        title.setAlignment(Qt.AlignCenter)
        displayName.setAlignment(Qt.AlignCenter)
        price.setAlignment(Qt.AlignCenter)
        #加入布局中
        gbox.addWidget(tp1,0,0,1,3)
        gbox.addWidget(title, 1, 0)
        gbox.addWidget(displayName, 1, 1)
        gbox.addWidget(price, 1, 2)
        gbox.setContentsMargins(0,0,0,3)
        hero_frame.setLayout(gbox)
        #将每一个英雄载入进表格中

        heroFormUI.tabHero.setCellWidget(y,x,hero_frame)
        heroFormUI.tabHero.setColumnWidth(x, 208)  # 设置某列的宽度
        heroFormUI.tabHero.setRowHeight(y, 130)#设置某行的宽度

#主要界面初始化
def mainWindowInitialize():

    '''
    界面初始化
    :return:
    '''
    mainWindow.move(0, 0)
    mainWindow.setWindowTitle('自用拿牌 www.52pojie.cn')
    ui.horizontalLayout.setContentsMargins(0,0,1,0)
    mainWindow.resize(500, 40)
    mainWindow.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    mainWindow.setAttribute(Qt.WA_TranslucentBackground)#窗口透明
    # 绑定事件
    ui.bt_zdlb.clicked.connect(buttonClick)
    ui.bt_gfzr.clicked.connect(buttonClick)
    ui.bt_yx.clicked.connect(buttonClick)
    ui.bt_ds.clicked.connect(buttonClick)
    ui.bt_zb.clicked.connect(buttonClick)
    ui.bt_gb.clicked.connect(buttonClick)

    ui.bt_zdlb.setToolTip('<b>提示:</b><br>1.支持多选和Ctrl+A全选,选中多个后可以按Del键删除<br>2.双击删除指定英雄<br>3.点击英雄左上方的灯泡可以暂时不点它')
def straFormInitialize():
    # 加载攻略栏目
    straFormUI.horizontalLayout.setContentsMargins(0, 0, 0, 0)
    straForm.setCursor(QCursor(Qt.PointingHandCursor))
    straForm.resize(504, 40)
    straForm.move(app.desktop().screenGeometry().width()-straForm.geometry().width(), 0)
    straForm.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    straForm.setAttribute(Qt.WA_TranslucentBackground)#窗口透明
    #绑定栏目按钮功能
    straFormUI.bt_spjz.clicked.connect(showShouPaiJieZou)
    straFormUI.bt_zrzw.clicked.connect(showZhengRongZW)
    straFormUI.bt_zqgd.clicked.connect(showZaoQiGD)
    straFormUI.bt_zbfx.clicked.connect(showZhuangBeiFX)

    straFormUI.bt_qrzd.clicked.connect(updataAutoChess)
def squadListInitialize():
    '''
    界面初始化
    :return:
    '''
    # 加载官方列表
    squadList.resize(740, 240)


    squadList.setCursor(QCursor(Qt.PointingHandCursor))
    squadListUI.verticalLayout.setContentsMargins(0, 0, 0, 0)
    squadList.move(0, mainWindow.geometry().height())
    squadList.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    squadList.setAttribute(Qt.WA_TranslucentBackground)#窗口透明
    # 禁止编辑
    squadListUI.tabZhengR.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 整行选择
    squadListUI.tabZhengR.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 水平表格头显示和隐藏
    squadListUI.tabZhengR.horizontalHeader().setVisible(False)
    # 垂直表格头显示和隐藏
    squadListUI.tabZhengR.verticalHeader().setVisible(False)
    # 隐藏横向滚动条
    squadListUI.tabZhengR.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # 隐藏分割线
    squadListUI.tabZhengR.setShowGrid(False)
    #绑定点击事件槽
    squadListUI.tabZhengR.clicked.connect(tablistClick)
def zdListInitialize():
    '''
    界面初始化
    :return:
    '''
    # 加载自动列表
    zdlistForm.resize(566, 30)
    #鼠标
    zdlistForm.setCursor(QCursor(Qt.PointingHandCursor))
    #位置
    zdlistForm.move(0, mainWindow.geometry().height())
    #去掉标题和置顶
    zdlistForm.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    #窗口透明
    zdlistForm.setAttribute(Qt.WA_TranslucentBackground)
    zdlistUI.tabZDlist.setContentsMargins(0, 0, 0, 0)
    # 禁止编辑
    zdlistUI.tabZDlist.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 水平表格头显示和隐藏
    zdlistUI.tabZDlist.horizontalHeader().setVisible(False)
    # 垂直表格头显示和隐藏
    zdlistUI.tabZDlist.verticalHeader().setVisible(False)
    #隐藏分割线
    zdlistUI.tabZDlist.setShowGrid(False)
    #绑定双击事件 删除一列数据
    zdlistUI.tabZDlist.doubleClicked.connect(double_click_Hero_remove)
    #重新键盘事件
    zdlistUI.tabZDlist.keyReleaseEvent=keyReleaseEvent_zd
    #从文件中加载之前的记录
    try:
        with open('data/zdlist.ini', 'r') as f:
            clist = f.read().split()
        zdlistLoading(clist)
        atpc.chess = clist
        print('目前的自动列表:',atpc.chess)
    except:
        pass
def heroFormInitialize():
    '''
    界面初始化
    :return:
    '''
    # 加载自动列表
    heroForm.resize(566, 500)

    #鼠标
    heroForm.setCursor(QCursor(Qt.PointingHandCursor))
    #去掉标题和置顶
    heroForm.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    #窗口透明
    heroForm.setAttribute(Qt.WA_TranslucentBackground)
    heroFormUI.verticalLayout.setContentsMargins(1, 0, 1, 0)

    # 禁止编辑
    heroFormUI.tabHero.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 水平表格头显示和隐藏
    heroFormUI.tabHero.horizontalHeader().setVisible(False)
    # 垂直表格头显示和隐藏
    heroFormUI.tabHero.verticalHeader().setVisible(False)
    #隐藏分割线
    heroFormUI.tabHero.setShowGrid(False)
    #绑定双击事件
    heroFormUI.tabHero.doubleClicked.connect(double_click_Hero_Add)
    #动态加载筛选条件控件
    # -----------------费用
    #设置一些边框距离.
    heroFormUI.hbox_price.setContentsMargins(20, 20, 0, 0)
    heroFormUI.hbox_job.setContentsMargins(20, 20, 0, 0)
    heroFormUI.hbox_race.setContentsMargins(20, 20, 0, 0)
    price = ['全部', '1金币', '2金币', '3金币', '4金币', '5金币']
    for item in price:
        rb_price = QRadioButton(item)
        # 绑定事件槽  并且传递一个参数,用来标记,是什么类型的条件
        rb_price.toggled.connect(lambda: rb_click('price'))
        if item == '全部':  # 第一个为全部
            rb_price.setChecked(True)
        heroFormUI.hbox_price.addWidget(rb_price)

    led_keyword = QLineEdit()
    heroFormUI.hbox_price.addWidget(led_keyword)
    pb_sosuo=QPushButton('搜索')
    heroFormUI.hbox_price.addWidget(pb_sosuo)
    # 尾部增加一个弹簧占位置
    heroFormUI.hbox_price.addStretch()

    # -----------------职业
    rb_job = QRadioButton('全部')  # 第一个为全部
    # 绑定事件槽
    rb_job.toggled.connect(lambda: rb_click('job'))
    rb_job.setChecked(True)
    heroFormUI.hbox_job.addWidget(rb_job)
    for item in job:
        rb_job = QRadioButton(item['name'])
        # 绑定事件槽
        rb_job.toggled.connect(lambda: rb_click('job'))
        heroFormUI.hbox_job.addWidget(rb_job)
    heroFormUI.hbox_job.addStretch()

    # -----------------羁绊
    rb_race = QRadioButton('全部')  # 第一个为全部
    # 绑定事件槽
    rb_race.toggled.connect(lambda: rb_click('race'))
    rb_race.setChecked(True)
    heroFormUI.hbox_race.addWidget(rb_race)
    for item in race:
        rb_race = QRadioButton(item['name'])
        # 绑定事件槽
        rb_race.toggled.connect(lambda: rb_click('race'))
        heroFormUI.hbox_race.addWidget(rb_race)
    #尾部加上弹簧.布局
    heroFormUI.hbox_race.addStretch()
    #将搜索按钮的单击事件绑定
    pb_sosuo.clicked.connect(lambda: rb_click('keyword'))
    led_keyword.editingFinished.connect(lambda: bjk_editing(led_keyword))
def equipFormInitialize():

    equipForm.setContentsMargins(0,0,0,0)
    equipForm.setCursor(QCursor(Qt.PointingHandCursor))
    equipForm.setWindowFlags(Qt.Tool | Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    equipForm.setAttribute(Qt.WA_TranslucentBackground)  # 窗口透明
    equipForm.move(0, mainWindow.height())



#攻略组件
def showShouPaiJieZou():
    global zbfxFrom,zrzwFrom,zqgdFrom,spjzFrom
    # ----------搜牌节奏-克制分析------------------
    if spjzFrom!='':
        if spjzFrom.isVisible() :
            spjzFrom.setVisible(False)
            return


    if dangqianData!='':
        spjzFrom = Form_souPaiJieZou.SoPaiJieZou(dangqianData)
        try:
            zbfxFrom.setVisible(False)
        except:
            pass
        try:  # 把其它的界面先隐藏掉
            zrzwFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass
        try:  # 把其它的界面先隐藏掉
            zqgdFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass

        spjzFrom.setCursor(QCursor(Qt.PointingHandCursor))
        spjzFrom.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        spjzFrom.setAttribute(Qt.WA_TranslucentBackground)
        spjzFrom.show()
        spjzFrom.move(app.desktop().screenGeometry().width() - spjzFrom.geometry().width(),straForm.geometry().height() )
def showZhengRongZW():
    global zbfxFrom,zrzwFrom,zqgdFrom,spjzFrom
    # ----------阵容站位------------------

    if zrzwFrom != '':
        if zrzwFrom.isVisible():
            zrzwFrom.setVisible(False)
            return
    if dangqianData!='':
        zrzwFrom = Form_zhengrongZW.ZhengRongZW(dangqianData, chess,job,race)
        try:
            zbfxFrom.setVisible(False)
        except:
            pass
        try:
            zqgdFrom.setVisible(False)
        except:
            pass
        try:
            spjzFrom.setVisible(False)
        except:
            pass


        zrzwFrom.setCursor(QCursor(Qt.PointingHandCursor))
        zrzwFrom.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        zrzwFrom.setAttribute(Qt.WA_TranslucentBackground)
        zrzwFrom.show()
        zrzwFrom.move(app.desktop().screenGeometry().width() - zrzwFrom.geometry().width(),straForm.geometry().height() )
def showZaoQiGD(kg=False):
    global zbfxFrom,zrzwFrom,zqgdFrom,spjzFrom
    # ----------早期过渡------------------
    # 如果不是列表里直接点过来的,不需要重新创建界面 只需要可视和不可视操作
    if kg != True:
        if zqgdFrom!='':
            if zqgdFrom.isVisible() :#如果已经有了
                zqgdFrom.setVisible(False)
                #当自己关闭的时候,,要把下方的装备分析的位置放上来
                zbfxFrom.move(app.desktop().screenGeometry().width() - zbfxFrom.geometry().width(),
                              straForm.geometry().height())
                return
    # 如果不是列表里点进来的.则分析一下情况
    if dangqianData!='':#如果数据正常的话继续执行
        #创建窗口
        zqgdFrom = Form_zaoqiGD.ZhaoQiGD(dangqianData, chess,job,race)
        try:#把其它的界面先隐藏掉
            if kg != True:
                zbfxFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass
        try:  # 把其它的界面先隐藏掉
            zrzwFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass
        try:  # 把其它的界面先隐藏掉
            spjzFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass


        #正常初始化设置
        #设置鼠标为手
        zqgdFrom.setCursor(QCursor(Qt.PointingHandCursor))
        # 设置窗口无边框置顶
        zqgdFrom.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 设置窗口透明
        zqgdFrom.setAttribute(Qt.WA_TranslucentBackground)
        # 要先显示出来,具体原因,没搞懂,,不然会偏移很多位置
        zqgdFrom.show()
        # 设置位置
        zqgdFrom.move(app.desktop().screenGeometry().width() - zqgdFrom.geometry().width(),straForm.geometry().height())

def showZhuangBeiFX(kg=False):
    global zbfxFrom,zrzwFrom,zqgdFrom,spjzFrom
    # ----------装备分析------------------
    if kg!=True:
        if zbfxFrom!='':
            if zbfxFrom.isVisible() :
                zbfxFrom.setVisible(False)
                return
    if dangqianData!='':
        zbfxFrom = Form_zhuanbeiFX.ZhuangGeiFX(dangqianData, chess, job, race, equip)
        zbfxFrom.setCursor(QCursor(Qt.PointingHandCursor))
        zbfxFrom.setWindowFlags(Qt.Tool|Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        zbfxFrom.setAttribute(Qt.WA_TranslucentBackground)
        zbfxFrom.show()
        #判断站位窗口是否被打开
        try:
            if kg != True:
                zqgdFrom.setVisible(False)
        except:
            pass
        try:  # 把其它的界面先隐藏掉
            zrzwFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass
        try:  # 把其它的界面先隐藏掉
            spjzFrom.setVisible(False)
        except:  # 如果错误就说明别的攻略窗口都没创建,就跳过
            pass
        try:

            if zqgdFrom.isVisible():
                zbfxFrom.move(app.desktop().screenGeometry().width() - zbfxFrom.geometry().width(),
                              straForm.geometry().height()+zqgdFrom.geometry().height())
            else:
                zbfxFrom.move(app.desktop().screenGeometry().width() - zbfxFrom.geometry().width(),
                              straForm.geometry().height() )
        except:
            zbfxFrom.move(app.desktop().screenGeometry().width() - zbfxFrom.geometry().width(),
                          straForm.geometry().height())
if __name__=='__main__':

    #数据初始化和获取--------------------------
    dangqianData=''#当前阵容数据全局占位
    spjzFrom = ''#搜牌节奏窗口全局占位
    zrzwFrom = ''#阵容占位窗口全局占位
    zqgdFrom=''#早期过渡窗口全局占位
    zbfxFrom=''#装备分析窗口全局占位
    heroItems=[]#英雄框数据占位置
    tj_chess=['0','0','0','']#棋子搜索条件初始化
    #全局路径-----------------------------------
    # 检查目录结构,防止错误
    if os.path.isdir(Path_chess) == False:
        os.makedirs(Path_chess)
    if os.path.isdir(Path_chess_D) == False:
        os.makedirs(Path_chess_D)
    if os.path.isdir(Path_equip) == False:
        os.makedirs(Path_equip)
    if os.path.isdir(Path_job) == False:
        os.makedirs(Path_job)
    if os.path.isdir(Path_race) == False:
        os.makedirs(Path_race)
    if os.path.isdir(Path_job2) == False:
        os.makedirs(Path_job2)
    if os.path.isdir(Path_race2) == False:
        os.makedirs(Path_race2)
    #官方阵容 爬取对象-----------------------------
    tft = TFT()
    chess = tft.get_chess()  # 获取所有的棋子数据 返回一个列表
    equip = tft.get_equip()  # 获取所有的装备数据 返回一个列表
    job = tft.get_job()  # 获取所有的职业数据 返回一个列表
    race = tft.get_race()  # 获取所有的羁绊数据 返回一个列表
    downSJ()  # 下载所有数据
    line_list = tft.get_linelist()
    strategyS = []

    ver_info = '0001'  # 附加信息,主要用于查询消费情况 填了更好查询,不填也无所谓
    dictPath = r'1920.txt'  # 字库路径
    processName = 'League of Legends.exe'  # 进程名
    #-------------------界面----------------------------------------------------
    # 创建一个QApplication类的实例 可以看做是屏幕 要有屏幕对象,才能开始画窗口
    app=QApplication(sys.argv)
    #----------mainwindow主窗口------------------
    mainWindow=QMainWindow()#创建一个界面
    ui=MainWindow.Ui_MainWindow()#实例化ui界面对象
    ui.setupUi(mainWindow)#运行里面的代码
    mainWindowInitialize() #初始化赋值
    mainWindow.show() #显示
    #读取注册码---------------------------------
    try:
        with open('大漠注册码.txt', 'r')as f:
            reg_code = f.read()  # 大漠后台的注册码
    except:
        reg_code = ''
        QMessageBox.warning(mainWindow, "警告!", '您的注册码有误!,请确保您在根目录下 大漠注册码.txt中填了正确的注册码')
    # ----------strategyForm攻略选项面板------------------
    straForm = QDialog()  # 创建一个界面
    straFormUI = Form_strategy.Ui_strategyForm()  # 实例化ui界面对象
    straFormUI.setupUi(straForm)  # 运行里面的代码
    straFormInitialize()  # 初始化赋值
    straForm.show()  # 显示
    # ----------hero英雄面板------------------
    heroForm = QDialog()  # 创建一个界面
    heroFormUI = Form_hero.Ui_Form_hero()  # 实例化ui界面对象
    heroFormUI.setupUi(heroForm)  # 运行里面的代码
    heroFormInitialize()  # 初始化赋值
    heroForm.show()  # 显示
    heroForm.setVisible(False)#暂时隐藏  还没存数据呢
    # ----------equip装备面板------------------
    equipForm = Form_zb.ui_zb(equip) # 创建一个界面
    equipFormInitialize()
    equipForm.show()  # 显示
    equipForm.setVisible(False)  # 暂时隐藏  还没存数据呢
    #------------squadList官方阵容--------------------
    squadList = QDialog()
    squadListUI = Form_SquadList.Ui_SquadFrom()
    squadListUI.setupUi(squadList)
    squadListInitialize()
    # ----------------------------------------------------------------------------
    # 创建自动购买棋子对象,然后创建线程启动运行
    atpc = AutoOPlayingChess()
    # ----------自动列表创建出来------------------
    zdlistForm = QDialog()  # 创建一个界面
    zdlistUI = Form_zdlist.Ui_zdlistForm()  # 实例化ui界面对象
    zdlistUI.setupUi(zdlistForm)  # 运行里面的代码
    zdListInitialize()  # 初始化赋值
    zdlistForm.show()  # 显示


    # 登录大漠,免费版的大漠就可以省略这一步
    value = atpc.dmReg(reg_code, ver_info)
    # 设置好字库和配置
    atpc.SetDict(dictPath)
    # 判断是否登录成功
    if value == 1:  # 免费版的就不要这个if了
        print(f'验证成功!')# 接下来就可以自己查接口说明来使用里面的全部方法了
        # 启动自动购买棋子程序线程
        t = threading.Thread(target=atpc.startAuto)
        t.setDaemon(True)
        t.start()
        # 进入程序主循环,并通过exit函数确保主循环安全结束

        sys.exit(app.exec_())
    else:
        if value == -2:
            QMessageBox.warning(mainWindow, "警告!", '进程没有以管理员方式运行或者被第三方杀毒拦截. (建议关闭uac和杀毒软件),请用管理员权限运行本程序!')

        else:
            QMessageBox.warning(mainWindow,  "警告!", f'验证失败,失败代码为:{value},大概率是被杀毒拦截了!')
        app.quit()
        






