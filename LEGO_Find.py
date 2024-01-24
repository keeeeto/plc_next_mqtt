import Mqtt_Tag as mt
import tkinter as tk
import threading
import time


def change_color(new_color):
    global color, call_state
    color.set(new_color)
    selected_color = color.get()
    print("Selected color:", selected_color)
    tag.SetCallState(0)
    update_call_state()
    call_state.set(tag.GetCallState())


def update_call_state():
    global call_state_label, call_state, tag

    if call_state.get() == 1:
        call_state_label.config(text="呼び出し中")
    else:
        call_state_label.config(text="待機中")


def MqttTask(stop_event):
    global color
    global tag
    global call_state
    tag = mt.Mqtt_Tag("mqtt-tag-server", 1883)
    tag.Mqtt_start()
    while not stop_event.is_set():
        # print("Mqttタスクが実行されました")
        if (not tag.GetCallState() and color.get() != ""):
            tag.CallProductCode(color.get())
            color.set("")
        time.sleep(0.5)
        call_state.set(tag.GetCallState())
        update_call_state()

# Tkinter GUIの作成


def create_gui(stop_event):
    global color, call_state, call_state_label

    gui_root = tk.Tk()
    gui_root.title("Mqtt Tag")

    label_instruction = tk.Label(
        gui_root, text="Click the color you want to call", font=("Helvetica", 14))
    label_instruction.grid(row=1, column=0, columnspan=6, pady=10)

    color = tk.StringVar()
    color.set("")

    call_state = tk.IntVar()
    call_state.set(0)  # 初期値は待機中

    button_red = tk.Button(
        gui_root, text="Red", command=lambda: change_color("Red"), bg="red", width=10)
    button_blue = tk.Button(gui_root, text="Blue", command=lambda: change_color(
        "Blue"), bg="blue", width=10)
    button_green = tk.Button(gui_root, text="Green", command=lambda: change_color(
        "Green"), bg="green", width=10)
    button_yellow = tk.Button(gui_root, text="Yellow", command=lambda: change_color(
        "Yellow"), bg="yellow", width=10)
    button_black = tk.Button(gui_root, text="Black", command=lambda: change_color(
        "Black"), bg="black", fg="white", width=10)
    button_white = tk.Button(gui_root, text="White", command=lambda: change_color(
        "White"), bg="white", width=10)

    button_red.grid(row=0, column=0, padx=10, pady=10)
    button_blue.grid(row=0, column=1, padx=10, pady=10)
    button_green.grid(row=0, column=2, padx=10, pady=10)
    button_yellow.grid(row=0, column=3, padx=10, pady=10)
    button_black.grid(row=0, column=4, padx=10, pady=10)
    button_white.grid(row=0, column=5, padx=10, pady=10)

    # ウィンドウが閉じられたときのイベントハンドラを追加
    gui_root.protocol("WM_DELETE_WINDOW",
                      lambda: on_closing(gui_root, stop_event))

    # 呼び出し状態を表示するラベル
    call_state_label = tk.Label(gui_root, text="待機中", font=("Helvetica", 14))
    call_state_label.grid(row=2, column=0, columnspan=6, pady=10)
    update_call_state()

    # Mqttタスクを開始
    mqtt_thread = threading.Thread(target=MqttTask, args=(stop_event,))
    mqtt_thread.start()

    gui_root.mainloop()


def on_closing(root, stop_event):
    stop_event.set()  # MqttTaskを終了するためのイベントをセット
    root.destroy()    # Tkinterのウィンドウを閉じる


# MqttタスクとTkinter GUIを並列に実行
stop_event = threading.Event()
create_gui(stop_event)
