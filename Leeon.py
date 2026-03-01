import customtkinter as ctk
from PIL import Image
import os
import subprocess

class LeeonDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Leeon E-Commerce Dashboard")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        
        # Path Setup
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Images Load Karein
        self.load_assets()
        
        # Start with Welcome Screen
        self.show_welcome_screen()

    def load_assets(self):
        """Sari images ko load karne ka function"""
        try:
            # Logo (Top Left ke liye)
            self.logo_img = ctk.CTkImage(light_image=Image.open(os.path.join(self.current_dir, "LeeonLogo.png")),
                                         dark_image=Image.open(os.path.join(self.current_dir, "LeeonLogo.png")),
                                         size=(150, 70))
            
            # First Page Artwork
            self.first_art = ctk.CTkImage(light_image=Image.open(os.path.join(self.current_dir, "Firstpageartwork.png")),
                                          dark_image=Image.open(os.path.join(self.current_dir, "Firstpageartwork.png")),
                                          size=(450, 350))
            
            # Second Page Artwork
            self.second_art = ctk.CTkImage(light_image=Image.open(os.path.join(self.current_dir, "Secondpageartwork.png")),
                                           dark_image=Image.open(os.path.join(self.current_dir, "Secondpageartwork.png")),
                                           size=(400, 450))
        except Exception as e:
            print(f"Error loading images: {e}. Make sure filenames are correct in the folder.")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def add_logo(self, master):
        """Common logo added to top left"""
        logo_label = ctk.CTkLabel(master, image=self.logo_img, text="")
        logo_label.place(x=30, y=20)

    def show_welcome_screen(self):
        self.clear_screen()
        
        main_frame = ctk.CTkFrame(self, fg_color="#0f1123")
        main_frame.pack(fill="both", expand=True)

        # Logo Add karein
        self.add_logo(main_frame)

        # Left Side Content
        label = ctk.CTkLabel(main_frame, text="Welcome to Leeon\nE-Commerce", 
                             font=("Helvetica", 55, "bold"), text_color="white", justify="left")
        label.place(relx=0.08, rely=0.35)

        sub_label = ctk.CTkLabel(main_frame, text="One stop for all E-Commerce Solutions", 
                                 font=("Helvetica", 18), text_color="#9da0b5")
        sub_label.place(relx=0.08, rely=0.58)

        start_btn = ctk.CTkButton(main_frame, text="Let's Start", corner_radius=25,
                                  fg_color="#6a5af9", hover_color="#5142d4",
                                  font=("Helvetica Bold", 18), height=55, width=220,
                                  command=self.show_services_screen)
        start_btn.place(relx=0.08, rely=0.72)

        # Right Side Artwork (First Page)
        art_label = ctk.CTkLabel(main_frame, image=self.first_art, text="")
        art_label.place(relx=0.55, rely=0.25)

    def show_services_screen(self):
        self.clear_screen()
        
        service_frame = ctk.CTkFrame(self, fg_color="#0f1123")
        service_frame.pack(fill="both", expand=True)

        # Logo Add karein
        self.add_logo(service_frame)

        # Left Side: Header & Buttons
        header = ctk.CTkLabel(service_frame, text="Services", font=("Helvetica Bold", 48), text_color="white")
        header.place(relx=0.08, rely=0.15)

        btn_container = ctk.CTkFrame(service_frame, fg_color="transparent")
        btn_container.place(relx=0.08, rely=0.30)

        # --- Sabhi Buttons Yahan Hain ---
        self.create_service_button(btn_container, "Flipkart Label & Invoice Separator", "Flipkart_PDF_Cropper.py")
        self.create_service_button(btn_container, "PDF Merge", "pdf_merge.py")
        self.create_service_button(btn_container, "Catalogue Image Link Generator", "catalogue_gen.py")
        self.create_service_button(btn_container, "Dropbox JPG Image Link Generator", "Dropbox_JPG_Link_Generator.py")
        
        # Naya Button: iPhone Image Converter
        self.create_service_button(btn_container, "iPhone Image Converter (HEIC to JPG)", "heic_to_Jpg_Converter.py")

        # Right Side Artwork (Second Page)
        art_label = ctk.CTkLabel(service_frame, image=self.second_art, text="")
        art_label.place(relx=0.6, rely=0.2)

    def create_service_button(self, master, text, script_name):
        btn = ctk.CTkButton(master, text=f"    {text}", corner_radius=22,
                            fg_color="#644ef1", hover_color="#a34ef1",
                            font=("Helvetica", 15), height=42, width=380,
                            anchor="w",
                            command=lambda: self.run_python_script(script_name))
        btn.pack(pady=8)

    def run_python_script(self, script_name):
        full_path = os.path.join(self.current_dir, script_name)
        try:
            if os.path.exists(full_path):
                subprocess.Popen(['python', full_path], cwd=self.current_dir)
            else:
                print(f"Error: {script_name} not found at {full_path}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = LeeonDashboard()
    app.mainloop()