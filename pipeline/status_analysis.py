import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle

# Set style
sns.set_style('whitegrid')

# Load the merged DataFrame
merged_df = pd.read_csv("Data/MOCK_DATA.csv")
def transaction_status_analysis():
    """
    This function analyzes transaction statuses in the last month,
    calculates financial metrics, and creates a visualization of status distribution
    and financial breakdown.
    """
    # Convert payment_date to datetime
    merged_df['payment_date'] = pd.to_datetime(merged_df['payment_date'])
    # Filter for the last month
    last_month_date = datetime.now() - timedelta(days=30)
    filtered_df = merged_df[merged_df['payment_date'] >= last_month_date].copy()
    
    # Calculate metrics
    filtered_df['net_revenue'] = filtered_df['paid_amount'] - filtered_df['fee'] - filtered_df['commission_amount']
    status_counts = filtered_df['status'].value_counts()
    
    # Create figure with surrounding box
    fig = plt.figure(figsize=(8.27,11.69))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1.5, 1], hspace=0.3)
    
    # Create surrounding box
    box = Rectangle((0.01, 0.01), 0.98, 0.98, linewidth=2, edgecolor='black',
                    facecolor='none', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([box])
    
    # Add horizontal separator line
    separator_1 = Rectangle((0.01, 0.91), 0.98, 0.08, linewidth=1.5, edgecolor='black',
                         facecolor='#b7cbbf', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([separator_1])
    
    # Add horizontal separator line
    separator_2 = Rectangle((0.01, 0.50), 0.98, 0.002, linewidth=1.5, edgecolor='black',
                         facecolor='none', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([separator_2])
    
    # Add title for the entire visualization
    fig.suptitle('Transaction status Analysis - Last 30 Days', fontsize=18, y=0.96)
    
    
    # --- Pie Chart (Top Left) ---
    ax_pie = fig.add_subplot(gs[0, 0])
    wedges, texts, autotexts = ax_pie.pie(status_counts,
                                        labels=status_counts.index,
                                        autopct='%1.1f%%',
                                        colors=sns.color_palette('pastel'),
                                        startangle=90,
                                        textprops={'fontsize': 12})
    ax_pie.set_title('Transaction Status Distribution', fontsize=14, pad=5, loc='right',x=1.3)
    
    # Make autopct labels white and bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    # --- Status Count Table (Top Right) ---
    ax_table = fig.add_subplot(gs[0, 1])
    ax_table.axis('off')
    
    # Prepare table data
    table_data = []
    for status, count in status_counts.items():
        table_data.append([status, f"{count:,}"])
    
    # Add "Total" row
    table_data.append(["Total", f"{status_counts.sum():,}"])
    
    # Create table
    status_table = ax_table.table(cellText=table_data,
                                colWidths=[0.4, 0.3],
                                loc='center',
                                cellLoc='left',
                                colLabels=["Status", "Count"])
    
    # Style table
    status_table.auto_set_font_size(False)
    status_table.set_fontsize(12)
    status_table.scale(1, 1.8)
    
    # Highlight header and rows
    for (i, j), cell in status_table._cells.items():
        if i == 0:  # Header row
            cell.set_facecolor('#2a7fcc')  # Keep header blue
            cell.set_text_props(color='white', weight='bold')
        elif i == 1:  # First data row (e.g., Success)
            cell.set_facecolor('#F44336')  # Green
            cell.set_text_props(color='white', weight='bold')
        elif i == 2:  # Second data row (e.g., Failed)
            cell.set_facecolor('#4CAF50')  # Red
            cell.set_text_props(color='white', weight='bold')
        elif i == len(table_data):  # Total row
            cell.set_facecolor('#e6f2ff')  # Light blue
            cell.set_text_props(weight='bold')
    
    # --- Bar Chart (Bottom) ---
    ax_bar = fig.add_subplot(gs[1, :])  # Span all columns
    
    # Prepare values
    financial_values = [
        filtered_df['paid_amount'].sum(),
        filtered_df['net_revenue'].sum(),
        filtered_df['fee'].sum(),
        filtered_df['commission_amount'].sum()
    ]
    financial_labels = ['Paid Amount', 'Net Revenue', 'Fee', 'Commission']
    
    bars = ax_bar.bar(financial_labels, financial_values, color=sns.color_palette('Set2'))
    ax_bar.set_title('Financial Breakdown', fontsize=14, pad=20)
    ax_bar.set_ylabel('Amount ($)', fontsize=12)
    ax_bar.grid(True, axis='y')
    
    # Add value annotations
    for bar in bars:
        height = bar.get_height()
        ax_bar.annotate(f"${height:,.2f}",
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 5),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=11)
    
    # Save as PNG
    plt.savefig('artifacts/financial_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'financial_performance_analysis.png'")

if __name__ == "__main__":
    transaction_status_analysis()
    print("Transaction status analysis completed successfully.")