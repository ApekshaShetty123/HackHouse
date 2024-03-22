import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np


class TrendMatrix:
    def __init__(self, dist,data):
        df = data[data["District_Name"] == dist].copy()  # Ensure a copy of the DataFrame is created
        df['Offence_From_Date'] = pd.to_datetime(df['Offence_From_Date'], errors='coerce')  # Convert to datetime
        df['Offence_To_Date'] = pd.to_datetime(df['Offence_To_Date'], errors='coerce')  # Convert to datetime
        # Drop rows with NaT values
        df = df.dropna(subset=['Offence_From_Date', 'Offence_To_Date'])
        # Calculate response time in minutes
        df['Response_Time'] = (df['Offence_To_Date'] - df['Offence_From_Date']).dt.total_seconds() / 60
        
        self.df = df

    def create_line(self):
        plt.figure(figsize=(10, 6))
        # Check if 'Offence_From_Date' and 'Response_Time' are numeric columns
        if self.df['Offence_From_Date'].dtype == 'datetime64[ns]' and self.df['Response_Time'].dtype in ['int64', 'float64']:
            self.df.plot(x='Offence_From_Date', y='Response_Time', kind='line')
            plt.xlabel('Offence From Date')
            plt.ylabel('Response Time (minutes)')
            plt.title('Response Time Trend')
            plt.xticks(rotation=45)
            plt.tight_layout()
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()
            return plot_url
        
    def create_pie(self):
        plt.figure(figsize=(8, 8))
        offence_counts = self.df['Complaint_Mode'].value_counts()
        offence_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribution of Offence Types')
        plt.axis('equal')
        plt.tight_layout()
        plt.legend(title="Distribution of Offence Types", labels=offence_counts.index, loc="best")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url

    def create_histogram(self):
        plt.figure(figsize=(10, 6))
        offence_counts = self.df['Complaint_Mode'].value_counts()
        offence_counts.plot(kind='bar')
        plt.xlabel('Offence Type')
        plt.ylabel('Number of Offences')
        plt.title('Offence Type Distribution')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url


    


