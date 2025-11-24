# PDF Report Generator

Automated professional PDF report generator from Excel/CSV data.

### Features

- 📄 Professional PDF generation
- 📊 Automatic chart creation (bar, line, comparison)
- 📈 Statistical analysis
- 🎨 Branded templates with custom colors
- 📋 Data tables with styling
- 🔢 Key metrics summary boxes

### Tech Stack

- Python 3.10+
- ReportLab (PDF generation)
- Pandas (data processing)
- Matplotlib (chart creation)
- OpenPyXL (Excel reading)

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit `config.py`:

```python
COMPANY_NAME = "Your Company"
REPORT_TITLE = "Monthly Business Report"
PRIMARY_COLOR = HexColor('#2C3E50')
```

### Usage

```bash
python main.py
```

The tool will:
1. Load data from Excel/CSV
2. Generate statistics
3. Create visualizations
4. Build professional PDF report

Reports saved to `reports/` folder.

### Input Format

Excel/CSV with columns like:
- Month, Sales, Revenue, Customers
- Or any numerical data

### Sample Output

Professional PDF including:
- Cover page with branding
- Executive summary
- Key metrics table
- Data visualizations
- Detailed analysis
- Conclusions & recommendations

### Use Cases

- Monthly business reports
- Client performance summaries
- Sales team dashboards
- Marketing campaign results
- Financial analysis reports

### Customization

Easily customize:
- Colors and branding
- Chart types
- Report sections
- Logo placement

### License

MIT

---

MIT

---

Built with ⚡ by [Forge270](https://github.com/Forge270)
