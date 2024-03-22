import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np


class CrimeMatrix:
    def __init__(self, dist,data):
        df = data[data["District_Name"] == dist].copy()  # Ensure a copy of the DataFrame is created
        self.df = df

    def create_histogram(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['Year'], kde=True)
        plt.title('Response Time Histogram')
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

    def create_line(self):
        # Generate line chart
        plt.figure(figsize=(10, 6))
        self.df['Offence_From_Date'] = pd.to_datetime(self.df['Offence_From_Date'])  # Convert Offence_From_Date column to datetime
        df_sorted = self.df.groupby('Offence_From_Date')['FIRNo'].count().reset_index()  # Count FIR numbers for each date
        plt.plot(df_sorted['Offence_From_Date'], df_sorted['FIRNo'], marker='o', markersize=5)  # Increase marker size
        plt.title('Line Chart')
        plt.xlabel('Offence From Date')
        plt.ylabel('Number of FIRs')
        plt.grid(True)
        plt.xticks(rotation=90)  # Rotate x-axis labels by 90 degrees
        plt.tight_layout() 
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url

    def create_pie(self):
        plt.figure(figsize=(14, 12))
        data = self.df['Year'].value_counts()
        labels = data.index
        plt.pie(data,  autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of FIRs by Year')
        plt.axis('equal')  
        plt.tight_layout()
        plt.legend(title="Distribution of FIRs by Year", labels=labels, loc="best")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url


    
