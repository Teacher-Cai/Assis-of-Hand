import tkinter

from pymouse import PyMouse

import gui
import utils
from global_info import GlobalInfo

# init
GlobalInfo.iMouse = PyMouse()

GlobalInfo.keep_config = utils.load_config()
if GlobalInfo.keep_config.get('text'):
    GlobalInfo.config = GlobalInfo.keep_config['text']
    GlobalInfo.config_win.insert(tkinter.INSERT, GlobalInfo.config)

if GlobalInfo.keep_config.get('times'):
    GlobalInfo.loop_times.set(int(GlobalInfo.keep_config['times']))

# gui
gui.gui_run()
