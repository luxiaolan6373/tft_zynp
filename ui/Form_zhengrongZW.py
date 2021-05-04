from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from goneng import chessId_get_data,tanChudataForm
from setting import *


class ZhengRongZW(QDialog):
    def __init__(self,data,chess,job,race):
        super().__init__()
        self.data=data
        self.chess=chess
        self.job=job
        self.race=race
        self.initshow()
    def initshow(self):
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)

        self.setObjectName('zhengrongZW')
        self.zrzwTitle=QLabel('阵容站位')
        self.zrzwTitle.setObjectName('Title')
        self.zrzwDoc=QLabel(self.data['location_info'])
        hero_location = self.data['hero_location']
        self.zrzwDoc.setObjectName('Doc')
        self.zrzwDoc.setWordWrap(True)
        #创建站位图
        self.zwbjFrom=QFrame()#站位框架
        self.zwbjFrom.setMinimumWidth(430)
        self.zwbjFrom.setMaximumWidth(430)
        self.zwGFBox=QVBoxLayout(self.zwbjFrom)#创建纵向布局
        self.zwGFBox.setContentsMargins(0,0,0,5)#边距
        self.zwGFBox.setSpacing(5)# 控件间距
        self.zwHBoxs=[]#横向的
        for i in range(4):
            qvbox=QHBoxLayout()
            qvbox.setContentsMargins(0,0,0,0)
            qvbox.setSpacing(10)
            self.zwHBoxs.append(qvbox)
            if i==1 or i==3:
                spacerItem = QSpacerItem(25, 10)
                qvbox.addItem(spacerItem)

            for j in range(7):
                zw = QLabel()
                # 让图像适应标签
                zw.setScaledContents(True)
                zwpath = Path_img+'none.png'
                #判断是否有需要填站位的图..如果有就换英雄图
                for item in hero_location:
                    pos=item['location'].split(',')
                    if int(pos[0])-1==i and int(pos[1])-1==j:
                        try:
                            if item['hero_id'] == "wolf":  # 如果是随从
                                chessData = {}
                                chessData['name'] = 'wolf.jpg'
                                chessData['title'] = '狼灵'
                                chessData['displayName'] = 'wolf'
                                chessData['price'] = '1'
                                chessData['skillName'] = '无'
                                chessData['skillIntroduce'] = '无'
                            elif item['hero_id'] == "drogon":
                                chessData = {}
                                chessData['name'] = 'dragon.jpg'
                                chessData['title'] = '龙宝宝'
                                chessData['displayName'] = 'dragon'
                                chessData['price'] = '1'
                                chessData['skillName'] = '无'
                                chessData['skillIntroduce'] = '无'
                            else:
                                chessData=chessId_get_data(self.chess,item['hero_id'])
                            if chessData==None:
                                continue
                        except:
                            continue
                        zw.setToolTip(tanChudataForm(chessData, self.job, self.race))
                        zwpath=Path_chess+chessData['name']
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
                        break
                zw.setPixmap(QPixmap(zwpath))
                zw.setMaximumSize(50, 50)
                zw.setMinimumSize(50, 50)
                zw.setObjectName('jj')
                if i==1 or i==3:
                    if zwpath != Path_img+'none.png':
                        zw.setStyleSheet('''#jj{margin-top: 2px;border: 1px solid %s;border-radius: 10px;  }''' % color)
                    else:
                        zw.setStyleSheet('''#jj{margin-top: 2px; }''')
                else:
                    zw.setObjectName('zz')
                    if zwpath != Path_img+'none.png':
                        zw.setStyleSheet('''#zz{margin-top: 2px;border: 1px solid %s;border-radius: 10px;  }''' % color)
                    else:
                        zw.setStyleSheet('''#zz{margin-top: 2px; }''')
                self.zwHBoxs[-1].addWidget(zw)
            if i==0 or i==2:
                spacerItem = QSpacerItem(30, 10)
                self.zwHBoxs[-1].addItem(spacerItem)
            self.zwGFBox.addLayout(self.zwHBoxs[-1])
        self.hbox=QVBoxLayout()
        self.hbox.addWidget(self.zrzwTitle)
        self.hbox.addWidget(self.zwbjFrom)
        self.hbox.addWidget(self.zrzwDoc)
        self.hbox.setSpacing(2)
        self.setLayout(self.hbox)
        self.setStyleSheet('''
        #zhengrongZW{
            border: 1px solid rgb(185, 185, 185);  
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




