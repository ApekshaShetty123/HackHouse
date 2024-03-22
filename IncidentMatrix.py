import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np


class IncidentMatrix:
    def __init__(self, dist,data):
        df = data[data["District_Name"] == dist].copy()  # Ensure a copy of the DataFrame is created
        self.df = df

    def create_histogram(self):
        plt.figure(figsize=(14, 10))  # Adjust the figsize parameter for a bigger size
        sns.histplot(self.df['Year'], kde=True)
        plt.title('Incident Severity Metrics by District')
        plt.xlabel('District Name')
        plt.ylabel('Number of Incidents')
        plt.grid(True)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url

    def create_line(self):
        self.df['FIR_Date'] = pd.to_datetime(self.df['FIR_Date'], format='%d/%m/%Y')
        incident_count_by_date = self.df.groupby('FIR_Date').size()
        plt.figure(figsize=(10, 6))
        incident_count_by_date.plot(kind='line', marker='o', color='b', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Number of Incidents')
        plt.title('Incidents Over Time')
        plt.grid(True)
        plt.xticks(rotation=45)
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
        plt.title('Incident Severity Metrics (Pie Chart)')
        plt.axis('equal')  
        plt.tight_layout()
        plt.legend(title="Incident Severity Metrics", labels=labels, loc="best")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url

