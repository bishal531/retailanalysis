"""
Generate sample retail sales data for EDA project
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_retail_sales_data(n_records=1000):
    """
    Generate sample retail sales dataset
    
    Parameters:
    -----------
    n_records : int
        Number of sales records to generate
    
    Returns:
    --------
    pd.DataFrame
        Sample retail sales dataset
    """
    
    np.random.seed(42)
    
    # Generate dates over 2 years
    start_date = datetime(2022, 1, 1)
    dates = [start_date + timedelta(days=int(x)) for x in np.random.uniform(0, 730, n_records)]
    
    # Create sample data
    data = {
        'transaction_id': range(1, n_records + 1),
        'date': dates,
        'store_id': np.random.randint(1, 11, n_records),  # 10 stores
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books'], n_records),
        'quantity': np.random.randint(1, 10, n_records),
        'unit_price': np.random.uniform(10, 500, n_records),
        'customer_age': np.random.randint(18, 80, n_records),
        'customer_gender': np.random.choice(['M', 'F'], n_records),
        'payment_method': np.random.choice(['Cash', 'Credit Card', 'Debit Card', 'Online'], n_records),
    }
    
    df = pd.DataFrame(data)
    df['total_sales'] = df['quantity'] * df['unit_price']
    
    return df

if __name__ == "__main__":
    print("Generating sample retail sales dataset...")
    df = generate_retail_sales_data(1000)
    
    # Save to CSV
    df.to_csv('data/retail_sales.csv', index=False)
    print(f"✓ Dataset generated successfully!")
    print(f"  Records: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Saved to: data/retail_sales.csv")
    print("\nFirst few rows:")
    print(df.head())
