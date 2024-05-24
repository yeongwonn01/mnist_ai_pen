import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ai_test_updated import *

#PyQt5를 활용한 보드 만들기
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 
class CWidget(QWidget): 
 
    def __init__(self):
 
        super().__init__()
 
        # 전체 폼 박스
        formbox = QHBoxLayout()
        self.setLayout(formbox)
 
        # 좌, 우 레이아웃박스
        left = QVBoxLayout()
        right = QVBoxLayout()
          
        # 우 레이아웃 박스에 그래픽 뷰 추가
        self.view = CView(self)       
        right.addWidget(self.view)        
 
        # 전체 폼박스에 좌우 박스 배치
        formbox.addLayout(left)
        formbox.addLayout(right)
 
        formbox.setStretchFactor(left, 0)
        formbox.setStretchFactor(right, 1)
         
        self.setGeometry(100, 100, 800, 500) 
 
class CView(QGraphicsView):
    
    def __init__(self, parent):
 
        super().__init__(parent)       
        self.scene = QGraphicsScene()        
        self.setScene(self.scene)
 
        self.items = []
         
        self.start = QPointF()
        self.end = QPointF()
 
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        
 
    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)
 
        self.scene.setSceneRect(rect)
 
    def mousePressEvent(self, e):
 
        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.start = e.pos()
            self.end = e.pos()

    # 마우스를 클릭했다면 그림 그리기
    def mouseMoveEvent(self, e):  
         
        # e.buttons()는 정수형 값을 리턴, e.button()은 move시 Qt.Nobutton 리턴 
        if e.buttons() & Qt.LeftButton:           
 
            self.end = e.pos()
            pen = QPen(QColor(0,0,0), 10)

            # Path 이용
            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.scene.addPath(path, pen)
                
            # 시작점을 다시 기존 끝점으로
            self.start = e.pos()
    
    #s 키를 눌렀을 때 화면 캡쳐 저장 후 예측 ( predi() )
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_S:
            screen = app.primaryScreen()
            pixmap = screen.grabWindow(0, x+15,y+15,770,470)
            pixmap.save("check2.png", "PNG")
            predi()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()   
    x = w.x()
    y = w.y()
    w.show()
    sys.exit(app.exec_())
