#--------------------------------------------------------------------------------------------------
# タイトル：手書きメモボード
# 内容：
#    タッチパネルで使える手書きメモボード
#    ペンの太さと色が選べる
#    保存はまだできない
# 作成者：だいちゃまめ
#--------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.graphics import Color, Line
import sys

# ウィンドウサイズの指定
Window.maximize()
#--------------------------------------------------------------------------------------
# キャンバス描画用ウィジット
#--------------------------------------------------------------------------------------
class DrawCanvas(Widget):
    # 初期処理
    def __init__(self, **kwargs):
        super(DrawCanvas, self).__init__(**kwargs)  
    # 線を描く（始点と終点で線を描く）
    def draw(self,pos_s,pos_e,color,pen_size):
        # キャンバス内であれば、描く
        if((pos_s[1] > self.y+pen_size)*(pos_s[1] < self.y + self.height-pen_size)* \
           (pos_e[1] > self.y+pen_size)*(pos_e[1] < self.y + self.height-pen_size)):
            self.canvas.add(Color(color >> 2 ,color >> 1 & 0x01,color & 0x01))  # 描画色を設定
            self.canvas.add(Line(points=[pos_s[0],pos_s[1],pos_e[0],pos_e[1]],width=pen_size))
    # キャンバス消去
    def clear(self):
        self.canvas.clear()
#--------------------------------------------------------------------------------------
# プログラムの終了ダイアログ
#--------------------------------------------------------------------------------------
class PopupExitDialog(Popup):
    pass
    # プログラム終了
    def exec_exit(self):
       sys.exit()
#--------------------------------------------------------------------------------------
# メインウィジット
#--------------------------------------------------------------------------------------
class MameWidget(Widget):
    points = ListProperty([])   # 位置情報格納用
    select_color = 7            # 選択色
    pen_size = 2                # ペンのサイズ
    # 初期処理
    def __init__(self, **kwargs):
        super(MameWidget, self).__init__(**kwargs)
    # タッチした時の処理
    def on_touch_down(self, touch):
        if super(MameWidget, self).on_touch_down(touch):
             return True
        self.points=(int(touch.pos[0]+1),int(touch.pos[1])) # 終点を1pixelだけずらした
        self.ids.id_drawcanvas.draw(touch.pos,self.points,self.select_color,self.pen_size)
        touch.grab(self)
        return True
    # タッチしたまま移動した時の処理
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.ids.id_drawcanvas.draw(self.points,touch.pos,self.select_color,self.pen_size)
            self.points = touch.pos # 次の始点に設定
            return True
        return super(MameWidget, self).on_touch_move(touch)
    # タッチした状態から離れた時の処理
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.points =touch.pos  # 次の始点に設定
            return True
        return super(MameWidget, self).on_touch_up(touch)
    # 描画色セット
    def set_color(self,color_no):
        self.select_color=color_no
        self.ids.id_lbl.background_color=(color_no >> 2 ,color_no >> 1 & 0x01,color_no & 0x01,1)
    # ペンの太さセット(サイズはkv ファイルで指定)
    def set_pen(self,size):
        self.pen_size=size
        if(size == 2):
            self.ids.id_lbl.text="細"
        else:
            self.ids.id_lbl.text="太"
    # キャンバス初期化
    def clear_canvas(self):
        self.ids.id_drawcanvas.clear()
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()
# アプリの定義
class DrawCanvasApp(App):  
    def __init__(self, **kwargs):
        super(DrawCanvasApp,self).__init__(**kwargs)
        self.title="メモボード"              # ウィンドウタイトル名
# メインの定義
if __name__ == '__main__':
    DrawCanvasApp().run()                   # クラスを指定

Builder.load_file('drawcanvas.kv')          # kvファイル名
