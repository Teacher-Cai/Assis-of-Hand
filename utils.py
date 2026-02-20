# little func
import json
import os
import time
import tkinter as tk


def where_is_cursor(mouse, hook):
    """

    :param mouse: instance of pymouse
    :return: tuple, x,y
    """
    while True:
        time.sleep(0.1)
        posi = ",".join(map(str, mouse.position()))
        hook.set(posi)


def detect_mouse_move_to_break(give_me_a_position, mouse):
    time.sleep(0.05)
    x, y = mouse.position()
    if int(give_me_a_position[0]) != x or int(give_me_a_position[1]) != y:
        print("detect mouse move, stop!", give_me_a_position, x, y)
        return True


def load_config():
    if os.path.exists('assist_of_hand.config'):
        with open('assist_of_hand.config', 'r') as f:
            config = f.read()
        if config:
            return json.loads(config)
        else:
            return {}
    else:
        return {}


def write_config(json_file):
    with open('assist_of_hand.config', 'w') as f:
        f.write(json.dumps(json_file))


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """自定义多行文本框类，可实时监控变化事件"""
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + '_orig'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        if command == 'get' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return
        if command == 'delete' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if command in ('insert', 'delete', 'replace'):
            self.event_generate('<<TextModified>>')
        return result
