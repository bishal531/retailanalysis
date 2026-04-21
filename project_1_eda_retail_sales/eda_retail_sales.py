"""
EDA on Retail Sales Data
Author: bishal531
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Set visualization styles
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class RetailEDA:
    """
    Exploratory Data Analysis for Retail Sales Data
    """
    
    def __init__(self, data_path):
        """
        Initialize the EDA class with data path
        
        Parameters:
        -----------
        data_path : str
            Path to the retail sales data file
        """
        self.data_path = data_path
        self.df = None
        self.descriptive_stats = None
        
    def load_data(self):
        """Load the retail sales dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✓ Data loaded successfully!")
            print(f"  Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return None
    
    def data_info(self):
        """Display basic information about the dataset"""
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print("DATASET INFORMATION")
        print("="*50)
        
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"Rows: {self.df.shape[0]}, Columns: {self.df.shape[1]}")
        
        print("\n--- Column Information ---")
        print(self.df.info())
        
        print("\n--- Missing Values ---")
        missing = self.df.isnull().sum()
        if missing.sum() == 0:
            print("✓ No missing values found")
        else:
            print(missing[missing > 0])
        
        print("\n--- First Few Rows ---")
        print(self.df.head())
    
    def descriptive_statistics(self):
        """Calculate and display descriptive statistics"""
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print("DESCRIPTIVE STATISTICS")
        print("="*50)
        
        self.descriptive_stats = self.df.describe()
        print(self.descriptive_stats)
        
        # Calculate additional statistics (numeric columns only)
        numeric_df = self.df.select_dtypes(include=[np.number])
        print("\n--- Additional Statistics ---")
        print(f"Skewness:\n{numeric_df.skew()}\n")
        print(f"Kurtosis:\n{numeric_df.kurtosis()}\n")
    
    def correlation_analysis(self):
        """Analyze correlations between numeric columns"""
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print("CORRELATION ANALYSIS")
        print("="*50)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            correlation_matrix = self.df[numeric_cols].corr()
            print(correlation_matrix)
            
            # Visualize correlation heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                       center=0, fmt='.2f', square=True)
            plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('visualizations/correlation_heatmap.png', dpi=300, bbox_inches='tight')
            print("\n✓ Correlation heatmap saved to visualizations/correlation_heatmap.png")
            plt.close()
        else:
            print("Not enough numeric columns for correlation analysis")
    
    def distribution_analysis(self):
        """Analyze distributions of numeric columns"""
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print("DISTRIBUTION ANALYSIS")
        print("="*50)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Create histograms for numeric columns
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.ravel()
        
        for idx, col in enumerate(numeric_cols[:4]):
            axes[idx].hist(self.df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
        
        # Hide unused subplots
        for idx in range(len(numeric_cols[:4]), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig('visualizations/distributions.png', dpi=300, bbox_inches='tight')
        print("✓ Distribution plots saved to visualizations/distributions.png")
        plt.close()
    
    def categorical_analysis(self):
        """Analyze categorical columns"""
        if self.df is None:
            print("No data loaded. Call load_data() first.")
            return
        
        print("\n" + "="*50)
        print("CATEGORICAL ANALYSIS")
        print("="*50)
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols[:3]:  # Analyze first 3 categorical columns
            print(f"\n--- {col} ---")
            print(self.df[col].value_counts())
    
    def generate_report(self):
        """Generate a comprehensive EDA report"""
        print("\n" + "="*60)
        print("EXPLORATORY DATA ANALYSIS REPORT")
        print("Retail Sales Data Analysis")
        print("="*60)
        
        self.data_info()
        self.descriptive_statistics()
        self.correlation_analysis()
        self.distribution_analysis()
        self.categorical_analysis()
        
        print("\n" + "="*60)
        print("EDA COMPLETE!")
        print("="*60)
        print("\nGenerated visualizations saved in 'visualizations/' folder")


def main():
    """Main execution function"""
    print("Starting Retail Sales EDA Analysis...")
    print("="*60)
    
    # Create EDA instance (update path when dataset is available)
    eda = RetailEDA('data/retail_sales.csv')
    
    # Load and analyze data
    if eda.load_data() is not None:
        eda.generate_report()
    else:
        print("Please ensure the data file is placed at: data/retail_sales.csv")


if __name__ == "__main__":
    main()
