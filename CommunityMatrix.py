import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np




class CommunityMatrix:
    def __init__(self, dist, data):
        df = data[data["District_Name"] == dist].copy()  # Ensure a copy of the DataFrame is created
        df['Year_Month'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str), format='%Y-%m')
        self.df = df

    def create_line(self):
        plt.figure(figsize=(10, 6))
        crime_counts = self.df.groupby(['Year_Month', 'CrimeGroup_Name']).size().reset_index(name='Count') 
        for crime_group, group_data in crime_counts.groupby('CrimeGroup_Name'):
            plt.plot(group_data['Year_Month'], group_data['Count'], label=crime_group)
        plt.xlabel('Year-Month')
        plt.ylabel('Count')
        plt.title('Trend of Crime by Crime Group Name')
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
        crime_group_counts = self.df['CrimeGroup_Name'].value_counts()
        # Adjust the label format to show percentages for significant slices only
        def func(pct, all_vals):
            absolute = int(pct/100.*sum(all_vals))
            return f'{pct:.1f}%\n({absolute:d} cases)'

        plt.pie(crime_group_counts, autopct=lambda pct: func(pct, crime_group_counts),
                startangle=140)
        plt.axis('equal')
        plt.title('Distribution of Crime by Crime Group Name')
        plt.tight_layout()
        plt.legend(title="Distribution of Crime by Crime Group Name", labels=crime_group_counts.index, loc="best")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url



    def create_histogram(self):
        plt.figure(figsize=(10, 6))
        top_crime_groups = self.df['CrimeGroup_Name'].value_counts().head(10)  # Select top 10 crime groups
        filtered_df = self.df[self.df['CrimeGroup_Name'].isin(top_crime_groups.index)]  # Filter data for top crime groups
        filtered_df['CrimeGroup_Name'].value_counts().plot(kind='bar', alpha=0.7, color='blue', edgecolor='black')
        plt.xlabel('Crime Group Name')
        plt.ylabel('Frequency')
        plt.title('Frequency of Top Crime Groups')
        plt.grid(True)
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return plot_url



