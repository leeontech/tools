import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import pillow_heif
import os
import threading

# HEIC support enable karna
pillow_heif.register_heif_opener()

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG Converter")
        self.root.geometry("400x250")
        self.root.configure(bg="#f4f4f4")

        # --- Welcome Screen ---
        self.main_frame = tk.Frame(self.root, padx=20, pady=40, bg="#f4f4f4")
        self.main_frame.pack(expand=True, fill="both")

        tk.Label(self.main_frame, text="HEIC Converter", 
                 font=("Segoe UI", 20, "bold"), bg="#f4f4f4", fg="#333").pack()
        
        tk.Label(self.main_frame, text="Convert your photos with custom settings", 
                 bg="#f4f4f4", fg="#666").pack(pady=10)

        self.start_btn = tk.Button(self.main_frame, text="Select Files & Start", 
                                   command=self.start_workflow,
                                   bg="#0078D7", fg="white", font=("Arial", 11, "bold"),
                                   padx=20, pady=8, cursor="hand2", relief="flat")
        self.start_btn.pack(pady=20)

    def start_workflow(self):
        # 1. Select Files
        files = filedialog.askopenfilenames(title="Select HEIC Files", filetypes=[("HEIC Files", "*.heic")])
        if not files: return

        # 2. Select Save Location
        save_dir = filedialog.askdirectory(title="Select Destination Folder")
        if not save_dir: return

        # 3. Show Settings Popup (Sliders for Quality & Size)
        self.show_settings_popup(files, save_dir)

    def show_settings_popup(self, files, save_dir):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Conversion Settings")
        settings_win.geometry("350x350")
        settings_win.grab_set() 

        tk.Label(settings_win, text="Fine-tune your output", font=("Arial", 12, "bold")).pack(pady=15)

        # Quality Slider
        tk.Label(settings_win, text="Image Quality (10-100):").pack(anchor="w", padx=40)
        quality_val = tk.IntVar(value=85)
        tk.Scale(settings_win, from_=10, to=100, orient="horizontal", variable=quality_val).pack(fill="x", padx=40, pady=5)

        # Size (Rescale) Slider
        tk.Label(settings_win, text="Image Size % (10-100):").pack(anchor="w", padx=40, pady=(10, 0))
        size_val = tk.IntVar(value=100) # Default 100% (No resize)
        tk.Scale(settings_win, from_=10, to=100, orient="horizontal", variable=size_val).pack(fill="x", padx=40, pady=5)

        def proceed():
            q = quality_val.get()
            s = size_val.get()
            settings_win.destroy()
            self.run_conversion(files, save_dir, q, s)

        tk.Button(settings_win, text="Convert Now", command=proceed,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), pady=8).pack(pady=30, fill="x", padx=40)

    def run_conversion(self, files, save_dir, quality, scale_percent):
        # Progress Window
        progress_win = tk.Toplevel(self.root)
        progress_win.title("Processing")
        progress_win.geometry("300x120")
        
        pbar = ttk.Progressbar(progress_win, orient="horizontal", length=250, mode="determinate")
        pbar.pack(pady=20)
        p_label = tk.Label(progress_win, text="Starting...")
        p_label.pack()

        threading.Thread(target=self.process_logic, args=(files, save_dir, quality, scale_percent, pbar, p_label, progress_win)).start()

    def process_logic(self, files, save_dir, quality, scale, pbar, p_label, p_win):
        total = len(files)
        pbar["maximum"] = total
        
        for i, path in enumerate(files):
            try:
                img = Image.open(path)
                
                # Resize logic based on slider %
                if scale < 100:
                    new_w = int(img.width * (scale / 100))
                    new_h = int(img.height * (scale / 100))
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                target = os.path.join(save_dir, os.path.splitext(os.path.basename(path))[0] + ".jpg")
                img.save(target, "JPEG", quality=quality, optimize=True)

                pbar["value"] = i + 1
                p_label.config(text=f"Converted {i+1} of {total}")
                self.root.update_idletasks()
            except Exception as e:
                print(f"Error: {e}")

        p_win.destroy()
        messagebox.showinfo("Success", "All files converted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()