import csv
import os
from tkinter import messagebox

import customtkinter as ctk
import tkinter as tk
import datetime as dt
import files
from PIL import ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("assets/gold.json")

appWidth, appHeight = 500, 500


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Vehicle Logger")
        self.geometry(f"{appWidth}x{appHeight}")

        self.iconpath = ImageTk.PhotoImage(file=os.path.join("assets", "Logo.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.getPaths()

        # Name Label and Entry Field
        self.nameLabel = ctk.CTkLabel(self, text="Name")
        self.nameLabel.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.nameEntry = ctk.CTkEntry(self, placeholder_text="Enter your name")
        self.nameEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

        # Vehicle Label and Dropdown
        self.vehicleLabel = ctk.CTkLabel(self, text="Vehicle")
        self.vehicleLabel.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.vehicleDropdown = ctk.CTkOptionMenu(self, values=self.read_info("vehicles"))
        self.vehicleDropdown.grid(row=1, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

        # Date Label (Auto Applied)
        date = dt.date.today()
        self.dateLabel = ctk.CTkLabel(self, text="Date")
        self.dateLabel.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.dateLabelValue = ctk.CTkLabel(self, text=date.__str__())
        self.dateLabelValue.grid(row=2, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

        # Time Label (Auto Applied)
        time = dt.datetime.now().strftime("%H:%M:%S")
        self.timeLabel = ctk.CTkLabel(self, text="Time")
        self.timeLabel.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.timeLabelValue = ctk.CTkLabel(self, text=time.__str__())
        self.timeLabelValue.grid(row=3, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

        # Availability Label and Radio Buttons
        self.availabilityLabel = ctk.CTkLabel(self, text="Check out/In")
        self.availabilityLabel.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.availabilityVar = tk.StringVar(value="Check out")
        self.availRadioButton = ctk.CTkRadioButton(self, text="Check Out", variable=self.availabilityVar,
                                                   value="Check Out")
        self.availRadioButton.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        self.notAvailRadioButton = ctk.CTkRadioButton(self, text="Check in", variable=self.availabilityVar,
                                                      value="Check In")
        self.notAvailRadioButton.grid(row=4, column=2, padx=20, pady=10, sticky="w")

        # Location Label and Entry Field
        self.locationLabel = ctk.CTkLabel(self, text="Location")
        self.locationLabel.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.locationEntry = ctk.CTkEntry(self, placeholder_text="Enter your location")
        self.locationEntry.grid(row=5, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

        # Reason Label and Dropdown
        self.reasonLabel = ctk.CTkLabel(self, text="Reason")
        self.reasonLabel.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.reasonDropdown = ctk.CTkOptionMenu(self, values=self.read_info("reasons"))
        self.reasonDropdown.grid(row=6, column=1, columnspan=3, padx=20, pady=10, sticky="ew")

        # Submit Button
        self.submitButton = ctk.CTkButton(self, text="Submit", command=self.submitForm)
        self.submitButton.grid(row=7, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

    # Function to handle form submission
    def submitForm(self):
        name = self.nameEntry.get()
        vehicle = self.vehicleDropdown.get()
        date = self.dateLabelValue.cget("text")
        time = self.timeLabelValue.cget("text")
        availability = self.availabilityVar.get()
        location = self.locationEntry.get()
        reason = self.reasonDropdown.get()

        if not all([name, vehicle, date, time, availability, location, reason]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        with open(self.dataPath, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([vehicle, date, time, availability, location, reason])

        log_data = f"{dt.datetime.now()} - Vehicle: {vehicle}, Date: {date}, Time: {time}, " \
                   f"Availability: {availability}, Location: {location}, Reason: {reason}\n"
        with open(self.logPath, "a") as log_file:
            log_file.write(log_data)

        for w in self.winfo_children():
            if isinstance(w, ctk.CTkEntry):
                w.delete(0, 'end')
            if isinstance(w, ctk.CTkRadioButton):
                w.deselect()
            if isinstance(w, ctk.CTkOptionMenu):
                w.set(" ")



    def getPaths(self):
        self.dataPath = ""

        with open("Paths.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if (row[0] == "info"):
                    self.infoPath = row[1].strip()
                if (row[0] == "data"):
                    self.dataPath = row[1].strip()
                if (row[0] == "log"):
                    self.logPath = row[1].strip()

    def read_info(self, item):
        with open(self.infoPath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if (row[0] == item):
                    return row[1].split('/')


if __name__ == "__main__":
    app = App()
    app.mainloop()
