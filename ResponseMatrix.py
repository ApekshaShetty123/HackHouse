import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np



class ResponseMatrix:
    def __init__(self, dist, data):
        df = data[data["District_Name"] == dist].copy()  # Ensure a copy of the DataFrame is created
        df['FIR_Reg_DateTime'] = pd.to_datetime(df['FIR_Reg_DateTime'])
        df['Offence_From_Date'] = pd.to_datetime(df['Offence_From_Date'])
        df['Response_Time'] = (df['FIR_Reg_DateTime'] - df['Offence_From_Date']).dt.total_seconds() / (3600)  # Convert to hours
        self.df = df

    def create_line(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['FIR_Reg_DateTime'], self.df['Response_Time'], marker='o')
        plt.xlabel('FIR Registration Date/Time')
        plt.ylabel('Response Time (hours)')
        plt.title('Response Time Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url
    
    def create_pie(self):
        plt.figure(figsize=(8, 8))
        data = self.df['Year'].value_counts()
        labels = data.index
        plt.pie(data,  autopct='%1.1f%%', startangle=140)
        plt.title('FIR Stage')
        plt.axis('equal')
        plt.tight_layout()
        plt.legend(title="FIR Stage", labels=labels, loc="best")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url
    
    def create_histogram(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['Response_Time'], bins=10)
        plt.title('Histogram')
        plt.xlabel('Response Time (minutes)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url
