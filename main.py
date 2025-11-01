from pdf_generator import PDFReportGenerator
from data_processor import DataProcessor
import pandas as pd
import os
import config

def create_sample_data():
    """Ornek veri olustur"""
    data = {
        'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
        'Sales': [15000, 18000, 16500, 22000, 19500, 25000],
        'Revenue': [150000, 180000, 165000, 220000, 195000, 250000],
        'Customers': [120, 145, 135, 180, 160, 200]
    }
    
    df = pd.DataFrame(data)
    df.to_excel(config.SAMPLE_DATA_FILE, index=False)
    print(f"Ornek veri olusturuldu: {config.SAMPLE_DATA_FILE}")
    return config.SAMPLE_DATA_FILE

def main():
    print("="*60)
    print("PDF REPORT GENERATOR")
    print("="*60)
    
    # Veri dosyasi kontrol
    if not os.path.exists(config.SAMPLE_DATA_FILE):
        print("\nOrnek veri bulunamadi, olusturuluyor...")
        data_file = create_sample_data()
    else:
        data_file = config.SAMPLE_DATA_FILE
    
    print(f"\nVeri dosyasi: {data_file}")
    
    # Veriyi isle
    print("\n1. Veri isleniyor...")
    processor = DataProcessor(data_file)
    
    if not processor.load_data():
        print("Veri yuklenemedi!")
        return
    
    # Istatistikler
    print("\n2. Istatistikler hesaplaniyor...")
    stats = processor.get_summary_stats()
    
    # Grafikler olustur
    print("\n3. Grafikler olusturuluyor...")
    bar_chart = processor.create_bar_chart('Month', 'Sales', 'Monthly Sales')
    line_chart = processor.create_line_chart('Month', 'Revenue', 'Revenue Trend')
    
    # PDF olustur
    print("\n4. PDF raporu olusturuluyor...")
    pdf = PDFReportGenerator(
        title="Monthly Business Report",
        output_filename="business_report.pdf"
    )
    
    # Kapak
    pdf.add_title_page()
    
    # Executive Summary
    pdf.add_section(
        "Executive Summary",
        "This report provides a comprehensive overview of business performance for the reporting period. Key metrics show positive growth trends across all major indicators."
    )
    
    # Metrikler
    pdf.add_summary_box(stats)
    
    # Veri tablosu
    table_data = processor.get_table_data(max_rows=10)
    pdf.add_table(table_data, title="Detailed Data")
    
    # Grafikler
    pdf.add_page_break()
    pdf.add_section("Visual Analysis", "The following charts provide visual representation of key trends.")
    
    if bar_chart:
        pdf.add_chart(bar_chart, title="Sales Performance")
    
    if line_chart:
        pdf.add_chart(line_chart, title="Revenue Trends")
    
    # Sonuc
    pdf.add_page_break()
    pdf.add_section(
        "Conclusion",
        [
            "Strong performance across all key metrics",
            "Revenue growth of 67% over the period",
            "Customer acquisition increased by 67%",
            "Recommended actions: Continue current strategy and increase marketing spend"
        ]
    )
    
    # PDF olustur
    result = pdf.generate()
    
    # Temizlik
    processor.cleanup_charts()
    
    if result:
        print("\n" + "="*60)
        print("BASARILI!")
        print("="*60)
        print(f"Rapor olusturuldu: {result}")
        print("="*60)
    else:
        print("\nPDF olusturulamadi!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram durduruldu")
    except Exception as e:
        print(f"\nHata: {e}")
        import traceback
        traceback.print_exc()