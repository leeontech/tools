import fitz  # PyMuPDF
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class FlipkartPreciseCropper(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Flipkart Precise Cropper (Final Modified)")
        self.geometry("500x420") 
        ctk.set_appearance_mode("dark")

        self.selected_file_path = None

        # --- UI Elements ---
        self.label = ctk.CTkLabel(self, text="Flipkart PDF Label & Invoice Cropper", font=("Arial", 18, "bold"))
        self.label.pack(pady=(30, 10))

        self.sub_label = ctk.CTkLabel(self, text="Select PDF to start trimming", font=("Arial", 12))
        self.sub_label.pack(pady=(0, 20))

        self.entry_path = ctk.CTkEntry(self, placeholder_text="Path yahan dikhega...", width=400)
        self.entry_path.pack(pady=10)

        self.btn_select = ctk.CTkButton(self, text="Browse PDF", command=self.select_file)
        self.btn_select.pack(pady=10)

        self.btn_crop = ctk.CTkButton(self, text="CROP & SAVE FINAL", command=self.process_pdf, 
                                     fg_color="#28a745", hover_color="#218838", height=45, font=("Arial", 14, "bold"))
        self.btn_crop.pack(pady=30)

        # --- Footer Credit (Developed by Rakesh Kumar) ---
        self.footer_label = ctk.CTkLabel(self, text="This program is developed by Rakesh Kumar", 
                                         font=("Arial", 11, "italic"), text_color="#aaaaaa")
        self.footer_label.pack(side="bottom", pady=15)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.selected_file_path = file_path
            self.entry_path.delete(0, 'end')
            self.entry_path.insert(0, file_path)

    def process_pdf(self):
        if not self.selected_file_path:
            messagebox.showwarning("Warning", "Pehle PDF file select karein!")
            return

        save_dir = filedialog.askdirectory(title="Save Location Select Karein")
        if not save_dir:
            return

        try:
            doc = fitz.open(self.selected_file_path)
            label_doc = fitz.open()
            invoice_doc = fitz.open()

            for page in doc:
                rect = page.rect
                
                # --- Final Ratio Settings ---
                top_cut = rect.height * 0.02  # Upar se 2%
                split_point = rect.height * 0.46 # 46% split point
                
                label_left = rect.width * 0.27
                label_right = rect.width * 0.73

                inv_left = rect.width * 0.05
                inv_right = rect.width * 0.95
                inv_bottom = rect.height * 0.90 # Bottom 10% cut

                # 1. Shipping Label Calculation
                label_rect = fitz.Rect(label_left, top_cut, label_right, split_point)
                
                # 2. Tax Invoice Calculation
                invoice_rect = fitz.Rect(inv_left, split_point, inv_right, inv_bottom)

                # Label page creation
                lp = label_doc.new_page(width=(label_right - label_left), height=(split_point - top_cut))
                lp.show_pdf_page(lp.rect, doc, page.number, clip=label_rect)

                # Invoice page creation
                ip = invoice_doc.new_page(width=(inv_right - inv_left), height=(inv_bottom - split_point))
                ip.show_pdf_page(ip.rect, doc, page.number, clip=invoice_rect)

            # File Saving
            label_path = os.path.join(save_dir, "Flipkart_Label_Final.pdf")
            invoice_path = os.path.join(save_dir, "Flipkart_Invoice_Final.pdf")

            label_doc.save(label_path)
            invoice_doc.save(invoice_path)
            
            doc.close()
            messagebox.showinfo("Success", "Files perfectly save ho gayi hain!\n\nDeveloped by Rakesh Kumar")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

if __name__ == "__main__":
    app = FlipkartPreciseCropper()
    app.mainloop()