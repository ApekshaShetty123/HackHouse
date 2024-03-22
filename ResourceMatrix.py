from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
# Calculate resource allocation metrics


class ResourceMatrix:
    def __init__(self, dist, data):
        df = data[data["District_Name"] == dist].copy()  # Ensure a copy of the DataFrame is created
        self.df = df

# Function to generate the chart and convert it to base64 encoding
    def create_line(self):
        plt.figure(figsize=(10, 6))
        fir_stage_counts = self.df['FIR_Stage'].value_counts()
        fir_stage_counts.plot(kind='line', marker='o')
        plt.title('FIR Stage Counts')
        plt.xlabel('FIR Stage')
        plt.ylabel('Count')
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
        plt.figure(figsize=(10, 6))
        fir_stage_counts = self.df['FIR_Stage'].value_counts()
        plt.pie(fir_stage_counts, autopct='%1.1f%%', startangle=140)
        plt.title('FIR Stage Distribution')
        plt.axis('equal')
        plt.tight_layout()
        
        # Adding a legend for better representation
        plt.legend(title="FIR Stage", labels=fir_stage_counts.index, loc="best")
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url


    def create_histogram(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.df, x='FIR_Stage')
        plt.title('FIR Stage Distribution')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.yticks(rotation=90)  # Rotate y-axis labels vertically
        plt.grid(True)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url
    
    

