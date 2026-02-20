import threading
import tkinter as tk

import key_func
import utils
from global_info import GlobalInfo

root = tk.Tk()
root.title('手的助手👍')
root.geometry("520x350")

# up structure
up_structure = tk.Frame(root)
up_structure.pack()

# left structure, config text show
up_left_structure = tk.Frame(up_structure)
up_left_structure.pack(side=tk.LEFT, padx=10)
config_label = tk.Label(up_left_structure, text="执行配置信息：")
config_label.pack()
config_judge_text = tk.StringVar()
config_judge = tk.Label(up_left_structure, textvariable=config_judge_text, fg='red')
config_judge.pack()
config_text = utils.CustomText(up_left_structure, width=30, height=15)
config_text.pack()
GlobalInfo.config_win = config_text


def on_text_change(event):
    try:
        if type(eval(GlobalInfo.config_win.get('1.0', 'end'))) == dict:
            GlobalInfo.config = eval(GlobalInfo.config_win.get('0.0', 'end'))
            config_judge_text.set(" ")
    except Exception as e:
        config_judge_text.set("请输入正确的配置格式!")
        print(e)


config_text.bind('<<TextModified>>', on_text_change)

# right structure
right_structure = tk.Frame(up_structure)
right_structure.pack(side=tk.RIGHT)

top_show = tk.Frame(right_structure)
top_show.pack(pady=10)
cursor_now_location = tk.Label(top_show, text="当前鼠标位置：", fg="green")
cursor_now_location.pack(side=tk.LEFT)
cursor_now_location_str = tk.StringVar()
GlobalInfo.current_cursor_location = cursor_now_location_str
show_cursor_now_loact_entry = tk.Label(top_show, textvariable=cursor_now_location_str)
show_cursor_now_loact_entry.pack(side=tk.LEFT)

a_select_item = tk.Frame(right_structure)
a_select_item.pack()

index_of_write = tk.Label(a_select_item, text="点击序号：")
index_of_write.grid(row=0, column=0)
str_index_of_write = tk.IntVar()
str_index_of_write.set(1)
index_of_write_input = tk.Entry(a_select_item, textvariable=str_index_of_write)
index_of_write_input.grid(row=0, column=1)

left_or_right = tk.IntVar()
left_or_right.set(1)
left_button = tk.Radiobutton(a_select_item, value=1, variable=left_or_right, text="鼠标左键")
left_button.grid(row=1, column=0)
right_button = tk.Radiobutton(a_select_item, value=2, variable=left_or_right, text="鼠标右键")
right_button.grid(row=1, column=1)

location_label = tk.Label(a_select_item, text="点击位置：")
location_label.grid(row=2, column=0)
str_cursor_location = tk.StringVar()
str_cursor_location.set("0,0")
show_local_input = tk.Entry(a_select_item, textvariable=str_cursor_location)
show_local_input.grid(row=2, column=1)

short_or_long = tk.IntVar()
short_button = tk.Radiobutton(a_select_item, value=0, variable=short_or_long, text="短按")
short_button.grid(row=3, column=0)
long_button = tk.Radiobutton(a_select_item, value=1, variable=short_or_long, text="长按")
long_button.grid(row=3, column=1)

location_label = tk.Label(a_select_item, text="等待时长（秒）：")
location_label.grid(row=4, column=0)
wait_time_sec = tk.DoubleVar()
wait_time_sec.set(1.0)
show_local_input = tk.Entry(a_select_item, textvariable=wait_time_sec)
show_local_input.grid(row=4, column=1)


def get_current_config():
    tmp_config = {'location': str_cursor_location.get(), 'wait_sec': wait_time_sec.get(),
                  'left_or_right': left_or_right.get(), 'short_or_long': short_or_long.get()}
    GlobalInfo.config[str(str_index_of_write.get())] = tmp_config

    GlobalInfo.config_win.delete('1.0', 'end')
    GlobalInfo.config_win.insert(tk.INSERT, GlobalInfo.config)

    str_index_of_write.set(str_index_of_write.get() + 1)


write_button_frame = tk.Frame(right_structure)
write_button_frame.pack()
write_button = tk.Button(write_button_frame, text="配置写入", command=get_current_config)
write_button.pack(pady=15)

# 执行按钮 bottom
bottom_show = tk.Frame(root)
bottom_show.pack(pady=30)
loop_times_lable = tk.Label(bottom_show, text="循环次数：")
loop_times_lable.grid(row=0, column=0)
loop_times_var = tk.IntVar()
loop_times_var.set(1)
GlobalInfo.loop_times = loop_times_var
loop_times_entry = tk.Entry(bottom_show, textvariable=loop_times_var, width=5)
loop_times_entry.grid(row=0, column=1)


def run_for_one():
    root.iconify()
    key_func.do_for_one()


test_button = tk.Button(bottom_show, text="测试一次", command=run_for_one)
test_button.grid(row=0, column=3, padx=10)


def run():
    root.iconify()
    key_func.do()


run_button = tk.Button(bottom_show, text="运行", command=run)
run_button.grid(row=0, column=2)


def write_now_cursor_location(event):
    tmp = GlobalInfo.current_cursor_location.get()
    str_cursor_location.set(tmp)


# bind
root.bind("<Return>", write_now_cursor_location)  # load current cursor location
root.bind("<Escape>", lambda _: root.destroy())  # load current cursor location


def when_close():
    GlobalInfo.keep_config['times'] = loop_times_var.get()
    GlobalInfo.keep_config['text'] = GlobalInfo.config
    utils.write_config(GlobalInfo.keep_config)
    root.destroy()


root.protocol('WM_DELETE_WINDOW', when_close)


def gui_run():
    # show cursor position
    show_cursor_position_thread = threading.Thread(target=utils.where_is_cursor,
                                                   args=(GlobalInfo.iMouse, GlobalInfo.current_cursor_location))
    show_cursor_position_thread.daemon = True
    show_cursor_position_thread.start()

    root.mainloop()


if __name__ == "__main__":
    gui_run()
