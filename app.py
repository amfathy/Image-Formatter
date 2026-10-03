  import os
import threading
import time
from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from tkinter.ttk import Progressbar
from PIL import Image, ImageOps

# ================== GLOBALS ==================
border_color = "#ffffff"
border_pt = 1.0
folders_list = []

BORDER_OPTIONS = ["0 pt", "0.25 pt", "0.5 pt", "1 pt", "2.25 pt", "3 pt", "4.5 pt", "6 pt"]

# ================== FUNCTIONS ==================

def add_folder():
    folder = filedialog.askdirectory(title="اختر مجلد الصور")
    if folder and folder not in folders_list:
        folders_list.append(folder)
        folders_box.insert(END, folder)

def remove_folder():
    selected = folders_box.curselection()
    if selected:
        index = selected[0]
        folders_box.delete(index)
        folders_list.pop(index)

def clear_folders():
    folders_box.delete(0, END)
    folders_list.clear()

def choose_border_color():
    global border_color
    color = colorchooser.askcolor(title="لون الإطار")
    if color[1]:
        border_color = color[1]
        color_preview.config(bg=border_color)

def get_images(folder):
    return [os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

def safe_path(folder, file_path):
    filename = os.path.basename(file_path)
    base, ext = os.path.splitext(filename)
    name = filename
    i = 1
    while os.path.exists(os.path.join(folder, name)):
        name = f"{base}_{i}{ext}"
        i += 1
    return os.path.join(folder, name)

def resize_images():
    if not folders_list:
        messagebox.showerror("خطأ", "يرجى إضافة مجلد واحد على الأقل")
        return
    try:
        w_cm = float(width_entry.get())
        h_cm = float(height_entry.get())
    except ValueError:
        messagebox.showerror("خطأ", "الطول والعرض يجب أن يكونا أرقام")
        return

    px_per_cm = 96 / 2.54
    w_px = int(w_cm * px_per_cm)
    h_px = int(h_cm * px_per_cm)
    border_px = int(border_pt * 96 / 72)

    total_images = sum(len(get_images(f)) for f in folders_list)
    if total_images == 0:
        messagebox.showerror("خطأ", "لا توجد صور داخل المجلدات")
        return

    progress.pack(pady=14)
    progress["value"] = 0
    processed = 0

    for folder in folders_list:
        images = get_images(folder)
        if not images:
            continue
        out = os.path.join(folder, "resized images")
        os.makedirs(out, exist_ok=True)

        for img_path in images:
            img = Image.open(img_path)
            img = img.resize((w_px, h_px), Image.LANCZOS)
            if border_px > 0:
                img = ImageOps.expand(img, border=border_px, fill=border_color)
            img.save(safe_path(out, img_path))

            processed += 1
            progress["value"] = (processed / total_images) * 100
            root.update_idletasks()
            time.sleep(0.02)

    progress.pack_forget()
    messagebox.showinfo("تم", "تم معالجة جميع المجلدات بنجاح")

def start():
    threading.Thread(target=resize_images).start()

# ================== GUI ==================

root = Tk()
root.geometry("950x620")
root.configure(bg="#0e0e0e")
root.resizable(False, False)
root.title("Image Resizer |  مطور من فرع النظم - *********************** ")

if os.path.exists("icon.ico"):
    root.iconbitmap("icon.ico")

FONT = ("Segoe UI", 11)

def modern_entry(parent, width):
    return Entry(parent, width=width, bg="#2a2a2a", fg="white",
                 insertbackground="white", relief=FLAT, font=FONT)

def modern_button(parent, text, cmd, bg):
    return Button(parent, text=text, command=cmd, bg=bg, fg="white",
                  font=("Segoe UI", 11, "bold"), relief=FLAT, padx=18, pady=8,
                  activebackground="#3a3a3a")

main = Frame(root, bg="#0e0e0e")
main.pack(expand=True, fill=BOTH)

Label(main, text="تغيير حجم الصور", fg="white", bg="#0e0e0e",
      font=("Segoe UI", 20, "bold")).pack(pady=16)

# -------- Folder List --------
folders_box = Listbox(main, width=90, height=6, bg="#2a2a2a",
                      fg="white", selectbackground="#2563eb", relief=FLAT)
folders_box.pack(pady=10)

btn_folder = Frame(main, bg="#0e0e0e")
btn_folder.pack(pady=8)

modern_button(btn_folder, "إضافة مجلد", add_folder, "#2563eb").grid(row=0, column=0, padx=8)
modern_button(btn_folder, "حذف المحدد", remove_folder, "#444").grid(row=0, column=1, padx=8)
modern_button(btn_folder, "مسح الكل", clear_folders, "#444").grid(row=0, column=2, padx=8)

# -------- Size --------
size_frame = Frame(main, bg="#0e0e0e")
size_frame.pack(pady=14)

Label(size_frame, text="العرض (سم)", fg="white", bg="#0e0e0e", font=FONT).grid(row=0, column=0, padx=18)
width_entry = modern_entry(size_frame, 12)
width_entry.grid(row=1, column=0)

Label(size_frame, text="الطول (سم)", fg="white", bg="#0e0e0e", font=FONT).grid(row=0, column=1, padx=18)
height_entry = modern_entry(size_frame, 12)
height_entry.grid(row=1, column=1)

# -------- Border --------
border_frame = Frame(main, bg="#0e0e0e")
border_frame.pack(pady=18)

border_var = StringVar()
border_var.set("سمك الإطار") 

def update_border(value):
    global border_pt
    border_pt = float(value.replace(" pt", ""))
    border_var.set(value)

border_menu = OptionMenu(border_frame, border_var, *BORDER_OPTIONS, command=update_border)
border_menu.config(bg="#444", fg="white", font=("Segoe UI", 11, "bold"), relief=FLAT, padx=10, pady=5, activebackground="#3a3a3a")
border_menu["menu"].config(bg="#2a2a2a", fg="white", font=("Segoe UI", 11))
border_menu.grid(row=0, column=0, padx=8)

modern_button(border_frame, "لون الإطار", choose_border_color, "#444").grid(row=0, column=1, padx=8)
color_preview = Label(border_frame, bg=border_color, width=3, height=1)
color_preview.grid(row=0, column=2)

# -------- Progress --------
progress = Progressbar(main, length=600)

# -------- Action Buttons --------
btns = Frame(main, bg="#0e0e0e")
btns.pack(pady=26)
modern_button(btns, "بدء", start, "#16a34a").grid(row=0, column=0, padx=16)
modern_button(btns, "إنهاء", root.quit, "#b91c1c").grid(row=0, column=1, padx=16)

root.mainloop()
