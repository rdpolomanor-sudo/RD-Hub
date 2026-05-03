import base64
import os
import json

base_dir = r'e:\rd_hub'
html_file = os.path.join(base_dir, 'RD_Hub_v3.6.html')

pdf_mapping = {
    'design_team_leader': 'RD_RC_Design Team Leader.pdf',
    'product_designer': 'RD_RC_Product Designer.pdf',
    'merchandiser': 'RD_RC_Merchandiser.pdf',
    'tqa_team_leader': 'RD_RC_Tech Quality Control Team Leader.pdf',
    'qc_staff': 'RD_RC_Quality Control Staff.pdf'
}

pdf_data = {}
for key, filename in pdf_mapping.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'rb') as f:
        pdf_data[key] = base64.b64encode(f.read()).decode('utf-8')

js_code = '\n<script>\nconst RC_PDF_DATA = ' + json.dumps(pdf_data) + ';\n</script>\n</body>'

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace openRCPDF calls
html_content = html_content.replace("openRCPDF('rc_pdfs/RD_RC_Design_Team_Leader.pdf')", "openRCPDF('design_team_leader')")
html_content = html_content.replace("openRCPDF('rc_pdfs/RD_RC_Product_Designer.pdf')", "openRCPDF('product_designer')")
html_content = html_content.replace("openRCPDF('rc_pdfs/RD_RC_Merchandiser.pdf')", "openRCPDF('merchandiser')")
html_content = html_content.replace("openRCPDF('rc_pdfs/RD_RC_Tech_Quality_Control_Team_Leader.pdf')", "openRCPDF('tqa_team_leader')")
html_content = html_content.replace("openRCPDF('rc_pdfs/RD_RC_Quality_Control_Staff.pdf')", "openRCPDF('qc_staff')")

# Update openRCPDF function definition
old_func = """function openRCPDF(pdfFile) {
  const overlay = document.getElementById('pdf-modal-overlay');
  const frame = document.getElementById('pdf-modal-frame');
  const title = document.getElementById('pdf-modal-title');
  title.textContent = pdfFile.split('/').pop();
  frame.src = pdfFile;
  overlay.classList.add('show');
}"""

new_func = """function openRCPDF(pdfKey) {
  const overlay = document.getElementById('pdf-modal-overlay');
  const frame = document.getElementById('pdf-modal-frame');
  const title = document.getElementById('pdf-modal-title');
  title.textContent = pdfKey.replace(/_/g, ' ').toUpperCase() + ' RC';
  // Use #toolbar=0 to disable download/print in PDF viewer
  frame.src = 'data:application/pdf;base64,' + RC_PDF_DATA[pdfKey] + '#toolbar=0&navpanes=0&scrollbar=0';
  overlay.classList.add('show');
  
  // To further prevent right-click and copying inside the overlay
  document.addEventListener('contextmenu', event => event.preventDefault());
}"""

html_content = html_content.replace(old_func, new_func)

# Append JS code before </body>
html_content = html_content.replace('</body>', js_code)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Done!')
