#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#・プロジェクト：ライフゲーム
#・作成日：2017/01/28
#
#-------------------------------------------------------------------------------

import sys, random, copy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

NUM = 100 #行数（列数）
DEAD = 0 
ALIVE = 1
SIZE = 8 #1セルのサイズ

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.myInit()
    def myInit(self):
        
    
        self.setGeometry(300, 50, 1210, 1210)
        self.setWindowTitle("Life Game")
        
        self.label0 = QLabel("Generation", self)
        self.label0.move(950, 300)
                
        self.generationCounter = QLabel("0", self)
        self.generationCounter.setGeometry(1050, 300, 50, 20)
        
        #---ResetボタンとStartボタンの作成--------------------------------------
        self.btnReset = QPushButton("Reset", self)
        self.btnReset.move(950, 200)
        self.btnReset.clicked.connect(self.ResetGame)
        self.btnStart = QPushButton("Start", self)
        self.btnStart.move(950, 100)
        self.btnStart.clicked.connect(self.StartGame)
        #-----------------------------------------------------------------------
        
        
        #---Speed変更バーとDensity変更バーの作成--------------------------------
        self.label1 = QLabel("Speed", self)
        self.label1.move(950, 370)
        
        self.speed = QSlider(Qt.Horizontal, self)
        self.speed.setRange(0, 990)
        self.speed.setValue(0)
        self.speed.setGeometry(950, 400, 200, 50)
        self.speed.setTickPosition(QSlider.TicksBothSides)
        self.speed.setTickInterval(100)
        self.speed.valueChanged.connect(self.ChangeInterval)
        
        self.label2 = QLabel("Density", self)
        self.label2.move(950, 470)
        
        self.density = QSlider(Qt.Horizontal, self)
        self.density.setRange(0, 19)
        self.density.setValue(15)
        self.density.setGeometry(950, 500, 200, 50)
        self.density.setTickPosition(QSlider.TicksBothSides)
        self.density.setTickInterval(1)
        self.density.valueChanged.connect(self.ChangeDensity)
        #-----------------------------------------------------------------------
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.StartGame)
        self.interval = 1000
        
        self.ChangeDensity()
        self.ResetGame()
        
        #---デバッグ用にターミナルに表示-------------------------------------------------------------------
        for i in range(NUM):
            for j in range(NUM):
                if j != NUM - 1:
                    print(self.nextCell[j][i], end="") #エラー出るけど問題ない、改行せずにprint()する方法
                else:
                    print(self.nextCell[j][i])
        print("")
        #--------------------------------------------------------------------------------------------------
        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(NUM):
            for j in range(NUM):
                if self.nextCell[i][j] == ALIVE: 
                    painter.setBrush(QColor(90, 150, 50))
                    painter.drawRect(10 + i * (SIZE + 1), 10 + j * (SIZE + 1), SIZE ,SIZE)
                else:
                    painter.setBrush(Qt.black)
                    painter.drawRect(10 + i * (SIZE + 1), 10 + j * (SIZE + 1), SIZE ,SIZE)
                    
    def StartGame(self):
        #---各セルについて、周囲のセルの状態を調べて、生きてるセルの数で次世代での状態を決める
        for i in range(1, NUM - 1):
            for j in range(1, NUM - 1):
                self.count = 0
                if self.oldCell[i - 1][j - 1] == ALIVE:
                    self.count += 1
                if self.oldCell[i][j - 1] == ALIVE:
                    self.count += 1
                if self.oldCell[i + 1][j - 1] == ALIVE:
                    self.count += 1
                if self.oldCell[i - 1][j] == ALIVE:
                    self.count += 1
                if self.oldCell[i + 1][j] == ALIVE:
                    self.count += 1
                if self.oldCell[i - 1][j + 1] == ALIVE:
                    self.count += 1
                if self.oldCell[i][j + 1] == ALIVE:
                    self.count += 1
                if self.oldCell[i + 1][j + 1] == ALIVE:
                    self.count += 1
                
                
                if (self.count == 0) or (self.count == 1):
                    self.nextCell[i][j] = DEAD
                elif self.count == 2:
                    continue
                    #self.nextCell[i][j] = self.oldCell[i][j]
                elif self.count == 3:
                    self.nextCell[i][j] = ALIVE
                else:
                    self.nextCell[i][j] = DEAD
        #----------------------------------------------------------------------------------
        self.update()        
        self.oldCell = copy.deepcopy(self.nextCell) #深いコピー
                   
        self.generation += 1
        self.generationCounter.setNum(self.generation) #世代カウントの数値を一つ増やす
        self.timer.start(self.interval) #初回の呼び出し以降は、タイマーのオーバーフローでこのメソッドを呼び出す
        
    def ResetGame(self):
        print("Reset game.")
        
        self.timer.stop()
        self.count = 0
        self.generation = 0
        self.generationCounter.setNum(0)
        self.oldCell = [[DEAD for i in range(NUM)] for j in range(NUM)]
        self.nextCell = [[DEAD for i in range(NUM)] for j in range(NUM)]
        
        for i in range(1, NUM - 1):
            for j in range(1, NUM - 1):
                if self.initDensity != 20:
                    if random.randint(0, self.initDensity) == 1:
                        self.nextCell[i][j] = ALIVE
                else:
                    break
        
        #self.oldCell = self.nextCell[:][:]
        self.oldCell = copy.deepcopy(self.nextCell)
        self.update()
        
    def ChangeInterval(self):
        self.interval = 1000 - self.speed.value()
        
    def ChangeDensity(self):
        self.initDensity = 20 - self.density.value()
        self.ResetGame()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
    
