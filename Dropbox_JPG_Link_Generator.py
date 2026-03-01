import dropbox
import pandas as pd
import tkinter as tk
from tkinter import messagebox, Listbox, filedialog, ttk
import os
import webbrowser # Link open karne ke liye

class DropboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dropbox Bulk Link Collector")
        self.root.geometry("450x300")
        self.dbx = None
        self.token = ""
        
        # Icon Setup (leeon logo)
        logo_path = "leeon_logo.png" 
        if os.path.exists(logo_path):
            try:
                img = tk.PhotoImage(file=logo_path)
                self.root.iconphoto(False, img)
            except:
                pass

        # Welcome Screen
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True)
        
        tk.Label(self.main_frame, text="Leeon.in Link Collector", font=("Arial", 16, "bold"), fg="#2196F3").pack(pady=10)
        tk.Label(self.main_frame, text="Developed by Rakesh Kumar", font=("Arial", 9, "italic")).pack()
        
        tk.Button(self.main_frame, text="Let's Start", command=self.ask_token, bg="#4CAF50", fg="white", width=20, font=("Arial", 11, "bold")).pack(pady=30)

    def open_help_link(self):
        # Help link open karne ka function
        webbrowser.open("https://leeon.co.in/blogs/news/how-to-generate-dropbox-token")

    def ask_token(self):
        self.token_win = tk.Toplevel(self.root)
        self.token_win.title("Step 1: Enter Token")
        self.token_win.geometry("400x250") # Window thodi badi ki hai button ke liye
        
        tk.Label(self.token_win, text="Paste your Dropbox Access Token:", font=("Arial", 10)).pack(pady=15)
        self.token_entry = tk.Entry(self.token_win, width=50)
        self.token_entry.pack(pady=5, padx=20)
        
        # Submit Button
        tk.Button(self.token_win, text="Submit & Fetch Folders", command=self.validate_token, bg="#2196F3", fg="white", font=("Arial", 9, "bold")).pack(pady=15)
        
        # Get Help Button (Naya Button)
        tk.Button(self.token_win, text="Get help to generate token", command=self.open_help_link, bg="#f0f0f0", fg="blue", relief=tk.FLAT, font=("Arial", 9, "underline")).pack(pady=5)

    def validate_token(self):
        self.token = self.token_entry.get().strip()
        if not self.token:
            messagebox.showerror("Error", "Token khali nahi ho sakta!")
            return
        self.token_win.destroy()
        self.fetch_folders()

    def fetch_folders(self):
        self.loading_win = tk.Toplevel(self.root)
        self.loading_win.title("Scanning...")
        self.loading_win.geometry("350x120")
        
        tk.Label(self.loading_win, text="Dropbox folders scan ho rahe hain...", font=("Arial", 10)).pack(pady=15)
        self.progress = ttk.Progressbar(self.loading_win, mode='indeterminate', length=280)
        self.progress.pack(pady=5)
        self.progress.start()
        self.root.update()
        
        try:
            self.dbx = dropbox.Dropbox(self.token)
            folders = []
            res = self.dbx.files_list_folder('', recursive=False)
            for entry in res.entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    folders.append(entry.path_display)
            
            self.loading_win.destroy()
            if folders:
                self.show_folder_list(folders)
            else:
                messagebox.showinfo("Empty", "Dropbox mein koi folder nahi mila!")
        except Exception as e:
            self.loading_win.destroy()
            messagebox.showerror("Auth Error", f"Token expired ya galat hai.\nNaya token use karein.\n\nError: {e}")

    def show_folder_list(self, folders):
        self.list_win = tk.Toplevel(self.root)
        self.list_win.title("Step 2: Select Folders")
        self.list_win.geometry("500x550")
        
        tk.Label(self.list_win, text="Folders select karein (Ctrl + Click for multiple):", font=("Arial", 11)).pack(pady=10)
        self.lb = Listbox(self.list_win, selectmode=tk.MULTIPLE, width=70, height=20, font=("Consolas", 10))
        for f in folders:
            self.lb.insert(tk.END, f)
        self.lb.pack(pady=10, padx=15)
        
        tk.Button(self.list_win, text="Next: Save Location", command=self.start_process, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def start_process(self):
        indices = self.lb.curselection()
        if not indices:
            messagebox.showwarning("Warning", "Ek folder toh select kijiye!")
            return
        
        selected_folders = [self.lb.get(i) for i in indices]
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Excel kahan save karun?")
        
        if save_path:
            self.list_win.destroy()
            self.process_with_progress(selected_folders, save_path)

    def process_with_progress(self, folders, save_path):
        self.prg_win = tk.Toplevel(self.root)
        self.prg_win.title("Processing Images")
        self.prg_win.geometry("450x200")
        
        self.status_label = tk.Label(self.prg_win, text="Taiyari ho rahi hai...", font=("Arial", 10))
        self.status_label.pack(pady=10)
        
        self.current_file_label = tk.Label(self.prg_win, text="", fg="blue", font=("Arial", 9))
        self.current_file_label.pack(pady=5)
        
        data_list = []
        try:
            for folder in folders:
                self.status_label.config(text=f"Scanning folder: {folder}")
                self.root.update()
                
                res = self.dbx.files_list_folder(folder)
                while True:
                    for entry in res.entries:
                        if isinstance(entry, dropbox.files.FileMetadata) and entry.name.lower().endswith('.jpg'):
                            self.current_file_label.config(text=f"Adding: {entry.name}")
                            self.root.update()
                            
                            try:
                                link = self.dbx.sharing_create_shared_link_with_settings(entry.path_lower).url
                            except:
                                link = self.dbx.sharing_list_shared_links(path=entry.path_lower, direct_only=True).links[0].url
                            
                            data_list.append({
                                "File Name": entry.name,
                                "Download Link": link.replace('?dl=0', '?raw=1')
                            })
                    
                    if res.has_more:
                        res = self.dbx.files_list_folder_continue(res.cursor)
                    else:
                        break
            
            self.prg_win.destroy()
            if data_list:
                pd.DataFrame(data_list).to_csv(save_path, index=False)
                # Final Credit
                final_msg = f"Kaam Ho Gaya!\n\nTotal Images: {len(data_list)}\nSaved at: {save_path}\n\n--- This program developed by Rakesh Kumar ---"
                messagebox.showinfo("Leeon.in - Success", final_msg)
            else:
                messagebox.showwarning("No JPGs", "Koi images nahi mili!")
                
        except Exception as e:
            self.prg_win.destroy()
            messagebox.showerror("Error", f"Processing fail: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DropboxApp(root)
    root.mainloop()