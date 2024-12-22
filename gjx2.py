from PyQt5 import QtCore, QtGui, QtWidgets
import os
import requests
import zipfile
import shutil
import webbrowser
import json

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化窗口
        self.setWindowTitle("菜盒|菜Games入库工具箱1.1")
        self.resize(800, 600)

        # 设置渐变背景
        self.background_image = None
        self.set_gradient_background()

        # 创建主窗口
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # 顶部标签
        label_top = QtWidgets.QLabel("本软件为菜Games出品，完全免费")
        label_top.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        label_top.setAlignment(QtCore.Qt.AlignCenter)
        label_top.setStyleSheet("color: #2ecc71;")  # 设置字体颜色为浅绿色

        # 右上角背景更换按钮
        self.bg_button = QtWidgets.QPushButton("更换背景")
        self.bg_button.setObjectName("bgButton")
        self.bg_button.clicked.connect(self.change_background_image)
        self.set_button_style(self.bg_button)

        # 侧边栏
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)

        # 主内容区，使用QStackedWidget来管理多个页面
        self.main_content = QtWidgets.QStackedWidget()

        # 整体布局
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.main_content, 1)

        # 顶部和主布局组合
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.addWidget(label_top)
        main_layout.addWidget(self.bg_button, 0, QtCore.Qt.AlignRight)  # 将按钮添加到顶部右侧
        main_layout.addLayout(layout)

        # 创建底部标签
        self.footer_label = QtWidgets.QLabel("作者pvzcxw，如果你有工具引荐，可联系qq3147519214")
        self.footer_label.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Normal))
        self.footer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.footer_label.setStyleSheet("color: #95a5a6;")  # 设置字体颜色为灰色

        # 添加底部标签到布局
        main_layout.addWidget(self.footer_label, 0, QtCore.Qt.AlignBottom)

        # 下载历史记录文件
        self.history_file = 'download_history.json'
        self.download_history = self.load_download_history()

        # 创建侧边栏按钮
        self.pages = {}
        buttons = [
            ("入库辅助", [
                ("One Key", self.get_onekey_latest_url(), "Onekey.exe", "由ikun制作的自动清单下载器，适合小白", False),
                ("one key1.1.0", "https://github.com/ikunshare/Onekey/releases/download/1.1.0/Onekey---1.1.0.exe", "Onekey---1.1.0.exe", "旧版one key，新版闪退报错时使用", False)
            ]),
            ("解锁工具", [
                ("Steam Tools", "https://steamtools.net/res/SteamtoolsSetup.exe", "SteamtoolsSetup.exe", "入库界的大哥，解锁工具的巅峰", False),
                ("Green Luma", "https://github.com/clinlx/CN_GreenLumaGUI/releases/download/v1.2.19/CN_GreenLumaGUI.v1.2.19.36778.zip", "CN_GreenLumaGUI.v1.2.19.36778.zip", "传统的工具，好用与简洁一体", True),
                ("Goldbery", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/GoldbergGUI-0.3.0.7z", "GoldbergGUI-0.3.0.7z", "本人不出名，小弟名天下", False)
            ]),
            ("网站推荐", [
                ("菜玩社区", "https://caigames.cn", None, "新建的社区，综合一体，福利多多", False),
                ("ikun分享", "https://ikunshare.com", None, "ikun的本人论坛，大佬汇聚", False),
                ("Steam Tools论坛", "https://bbs.steamtools.net", None, "tools官方论坛，清单超多，找某种游戏时的首选", False),
                ("70Game", "https://70games.net", None, "顶尖账号分享社区", False),
                ("Sttls", "https://bbs.sttls.cn", None, "老牌清单分享论坛", False),
                ("离线啦", "https://lixianla.com", None, "综合账号分享社区", False)
            ]),
            ("游戏盒子", [
                ("985盒子", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/985hezi.exe", "985hezi.exe", "老牌找号盒子，dszzsl，自费共享账号:caigames密码:985hezinb", False),
                ("Game Box", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/gamebox.exe", "gamebox.exe", "新版gamebox，免费简洁", False),
                ("凡客离线盒子", "http://218p0415c2.zicp.fun:5025/steam.zip", "steam.zip", "凡客新版游戏盒子，自费共享账号:pvzcwx密码:12qwaszx", True) 
            ]),
            ("其它工具", [
                ("Steamless", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/Steamless.v3.1.0.3.-.by.atom0s.zip", "Steamless.v3.1.0.3.-.by.atom0s.zip", "基于GB,解决报错与脱离的工具", False),
                ("SteamAutoCracker", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/steamautocrack.exe", "steamautocrack.exe", "基于GB,解决报错与脱离的工具", False),
                ("SteamLoader", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/steamloader.rar", "steamloader.rar", "基于GB,D加密脱离补丁", False),
                ("cream", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/CreamInstallerGUI.exe", "CreamInstallerGUI.exe", "一款优秀的dlc解锁工具", False),
                ("Mod.Authority", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/Mod.Authority.zip", "Mod.Authority.zip", "steam创意工坊下载工具", True),
                ("sacm", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/sacm.zip", "sacm.zip", "游戏脱离工具", True),
                ("SteamAchievementManager", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/SteamAchievementManager-7.0.25.zip", "SteamAchievementManager-7.0.25.zip", "Steam成就解锁器", True),
                ("vdf下载器", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/vdf.exe", "vdf.exe", "自制的vdf文件下载器", False)
            ]),
            ("各种教程", [
                ("懒人制作教程", "https://github.com/pvzcxw/gjxget/releases/download/gjxget/LANREN.tools.24.8.29.html", "LANREN.tools.24.8.29.html", "懒人制作教程文件", False),
                ("入库常见问题教程|菜玩制作", "https://caigames.cn/thread-434.htm", None, "作者自制教程", False)
            ]),
            ("友情链接", [
                ("ikun作者github", "https://github.com/ikunshare/Onekey", None, "one key作者ikun本人github", False),
                ("one key发布下载页", "https://lanzoui.com/s/Onekey", None, "one key发布页，如软件无法正常下载请点此下载，提取码onekey", False)
            ])
        ]

        # 在侧边栏添加各个功能按钮
        for category, btn_list in buttons:
            btn = QtWidgets.QPushButton(category)
            btn.setObjectName("sidebarButton")
            btn.clicked.connect(lambda _, l=btn_list, c=category: self.show_buttons(l, c))
            self.set_button_style(btn)
            sidebar_layout.addWidget(btn)

        self.show()

    # 设置渐变背景
    def set_gradient_background(self):
        if self.background_image:
            # 使用用户选择的背景图
            self.set_background_image(self.background_image)
        else:
            # 使用渐变背景
            gradient = QtGui.QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QtGui.QColor("#3498db"))  # 从深蓝色开始
            gradient.setColorAt(1, QtGui.QColor("#2ecc71"))  # 渐变到浅绿色

            palette = QtGui.QPalette()
            palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(gradient))
            self.setPalette(palette)

    # 设置背景图片
    def set_background_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.setPalette(palette)

    # 更换背景图片
    def change_background_image(self):
        file_dialog = QtWidgets.QFileDialog(self, "选择背景图片", "", "Images (*.png *.jpg *.bmp)")
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            image_path = file_dialog.selectedFiles()[0]
            self.background_image = image_path
            self.set_gradient_background()

    # 显示相应的按钮列表
    def show_buttons(self, button_list, page_name):
        if page_name in self.pages:
            self.main_content.setCurrentWidget(self.pages[page_name])
        else:
            page = QtWidgets.QFrame()
            layout = QtWidgets.QVBoxLayout(page)

            for btn_text, btn_url, btn_filename, tooltip_text, extract in button_list:
                btn = QtWidgets.QPushButton(btn_text)
                btn.setObjectName("sidebarButton")
                btn.setToolTip(tooltip_text)
                if btn_url and btn_filename:
                    btn.clicked.connect(lambda _, u=btn_url, f=btn_filename, e=extract: self.download_or_open_file(u, f, e))
                elif btn_url:
                    btn.clicked.connect(lambda _, u=btn_url: self.open_web_page(u))
                else:
                    btn.clicked.connect(lambda: self.open_web_page(tooltip_text))
                self.set_button_style(btn)
                layout.addWidget(btn)

            layout.addStretch()
            self.pages[page_name] = page
            self.main_content.addWidget(page)
            self.main_content.setCurrentWidget(page)

    # 加载下载历史记录
    def load_download_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}

    # 保存下载历史记录
    def save_download_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.download_history, f)

    # 检查文件是否已下载
    def is_file_downloaded(self, filename):
        return filename in self.download_history and os.path.exists(self.download_history[filename])

    # 获取OneKey的最新版本URL
    def get_onekey_latest_url(self):
        base_url = "https://github.com/ikunshare/Onekey/releases/download/"
        current_version = self.download_history.get("onekey_version", "1.1.4")
        major, minor, patch = map(int, current_version.split('.'))

        while True:
            next_version = f"{major}.{minor}.{patch + 1}"
            next_url = f"{base_url}{next_version}/Onekey---{next_version}.exe"
            response = requests.head(next_url)
            if response.status_code == 200:
                patch += 1
            else:
                break

        latest_version = f"{major}.{minor}.{patch}"
        latest_url = f"{base_url}{latest_version}/Onekey---{latest_version}.exe"
        self.download_history["onekey_version"] = latest_version
        self.download_history["onekey_url"] = latest_url
        self.save_download_history()
        return latest_url

    # 下载或打开文件
    def download_or_open_file(self, url, filename, extract=False):
        latest_url = self.get_onekey_latest_url() if "Onekey" in filename else url
        if self.is_file_downloaded(filename):
            # 检查是否有新版本
            if url == self.download_history.get("onekey_url"):
                self.open_file(filename)
            else:
                self.download_and_run(latest_url, filename, extract)
        else:
            self.download_and_run(latest_url, filename, extract)

    # 下载并运行文件
    def download_and_run(self, url, filename, extract=False):
        ruku_folder = "ruku"
        if not os.path.exists(ruku_folder):
            os.makedirs(ruku_folder)

        file_path = os.path.join(ruku_folder, filename)

        response = requests.get(url, stream=True)
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

        # 根据文件扩展名处理
        if filename.endswith('.zip') and extract:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(ruku_folder)
            extracted_files = zip_ref.namelist()
            # 查找提取出的 .exe 文件
            exe_files = [f for f in extracted_files if f.endswith('.exe')]
            if exe_files:
                exe_path = os.path.join(ruku_folder, exe_files[0])
                self.download_history[filename] = exe_path
                self.save_download_history()
                os.startfile(exe_path)
        elif filename.endswith('.exe'):
            self.download_history[filename] = file_path
            self.save_download_history()
            os.startfile(file_path)
        elif filename.endswith('.html'):
            # 自动打开 HTML 文件
            os.startfile(file_path)

    # 直接打开已下载的文件
    def open_file(self, filename):
        file_path = self.download_history[filename]
        if os.path.exists(file_path):
            os.startfile(file_path)

    # 打开网页
    def open_web_page(self, url):
        if url:
            webbrowser.open(url)

    # 设置按钮样式及点击效果
    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #27ae60;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)
        button.setAutoFillBackground(True)
        button.pressed.connect(self.animate_button)

    # 按钮点击动画
    def animate_button(self):
        button = self.sender()
        animation = QtCore.QPropertyAnimation(button, b"geometry")
        original_geometry = button.geometry()
        animation.setDuration(100)
        animation.setStartValue(original_geometry)
        animation.setEndValue(original_geometry.adjusted(-5, -5, 5, 5))
        animation.setEasingCurve(QtCore.QEasingCurve.OutBounce)
        animation.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
