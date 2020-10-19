from PyQt5.QtWidgets import QLabel,QVBoxLayout,QDialog,QFrame,QHBoxLayout
from PyQt5.QtGui import QPixmap
from goneng import chessId_get_data,jobId_get_data,raceId_get_data,tanChudataForm
from setting import*
class ZhaoQiGD(QDialog):
    def __init__(self,data,chess,job,race):
        super().__init__()
        self.data=data
        self.chess=chess
        self.job=job
        self.race=race
        self.initshow()
    def initshow(self):
        self.setMinimumWidth(504)
        self.setMaximumWidth(530)
        self.setObjectName('ZhaoQiGD')
        self.spTitle=QLabel('早期过渡')
        self.spTitle.setObjectName('Title')
        self.spDoc=QLabel(self.data['early_info'])
        self.spDoc.setObjectName('Doc')
        self.spDoc.setWordWrap(True)
        #按照顺序加入
        self.vbox=QVBoxLayout()
        self.vbox.addWidget(self.spTitle)
        self.vbox.addWidget(self.spDoc)
        #前期列表------------------------------------------------------------
        self.qqFrame=QFrame()#前期容器
        self.qqHbox=QHBoxLayout()#前期布局

        self.qqtitle=QLabel('前期 >')
        self.qqtitle.setObjectName('Title')
        self.qqHbox.addWidget(self.qqtitle)
        #往里面加图片
        if self.data['early_heros']!='':
            for item in self.data['early_heros'].split(','):
                chessData = chessId_get_data(self.chess, item)
                zwpath = Path_chess+chessData['name']

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
                tp_zqgd = QLabel()
                # 让图像适应标签
                tp_zqgd.setScaledContents(True)
                tp_zqgd.setPixmap(QPixmap(zwpath))
                tp_zqgd.setMaximumSize(50, 50)
                tp_zqgd.setMinimumSize(50, 50)
                tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
                tp_zqgd.setObjectName('tp_zqgd')
                tp_zqgd.setStyleSheet('''#tp_zqgd{border: 1px solid %s;border-radius: 10px;  }
                                ''' % color)

                self.qqHbox.addWidget(tp_zqgd)
            self.qqHbox.addStretch()
            self.qqFrame.setLayout(self.qqHbox)
            self.vbox.addWidget(self.qqFrame)

        # 中期列表-----------------------------------
        self.zqFrame = QFrame()#中期容器
        self.zqHbox = QHBoxLayout()#中期布局
        self.zqtitle = QLabel('中期 >')
        self.zqtitle.setObjectName('Title')
        self.zqHbox.addWidget(self.zqtitle)
        # 往里面加图片
        if self.data['metaphase_heros'] != '':
            for item in self.data['metaphase_heros'].split(','):
                chessData = chessId_get_data(self.chess, item)
                zwpath = Path_chess+chessData['name']
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
                tp_zqgd = QLabel()
                # 让图像适应标签
                tp_zqgd.setScaledContents(True)
                tp_zqgd.setPixmap(QPixmap(zwpath))
                tp_zqgd.setMaximumSize(50, 50)
                tp_zqgd.setMinimumSize(50, 50)
                tp_zqgd.setObjectName('tp_zqgd')
                tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
                tp_zqgd.setStyleSheet('''#tp_zqgd{border: 1px solid %s;border-radius: 10px;  }
                                               ''' % color)

                self.zqHbox.addWidget(tp_zqgd)
            self.zqHbox.addStretch()
            self.zqFrame.setLayout(self.zqHbox)
            self.vbox.addWidget(self.zqFrame)

        # 备选-----------------------------
        self.bxFrame = QFrame()#备选布局
        self.bxHbox = QHBoxLayout()#备选布局
        self.bxtitle = QLabel('备选 >')
        self.bxtitle.setObjectName('Title')
        self.bxHbox.addWidget(self.bxtitle)
        # 往里面加图片
        if self.data['hero_replace'] != '':
            for item in self.data['hero_replace']:
                # 需要备选的英雄
                for bxhero in item['hero_id'].split(','):
                    chessData = chessId_get_data(self.chess, bxhero)
                    zwpath = Path_chess+chessData['name']
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
                    tp_zqgd = QLabel()
                    # 让图像适应标签
                    tp_zqgd.setScaledContents(True)
                    tp_zqgd.setPixmap(QPixmap(zwpath))
                    tp_zqgd.setMaximumSize(50, 50)
                    tp_zqgd.setMinimumSize(50, 50)
                    tp_zqgd.setObjectName('tp_zqgd')
                    tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
                    tp_zqgd.setStyleSheet('''#tp_zqgd{border: 1px solid %s;border-radius: 10px;  }
                                                                    ''' % color)
                    self.bxHbox.addWidget(tp_zqgd)



                # 中间的指针箭头
                tp_jt = QLabel('>')
                tp_jt.setObjectName('Title')
                self.bxHbox.addWidget(tp_jt)

                # 备选英雄replace_heros
                for replace in item['replace_heros'].split(','):
                    chessData = chessId_get_data(self.chess, replace)
                    zwpath = Path_chess+chessData['name']
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
                    tp_zqgd = QLabel()
                    # 让图像适应标签
                    tp_zqgd.setScaledContents(True)
                    tp_zqgd.setPixmap(QPixmap(zwpath))
                    tp_zqgd.setMaximumSize(50, 50)
                    tp_zqgd.setMinimumSize(50, 50)
                    tp_zqgd.setObjectName('tp_zqgd')
                    tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
                    tp_zqgd.setStyleSheet('''#tp_zqgd{border: 1px solid %s;border-radius: 10px;  }
                                                                                ''' % color)

                    self.bxHbox.addWidget(tp_zqgd)
                self.bxHbox.addWidget(QLabel(' '))
            self.bxHbox.addStretch()
            self.bxFrame.setLayout(self.bxHbox)
            self.vbox.addWidget(self.bxFrame)


        # 天选之人--------------------------
        self.txFrame = QFrame()#天选容器
        self.txHbox = QHBoxLayout()#天选布局
        # 往里面加图片
        for item in self.data['hero_location']:
            try:
                if item['isChosenHero'] !=None:
                    #天选羁绊id
                    txData=item['isChosenHero']
                    #天选英雄
                    txchessid=item['hero_id']

                    break
                else:
                    # 没有天选英雄
                    txData = ''
                    txchessid = ''
            except:
                # 没有天选英雄
                txData = ''
                txchessid = ''

        if txData != '':
            txjb=str(txData).replace("'",'').replace("{",'').replace("}",'').replace(" ",'').split(':')

            if   txjb[0]=="job":
                txt=jobId_get_data(self.job, txjb[1])['name']
            else:
                txt = raceId_get_data(self.race, txjb[1])['name']

            self.txtitle = QLabel(f'天选(<b style="color:#E53333;">{txt}</b>) >')
            self.txtitle.setObjectName('Title')
            self.txHbox.addWidget(self.txtitle)
            chessData = chessId_get_data(self.chess, txchessid)
            zwpath = Path_chess+chessData['name']
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
            tp_zqgd = QLabel()
            # 让图像适应标签
            tp_zqgd.setScaledContents(True)
            tp_zqgd.setPixmap(QPixmap(zwpath))
            tp_zqgd.setMaximumSize(50, 50)
            tp_zqgd.setMinimumSize(50, 50)
            tp_zqgd.setObjectName('tp_zqgd')
            tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
            tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
            tp_zqgd.setStyleSheet('''#tp_zqgd{border: 1px solid %s;border-radius: 10px;  }
                                                                ''' % color)
            self.txHbox.addWidget(tp_zqgd)

            replace_chosen_heros=self.data['replace_chosen_heros']
            if replace_chosen_heros != '':
                txjt=QLabel('>')
                txjt.setObjectName('Title')
                self.txHbox.addWidget(txjt)
                for item in replace_chosen_heros.split(','):
                    # 天选备选英雄
                    chessData = chessId_get_data(self.chess, item)
                    zwpath = Path_chess+chessData['name']
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
                    tp_zqgd = QLabel()
                    # 让图像适应标签
                    tp_zqgd.setScaledContents(True)
                    tp_zqgd.setPixmap(QPixmap(zwpath))
                    tp_zqgd.setMaximumSize(50, 50)
                    tp_zqgd.setMinimumSize(50, 50)
                    tp_zqgd.setObjectName('tp_zqgd')
                    tp_zqgd.setToolTip(tanChudataForm(chessData, self.job, self.race))
                    tp_zqgd.setStyleSheet('''#tp_zqgd{border: 1px solid %s;border-radius: 10px;  }
                                                                        ''' % color)
                    self.txHbox.addWidget(tp_zqgd)


            self.txHbox.addStretch()
            self.txFrame.setLayout(self.txHbox)
            self.vbox.addWidget(self.txFrame)
        self.vbox.setSpacing(2)
        self.setLayout(self.vbox)
        self.setStyleSheet('''
        #ZhaoQiGD{
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




