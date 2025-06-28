import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates

# Set style
sns.set_style('whitegrid')

# Load the merged DataFrame
merged_df = pd.read_csv("Data/MOCK_DATA.csv")
def user_analysis_metrics(df, merged_df, merchent_id):
    """
    This function analyzes user metrics in the last month,
    calculates total users, new users, market share, and creates a
    visualization of daily user counts with KPIs.
    """
    # Convert payment_date to datetime
    merged_df['payment_date'] = pd.to_datetime(merged_df['payment_date'])
    merged_df = merged_df[merged_df['merchant_id'] == merchent_id]
    
    # Prepare data
    last_month_start = datetime.now() - timedelta(days=30)
    total_users = merged_df['user_id'].nunique()
    new_users = merged_df[merged_df['payment_date'] >= last_month_start]['user_id'].nunique()
    
    # For market share - replace with actual platform users
    total_platform_users = df.shape[0]
    market_share = (total_users / total_platform_users) * 100
    
    # Daily user counts for last month
    daily_users = merged_df[merged_df['payment_date'] >= last_month_start].groupby(
        merged_df['payment_date'].dt.date
    )['user_id'].nunique()
    
    # Create figure
    fig = plt.figure(figsize=(8.27,11.69))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2], hspace=0.3)
    
    # Create surrounding box
    box = Rectangle((0.01, 0.01), 0.98, 0.98, linewidth=2, edgecolor='black',
                    facecolor='none', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([box])
    
    # Add horizontal separator line
    separator_1 = Rectangle((0.01, 0.91), 0.98, 0.08, linewidth=1.5, edgecolor='black',
                         facecolor='#b7cbbf', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([separator_1])
    
    # Add horizontal separator line
    separator_2 = Rectangle((0.01, 0.66), 0.98, 0.002, linewidth=1.5, edgecolor='black',
                         facecolor='none', transform=fig.transFigure, zorder=-1)
    fig.patches.extend([separator_2])
    
    # Add main title
    fig.suptitle('User Metrics Analysis - Last 30 Days', fontsize=18, y=0.96)
    
    # --- KPI Table (Top) ---
    ax_table = fig.add_subplot(gs[0])
    ax_table.axis('off')
    
    kpi_data = [
        ["Total Unique Users", f"{total_users:,}"],
        ["Market Share", f"{market_share:.1f}%"],
        ["New Users Last 30 Days", f"{new_users:,}"]
    ]
    
    kpi_table = ax_table.table(
        cellText=kpi_data,
        colWidths=[0.4, 0.4],
        loc='center',
        cellLoc='left',
        colLabels=["Metric", "Value"]
    )
    
    # Style the table
    kpi_table.auto_set_font_size(False)
    kpi_table.set_fontsize(12)
    kpi_table.scale(1, 2)
    
    # Highlight cells
    for (i, j), cell in kpi_table._cells.items():
        if i == 0:  # Header
            cell.set_facecolor('#2a7fcc')
            cell.set_text_props(color='white', weight='bold')
        elif i == 1:  # Total Users
            cell.set_facecolor('#4CAF50')  # Green
            cell.set_text_props(color='black', weight='bold')
        elif i == 2:  # Market Share
            cell.set_facecolor('#FF9800')  # Orange
            cell.set_text_props(color='black', weight='bold')
        elif i == 3:  # New Users
            cell.set_facecolor('#F5F5DC')  # Purple
            cell.set_text_props(color='black', weight='bold')
    
    # --- Daily User Chart (Bottom) ---
    ax_chart = fig.add_subplot(gs[1])
    
    # Plot daily users with trend line
    bars = ax_chart.bar(
        daily_users.index,
        daily_users.values,
        color='#9C27B0',  # Purple
        alpha=0.7,
        edgecolor='white',
        width=0.8
    )
    
    # Add 7-day moving average
    rolling_avg = daily_users.rolling(window=7).mean()
    ax_chart.plot(
        daily_users.index,
        rolling_avg,
        color='#FF5722',  # Deep orange
        linewidth=2,
        label='7-Day Average'
    )
    
    ax_chart.set_title('Daily Frequency of Users', fontsize=14, pad=20)
    ax_chart.set_ylabel('Number of Users', fontsize=12)
    ax_chart.grid(True, axis='y')
    ax_chart.legend()
    
    # Format x-axis
    ax_chart.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_chart.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.setp(ax_chart.get_xticklabels(), rotation=45)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax_chart.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10
            )
    
    
    plt.tight_layout()
    
    # Save as PNG
    plt.savefig('artifacts/daily_user_metrics.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'daily_user_metrics.png'")

if __name__ == "__main__":
    user_analysis_metrics(merged_df, merchent_id=3)
    print("User analysis completed successfully.")