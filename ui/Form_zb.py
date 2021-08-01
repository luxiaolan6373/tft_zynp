from PyQt5.QtWidgets import QLabel,QGridLayout,QFrame,QDialog
from PyQt5.QtGui import QPixmap
from setting import*
from goneng import*

class ui_zb(QDialog):
    def __init__(self,equip):
        super().__init__()
        self.equip=equip
        self.initshow()

    def initshow(self):
        cc=40
        self.setObjectName('ZhaoQiGD')
        self.from_kj=QLabel(parent=self)
        self.from_kj.setContentsMargins(0,0,0,0)
        self.from_kj.setObjectName('from_kj')
        self.from_kj.setMinimumSize(600,600)
        # 创建网格布局
        gbox = QGridLayout()
        zb_list=[]
        #小件装备列表
        for i,item in enumerate(self.equip):
            if i>8:
                break
            #把序号存起来
            if item['type'] == '1':
                zb_list.append(item)
                tp_zb_x = QLabel()
                tp_zb_x.setScaledContents(True)
                tp_zb_x.setPixmap(QPixmap(Path_equip+zb_list[-1]['imagePath'].split('/')[-1]))
                tp_zb_x.setMaximumSize(cc, cc)
                tp_zb_x.setMinimumSize(cc, cc)
                tp_zb_x.setToolTip("")
                tp_zb_x.setObjectName('tp_zqgd')
                gbox.addWidget(tp_zb_x, 0, i + 1)

                tp_zb_y = QLabel()
                tp_zb_y.setScaledContents(True)
                tp_zb_y.setPixmap(QPixmap(Path_equip+zb_list[-1]['imagePath'].split('/')[-1]))
                tp_zb_y.setMaximumSize(cc, cc)
                tp_zb_y.setMinimumSize(cc, cc)
                tp_zb_y.setToolTip("")
                tp_zb_y.setObjectName('tp_zqgd')
                if i>8:
                    pass
                else:
                    gbox.addWidget(tp_zb_y, i + 1, 0)

        # 往里面加装备图


        length=len(zb_list)
        for v in range(length):
            for h in range(length-v):
                zbdata=equip_get_dj_Data(self.equip,zb_list[v]['equipId'],zb_list[h+v]['equipId'])
                if zbdata==None:
                    continue
                imgPath=Path_equip+ zbdata['imagePath'].split('/')[-1]
                tp_zb = QLabel()
                tp_zb.setScaledContents(True)
                tp_zb.setPixmap(QPixmap(imgPath))
                tp_zb.setMaximumSize(cc, cc)
                tp_zb.setMinimumSize(cc, cc)
                tp_zb.setToolTip(tanChu_EquipData(self.equip,zbdata))
                tp_zb.setObjectName('tp_zb')
                if v>8:
                    gbox.addWidget(tp_zb,v+1-9,h+v+1)
                else:
                    gbox.addWidget(tp_zb,v+1,h+v+1)

        self.from_kj.setLayout(gbox)

        self.setStyleSheet('''
       QToolTip,#tp_zb{
            border: 1px solid qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));   
	        background-color: rgb(22,26,32);
	        ridge:ridge;
	        padding: 1px;
	        border-radius:2px;
        }
        
        #from_kj{background: rgba(22,26,32, 200);}
        
        #tp_zb:hover{
            border: 2px solid qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.19397 rgba(0, 0, 0, 255), stop:0.202312 rgba(122, 97, 0, 255), stop:0.495514 rgba(76, 58, 0, 255), stop:0.504819 rgba(255, 255, 255, 255), stop:0.79 rgba(255, 255, 255, 255), stop:1 rgba(255, 158, 158, 255));      
	        background-color: rgb(22,26,32);
	        ridge:ridge;
	       
	        border-radius:5px;
        }
      
        
        ''')



