from PySide6.QtWidgets import (
    QWidget,
    QApplication, 
    QMainWindow,
    QStyle,
    QFileDialog
)

from PySide6.QtCore import Qt, QStandardPaths, QPoint

from PySide6.QtGui import (
    QPixmap,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QPolygon
)

import circle, rectangle, triangle

class DisplayWidget(QWidget):
    def __init__(self, ed):
        super().__init__()
        self.editor = ed
        self.prev_pos_x = None
        self.prev_pos_y = None
        self.painter = QPainter()
        self.rad = 50
        self.side = 100
        self.side_x = 150
        self.side_y = 50
        self.initUI()
        self.select_size = 10
        
    def initUI(self):        
        self.setWindowTitle("Graphical Editor")
        self.setFixedSize(800, 600)
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill()
        
    def paintEvent(self, event: QPaintEvent):
        with QPainter(self) as painter:
            painter.drawPixmap(0, 0, self.pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        self.prev_pos_x = event.position().x()
        self.prev_pos_y = event.position().y()
        
        found = False
        for obj in list(reversed(self.editor.objects)):
            if obj.dot_inside(self.prev_pos_x, self.prev_pos_y):
                self.editor.selection = obj
                found = True
                break
        if not found:
            self.editor.selection = None
        
        self.draw()
                
        QWidget.mousePressEvent(self, event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        cur_pos_x = event.position().x()
        cur_pos_y = event.position().y()
        if self.editor.selection is not None:
            self.editor.move_object(cur_pos_x, cur_pos_y)
            self.editor.selection.move(cur_pos_x, cur_pos_y)
    
        self.prev_pos_x = cur_pos_x
        self.prev_pos_y = cur_pos_y
        self.draw()
    
    def draw_circle(self, x, y, rad):
        self.painter.begin(self.pixmap)
        self.painter.setBrush(Qt.green)
        self.painter.drawEllipse(x - rad, y - rad, rad * 2, rad * 2)
        self.painter.end()
        
        self.update()
        
    def draw_triangle(self, x, y, side):
        tr = QPolygon()
        tr << QPoint(x, y - side / 3 ** 0.5) << QPoint(x - side / 2, y + side / 2 / 3 ** 0.5) << \
            QPoint(x + side / 2, y + side / 2 / 3 ** 0.5)
        self.painter.begin(self.pixmap)
        self.painter.setBrush(Qt.red)
        self.painter.drawPolygon(tr)
        self.painter.end()
        
        self.update()
        
    def draw_rectangle(self, x, y, side_x, side_y):
        self.painter.begin(self.pixmap)
        self.painter.setBrush(Qt.blue)
        self.painter.drawRect(x - side_x / 2, y - side_y / 2, side_x, side_y)
        self.painter.end()
        
        self.update()
    
    def draw_selected(self, x, y):
        self.painter.begin(self.pixmap)
        self.painter.setBrush(Qt.yellow)
        self.painter.drawEllipse(x - self.select_size, y - self.select_size, self.select_size * 2, self.select_size * 2)
        self.painter.end()
        
        self.update()
        
    def draw(self):
        self.clear()
        for sh in self.editor.objects:
            if isinstance(sh, circle.Circle):
                self.draw_circle(sh.x, sh.y, self.rad)
            elif isinstance(sh, triangle.Triangle):
                self.draw_triangle(sh.x, sh.y, self.side)
            elif isinstance(sh, rectangle.Rectangle):
                self.draw_rectangle(sh.x, sh.y, sh.side_x, sh.side_y)  
        if self.editor.selection is not None:
            self.draw_selected(self.editor.selection.x, self.editor.selection.y)
        
    def clear(self):
        self.pixmap.fill()
        self.update()
        
    def save(self, filename: str):
        self.pixmap.save(filename)
            
class MainWindow(QMainWindow):
    def __init__(self, editor):
        QMainWindow.__init__(self)
        self.display_widget = DisplayWidget(editor)
        self.bar = self.addToolBar("Menu")
        self.bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        self.save_action = self.bar.addAction(
            QApplication.instance().style().standardIcon(QStyle.SP_DialogSaveButton), "Save", self.on_save
        )
        
        self.reset_action = self.bar.addAction(
            QApplication.instance().style().standardIcon(QStyle.SP_DesktopIcon), "Reset", self.on_reset
        )
        
        self.exit_action = self.bar.addAction(
            QApplication.instance().style().standardIcon(QStyle.SP_BrowserStop), "Exit", self.on_exit
        )
        
        self.setCentralWidget(self.display_widget)
        
        self.mime_type_filters = ["image/png", "image/jpeg"]
        
    def on_save(self):
        dialog = QFileDialog(self, "Save File")
        dialog.setMimeTypeFilters(self.mime_type_filters)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("png")
        dialog.setDirectory(
            QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        )
        
        if dialog.exec() == QFileDialog.Accepted:
            if dialog.selectedFiles():
                self.display_widget.save(dialog.selectedFiles()[0])
    
    def on_reset(self):
        self.display_widget.clear()
        self.display_widget.editor.reset()
        
    def on_exit(self):
        self.close()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.display_widget.editor.create_circle(self.display_widget.prev_pos_x, self.display_widget.prev_pos_y, self.display_widget.rad)
            self.display_widget.draw()
        elif event.key() == Qt.Key_2:
            self.display_widget.editor.create_triangle(self.display_widget.prev_pos_x, self.display_widget.prev_pos_y, self.display_widget.side)
            self.display_widget.draw()
        elif event.key() == Qt.Key_3:
            self.display_widget.editor.create_rectangle(self.display_widget.prev_pos_x, self.display_widget.prev_pos_y, self.display_widget.side_x, self.display_widget.side_y)
            self.display_widget.draw()
        elif event.key() == Qt.Key_Delete:
            if self.display_widget.editor.selection is not None:
                self.display_widget.editor.objects.remove(self.display_widget.editor.selection)
                self.display_widget.editor.selection = None
                self.display_widget.draw()