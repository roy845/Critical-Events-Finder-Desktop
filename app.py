from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json
from typing import List, Tuple
from critical_events import find_critical_events


class CriticalEventsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Critical Events Finder")
        self.root.geometry("500x400")
        self.root.resizable(False, False) 

        self.main_frame = tk.Frame(root, bg="#f7f7f7", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(
            self.main_frame, text="Critical Events Finder",
            font=("Arial", 16, "bold"), bg="#f7f7f7", fg="#333"
        )
        self.title_label.pack(pady=20)

        self.import_button = tk.Button(
            self.main_frame, text="Import Data",
            font=("Arial", 12), bg="#4caf50", fg="white",
            activebackground="#45a049", activeforeground="white",
            command=self.import_data
        )
        self.import_button.pack(pady=10, ipadx=10, ipady=5)

        self.export_button = tk.Button(
            self.main_frame, text="Export Critical Events",
            font=("Arial", 12), bg="#2196f3", fg="white",
            activebackground="#1976d2", activeforeground="white",
            command=self.export_data
        )

        self.reset_button = tk.Button(
            self.main_frame, text="Reset",
            font=("Arial", 12), bg="#f44336", fg="white",
            activebackground="#d32f2f", activeforeground="white",
            command=self.reset
        )

        self.days_list = []
        self.critical_events = []

    def import_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx"), ("JSON Files", "*.json")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith(".xlsx"):
                data = pd.read_excel(file_path)
                self.days_list = self.process_excel(data)
            elif file_path.endswith(".json"):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.days_list = self.process_json(data)
            else:
                messagebox.showerror("Error", "Unsupported file type.")
                return

            self.critical_events = find_critical_events(self.days_list)

          
            if self.critical_events:
                messagebox.showinfo("Success", f"Critical events identified: {len(self.critical_events)}")
                
              
                if not self.export_button.winfo_ismapped():
                    self.export_button.pack(pady=10, ipadx=10, ipady=5)

            else:
                messagebox.showinfo("No Critical Events", "No critical events were identified in the imported data.")

          
            if not self.reset_button.winfo_ismapped():
                self.reset_button.pack(pady=10, ipadx=10, ipady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")

            file_path = filedialog.askopenfilename(
                filetypes=[("Excel Files", "*.xlsx"), ("JSON Files", "*.json")]
            )
            if not file_path:
                return

            try:
                if file_path.endswith(".xlsx"):
                    data = pd.read_excel(file_path)
                    self.days_list = self.process_excel(data)
                elif file_path.endswith(".json"):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        self.days_list = self.process_json(data)
                else:
                    messagebox.showerror("Error", "Unsupported file type.")
                    return

                self.critical_events = find_critical_events(self.days_list)

              
                if self.critical_events:
                    messagebox.showinfo("Success", f"Critical events identified: {len(self.critical_events)}")
                    if not self.export_button.winfo_ismapped():
                        self.export_button.pack(pady=10, ipadx=10, ipady=5, before=self.reset_button)
                else:
                    messagebox.showinfo("No Critical Events", "No critical events were identified in the imported data.")
                    if self.export_button.winfo_ismapped():
                        self.export_button.pack_forget()

              
                if not self.reset_button.winfo_ismapped():
                    self.reset_button.pack(pady=10, ipadx=10, ipady=5)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process file: {e}")

    def process_excel(self, data: pd.DataFrame) -> List[List[Tuple[str, str]]]:
        """
        Process Excel data where rows represent intersections and events for specific days.
        """
        days = defaultdict(list)
        for index, row in data.iterrows():
            day_id = row.iloc[0]  
            intersection = row.iloc[1]  
            event = row.iloc[2]  
            days[day_id].append((intersection, event))
        return list(days.values())

    def process_json(self, data: List[dict]) -> List[List[Tuple[str, str]]]:
        """
        Process JSON data where each day contains an ID and a list of events.
        """
        days = []
        for day in data:
            day_events = [(event["intersection"], event["event"]) for event in day["events"]]
            days.append(day_events)
        return days

    def export_data(self):
        if not self.critical_events:
            messagebox.showerror("Error", "No critical events to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", 
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            df = pd.DataFrame({"Critical Events": self.critical_events})
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Critical events exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export file: {e}")

    def reset(self):
        """
        Resets the application's state, clearing all loaded data and disabling buttons.
        """
        self.days_list = []
        self.critical_events = []

        self.export_button.pack_forget()
        self.reset_button.pack_forget()

        messagebox.showinfo("Reset", "Application has been reset successfully.")