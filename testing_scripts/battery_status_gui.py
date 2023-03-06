import can
import tkinter as tk


root = tk.Tk()
root.title("Battery Status")
root.attributes("-fullscreen", True)

battery_label = tk.Label(root, text="Battery: ", font=("Helvetica", 150), fg = "blue")
battery_label.pack()
battery_label.config(anchor = "center")
battery_label.place(relx=.5, rely=.5, anchor="center")


def on_message_received(msg):
    if msg.arbitration_id == 0x580:
        batter_percentage = msg.data[5]
        battery_label.config(text=f"Battery: {batter_percentage}%")
        

bus = can.interface.Bus(bustype='socketcan', channel='slcan0', bitrate=500000)

listener = can.Listener()
listener.on_message_received = on_message_received

notifier = can.Notifier(bus, [listener])


root.mainloop()
