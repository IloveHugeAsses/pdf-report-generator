from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
import os
import config

class PDFReportGenerator:
    def __init__(self, title=None, output_filename=None):
        self.title = title or config.REPORT_TITLE
        self.company_name = config.COMPANY_NAME
        self.author = config.REPORT_AUTHOR
        
        # Output klasorunu olustur
        if not os.path.exists(config.OUTPUT_FOLDER):
            os.makedirs(config.OUTPUT_FOLDER)
        
        # Dosya adi
        if output_filename:
            self.filename = f"{config.OUTPUT_FOLDER}/{output_filename}"
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.filename = f"{config.OUTPUT_FOLDER}/report_{timestamp}.pdf"
        
        # PDF belgesi olustur
        self.doc = SimpleDocTemplate(
            self.filename,
            pagesize=A4,
            topMargin=config.MARGIN_TOP,
            bottomMargin=config.MARGIN_BOTTOM,
            leftMargin=config.MARGIN_LEFT,
            rightMargin=config.MARGIN_RIGHT
        )
        
        # Icerik listesi
        self.story = []
        
        # Stiller
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Ozel stiller olustur"""
        # Baslik stili
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=config.PRIMARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        # Alt baslik
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=config.SECONDARY_COLOR,
            spaceBefore=20,
            spaceAfter=12
        ))
        
        # Normal metin
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            spaceAfter=12
        ))
    
    def add_title_page(self):
        """Kapak sayfasi ekle"""
        # Logo (varsa)
        if config.LOGO_PATH and os.path.exists(config.LOGO_PATH):
            logo = Image(config.LOGO_PATH, width=2*inch, height=1*inch)
            self.story.append(logo)
            self.story.append(Spacer(1, 0.5*inch))
        
        # Baslik
        title = Paragraph(self.title, self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Sirket adi
        company = Paragraph(
            f"<b>{self.company_name}</b>",
            self.styles['CustomBody']
        )
        self.story.append(company)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Tarih
        date_text = datetime.now().strftime('%B %d, %Y')
        date = Paragraph(date_text, self.styles['CustomBody'])
        self.story.append(date)
        
        # Yazar
        author = Paragraph(f"Prepared by: {self.author}", self.styles['CustomBody'])
        self.story.append(author)
        
        self.story.append(PageBreak())
    
    def add_section(self, title, content):
        """Bolum ekle"""
        # Baslik
        section_title = Paragraph(title, self.styles['CustomHeading'])
        self.story.append(section_title)
        
        # Icerik
        if isinstance(content, str):
            text = Paragraph(content, self.styles['CustomBody'])
            self.story.append(text)
        elif isinstance(content, list):
            for item in content:
                text = Paragraph(f"• {item}", self.styles['CustomBody'])
                self.story.append(text)
        
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_table(self, data, title=None, col_widths=None):
        """Tablo ekle"""
        if title:
            table_title = Paragraph(title, self.styles['CustomHeading'])
            self.story.append(table_title)
        
        # Tablo olustur
        table = Table(data, colWidths=col_widths)
        
        # Tablo stili
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), config.PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_chart(self, chart_path, title=None):
        """Grafik ekle"""
        if title:
            chart_title = Paragraph(title, self.styles['CustomHeading'])
            self.story.append(chart_title)
        
        if os.path.exists(chart_path):
            chart = Image(chart_path, width=5*inch, height=3*inch)
            self.story.append(chart)
            self.story.append(Spacer(1, 0.3*inch))
        else:
            print(f"Grafik bulunamadi: {chart_path}")
    
    def add_summary_box(self, metrics):
        """Ozet kutusu ekle (KPI'lar)"""
        data = [['Metric', 'Value']]
        
        for metric, value in metrics.items():
            data.append([metric, str(value)])
        
        self.add_table(data, title="Key Metrics Summary")
    
    def add_page_break(self):
        """Sayfa sonu ekle"""
        self.story.append(PageBreak())
    
    def generate(self):
        """PDF'i olustur"""
        try:
            self.doc.build(self.story)
            print(f"PDF olusturuldu: {self.filename}")
            return self.filename
        except Exception as e:
            print(f"PDF olusturma hatasi: {e}")
            return None

if __name__ == '__main__':
    # Test
    pdf = PDFReportGenerator(title="Test Report")
    pdf.add_title_page()
    pdf.add_section("Introduction", "This is a test report generated automatically.")
    
    # Ornek tablo
    data = [
        ['Product', 'Sales', 'Revenue'],
        ['Product A', '150', '$15,000'],
        ['Product B', '200', '$20,000'],
        ['Product C', '100', '$10,000']
    ]
    pdf.add_table(data, title="Sales Data")
    
    # Ornek metrikler
    metrics = {
        'Total Sales': '450 units',
        'Total Revenue': '$45,000',
        'Average Price': '$100',
        'Growth Rate': '+15%'
    }
    pdf.add_summary_box(metrics)
    
    pdf.generate()