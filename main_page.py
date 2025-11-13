from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DGG
import sys
from panda3d.core import WindowProperties, loadPrcFileData
from panda3d.core import TextNode

loadPrcFileData("", "window-title Buckshot Roulette")
loadPrcFileData("", "default-background-color 0 0 0 1")

class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0)
        self.maximize_window()
        font = self.loader.loadFont("NanumGothic-Regular.ttf")
        self.btn = DirectButton(
            text="종료",
            scale=0.05,
            pos=(0, 0, 0.5),
            frameColor=(0,0,0,0),
            text_fg=(1,1,1,1),
            command=self.exit_app,
            text_font = font
        )
        self.btn.bind(DGG.WITHIN, self.on_mouse_btn)
        self.btn.bind(DGG.WITHOUT, self.off_mouse_btn)
    def exit_app(self):
        sys.exit()
    def on_mouse_btn(self, event):
        self.btn["text_fg"] = (0.38, 0.38, 0.38, 1)
    def off_mouse_btn(self, event):
        self.btn["text_fg"] = (1,1,1,1)

    def maximize_window(self):
        # 화면 해상도 받아오기
        import tkinter as tk
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()

        # Panda3D 창 크기 설정
        props = WindowProperties()
        props.setSize(width, height)
        props.setOrigin(0, 0)
        self.win.requestProperties(props)

app = MainMenu()
app.run()
