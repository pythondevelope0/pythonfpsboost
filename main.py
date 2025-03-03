import os
import shutil
import ctypes
import subprocess
import sys
import tempfile
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import psutil

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

def clean_temp_files():
    temp_folder = tempfile.gettempdir()
    try:
        shutil.rmtree(temp_folder)
        os.mkdir(temp_folder)
        return True
    except Exception as e:
        print(f"Hata: {e}")
        return False

def empty_recycle_bin():
    try:
        subprocess.call(['cmd', '/c', 'rd /s /q %systemdrive%\\$Recycle.Bin'])
        return True
    except Exception as e:
        print(f"Hata: {e}")
        return False

def list_startup_programs():
    startup_dir = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
    return os.listdir(startup_dir)

def disable_startup_program(program_name):
    startup_dir = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"
    program_path = os.path.join(startup_dir, program_name)
    if os.path.exists(program_path):
        os.remove(program_path)
        return True
    else:
        return False

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('C:\\').percent
    return cpu_usage, ram_usage, disk_usage

class CleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Temizleyici ve Optimizasyon Aracı")
        self.root.geometry("500x400")
        
        title_label = Label(root, text="Sistem Temizleyici ve Optimizasyon Aracı", font=("Arial", 14))
        title_label.pack(pady=10)
        
        self.cpu_label = Label(root, text="")
        self.cpu_label.pack()
        self.ram_label = Label(root, text="")
        self.ram_label.pack()
        self.disk_label = Label(root, text="")
        self.disk_label.pack()
        self.update_system_info()
        
        temp_button = Button(root, text="Geçici Dosyaları Temizle", command=self.clean_temp)
        temp_button.pack(pady=10)
        
        recycle_button = Button(root, text="Çöp Kutusunu Boşalt", command=self.empty_recycle)
        recycle_button.pack(pady=10)
        
        startup_label = Label(root, text="Başlangıç Programları")
        startup_label.pack(pady=10)
        
        self.startup_listbox = Listbox(root)
        self.startup_listbox.pack()
        self.load_startup_programs()
        
        disable_button = Button(root, text="Seçili Programı Devre Dışı Bırak", command=self.disable_startup)
        disable_button.pack(pady=10)
    
    def update_system_info(self):
        cpu, ram, disk = get_system_info()
        self.cpu_label.config(text=f"CPU Kullanımı: {cpu}%")
        self.ram_label.config(text=f"RAM Kullanımı: {ram}%")
        self.disk_label.config(text=f"Disk Kullanımı: {disk}%")
        self.root.after(1000, self.update_system_info)
    
    def clean_temp(self):
        result = clean_temp_files()
        if result:
            messagebox.showinfo("Başarılı", "Geçici dosyalar temizlendi.")
        else:
            messagebox.showerror("Hata", "Geçici dosyalar temizlenemedi.")
    
    def empty_recycle(self):
        result = empty_recycle_bin()
        if result:
            messagebox.showinfo("Başarılı", "Çöp kutusu boşaltıldı.")
        else:
            messagebox.showerror("Hata", "Çöp kutusu boşaltılamadı.")
    
    def load_startup_programs(self):
        programs = list_startup_programs()
        for program in programs:
            self.startup_listbox.insert(END, program)
    
    def disable_startup(self):
        selected_program = self.startup_listbox.get(ACTIVE)
        result = disable_startup_program(selected_program)
        if result:
            messagebox.showinfo("Başarılı", f"{selected_program} devre dışı bırakıldı.")
            self.startup_listbox.delete(ACTIVE)
        else:
            messagebox.showerror("Hata", f"{selected_program} devre dışı bırakılamadı.")

if __name__ == "__main__":
    root = Tk()
    app = CleanerApp(root)
    root.mainloop()
