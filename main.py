
# -------------------------------
# IMPORT REQUIRED LIBRARIES
# -------------------------------
import tkinter as tk              # For building the user interface (GUI)
from tkinter import messagebox    # For popup messages (alerts)
import sqlite3                    # For database (data storage)
from datetime import datetime     # For timestamps

# -------------------------------
# DATABASE SETUP
# -------------------------------
# Create/connect to a database file
conn = sqlite3.connect("health.db")

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fever TEXT,
    cough TEXT,
    headache TEXT,
    result TEXT,
    timestamp TEXT
)
""")

# Save changes
conn.commit()

# -------------------------------
# DSS LOGIC (SIMULATED AI)
# -------------------------------
class HealthDSS:
    def diagnose(self, fever, cough, headache):
        """
        This function simulates intelligent decision-making
        using simple IF rules (rule-based AI).
        """

        # Decision rules
        if fever == "Yes" and cough == "Yes":
            return "Possible Flu → Rest and hydrate"

        elif fever == "Yes" and headache == "Yes":
            return "Possible Malaria → Visit clinic"

        elif cough == "Yes" and headache == "Yes":
            return "Possible Respiratory Infection"

        else:
            return "No serious condition → Monitor symptoms"

# Create object of the DSS
dss = HealthDSS()

# -------------------------------
# FUNCTION: SAVE & PROCESS DATA
# -------------------------------
def check_health():
    """
    This function:
    1. Gets user input
    2. Sends it to DSS logic
    3. Saves result to database
    4. Displays output
    """

    # Get selected values from dropdowns
    fever = fever_var.get()
    cough = cough_var.get()
    headache = headache_var.get()

    # Validate input (ensure user selected all fields)
    if fever == "" or cough == "" or headache == "":
        messagebox.showwarning("Error", "Select all symptoms")
        return

    # Get decision from DSS
    result = dss.diagnose(fever, cough, headache)

    # Get current date and time
    time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Insert data into database
    cursor.execute(
        "INSERT INTO records (fever, cough, headache, result, timestamp) VALUES (?, ?, ?, ?, ?)",
        (fever, cough, headache, result, time)
    )

    # Save changes
    conn.commit()

    # Display result on screen
    output_label.config(text=result)

    # Reload history list
    load_history()

# -------------------------------
# FUNCTION: LOAD HISTORY
# -------------------------------
def load_history():
    """
    This function retrieves all stored records
    and displays them in the listbox.
    """

    # Clear current list
    listbox.delete(0, tk.END)

    # Get all records from database
    cursor.execute("SELECT fever, cough, headache, result FROM records")

    # Loop through records and display them
    for row in cursor.fetchall():
        listbox.insert(
            tk.END,
            f"F:{row[0]} C:{row[1]} H:{row[2]} → {row[3]}"
        )

# -------------------------------
# USER INTERFACE (GUI)
# -------------------------------
# Create main window
root = tk.Tk()

# Set window title
root.title("Health Decision Support System")

# Set window size
root.geometry("500x500")

# Create variables to store user selections
fever_var = tk.StringVar()
cough_var = tk.StringVar()
headache_var = tk.StringVar()

# -------------------------------
# INPUT FIELDS
# -------------------------------

# Fever input
tk.Label(root, text="Fever").pack()
tk.OptionMenu(root, fever_var, "Yes", "No").pack()

# Cough input
tk.Label(root, text="Cough").pack()
tk.OptionMenu(root, cough_var, "Yes", "No").pack()

# Headache input
tk.Label(root, text="Headache").pack()
tk.OptionMenu(root, headache_var, "Yes", "No").pack()

# -------------------------------
# BUTTON
# -------------------------------
tk.Button(root, text="Check Condition", command=check_health).pack(pady=10)

# -------------------------------
# OUTPUT DISPLAY
# -------------------------------
output_label = tk.Label(root, text="", fg="blue")
output_label.pack()

# -------------------------------
# HISTORY SECTION
# -------------------------------
tk.Label(root, text="History").pack()

# Listbox to display past records
listbox = tk.Listbox(root, width=60)
listbox.pack()

# Load existing records when app starts
load_history()

# -------------------------------
# START APPLICATION
# -------------------------------
root.mainloop()
