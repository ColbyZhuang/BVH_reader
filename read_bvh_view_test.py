# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:42:26 2020

@author: zhuang
"""


import sys
import math
import numpy as np
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

import OpenGL.GL as gl
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *
import time

from motionfeature_bvh import BvhMotionFeature


class GLWidget(QOpenGLWidget):
    music_time_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        for coord in ('x', 'y', 'z', 'cx', 'cy', 'cz', 'rx', 'ry', 'rz'):
            setattr(self, coord, 50 if coord == 'z' else 0)
        
        self.motion_feature = BvhMotionFeature("./test_data/test.bvh", "./test_data/test.bvh")
        self.frame_time = self.motion_feature.frame_time
        self.frame = 0
        self.start_time = time.time()


    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)


    def paintGL(self):
        #if self.frame < len(self.motion_feature.poses)-1:
        self.frame = int((time.time()-self.start_time)*(1./self.frame_time)) % len(self.motion_feature.poses)
        print(self.frame)
        self.drawGrid()
        self.draw_one_frame()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.x, self.y + 8, self.z, self.cx, self.cy, self.cz, 0, 1, 0)

        self.update()



    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def wheelEvent(self, event):
        self.z += -2 if event.angleDelta().y() > 0 else 2

    def mouseMoveEvent(self, event):
        dx, dy = event.x() - self.last_pos.x(), event.y() - self.last_pos.y()
        if event.buttons() == Qt.LeftButton:
            self.x, self.y = self.x - 0.1 * dx, self.y + 0.1 * dy
        elif event.buttons() == Qt.RightButton:
            self.cx, self.cy = self.cx + dx / 50, self.cy + dy / 50
        self.last_pos = event.pos()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side, side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glFrustum(-3.0, +3.0, -1.5, 1.5, 5.0, 60.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -100.0)

    def drawGrid(self):
        gl.glLineWidth(1.0)
        gl.glColor4f(0.4, 0.4, 0.4, 0.5)
        gl.glBegin(gl.GL_LINES)
        g_grid_size = 1.0
        g_unit = 1.0

        for i in range(-15, 16):
            if i == 0:
                continue
            gl.glVertex3f( -15.0 * g_grid_size * g_unit, 0.0, i * g_grid_size * g_unit)
            gl.glVertex3f( 15.0 * g_grid_size * g_unit, 0.0, i * g_grid_size * g_unit)
        for i in range(-15, 16):
            if i == 0:
                continue
            gl.glVertex3f(i * g_grid_size * g_unit, 0.0, -15.0 * g_grid_size * g_unit)
            gl.glVertex3f(i * g_grid_size * g_unit, 0.0, 15.0 * g_grid_size * g_unit)
        gl.glEnd()
        gl.glLineWidth(2.5)

        gl.glColor4f(0.5, 0.5, 1.0, 1.0)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(-15.0 * g_grid_size * g_unit, 0.0, 0.0)
        gl.glVertex3f(15.0 * g_grid_size * g_unit, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, -15.0 * g_grid_size * g_unit)
        gl.glVertex3f(0.0, 0.0, 15.0 * g_grid_size * g_unit)
        gl.glEnd()

    def draw_one_frame(self):
        position, bones_pair = self.motion_feature.get_bvh_motion_pair(self.frame)
        
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor4f(139./255., 71./255., 38./255., 1.0)
        for b_p in bones_pair:
            gl.glVertex3f(0.1 * b_p[0][0], 0.1 * b_p[0][1], 0.1 * b_p[0][2])
            gl.glVertex3f(0.1 * b_p[1][0], 0.1 * b_p[1][1], 0.1 * b_p[1][2])
        glEnd()
        
        glPointSize(5)
        glBegin(GL_POINTS)
        glColor4f(205. / 255., 175. / 255, 149. / 255., 1.0)
        #position = self.motion_feature.one_frame_bone_position(0)
        for i, b_p in enumerate(position):
            gl.glVertex3f(0.1 * b_p[0], 0.1 * b_p[1], 0.1 * b_p[2])
        glEnd()



class Scene_MainWindow(QMainWindow):
    def __init__(self):
        super(Scene_MainWindow, self).__init__()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.glWidget = GLWidget()
        self.pixmapLabel = QLabel()

        self.glWidgetArea = QScrollArea()
        self.glWidgetArea.setWidget(self.glWidget)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setSizePolicy(QSizePolicy.Ignored,
                QSizePolicy.Ignored)
        self.glWidgetArea.setMinimumSize(1600, 1000)


        #music_time = self.createSlider(self.glWidget.set_music_time)
        # ySlider = self.createSlider(self.glWidget.yRotationChanged,
        #         self.glWidget.setYRotation)
        # zSlider = self.createSlider(self.glWidget.zRotationChanged,
        #         self.glWidget.setZRotation)

        self.createActions()
        self.createMenus()

        centralLayout = QGridLayout()
        centralLayout.addWidget(self.glWidgetArea, 0, 0)
        #centralLayout.addWidget(music_time, 1, 0)
        centralWidget.setLayout(centralLayout)

        #xSlider.setValue(0)


        self.setWindowTitle("BVH Reader")
        self.resize(800, 800)

 


    def about(self):
        QMessageBox.about(self, "About Grabber",
                "The <b>Grabber</b> example demonstrates two approaches for "
                "rendering OpenGL into a Qt pixmap.")

    def createActions(self):
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createSlider(self, Position):
        seekSlider = QSlider()
        seekSlider.setMinimum(0)
        seekSlider.setMaximum(270)
        seekSlider.setOrientation(Qt.Horizontal)
        seekSlider.setTracking(False)
        seekSlider.sliderMoved.connect(Position)

        return seekSlider




if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWin = Scene_MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
