import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class WeChatAuto(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        title_label = toga.Label(
            '微信消息助手',
            style=Pack(padding=10, font_size=20, font_weight='bold')
        )
        
        message_input = toga.MultilineTextInput(
            placeholder='请输入消息内容...',
            style=Pack(padding=10, flex=1)
        )
        
        send_button = toga.Button(
            '发送消息',
            on_press=lambda widget: self.send_message(message_input.value),
            style=Pack(padding=10, background_color='#007AFF', color='white')
        )
        
        main_box.add(title_label)
        main_box.add(message_input)
        main_box.add(send_button)
        
        self.main_window = toga.MainWindow(title='微信助手', size=(400, 300))
        self.main_window.content = main_box
        self.main_window.show()
    
    def send_message(self, message):
        print(f"准备发送消息: {message}")

def main():
    return WeChatAuto('微信助手', 'com.github.wechatauto')
