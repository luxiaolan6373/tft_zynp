from PyQt5.QtWidgets import QLabel,QVBoxLayout,QFrame,QGridLayout,QDialog
from PyQt5.QtGui import QPixmap
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
        self.setMinimumWidth(504)
        self.setMaximumWidth(530)
        self.setObjectName('zhengrongZW')
        self.zrzwTitle=QLabel('阵容站位')
        self.zrzwTitle.setObjectName('Title')
        self.zrzwDoc=QLabel(self.data['location_info'])
        hero_location = self.data['hero_location']
        self.zrzwDoc.setObjectName('Doc')
        self.zrzwDoc.setWordWrap(True)
        #创建站位图
        self.zwbjFrom=QFrame()
        self.zwGFBox=QGridLayout()#创建表格布局
        self.zwGFBox.setContentsMargins(0,0,0,0)
        # 控件间距
        self.zwGFBox.setSpacing(0)
        for i in range(4):

            for j in range(7):
                zw = QLabel(self.zwbjFrom)
                # 让图像适应标签
                zw.setScaledContents(True)
                zwpath = Path_img+'none.png'
                #判断是否有需要填站位的图..如果有就换英雄图
                for item in hero_location:
                    pos=item['location'].split(',')
                    if int(pos[0])-1==i and int(pos[1])-1==j:
                        try:

                            chessData=chessId_get_data(self.chess,item['hero_id'])
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

                if i==1 or i==3:
                    zw.setMaximumSize(67, 50)
                    zw.setMinimumSize(67, 50)
                    zw.setObjectName('jj')

                    if zwpath != Path_img+'none.png':
                        zw.setStyleSheet('''#jj{margin-left: 17px;margin-top: 2px;border: 1px solid %s;border-radius: 10px;  }
                            ''' % color)
                    else:
                        zw.setStyleSheet('''#jj{margin-left: 17px;margin-top: 2px; }
                                                                    ''')
                else:
                    zw.setObjectName('zz')

                    if zwpath != Path_img+'none.png':
                        zw.setStyleSheet('''#zz{margin-left: 0px;margin-top: 2px;border: 1px solid %s;border-radius: 10px;  }
                            ''' % color)
                    else:
                        zw.setStyleSheet('''#zz{margin-left: 0px;margin-top: 2px; }
                                                                    ''')

                self.zwGFBox.addWidget(zw, i, j)





        self.zwbjFrom.setLayout(self.zwGFBox)

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




