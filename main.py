import json
from fpdf import FPDF
import os # Yeh line add karein

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'INVOICE', 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_invoice(invoice_data):
    pdf = PDF()
    pdf.add_page()
    
    # --- Details ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, invoice_data['company_name'], 0, 1, 'L')
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 6, invoice_data['company_address'], 0, 1, 'L')
    pdf.ln(10)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Bill To:', 0, 1, 'L')
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 6, invoice_data['client_name'], 0, 1, 'L')
    pdf.cell(0, 6, invoice_data['client_address'], 0, 1, 'L')
    pdf.ln(10)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 10, 'Invoice Number:', 0, 0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, invoice_data['invoice_number'], 0, 1)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 10, 'Invoice Date:', 0, 0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, invoice_data['invoice_date'], 0, 1)
    pdf.ln(15)

    # --- Table ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(130, 10, 'Description', 1, 0, 'C')
    pdf.cell(60, 10, 'Amount', 1, 1, 'C')

    pdf.set_font('helvetica', '', 12)
    for item in invoice_data['items']:
        pdf.cell(130, 10, item['description'], 1, 0)
        pdf.cell(60, 10, f"${item['amount']:.2f}", 1, 1, 'R')
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(130, 10, 'Total', 1, 0, 'R')
    pdf.cell(60, 10, f"${invoice_data['total']:.2f}", 1, 1, 'R')
    pdf.ln(10)

    # --- Notes ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Notes:', 0, 1)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 10, invoice_data['notes'])

    # --- Save PDF ---
    # Output folder banayein agar mojood nahi hai
    if not os.path.exists('invoices'):
        os.makedirs('invoices')
    
    file_name = f"invoices/Invoice-{invoice_data['invoice_number']}.pdf"
    pdf.output(file_name)
    print(f"Successfully created {file_name}")

if __name__ == "__main__":
    try:
        with open('data.json', 'r') as f:
            invoice_data = json.load(f)
    except FileNotFoundError:
        print("Error: data.json not found.")
        exit()
    create_invoice(invoice_data)
