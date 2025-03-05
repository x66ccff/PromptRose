import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QSystemTrayIcon, QMenu, 
                            QDialog, QVBoxLayout, QHBoxLayout, 
                            QListWidget, QListWidgetItem, QLineEdit, 
                            QPushButton, QLabel, QTextEdit, QComboBox)
from PyQt6.QtGui import QIcon, QPainter, QColor, QFont, QPen, QBrush, QAction, QPainterPath, QCursor
from PyQt6.QtCore import Qt, QRectF, QPoint, pyqtSignal, QTimer, QObject, QPointF
import pyperclip
import keyboard
import math
from threading import Lock
import time
import win32clipboard
import win32con
import win32api
import win32gui

class HotkeySignaler(QObject):
    """用于将热键事件从非Qt线程安全传递到Qt主线程"""
    hotkey_pressed = pyqtSignal(str)  # 添加键名作为参数
    hotkey_released = pyqtSignal(str)  # 添加键名作为参数

class PromptWheel(QWidget):
    prompt_selected = pyqtSignal(str)
    
    def __init__(self, prompts):
        super().__init__()
        self.prompts = prompts
        self.selected_index = -1
        self.mouse_pos = QPoint(0, 0)
        self.tracking_timer = QTimer(self)
        self.tracking_timer.timeout.connect(self.update_mouse_position)
        self.tracking_timer.setInterval(10)  # 10ms更新一次鼠标位置
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
    
    def start_tracking(self):
        """开始跟踪鼠标位置"""
        self.center_pos = QCursor.pos()  # 记录显示轮盘时的鼠标位置
        self.tracking_timer.start()
        
    def stop_tracking(self):
        """停止跟踪鼠标位置"""
        self.tracking_timer.stop()
        
    def update_mouse_position(self):
        """更新鼠标位置并计算选择的扇区"""
        if not self.isVisible():
            return
            
        current_pos = QCursor.pos()
        screen_center = QPoint(self.width() // 2, self.height() // 2)
        
        # 计算鼠标相对于中心的位移
        dx = current_pos.x() - screen_center.x()
        dy = current_pos.y() - screen_center.y()
        
        # 仅当鼠标移动足够距离时才更新选择
        if dx*dx + dy*dy > 100:  # 最小距离阈值，可调整
            # 计算角度(弧度)
            angle = math.atan2(dy, dx)
            # 转换为度数
            angle_degrees = math.degrees(angle) % 360
            
            # 根据角度判断选择的提示
            if len(self.prompts) > 0:
                angle_step = 360.0 / len(self.prompts)
                self.selected_index = int(angle_degrees / angle_step)
                self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 半透明背景
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
        
        # 绘制轮盘
        center = QPoint(self.width() // 2, self.height() // 2)
        outer_radius = min(self.width(), self.height()) // 4
        inner_radius = int(outer_radius * 0.7)
        
        # 绘制外圆
        painter.setBrush(QBrush(QColor(30, 30, 30, 200)))
        painter.setPen(QPen(QColor(80, 80, 80, 255), 2))
        painter.drawEllipse(center, int(outer_radius), int(outer_radius))
        
        # 绘制内圆
        painter.setBrush(QBrush(QColor(50, 50, 50, 180)))
        painter.drawEllipse(center, int(inner_radius), int(inner_radius))
        
        # 设置文字样式
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 10)
        font.setBold(True)
        painter.setFont(font)
        
        # 绘制分割线和提示文本
        if len(self.prompts) > 0:
            angle_step = 360.0 / len(self.prompts)
            for i, prompt in enumerate(self.prompts):
                # 计算当前扇区的角度
                start_angle = i * angle_step
                
                # 绘制提示文本
                text_radius = (inner_radius + outer_radius) / 2
                text_angle = (start_angle + angle_step / 2) * math.pi / 180
                text_x = center.x() + text_radius * math.cos(text_angle)
                text_y = center.y() + text_radius * math.sin(text_angle)
                
                # 高亮选中的提示
                if i == self.selected_index:
                    painter.setPen(QColor(255, 200, 0))
                    painter.setBrush(QBrush(QColor(255, 200, 0, 80)))
                    
                    # 绘制高亮扇区
                    path = QPainterPath()
                    path.moveTo(QPointF(center.x(), center.y()))
                    # 修正后的代码：
                    path.arcTo(QRectF(center.x() - outer_radius, center.y() - outer_radius,
                                    outer_radius * 2, outer_radius * 2),
                            - start_angle, -angle_step)  # 已移除"90 -"
                    path.lineTo(QPointF(center.x(), center.y()))
                    painter.drawPath(path)
                else:
                    painter.setPen(QColor(255, 255, 255))
                
                # 绘制提示文本(显示前15个字符)
                display_text = prompt["name"][:15] + "..." if len(prompt["name"]) > 15 else prompt["name"]
                text_rect = QRectF(text_x - 100, text_y - 15, 200, 30)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, display_text)
        
        # 绘制中心文本
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 12)
        font.setBold(True)
        painter.setFont(font)
        center_rect = QRectF(center.x() - inner_radius * 0.7, center.y() - 15, 
                            inner_radius * 1.4, 30)
        painter.drawText(center_rect, Qt.AlignmentFlag.AlignCenter, "LLM Prompt轮盘")
        
    def confirm_selection(self):
        """确认选择并发出信号"""
        if 0 <= self.selected_index < len(self.prompts):
            self.prompt_selected.emit(self.prompts[self.selected_index]["prompt"])
        self.hide()
        self.stop_tracking()
    
    def keyPressEvent(self, event):
        # 处理Esc键关闭轮盘
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
            self.stop_tracking()
        # 处理其他键的默认行为
        super().keyPressEvent(event)
    
    def showEvent(self, event):
        print("轮盘窗口显示事件触发")
        # 重置选中索引
        self.selected_index = -1
        # 开始跟踪鼠标
        self.start_tracking()
        super().showEvent(event)

class SettingsDialog(QDialog):
    """设置对话框，用于配置热键等选项"""
    def __init__(self, settings, save_callback):
        super().__init__()
        self.settings = settings
        self.save_callback = save_callback
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("设置")
        self.setFixedSize(350, 200)
        
        layout = QVBoxLayout()
        
        # 热键选择
        hotkey_layout = QHBoxLayout()
        hotkey_layout.addWidget(QLabel("触发热键:"))
        self.hotkey_combo = QComboBox()
        hotkeys = ["alt", "ctrl", "shift", "ctrl+alt", "alt+shift", "ctrl+shift"]
        self.hotkey_combo.addItems(hotkeys)
        
        # 设置当前选中的热键
        current_hotkey = self.settings.get("hotkey", "alt")
        index = hotkeys.index(current_hotkey) if current_hotkey in hotkeys else 0
        self.hotkey_combo.setCurrentIndex(index)
        
        hotkey_layout.addWidget(self.hotkey_combo)
        layout.addLayout(hotkey_layout)
        
        # 粘贴方式选择
        paste_layout = QHBoxLayout()
        paste_layout.addWidget(QLabel("粘贴方式:"))
        self.paste_combo = QComboBox()
        self.paste_combo.addItems(["直接键盘粘贴", "复制到剪贴板"])
        
        # 设置当前选中的粘贴方式
        paste_method = self.settings.get("paste_method", "直接键盘粘贴")
        self.paste_combo.setCurrentIndex(0 if paste_method == "直接键盘粘贴" else 1)
        
        paste_layout.addWidget(self.paste_combo)
        layout.addLayout(paste_layout)
        
        # 保存按钮
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
    
    def save_settings(self):
        # 保存设置
        self.settings["hotkey"] = self.hotkey_combo.currentText()
        self.settings["paste_method"] = self.paste_combo.currentText()
        self.save_callback(self.settings)
        self.accept()

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
        name_layout.addWidget(QLabel("name:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        edit_layout.addLayout(name_layout)
        
        edit_layout.addWidget(QLabel("prompt content:"))
        self.prompt_edit = QTextEdit()
        edit_layout.addWidget(self.prompt_edit)
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("add")
        self.add_btn.clicked.connect(self.add_prompt)
        buttons_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("update")
        self.update_btn.clicked.connect(self.update_prompt)
        buttons_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("delete")
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

def main():
    # 创建QApplication实例
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 加载或创建提示数据和设置
    data_path = os.path.join(os.path.expanduser("~"), "prompt_wheel_data.json")
    settings_path = os.path.join(os.path.expanduser("~"), "prompt_wheel_settings.json")
    
    def load_prompts():
        try:
            if os.path.exists(data_path):
                with open(data_path, "r", encoding="utf-8") as f:
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
    
    def save_prompts(prompts):
        try:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(prompts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存提示失败: {e}")
    
    def load_settings():
        try:
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                # 默认设置
                return {
                    "hotkey": "alt",
                    "paste_method": "直接键盘粘贴"
                }
        except Exception as e:
            print(f"加载设置失败: {e}")
            return {"hotkey": "alt", "paste_method": "Paste via keyboard"}
    
    def save_settings(settings):
        try:
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")
    
    prompts = load_prompts()
    settings = load_settings()
    
    # 创建提示轮盘
    wheel = PromptWheel(prompts)
    
    # 创建热键信号器
    hotkey_signaler = HotkeySignaler()
    
    # 创建托盘图标
    tray_icon = QSystemTrayIcon()
    # 尝试加载图标，如果找不到则使用默认图标
    try:
        if os.path.exists("icon.png"):
            tray_icon.setIcon(QIcon("icon.png"))
        else:
            # 使用系统默认图标
            tray_icon.setIcon(QIcon.fromTheme("applications-accessories"))
    except Exception as e:
        print(f"加载图标失败: {e}")
    
    tray_icon.setVisible(True)
    
    # 创建托盘菜单
    tray_menu = QMenu()
    
    # 热键状态
    key_pressed = False
    hotkey_lock = Lock()
    
    # 显示函数
    def show_wheel():
        print("正在显示轮盘...")
        # 将轮盘居中显示在鼠标位置
        screen = QApplication.primaryScreen().geometry()
        wheel.setGeometry(0, 0, screen.width(), screen.height())
        wheel.show()
        wheel.raise_()
        wheel.activateWindow()
        print("轮盘显示命令已执行")
    
    # 热键按下处理函数 - 主线程执行
    def on_hotkey_press_in_main_thread(key_name):
        nonlocal key_pressed
        print(f"主线程中处理热键按下: {key_name}")
        with hotkey_lock:
            if (not key_pressed and not wheel.isVisible() and 
                key_name == settings["hotkey"]):
                key_pressed = True
                show_wheel()
    
    # 热键释放处理函数 - 主线程执行
    def on_hotkey_release_in_main_thread(key_name):
        nonlocal key_pressed
        print(f"主线程中处理热键释放: {key_name}")
        with hotkey_lock:
            if (key_pressed and wheel.isVisible() and 
                key_name == settings["hotkey"]):
                key_pressed = False
                wheel.confirm_selection()
    
    # 连接热键信号到主线程处理函数
    hotkey_signaler.hotkey_pressed.connect(on_hotkey_press_in_main_thread)
    hotkey_signaler.hotkey_released.connect(on_hotkey_release_in_main_thread)
    
    # 用于注册的热键处理函数
    registered_hotkeys = []
    
    def register_hotkeys():
        nonlocal registered_hotkeys
        
        # 先清除所有已注册的热键
        keyboard.unhook_all()
        registered_hotkeys = []
        
        # 解析并注册热键
        hotkey = settings["hotkey"]
        print(f"正在注册热键: {hotkey}")
        
        if "+" in hotkey:
            # 组合键，如ctrl+alt
            keys = hotkey.split("+")
            for key in keys:
                registered_hotkeys.append(key)
                # 为每个键注册事件
                keyboard.on_press_key(key, lambda e, k=key: on_hotkey_press(k))
                keyboard.on_release_key(key, lambda e, k=key: on_hotkey_release(k))
        else:
            # 单个键
            keyboard.on_press_key(hotkey, lambda e: on_hotkey_press(hotkey))
            keyboard.on_release_key(hotkey, lambda e: on_hotkey_release(hotkey))
            registered_hotkeys.append(hotkey)
        
        print(f"已注册热键: {registered_hotkeys}")
    
    # 热键按下回调 - 从keyboard线程调用
    def on_hotkey_press(key_name):
        print(f"热键按下 (keyboard线程): {key_name}")
        hotkey_signaler.hotkey_pressed.emit(key_name)
    
    # 热键释放回调 - 从keyboard线程调用
    def on_hotkey_release(key_name):
        print(f"热键释放 (keyboard线程): {key_name}")
        hotkey_signaler.hotkey_released.emit(key_name)
    
    # 注册热键
    try:
        register_hotkeys()
    except Exception as e:
        print(f"注册热键失败: {e}")
    
    # 管理函数
    def show_manager():
        manager = PromptManager(prompts, save_prompts)
        manager.exec()
        # 更新轮盘中的提示
        wheel.prompts = prompts
    
    # 设置函数
    def show_settings():
        dialog = SettingsDialog(settings, save_settings)
        if dialog.exec():
            # 重新注册热键
            register_hotkeys()
    
    # 提示选择处理 - 实现直接粘贴而非复制到剪贴板
    # 提示选择处理 - 实现直接粘贴而非复制到剪贴板
    # 提示选择处理 - 实现直接粘贴而非复制到剪贴板
    # 然后将on_prompt_selected函数改为:
    def on_prompt_selected(prompt_text):
        # 根据设置决定粘贴方式
        if settings["paste_method"] == "直接键盘粘贴":
            try:
                # 将文本放入Windows剪贴板
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(prompt_text, win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                
                # 给一点时间让应用程序准备好
                time.sleep(0.1)
                
                # 模拟Ctrl+V
                win32api.keybd_event(0x11, 0, 0, 0)  # Ctrl键按下
                win32api.keybd_event(0x56, 0, 0, 0)  # V键按下
                win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)  # V键松开
                win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)  # Ctrl键松开
                
                tray_icon.showMessage("提示已粘贴", "提示文本已自动粘贴", QSystemTrayIcon.MessageIcon.Information, 2000)
            except Exception as e:
                print(f"自动粘贴失败: {e}")
                pyperclip.copy(prompt_text)
                tray_icon.showMessage("自动粘贴失败", "已复制到剪贴板，请手动粘贴", QSystemTrayIcon.MessageIcon.Warning, 2000)
        else:
            # 仅复制到剪贴板
            pyperclip.copy(prompt_text)
            tray_icon.showMessage("提示已复制", "提示文本已复制到剪贴板", QSystemTrayIcon.MessageIcon.Information, 2000)
    
    wheel.prompt_selected.connect(on_prompt_selected)
    
    # 创建菜单项
    show_action = QAction("显示轮盘", tray_menu)
    show_action.triggered.connect(show_wheel)
    tray_menu.addAction(show_action)
    
    manage_action = QAction("管理Prompt", tray_menu)
    manage_action.triggered.connect(show_manager)
    tray_menu.addAction(manage_action)
    
    settings_action = QAction("设置", tray_menu)
    settings_action.triggered.connect(show_settings)
    tray_menu.addAction(settings_action)
    
    tray_menu.addSeparator()
    
    exit_action = QAction("退出", tray_menu)
    exit_action.triggered.connect(app.quit)
    tray_menu.addAction(exit_action)
    
    tray_icon.setContextMenu(tray_menu)
    
    # 开始事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
