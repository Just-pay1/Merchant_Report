import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import pandas as pd

# Set style
sns.set_style('whitegrid')

# Load the merged DataFrame
merged_df = pd.read_csv("Data/MOCK_DATA.csv")
def user_state_distribution(merged_df, merchant_id):
    """
    This function analyzes user distribution by state,
    calculates the top states by user count, and creates a pie chart visualization.
    """
    # Convert payment_date to datetime
    merged_df['payment_date'] = pd.to_datetime(merged_df['payment_date'])
    merged_df = merged_df[merged_df['merchant_id'] == merchant_id]
    
    # Calculate top states
    user_state_dist = merged_df.groupby('user_id')['state'].first().value_counts()
    top_states = user_state_dist.head(10)
    
    # Create single figure
    fig, ax = plt.subplots(figsize=(8.27,11.69))
    
    # Plot pie chart
    ax.pie(top_states, labels=top_states.index, autopct='%1.1f%%',
           colors=sns.color_palette('pastel'), startangle=90)
    ax.set_title('Top 10 States by User Count', fontsize=14)
    
    # Add surrounding box
    box = Rectangle((0.01, 0.01), 0.98, 0.98, linewidth=2, edgecolor='black',
                    facecolor='none', transform=fig.transFigure, zorder=-1)
    fig.patches.append(box)
    
    # Add header bar
    separator = Rectangle((0.01, 0.91), 0.98, 0.08, linewidth=1.5, edgecolor='black',
                          facecolor='#b7cbbf', transform=fig.transFigure, zorder=-1)
    fig.patches.append(separator)
    
    # Add title
    fig.suptitle('User Distribution Analysis - Last 30 Days', fontsize=18, y=0.975)
    
    # Save as PNG
    output_path = "artifacts/user_state_distribution.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)

if __name__ == "__main__":
    user_state_distribution(merged_df, merchent_id=3)
    print("User state distribution analysis completed and saved as 'artifacts/user_state_distribution.png'.")