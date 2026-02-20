import time

from global_info import GlobalInfo
from utils import detect_mouse_move_to_break


def short_click(now_posi, button_num_int=1):
    x, y = map(int, now_posi.split(","))
    GlobalInfo.iMouse.click(x, y, button=int(button_num_int))


def long_click(now_posi, wait_sec=1, button_num_int=1):
    x, y = map(int, now_posi.split(","))
    GlobalInfo.iMouse.press(x, y, button=int(button_num_int))
    time.sleep(wait_sec)
    GlobalInfo.iMouse.release(x, y, button=int(button_num_int))


def do():
    n = len(GlobalInfo.config)
    for _ in range(GlobalInfo.loop_times.get()):
        for i in range(n):
            index = i + 1
            a_step_config = GlobalInfo.config[str(index)]
            location = a_step_config['location']
            wait_sec = a_step_config['wait_sec']
            left_or_right = a_step_config['left_or_right']
            short_or_long = a_step_config['short_or_long']

            if short_or_long == 0:
                short_click(location, button_num_int=left_or_right)
            else:
                long_click(location, button_num_int=left_or_right)

            time.sleep(wait_sec)
            if detect_mouse_move_to_break(location.split(","), GlobalInfo.iMouse):
                return


def do_for_one():
    n = len(GlobalInfo.config)
    for i in range(n):
        index = i + 1
        a_step_config = GlobalInfo.config[str(index)]
        location = a_step_config['location']
        wait_sec = a_step_config['wait_sec']
        left_or_right = a_step_config['left_or_right']
        short_or_long = a_step_config['short_or_long']

        if short_or_long == 0:
            short_click(location, button_num_int=left_or_right)
        else:
            long_click(location, button_num_int=left_or_right)

        time.sleep(wait_sec)

        if detect_mouse_move_to_break(location.split(","), GlobalInfo.iMouse):
            return
