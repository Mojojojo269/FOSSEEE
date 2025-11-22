import pandas as pd
from rest_framework import status
from rest_framework.response import Response


def validate_csv_columns(df):
    """
    Validate that CSV has required columns.
    """
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, None


def calculate_summary(df):
    """
    Calculate summary statistics from the dataframe.
    """
    summary = {
        'total_count': len(df),
        'avg_flowrate': float(df['Flowrate'].mean()),
        'avg_pressure': float(df['Pressure'].mean()),
        'avg_temperature': float(df['Temperature'].mean()),
        'type_distribution': df['Type'].value_counts().to_dict()
    }
    
    return summary


def process_csv_file(file):
    """
    Process uploaded CSV file and return data and summary.
    """
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate columns
        is_valid, error_message = validate_csv_columns(df)
        if not is_valid:
            return None, None, error_message
        
        # Validate numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    return None, None, f"Column '{col}' must contain numeric values"
        
        # Check minimum rows
        if len(df) < 1:
            return None, None, "CSV file must contain at least one row of data"
        
        # Calculate summary
        summary = calculate_summary(df)
        
        # Convert dataframe to list of dictionaries
        data = df.to_dict('records')
        
        return data, summary, None
        
    except pd.errors.EmptyDataError:
        return None, None, "CSV file is empty"
    except pd.errors.ParserError:
        return None, None, "Invalid CSV format"
    except Exception as e:
        return None, None, f"Error processing CSV: {str(e)}"
