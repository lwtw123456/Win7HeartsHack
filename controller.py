from ui import ControlWindowUi
from heartshack import HeartsHack
from cardselector import CardSelector

class ControlWindow(ControlWindowUi):
    def __init__(self):
        super().__init__()
        self.hack = HeartsHack(self)
        
    def on_switch_change(self, key):
        state = self.switch_vars[key].get()
        name_map = {"free_play":"自由模式","god_mode":"无敌模式","see_all":"透视模式","exposed_hand":"明牌模式","self_define":"自定模式"}
        status = "开启" if state else "关闭"
        is_success = (self.open_card_selector() if state else self.hack.cancel_set_cards()) if key=="self_define" else eval(f"self.hack.{'cancel_'*(not state)}{key}()")
        self.log(f"{name_map[key]}：{status}{'' if is_success else '失败'}")
        state and is_success and key=="self_define" and self.log(f"将在下次发牌时生效！")
        state and is_success and key=="exposed_hand" and self.log(f"将在下次发牌或换牌后生效！")
        not is_success and self.switch_vars[key].set(not state)

    def open_card_selector(self):
        selector = CardSelector(self)
        result = selector.show()
        if result:
            return self.hack.set_cards(result)
        else:
            return False

    def on_win(self):
        if self.hack.win():
            self.log("直接取胜成功！")
        else:
            self.log("直接取胜失败！")
        
if __name__ == "__main__":
    app = ControlWindow()
    app.mainloop()
