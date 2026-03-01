import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


# =====================================================
# AUTO INSTALL REQUIREMENTS
# =====================================================
if os.path.exists("Requirements.txt"):
    with open("Requirements.txt", "r") as f:
        packages = [line.strip() for line in f if line.strip()]

    for package in packages:
        try:
            __import__(package.split("==")[0].replace("-", "_"))
            print(f"{package} already installed ✅")
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# =====================================================
# CONFIG
# =====================================================
BASE_ANIME_PATH = r"C:\Users\shrey\Videos\Anime"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_SCRIPT = os.path.join(CURRENT_DIR, "animepahe.ps1")
FIX_SCRIPT = os.path.join(CURRENT_DIR, "fixing.ps1")

ICON_PATH = os.path.join(CURRENT_DIR, "required_images", "Logo.jpg")
BG_PATH = os.path.join(CURRENT_DIR, "required_images", "Background_Image.jpg")


# =====================================================
# FUNCTIONS
# =====================================================

def run_download():
    subprocess.Popen(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            DOWNLOAD_SCRIPT
        ],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    root.destroy()


def open_fix_window():
    root.destroy()

    if not os.path.exists(BASE_ANIME_PATH):
        messagebox.showerror("Error", "Anime folder path does not exist.")
        return

    fix_window = tk.Tk()
    fix_window.title("Select Anime Folder")
    fix_window.geometry("600x500")

    if os.path.exists(BG_PATH):
        bg_img = Image.open(BG_PATH).resize((600, 500))
        bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(fix_window, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    folders = [
        f for f in os.listdir(BASE_ANIME_PATH)
        if os.path.isdir(os.path.join(BASE_ANIME_PATH, f))
    ]

    if not folders:
        messagebox.showerror("Error", "No anime folders found.")
        fix_window.destroy()
        return

    frame = tk.Frame(fix_window, bg="black",
                     highlightbackground="green",
                     highlightthickness=2)
    frame.pack(pady=40, padx=40, fill="both", expand=True)

    tk.Label(frame,
             text="SELECT ANIME FOLDER",
             font=("Arial", 16, "bold"),
             bg="black",
             fg="green").pack(pady=20)

    listbox = tk.Listbox(frame, width=40, height=12)
    listbox.pack(pady=10)

    for folder in folders:
        listbox.insert(tk.END, folder)

    def run_fix():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a folder first.")
            return

        selected_folder = folders[selection[0]]
        target_path = os.path.join(BASE_ANIME_PATH, selected_folder)

        dest_script = os.path.join(target_path, "fixing.ps1")

        if not os.path.exists(dest_script):
            shutil.copy(FIX_SCRIPT, target_path)

        subprocess.Popen(
            [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                f'cd "{target_path}"; .\\fixing.ps1'
            ],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        fix_window.destroy()

    ttk.Button(frame,
               text="Fix Audio",
               command=run_fix).pack(pady=20)

    fix_window.mainloop()


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()
root.title("Chinnappa Swami")
root.geometry("750x550")
root.configure(bg="#7ac142")  # green background


# Background image (optional)
if os.path.exists(BG_PATH):
    bg_img = Image.open(BG_PATH).resize((750, 550))
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Window icon
if os.path.exists(ICON_PATH):
    icon_img = Image.open(ICON_PATH).resize((32, 32))
    icon_photo = ImageTk.PhotoImage(icon_img)
    root.iconphoto(True, icon_photo)


# ================= HEADER AREA =================

top_frame = tk.Frame(root, bg="black",
                     highlightbackground="green",
                     highlightthickness=2)
top_frame.pack(pady=30, padx=40, fill="x")

# Logo (left side)
if os.path.exists(ICON_PATH):
    logo_img = Image.open(ICON_PATH).resize((110, 110))
    logo_photo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(top_frame,
                          image=logo_photo,
                          bg="black")
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=30, pady=15)

# Title stacked
title_frame = tk.Frame(top_frame, bg="black")
title_frame.pack(side="left", padx=40)

tk.Label(title_frame,
         text="Chinnappa",
         font=("Arial", 28, "bold"),
         bg="black",
         fg="green").pack(anchor="w")

tk.Label(title_frame,
         text="Swami",
         font=("Arial", 28, "bold"),
         bg="black",
         fg="green").pack(anchor="w")


# ================= BUTTON AREA =================

button_frame = tk.Frame(
    root,
    bg="black",
    highlightbackground="green",
    highlightthickness=2,
    width=500,
    height=250
)

button_frame.pack(pady=50)
button_frame.pack_propagate(False)   # IMPORTANT → prevents shrinking

style = ttk.Style()
style.configure("TButton", font=("Arial", 16, "bold"), padding=12)

download_btn = ttk.Button(
    button_frame,
    text="Download Anime",
    command=run_download
)
download_btn.pack(pady=30, ipadx=40, ipady=8)

fix_btn = ttk.Button(
    button_frame,
    text="Fix Audio",
    command=open_fix_window
)
fix_btn.pack(pady=20, ipadx=40, ipady=8)


root.mainloop()