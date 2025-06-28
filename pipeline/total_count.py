import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

# Set style
sns.set_style('whitegrid')

# Load the merged DataFrame
merged_df = pd.read_csv("Data/MOCK_DATA.csv")

def total_count_calc(merged_df, merchent_id):
    """
    This function calculates the total transaction count in the last month,
    average daily transaction count, busiest and slowest days, and creates a
    visualization of daily transaction counts with KPIs.
    """
    # Convert payment_date to datetime
    merged_df['payment_date'] = pd.to_datetime(merged_df['payment_date'])
    merged_df = merged_df[merged_df['merchant_id'] == merchent_id]
    # Filter data for the last month
    last_month = merged_df[merged_df['payment_date'] >= (pd.to_datetime('today') - pd.DateOffset(months=1))]
    
    # Calculate transaction counts and KPIs
    daily_counts_last_month = last_month.groupby(last_month['payment_date'].dt.date).size()
    total_last_month = daily_counts_last_month.sum()
    avg_daily_last_month = daily_counts_last_month.mean()
    busiest_day = daily_counts_last_month.idxmax()
    busiest_count = daily_counts_last_month.max()
    slowest_day = daily_counts_last_month.idxmin()
    slowest_count = daily_counts_last_month.min()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(8.27,11.69))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 3], hspace=0.3)  # 1:3 ratio for table:chart
    
    # Create axes
    ax_table = fig.add_subplot(gs[0])
    ax_chart = fig.add_subplot(gs[1])
    
    # Create a surrounding box for both elements
    box = Rectangle((0.01, 0.01), 0.98, 0.98, linewidth=2, edgecolor='black', facecolor='none',
                    transform=fig.transFigure, zorder=-1)
    fig.patches.extend([box])
    
    # Add horizontal separator line
    separator_1 = Rectangle((0.01, 0.91), 0.98, 0.08, linewidth=1.5, edgecolor='black',
                         facecolor='#b7cbbf', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([separator_1])
    
    # Add horizontal separator line
    separator_2 = Rectangle((0.01, 0.70), 0.98, 0.002, linewidth=1.5, edgecolor='black',
                         facecolor='none', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([separator_2])
    
    # Add title for the entire visualization
    fig.suptitle('Transaction Count Analysis - Last 30 Days', fontsize=18, y=0.97)
    
    # KPI table (top)
    ax_table.set_title('Count Analysis', fontsize=12, pad=3)
    ax_table.axis('off')
    kpi_data = [
        ["Total Transactions", f"{total_last_month:,}"],
        ["Average Daily", f"{avg_daily_last_month:.1f}"],
        ["Busiest Day", f"{busiest_day} ({busiest_count} transactions)"],
        ["Slowest Day", f"{slowest_day} ({slowest_count} transactions)"]
    ]
    
    kpi_table = ax_table.table(
        cellText=kpi_data,
        colWidths=[0.3, 0.45],
        loc='center',
        cellLoc='left',
        colLabels=["Metric", "Value"]
    )
    
    # Style the table
    kpi_table.auto_set_font_size(False)
    kpi_table.set_fontsize(12)
    kpi_table.scale(1, 1.8)
    
    # Highlight header
    for (i, j), cell in kpi_table._cells.items():
        if i == 0:  # Header row
            cell.set_facecolor('#2a7fcc')
            cell.set_text_props(color='white', weight='bold')
        else:
            cell.set_facecolor('#f0f0f0')
    
    # Chart (bottom)
    bars = ax_chart.bar(
        daily_counts_last_month.index,
        daily_counts_last_month.values,
        color='green',
        alpha=0.7,
        edgecolor='darkgreen'
    )
    
    # Format x-axis
    ax_chart.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_chart.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.setp(ax_chart.get_xticklabels(), rotation=90)
    
    # Add labels and title
    ax_chart.set_title('Daily Transaction Counts', fontsize=14, pad=10)
    ax_chart.set_xlabel('Date', fontsize=12)
    ax_chart.set_ylabel('Number of Transactions', fontsize=12)
    ax_chart.grid(True, axis='y')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax_chart.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom'
        )
    
    # Adjust layout
    plt.tight_layout()
    
    # Save as PNG file
    plt.savefig('artifacts/transaction_count_analysis_last_month.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'transaction_count_analysis_last_month.png'")

if __name__ == "__main__":
    total_count_calc(merged_df, 3)
    print("Total count calculation completed.")