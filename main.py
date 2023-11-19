import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import json
import os


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IAE Limited Amount Ship Sale Timer For Nervous People (˵ •̀ ᴗ •́ ˵ ) ✧ ")
        self.root.configure(bg='white')
        self.events_file = os.path.expanduser("~/Documents/countdown_events.json")

        self.event_times = self.load_events()
        self.labels = {}
        self.check_vars = {}

        # Frame for the event labels and checkboxes
        self.events_frame = tk.Frame(root, bg='white')
        self.events_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Add Event Button
        tk.Button(root, text="Add Event(s)", command=self.add_event_window).pack(side='left', padx=10, pady=10)

        # Select save location
        tk.Button(root, text="Select Save Location", command=self.select_save_location).pack(side='left', padx=10,
                                                                                             pady=10)
        # Delete Event Button
        tk.Button(root, text="Delete Selected Event(s)", command=self.delete_selected).pack(side='left', padx=10, pady=10)

        # Delete .json Button
        tk.Button(root, text="Delete .json file", command=self.delete_json_file).pack(side='left', padx=10, pady=10)

        # Exit Button
        tk.Button(root, text="Exit", command=self.kill_app).pack(side='left', padx=10, pady=10)

        self.update_ui()

    def load_events(self):
        if os.path.exists(self.events_file):
            with open(self.events_file, 'r') as file:
                return json.load(file)
        return {}

    def select_save_location(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.events_file = os.path.join(folder_selected, 'countdown_events.json')
            self.save_events()  # Save the current events to the new location

    def save_events(self):
        with open(self.events_file, 'w') as file:
            json.dump(self.event_times, file, indent=4)

    def update_ui(self):
        for widgets in self.events_frame.winfo_children():
            widgets.destroy()

        for i, (event, times) in enumerate(self.event_times.items()):
            check_var = tk.BooleanVar()
            self.check_vars[event] = check_var
            check_button = tk.Checkbutton(self.events_frame, var=check_var, bg='white')
            check_button.grid(row=i, column=0, padx=5, pady=5)

            label = tk.Label(self.events_frame, text=event, bg='white', anchor='w')
            label.grid(row=i, column=1, sticky='ew', padx=5, pady=5)

            self.labels[event] = [tk.Label(self.events_frame, text="", bg='lightgreen') for _ in times]
            for j, label in enumerate(self.labels[event]):
                label.grid(row=i, column=j + 2, padx=5, pady=5)

        self.update_countdowns()

    def update_countdowns(self):
        now = datetime.now().timestamp()
        for event, times in self.event_times.items():
            for i, timestamp in enumerate(times):
                countdown_text, bg_color = self.calculate_countdown(timestamp, now)
                self.labels[event][i].config(text=countdown_text, bg=bg_color)

        self.root.after(1000, self.update_countdowns)

    @staticmethod
    def calculate_countdown(timestamp, current_time):
        time_diff = timestamp - current_time
        if time_diff <= 0:
            return "Event Ended", 'lightcoral'
        if time_diff <= 3600:
            return "Event Started", 'lightyellow'

        days = int(time_diff // (24 * 3600))
        time_diff = time_diff % (24 * 3600)
        hours = int(time_diff // 3600)
        time_diff %= 3600
        minutes = int(time_diff // 60)
        seconds = int(time_diff % 60)

        return f"{days}d {hours}h {minutes}m {seconds}s", 'lightgreen'

    def add_event_window(self):
        top = tk.Toplevel(self.root)
        top.title("Add Event")
        top.geometry("600x500")

        tk.Label(top, text="Enter Event Info:").pack(padx=10, pady=5, anchor='nw')

        event_info = tk.Text(top)
        event_info.pack(padx=10, pady=5, fill='both', expand=True)

        tk.Button(top, text="Add", command=lambda: self.add_event(event_info.get("1.0", tk.END), top)).pack(padx=10,
                                                                                                            pady=10)

    def add_event(self, event_str, top):
        for line in event_str.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split(" <t:")
            event_name = parts[0]
            timestamps = [int(ts.split(":")[0]) for ts in parts[1:]]
            self.event_times[event_name] = timestamps

        self.save_events()
        self.update_ui()
        top.destroy()

    def delete_selected(self):
        for event, var in list(self.check_vars.items()):
            if var.get():
                del self.event_times[event]
                del self.check_vars[event]

        self.save_events()
        self.update_ui()

    def delete_json_file(self):
        if os.path.exists(self.events_file):
            os.remove(self.events_file)
            self.event_times.clear()
            self.update_ui()

    def kill_app(self):
        root.quit()


# Create the main window
root = tk.Tk()
root.geometry("720x320")
app = CountdownApp(root)

root.mainloop()
