import json
from fpdf import FPDF
import os

# --- PDF Class (No changes needed here) ---
class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'INVOICE', 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# --- create_invoice function (Updated to be safer with .get()) ---
def create_invoice(invoice_data):
    pdf = PDF()
    pdf.add_page()
    
    # Details
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, invoice_data.get('company_name', 'N/A'), 0, 1, 'L')
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 6, invoice_data.get('company_address', 'N/A'), 0, 1, 'L')
    pdf.ln(10)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Bill To:', 0, 1, 'L')
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 6, invoice_data.get('client_name', 'N/A'), 0, 1, 'L')
    pdf.cell(0, 6, invoice_data.get('client_address', 'N/A'), 0, 1, 'L')
    pdf.ln(10)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 10, 'Invoice Number:', 0, 0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, invoice_data.get('invoice_number', 'N/A'), 0, 1)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 10, 'Invoice Date:', 0, 0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, invoice_data.get('invoice_date', 'N/A'), 0, 1)
    pdf.ln(15)

    # Table
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(130, 10, 'Description', 1, 0, 'C')
    pdf.cell(60, 10, 'Amount', 1, 1, 'C')

    pdf.set_font('helvetica', '', 12)
    total_amount = 0
    for item in invoice_data.get('items', []):
        amount = item.get('amount', 0)
        total_amount += amount
        pdf.cell(130, 10, item.get('description', 'N/A'), 1, 0)
        pdf.cell(60, 10, f"${amount:.2f}", 1, 1, 'R')
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(130, 10, 'Total', 1, 0, 'R')
    pdf.cell(60, 10, f"${total_amount:.2f}", 1, 1, 'R')
    pdf.ln(10)

    # Notes
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Notes:', 0, 1)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 10, invoice_data.get('notes', ''))

    # Save PDF
    if not os.path.exists('invoices'):
        os.makedirs('invoices')
    
    file_name = f"invoices/Invoice-{invoice_data.get('invoice_number', 'Unknown')}.pdf"
    pdf.output(file_name)
    print(f"Successfully created {file_name}")

# --- Main execution block (This is where the main change is) ---
if __name__ == "__main__":
    # This script will now read data sent from the frontend via the GitHub Action trigger
    
    event_path = os.getenv('GITHUB_EVENT_PATH')
    
    if not event_path:
        print("Error: GITHUB_EVENT_PATH not found. This script must be run from a GitHub Action.")
        exit(1)
        
    try:
        with open(event_path, 'r') as f:
            event_data = json.load(f)
        
        # The data sent from the Netlify function is inside 'client_payload'
        invoice_data_from_frontend = event_data.get('client_payload', {}).get('invoice_data', {})

        if not invoice_data_from_frontend:
            raise ValueError("No invoice data found in the event payload.")

    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing event data: {e}")
        exit(1)

    # Call the function to create the PDF with the data from the frontend
    create_invoice(invoice_data_from_frontend)
