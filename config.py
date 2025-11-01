import os
from reportlab.lib.colors import HexColor

# Report ayarlari
REPORT_TITLE = "Monthly Business Report"
COMPANY_NAME = "Your Company Name"
REPORT_AUTHOR = "Analytics Team"

# Renkler (Brand colors)
PRIMARY_COLOR = HexColor('#2C3E50')  # Koyu mavi
SECONDARY_COLOR = HexColor('#3498DB')  # Acik mavi
ACCENT_COLOR = HexColor('#E74C3C')  # Kirmizi
SUCCESS_COLOR = HexColor('#2ECC71')  # Yesil

# Dosya yollari
OUTPUT_FOLDER = 'reports'
TEMP_FOLDER = 'temp'
LOGO_PATH = None  # Opsiyonel: 'logo.png'

# Sayfa ayarlari
PAGE_SIZE = 'A4'
MARGIN_TOP = 72
MARGIN_BOTTOM = 72
MARGIN_LEFT = 72
MARGIN_RIGHT = 72

# Grafik ayarlari
CHART_DPI = 150
CHART_WIDTH = 5
CHART_HEIGHT = 3

# Ornek veri dosyasi
SAMPLE_DATA_FILE = 'sample_data.xlsx'