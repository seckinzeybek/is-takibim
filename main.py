
import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

FILENAME = "tasks.csv"
CSV_HEADERS = ["ID", "İş Adı", "Tür", "Önem", "Durum", "Planlanan Bitiş", "Eklenme", "İşleme Alınma", "Tamamlanma", "Süre (dk)"]

if not os.path.exists(FILENAME):
    with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

def add_task():
    name = entry_name.get()
    category = entry_category.get()
    priority = combo_priority.get()
    deadline = entry_deadline.get()

    if not name:
        messagebox.showwarning("Eksik Bilgi", "İş adı boş olamaz.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_id = datetime.now().strftime("%Y%m%d%H%M%S")

    with open(FILENAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([task_id, name, category, priority, "Yapılacak", deadline, now, "", "", ""])

    refresh_tasks()
    clear_inputs()

def refresh_tasks():
    listbox_tasks.delete(*listbox_tasks.get_children())
    with open(FILENAME, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            listbox_tasks.insert("", tk.END, values=row)

def update_status(new_status):
    selected = listbox_tasks.selection()
    if not selected:
        messagebox.showinfo("Seçim Yok", "Lütfen bir görev seçin.")
        return

    task_id = listbox_tasks.item(selected)["values"][0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated = []

    with open(FILENAME, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] == task_id:
                row[4] = new_status
                if new_status == "İşleme Alındı":
                    row[7] = now
                elif new_status == "Tamamlandı":
                    row[8] = now
                    if row[7]:
                        fmt = "%Y-%m-%d %H:%M:%S"
                        t1 = datetime.strptime(row[7], fmt)
                        t2 = datetime.strptime(now, fmt)
                        minutes = int((t2 - t1).total_seconds() // 60)
                        row[9] = str(minutes)
            updated.append(row)

    with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(updated)

    refresh_tasks()

def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    combo_priority.set("")
    entry_deadline.delete(0, tk.END)

root = tk.Tk()
root.title("📋 İş Takip Uygulaması")
root.geometry("1000x550")

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="İş Adı:").grid(row=0, column=0)
entry_name = tk.Entry(frame_inputs, width=25)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(frame_inputs, text="Tür:").grid(row=0, column=2)
entry_category = tk.Entry(frame_inputs, width=20)
entry_category.grid(row=0, column=3, padx=5)

tk.Label(frame_inputs, text="Önem:").grid(row=0, column=4)
combo_priority = ttk.Combobox(frame_inputs, values=["Düşük", "Orta", "Yüksek"], width=10)
combo_priority.grid(row=0, column=5, padx=5)

tk.Label(frame_inputs, text="Planlanan Bitiş (opsiyonel):").grid(row=0, column=6)
entry_deadline = tk.Entry(frame_inputs, width=15)
entry_deadline.grid(row=0, column=7, padx=5)

tk.Button(root, text="Görev Ekle", command=add_task, bg="#28a745", fg="white", width=25).pack(pady=10)

columns = CSV_HEADERS
listbox_tasks = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    listbox_tasks.heading(col, text=col)
    listbox_tasks.column(col, width=110, anchor="center")
listbox_tasks.pack()

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="İşleme Alındı", command=lambda: update_status("İşleme Alındı"), width=20).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Tamamlandı", command=lambda: update_status("Tamamlandı"), width=20).grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Yapılacak", command=lambda: update_status("Yapılacak"), width=20).grid(row=0, column=2, padx=10)

refresh_tasks()
root.mainloop()
