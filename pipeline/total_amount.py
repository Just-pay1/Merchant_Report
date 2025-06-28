import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle

# Set style
sns.set_style('whitegrid')

# Load the merged DataFrame
merged_df = pd.read_csv("Data/MOCK_DATA.csv")

def total_amount_calc(merged_df, merchent_id):
    """
    This function calculates the total amount paid in the last month,
    average daily paid amount, highest day with its amount, and creates a
    visualization of daily paid amounts with KPIs.
    """
    # Convert payment_date to datetime and filter last month
    merged_df['payment_date'] = pd.to_datetime(merged_df['payment_date'])
    merged_df = merged_df[merged_df['merchant_id'] == merchent_id]
    last_month_start = datetime.now() - timedelta(days=30)
    last_month = merged_df[merged_df['payment_date'] >= last_month_start]
    
    # Calculate KPIs
    total_paid_last_month = last_month['paid_amount'].sum()
    avg_daily_paid = last_month.groupby(last_month['payment_date'].dt.date)['paid_amount'].sum().mean()
    max_day = last_month.groupby(last_month['payment_date'].dt.date)['paid_amount'].sum().idxmax()
    max_amount = last_month.groupby(last_month['payment_date'].dt.date)['paid_amount'].sum().max()
    
    # Create daily paid amounts series
    daily_paid = last_month.groupby(last_month['payment_date'].dt.date)['paid_amount'].sum()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(8.27,11.69))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 3], hspace=0.3)
    
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
    
    
    ax_table.set_title('Amounts Analysis', fontsize=12, pad=3)
    # KPI table
    kpi_data = [
        ["Total Paid Amount", f"${total_paid_last_month:,.2f}"],
        ["Average Daily", f"${avg_daily_paid:,.2f}"],
        ["Highest Day", f"{max_day.strftime('%Y-%m-%d')} (${max_amount:,.2f})"]
    ]
    
    ax_table.axis('off')
    kpi_table = ax_table.table(
        cellText=kpi_data,
        colWidths=[0.3, 0.4],
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
    
    # Add title for the entire visualization
    fig.suptitle('Payment Analysis - Last 30 Days', fontsize=18, y=0.96)
    
    # Main histogram plot
    bars = ax_chart.bar(
        daily_paid.index,
        daily_paid.values,
        color='royalblue',
        alpha=0.7,
        edgecolor='white'
    )
    
    # Format x-axis
    ax_chart.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_chart.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.setp(ax_chart.get_xticklabels(), rotation=90)
    
    # Add labels and title
    ax_chart.set_title('Daily Paid Amounts', fontsize=14, pad=10)
    ax_chart.set_ylabel('Total Paid Amount ($)', fontsize=12)
    ax_chart.grid(True, axis='y')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax_chart.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'${height:,.0f}',
                ha='center',
                va='bottom',
                fontsize=9
            )
    
    # Add trend line (7-day moving average)
    if len(daily_paid) > 7:
        moving_avg = daily_paid.rolling(window=7).mean()
        ax_chart.plot(
            daily_paid.index,
            moving_avg.values,
            color='red',
            linestyle='--',
            linewidth=2,
            label='7-day Moving Avg'
        )
        ax_chart.legend()
    
    # Save as PNG file
    plt.savefig('artifacts/payment_analysis_last_month.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'payment_analysis_last_month.png'")

if __name__ == "__main__":
    total_amount_calc(merged_df, merchent_id=3)
    print("Total amount calculation and visualization completed.")