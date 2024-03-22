class PolicePerformance:
    def __init__(self, dist, data, unit_name):
        df = data[data['District_Name'] == dist]
        df = df[df["UnitName"] == unit_name]
        self.df = df
    
    def gef_officer_info(self, si_name):
        df = self.df.copy()
        si_df = df[df['IOName'] == si_name]
        total_cases = len(si_df)
        resolved_cases = len(si_df[si_df['FIR_Stage'] != 'Undetected'])
        conviction_cases = len(si_df[si_df['FIR_Stage'] == 'Convicted'])

        case_resolution_rate = (resolved_cases / total_cases) * 100 if total_cases > 0 else 0
        conviction_rate = (conviction_cases / resolved_cases) * 100 if resolved_cases > 0 else 0

        avg_response_time = si_df['Response_Time'].mean() if 'Response_Time' in si_df else 0

        efficiency = ((resolved_cases - (total_cases - resolved_cases)) / resolved_cases) * 100 if resolved_cases > 0 else 0

        return {
            "Total_Cases": total_cases,
            "Resolved_Cases": resolved_cases,
            "Conviction_Cases": conviction_cases,
            "Case_Resolution_Rate": case_resolution_rate,
            "Conviction_Rate": conviction_rate,
            "Average_Response_Time": avg_response_time,
            "Efficiency_Investigation": efficiency
        }
