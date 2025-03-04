import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu, 
                            QAction, QDialog, QVBoxLayout, QHBoxLayout, 
                            QListWidget, QListWidgetItem, QLineEdit, 
                            QPushButton, QLabel, QTextEdit)
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPoint, pyqtSignal, QSize
import keyboard
import pyperclip
import math
import tempfile
from PIL import Image, ImageDraw

# 创建一个简单的图标，用于程序没有icon.png时
def create_default_icon():
    try:
        # 确定图标路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是普通Python脚本
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(application_path, "icon.png")
        
        # 如果图标不存在，创建一个
        if not os.path.exists(icon_path):
            img = Image.new('RGBA', (128, 128), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制一个简单的圆形图标
            draw.ellipse((10, 10, 118, 118), fill=(30, 120, 200, 255))
            draw.ellipse((30, 30, 98, 98), fill=(200, 200, 200, 255))
            
            img.save(icon_path)
        
        return icon_path
    except Exception as e:
        print(f"创建图标失败: {e}")
        # 创建临时图标文件
        fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(fd)
        
        img = Image.new('RGBA', (128, 128), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((10, 10, 118, 118), fill=(30, 120, 200, 255))
        img.save(temp_path)
        
        return temp_path

class PromptWheel(QWidget):
    prompt_selected = pyqtSignal(str)
    
    def __init__(self, prompts):
        super().__init__()
        self.prompts = prompts
        self.selected_index = -1
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置轮盘大小
        self.wheel_size = 400
        self.setFixedSize(self.wheel_size, self.wheel_size)
    
    def showAtCursor(self):
        # 获取当前鼠标位置
        cursor_pos = QApplication.desktop().cursor().pos()
        
        # 设置轮盘位置，使其以鼠标为中心
        x = cursor_pos.x() - self.wheel_size // 2
        y = cursor_pos.y() - self.wheel_size // 2
        
        # 确保轮盘完全在屏幕内
        screen = QApplication.primaryScreen().geometry()
        if x < 0:
            x = 0
        elif x + self.wheel_size > screen.width():
            x = screen.width() - self.wheel_size
        
        if y < 0:
            y = 0
        elif y + self.wheel_size > screen.height():
            y = screen.height() - self.wheel_size
        
        self.move(x, y)
        self.show()
        self.updateSelectedSegment()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 半透明背景
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        
        # 绘制轮盘
        center = QPoint(self.width() // 2, self.height() // 2)
        outer_radius = min(self.width(), self.height()) // 2 - 20
        inner_radius = outer_radius * 0.5
        
        # 绘制外圆
        painter.setBrush(QBrush(QColor(30, 30, 30, 200)))
        painter.setPen(QPen(QColor(80, 80, 80, 255), 2))
        painter.drawEllipse(center, outer_radius, outer_radius)
        
        # 绘制内圆
        painter.setBrush(QBrush(QColor(50, 50, 50, 180)))
        painter.drawEllipse(center, inner_radius, inner_radius)
        
        # 设置文字样式
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)
        
        # 绘制分割线和提示文本
        if len(self.prompts) > 0:
            angle_step = 360.0 / len(self.prompts)
            for i, prompt in enumerate(self.prompts):
                # 计算当前扇区的角度
                start_angle = i * angle_step
                
                # 绘制分割线
                painter.setPen(QPen(QColor(100, 100, 100, 150), 1))
                line_angle = start_angle * math.pi / 180
                line_x = center.x() + outer_radius * math.cos(line_angle)
                line_y = center.y() - outer_radius * math.sin(line_angle)
                painter.drawLine(center, QPoint(int(line_x), int(line_y)))
                
                # 高亮选中的提示
                if i == self.selected_index:
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(QColor(255, 200, 0, 80)))
                    
                    # 绘制高亮扇区
                    path = QPainterPath()
                    path.moveTo(center)
                    path.arcTo(QRectF(center.x() - outer_radius, center.y() - outer_radius,
                                      outer_radius * 2, outer_radius * 2),
                              90 - start_angle, -angle_step)  # 注意Qt中角度是逆时针的
                    path.lineTo(center)
                    painter.drawPath(path)
                
                # 绘制提示文本
                painter.setPen(QColor(255, 255, 255) if i != self.selected_index else QColor(255, 220, 0))
                text_angle = (start_angle + angle_step / 2) * math.pi / 180
                text_radius = (inner_radius + outer_radius) * 0.75
                text_x = center.x() + text_radius * math.cos(text_angle)
                text_y = center.y() - text_radius * math.sin(text_angle)
                
                # 绘制提示文本(显示前15个字符)
                display_text = prompt["name"][:15] + "..." if len(prompt["name"]) > 15 else prompt["name"]
                # 计算文本矩形，考虑文本旋转
                font_metrics = painter.fontMetrics()
                text_width = font_metrics.width(display_text)
                text_height = font_metrics.height()
                
                # 保存当前画家状态
                painter.save()
                # 移动到文本位置
                painter.translate(text_x, text_y)
                # 旋转文本，使其垂直于半径
                rotation_angle = 90 - start_angle - angle_step / 2
                if 90 < start_angle + angle_step / 2 < 270:
                    rotation_angle += 180  # 下半部分的文本需要翻转180度以保持可读性
                painter.rotate(rotation_angle)
                # 绘制文本
                painter.drawText(-text_width / 2, text_height / 4, display_text)
                # 恢复画家状态
                painter.restore()
        
        # 绘制中心文本
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        center_rect = QRectF(center.x() - inner_radius * 0.7, center.y() - 15, 
                            inner_radius * 1.4, 30)
        painter.drawText(center_rect, Qt.AlignCenter, "LLM Prompt轮盘")
    
    def updateSelectedSegment(self):
        if len(self.prompts) == 0:
            return
            
        # 获取鼠标相对于轮盘中心的位置
        cursor_pos = self.mapFromGlobal(QApplication.desktop().cursor().pos())
        center = QPoint(self.width() // 2, self.height() // 2)
        
        dx = cursor_pos.x() - center.x()
        dy = center.y() - cursor_pos.y()  # 注意y轴向下为正
        
        # 计算鼠标与中心的距离
        distance = math.sqrt(dx**2 + dy**2)
        outer_radius = min(self.width(), self.height()) // 2 - 20
        inner_radius = outer_radius * 0.5
        
        # 只有鼠标在轮盘环形区域内才计算选择
        if inner_radius < distance < outer_radius:
            # 计算角度(弧度)
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi
                
            # 转换为角度(0-360)
            angle_deg = angle * 180 / math.pi
            
            # 根据角度判断选择的提示
            angle_step = 360.0 / len(self.prompts)
            self.selected_index = int((360 - angle_deg) % 360 / angle_step)
        else:
            self.selected_index = -1
            
        self.update()

class PromptManager(QDialog):
    def __init__(self, prompts, save_callback):
        super().__init__()
        self.prompts = prompts
        self.save_callback = save_callback
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Prompt管理")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # 提示列表
        self.prompt_list = QListWidget()
        self.update_prompt_list()
        layout.addWidget(self.prompt_list)
        
        # 编辑区域
        edit_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("名称:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        edit_layout.addLayout(name_layout)
        
        edit_layout.addWidget(QLabel("提示内容:"))
        self.prompt_edit = QTextEdit()
        edit_layout.addWidget(self.prompt_edit)
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("添加")
        self.add_btn.clicked.connect(self.add_prompt)
        buttons_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("更新")
        self.update_btn.clicked.connect(self.update_prompt)
        buttons_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("删除")
        self.delete_btn.clicked.connect(self.delete_prompt)
        buttons_layout.addWidget(self.delete_btn)
        
        edit_layout.addLayout(buttons_layout)
        
        layout.addLayout(edit_layout)
        
        self.setLayout(layout)
        
        # 连接列表选择信号
        self.prompt_list.itemClicked.connect(self.on_item_selected)
    
    def update_prompt_list(self):
        self.prompt_list.clear()
        for prompt in self.prompts:
            item = QListWidgetItem(prompt["name"])
            self.prompt_list.addItem(item)
    
    def on_item_selected(self, item):
        index = self.prompt_list.row(item)
        prompt = self.prompts[index]
        self.name_edit.setText(prompt["name"])
        self.prompt_edit.setText(prompt["prompt"])
    
    def add_prompt(self):
        name = self.name_edit.text().strip()
        prompt_text = self.prompt_edit.toPlainText().strip()
        
        if name and prompt_text:
            self.prompts.append({
                "name": name,
                "prompt": prompt_text
            })
            self.update_prompt_list()
            self.save_callback(self.prompts)
            self.name_edit.clear()
            self.prompt_edit.clear()
    
    def update_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if selected_items:
            index = self.prompt_list.row(selected_items[0])
            name = self.name_edit.text().strip()
            prompt_text = self.prompt_edit.toPlainText().strip()
            
            if name and prompt_text:
                self.prompts[index] = {
                    "name": name,
                    "prompt": prompt_text
                }
                self.update_prompt_list()
                self.save_callback(self.prompts)
    
    def delete_prompt(self):
        selected_items = self.prompt_list.selectedItems()
        if selected_items:
            index = self.prompt_list.row(selected_items[0])
            del self.prompts[index]
            self.update_prompt_list()
            self.save_callback(self.prompts)
            self.name_edit.clear()
            self.prompt_edit.clear()

class PromptWheelApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 创建资源目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是普通Python脚本
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        # 加载或创建提示数据
        self.data_path = os.path.join(os.path.expanduser("~"), "prompt_wheel_data.json")
        self.prompts = self.load_prompts()
        
        # 获取图标
        icon_path = create_default_icon()
        
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setVisible(True)
        
        # 创建托盘菜单
        self.tray_menu = QMenu()
        
        manage_action = QAction("管理Prompt", self.app)
        manage_action.triggered.connect(self.show_manager)
        self.tray_menu.addAction(manage_action)
        
        exit_action = QAction("退出", self.app)
        exit_action.triggered.connect(self.app.quit)
        self.tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # 创建提示轮盘
        self.wheel = PromptWheel(self.prompts)
        self.wheel.prompt_selected.connect(self.on_prompt_selected)
        
        # 轮盘是否显示
        self.wheel_visible = False
        
        # 设置键盘监听
        try:
            keyboard.on_press_key("ctrl", self.on_ctrl_pressed)
            keyboard.on_release_key("ctrl", self.on_ctrl_released)
        except Exception as e:
            self.tray_icon.showMessage("权限错误", 
                                     "无法监听键盘事件，请以管理员身份运行程序", 
                                     QSystemTrayIcon.Warning, 5000)
            print(f"键盘监听错误: {e}")
        
        # 定时更新选择的段
        self.timer = self.app.startTimer(50)  # 50毫秒更新一次
        
    def timerEvent(self, event):
        if self.wheel_visible and self.wheel.isVisible():
            self.wheel.updateSelectedSegment()
    
    def load_prompts(self):
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # 默认提示
                return [
                    {"name": "翻译为英文", "prompt": "请将以下文本翻译为英文:"},
                    {"name": "总结内容", "prompt": "请用简洁的语言总结以下内容:"},
                    {"name": "代码解释", "prompt": "请解释以下代码的功能和工作原理:"},
                    {"name": "写邮件", "prompt": "请帮我写一封关于以下主题的邮件:"}
                ]
        except Exception as e:
            print(f"加载提示失败: {e}")
            return []
    
    def save_prompts(self, prompts):
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(prompts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存提示失败: {e}")
    
    def on_ctrl_pressed(self, e):
        if not self.wheel_visible:
            self.wheel_visible = True
            self.wheel.showAtCursor()
    
    def on_ctrl_released(self, e):
        if self.wheel_visible:
            self.wheel_visible = False
            self.wheel.hide()
            
            # 如果有选中的提示，执行粘贴操作
            if self.wheel.selected_index >= 0 and self.wheel.selected_index < len(self.prompts):
                prompt_text = self.prompts[self.wheel.selected_index]["prompt"]
                self.paste_prompt(prompt_text)
    
    def paste_prompt(self, prompt_text):
        # 复制到剪贴板
        pyperclip.copy(prompt_text)
        
        # 尝试直接粘贴到当前焦点
        try:
            # 模拟Ctrl+V键盘事件
            keyboard.release('ctrl')  # 确保ctrl已释放
            keyboard.press_and_release('ctrl+v')
            self.tray_icon.showMessage("提示已使用", "提示文本已粘贴到当前位置", QSystemTrayIcon.Information, 2000)
        except Exception as e:
            # 如果粘贴失败，只显示复制成功的消息
            self.tray_icon.showMessage("提示已复制", "提示文本已复制到剪贴板", QSystemTrayIcon.Information, 2000)
            print(f"粘贴失败: {e}")
    
    def on_prompt_selected(self, prompt_text):
        self.paste_prompt(prompt_text)
    
    def show_manager(self):
        manager = PromptManager(self.prompts, self.save_prompts)
        manager.exec_()
    
    def run(self):
        # 显示托盘提示
        self.tray_icon.showMessage("Prompt轮盘已启动", 
                                "按住Ctrl键显示提示轮盘，右键点击托盘图标管理提示",
                                QSystemTrayIcon.Information, 5000)
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = PromptWheelApp()
    app.run()