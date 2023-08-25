import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import spacy
import tabula
import pandas as pd

class PDFExtractorGUI:
    def __init__(self, master):
        self.master = master
        master.title("WVF Intelligent Data Processor v0.1_Alpha Edition")

        self.file_path = ""

        self.file_label = ttk.Label(master, text="No file selected.")
        self.file_label.grid(row=0, column=0, padx=10, pady=10)

        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        self.dropzone = tk.Label(master, text="Drop files here", width=30, height=10, relief=tk.GROOVE, bg="#ADD8E6")
        self.dropzone.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        self.dropzone.drop_target_register(DND_FILES)
        self.dropzone.dnd_bind('<<Drop>>', self.handle_drop)

        self.extraction_tool_label = ttk.Label(master, text="Select Extraction Tool:")
        self.extraction_tool_label.grid(row=1, column=0, padx=10, pady=10)

        self.extraction_tool_var = tk.StringVar()
        self.extraction_tool_options = ["PDFMiner", "PyMuPDF", "PyPDF4"]
        self.extraction_tool_dropdown = ttk.OptionMenu(master, self.extraction_tool_var, self.extraction_tool_options[0], *self.extraction_tool_options)
        self.extraction_tool_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.transformer_label = ttk.Label(master, text="Select Transformer:")
        self.transformer_label.grid(row=2, column=0, padx=10, pady=10)

        self.transformer_var = tk.StringVar()
        self.transformer_options = ["SpaCy"]
        self.transformer_dropdown = ttk.OptionMenu(master, self.transformer_var, self.transformer_options[0], *self.transformer_options)
        self.transformer_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.extract_button = ttk.Button(master, text="Extract Text", command=self.extract_text)
        self.extract_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.export_button = ttk.Button(master, text="Export Excel", command=self.export_excel)
        self.export_button.grid(row=3, column=2, padx=10, pady=10)

        self.text_box = tk.Text(master, height=20, width=50)
        self.text_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.processed_text_box = tk.Text(master, height=20, width=50)
        self.processed_text_box.grid(row=4, column=2, columnspan=2, padx=10, pady=10)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=self.file_path)

    def handle_drop(self, event):
        files = event.data
        self.file_path = ''.join(files)  # Concatenate all dropped characters into the file path string
        self.file_label.config(text=self.file_path)

    def extract_text(self):
        extraction_tool = self.extraction_tool_var.get()

        if extraction_tool == "PDFMiner":
            text = self.extract_text_with_pdfminer()
        elif extraction_tool == "PyMuPDF":
            text = self.extract_text_with_pymupdf()
        elif extraction_tool == "PyPDF4":
            text = self.extract_text_with_pypdf4()
        else:
            text = "Invalid Extraction Tool selected."

        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.END, text)

        transformer = self.transformer_var.get()

        if transformer == "SpaCy":
            processed_text = self.process_text_with_spacy(text)
        else:
            processed_text = "Invalid Transformer selected."

        self.processed_text_box.delete('1.0', tk.END)
        self.processed_text_box.insert(tk.END, processed_text)

    def extract_text_with_pdfminer(self):
        import pdfminer.high_level
        with open(self.file_path, 'rb') as file:
            text = pdfminer.high_level.extract_text(file, page_numbers=None, maxpages=0, password=None)
            return text

    def extract_text_with_pymupdf(self):
        import fitz
        with fitz.open(self.file_path) as doc:
            text_list = [page.get_text() for page in doc]
            text = ''.join(text_list)
            return text

    def extract_text_with_pypdf4(self):
        import PyPDF4
        with open(self.file_path, 'rb') as file:
            reader = PyPDF4.PdfFileReader(file)
            text_list = [page.extractText() for page in reader.pages]
            text = ''.join(text_list)
            return text

    def process_text_with_spacy(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        entities = [(ent.label_, ent.text) for ent in doc.ents]
        processed_text = ""
        for entity in entities:
            processed_text += f"{entity[0]}: {entity[1]}\n"
        return processed_text

    def export_excel(self):
        # Path to the PDF file
        pdf_path = self.file_path

        # Read PDF and extract tables
        df = tabula.read_pdf(pdf_path, pages='all')

        # Export tables to an XLSX file
        output_path = "./Outputs/output_file.xlsx"
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            for i, table in enumerate(df, start=1):
                table.to_excel(writer, sheet_name=f"Table {i}", index=False)
                
root = TkinterDnD.Tk()
root.overrideredirect(False)
root.iconphoto(True, tk.PhotoImage(file=r"C:\Users\Admin\BillWVF\Spacy\Images\wvf.png"))
pdf_extractor = PDFExtractorGUI(root)
root.mainloop()