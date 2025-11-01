import pandas as pd
import matplotlib.pyplot as plt
import os
import config

class DataProcessor:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = None
        self.charts = []
        
        # Temp klasoru olustur
        if not os.path.exists(config.TEMP_FOLDER):
            os.makedirs(config.TEMP_FOLDER)
    
    def load_data(self):
        """Excel/CSV verisini yukle"""
        try:
            if self.data_file.endswith('.xlsx'):
                self.df = pd.read_excel(self.data_file)
            elif self.data_file.endswith('.csv'):
                self.df = pd.read_csv(self.data_file)
            else:
                print("Desteklenmeyen dosya formati")
                return False
            
            print(f"Veri yuklendi: {len(self.df)} satir")
            return True
            
        except Exception as e:
            print(f"Veri yukleme hatasi: {e}")
            return False
    
    def get_summary_stats(self):
        """Ozet istatistikler"""
        if self.df is None:
            return {}
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        stats = {}
        for col in numeric_cols:
            stats[f"{col} (Total)"] = f"{self.df[col].sum():,.0f}"
            stats[f"{col} (Average)"] = f"{self.df[col].mean():,.2f}"
            stats[f"{col} (Max)"] = f"{self.df[col].max():,.2f}"
        
        return stats
    
    def get_table_data(self, max_rows=10):
        """Tablo verisi al"""
        if self.df is None:
            return []
        
        # Ilk N satir
        data = [self.df.columns.tolist()]
        
        for idx, row in self.df.head(max_rows).iterrows():
            data.append([str(val) for val in row.values])
        
        return data
    
    def create_bar_chart(self, x_col, y_col, title="Bar Chart"):
        """Cubuk grafik olustur"""
        if self.df is None:
            return None
        
        try:
            plt.figure(figsize=(config.CHART_WIDTH, config.CHART_HEIGHT))
            
            # Ilk 10 satir
            data = self.df.head(10)
            
            plt.bar(data[x_col], data[y_col], color='#3498DB')
            plt.xlabel(x_col, fontsize=12, fontweight='bold')
            plt.ylabel(y_col, fontsize=12, fontweight='bold')
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            # Kaydet
            chart_path = f"{config.TEMP_FOLDER}/bar_chart.png"
            plt.savefig(chart_path, dpi=config.CHART_DPI)
            plt.close()
            
            self.charts.append(chart_path)
            print(f"Cubuk grafik olusturuldu: {chart_path}")
            return chart_path
            
        except Exception as e:
            print(f"Grafik olusturma hatasi: {e}")
            return None
    
    def create_pie_chart(self, column, title="Distribution"):
        """Pasta grafik olustur"""
        if self.df is None:
            return None
        
        try:
            plt.figure(figsize=(config.CHART_WIDTH, config.CHART_HEIGHT))
            
            # Ilk 5 kategori
            value_counts = self.df[column].value_counts().head(5)
            
            plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
            plt.title(title)
            plt.axis('equal')
            plt.tight_layout()
            
            # Kaydet
            chart_path = f"{config.TEMP_FOLDER}/pie_chart.png"
            plt.savefig(chart_path, dpi=config.CHART_DPI)
            plt.close()
            
            self.charts.append(chart_path)
            print(f"Pasta grafik olusturuldu: {chart_path}")
            return chart_path
            
        except Exception as e:
            print(f"Grafik olusturma hatasi: {e}")
            return None
    
    def create_line_chart(self, x_col, y_col, title="Trend"):
        """Cizgi grafik olustur"""
        if self.df is None:
            return None
        
        try:
            plt.figure(figsize=(config.CHART_WIDTH, config.CHART_HEIGHT))
            
            plt.plot(self.df[x_col], self.df[y_col], marker='o', linewidth=2, markersize=8, color='#2C3E50')
            plt.xlabel(x_col, fontsize=12, fontweight='bold')
            plt.ylabel(y_col, fontsize=12, fontweight='bold')
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.fill_between(self.df[x_col].index, self.df[y_col], alpha=0.2, color='#3498DB')
            plt.tight_layout()
            
            # Kaydet
            chart_path = f"{config.TEMP_FOLDER}/line_chart.png"
            plt.savefig(chart_path, dpi=config.CHART_DPI)
            plt.close()
            
            self.charts.append(chart_path)
            print(f"Cizgi grafik olusturuldu: {chart_path}")
            return chart_path
            
        except Exception as e:
            print(f"Grafik olusturma hatasi: {e}")
            return None
    
    def create_comparison_chart(self, columns, title="Comparison"):
        """Karsilastirma grafigi - birden fazla metric"""
        if self.df is None or len(columns) < 2:
            return None
        
        try:
            fig, ax = plt.subplots(figsize=(config.CHART_WIDTH, config.CHART_HEIGHT))
            
            x = range(len(self.df))
            width = 0.25
            colors_list = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']
            
            for i, col in enumerate(columns):
                offset = width * i
                ax.bar([p + offset for p in x], self.df[col], width, 
                      label=col, color=colors_list[i % len(colors_list)])
            
            ax.set_xlabel('Index', fontsize=12, fontweight='bold')
            ax.set_ylabel('Values', fontsize=12, fontweight='bold')
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xticks([p + width for p in x])
            ax.set_xticklabels(self.df.index)
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            chart_path = f"{config.TEMP_FOLDER}/comparison_chart.png"
            plt.savefig(chart_path, dpi=config.CHART_DPI)
            plt.close()
            
            self.charts.append(chart_path)
            print(f"Karsilastirma grafigi olusturuldu: {chart_path}")
            return chart_path
            
        except Exception as e:
            print(f"Grafik olusturma hatasi: {e}")
            return None
    
    def cleanup_charts(self):
        """Gecici grafikleri temizle"""
        for chart_path in self.charts:
            if os.path.exists(chart_path):
                os.remove(chart_path)
        self.charts = []

if __name__ == '__main__':
    # Test
    print("Data processor test - ornek veri ile calistirin")