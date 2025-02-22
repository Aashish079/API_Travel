import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Training loss data
steps = np.arange(1, 61)
loss_values = [
    2.203500, 2.073700, 2.102900, 1.883600, 2.110300, 2.270200, 1.806200, 1.676100, 1.625200, 1.585700,
    1.585000, 1.366600, 1.494000, 1.368600, 1.180900, 1.223300, 1.255600, 1.232100, 1.159600, 1.104800,
    1.066600, 1.062100, 0.982200, 0.820600, 1.049700, 0.847800, 0.698200, 0.880400, 0.580400, 0.726900,
    0.612000, 0.677400, 0.571000, 0.560700, 0.598300, 0.680500, 0.486900, 0.452100, 0.467400, 0.398800,
    0.390200, 0.511400, 0.309800, 0.305300, 0.289200, 0.261300, 0.236200, 0.239300, 0.234400, 0.270000,
    0.270100, 0.168200, 0.219400, 0.224200, 0.226300, 0.108100, 0.190300, 0.196600, 0.226300, 0.196700
]

# Calculate moving average (window size = 5)
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

moving_avg = moving_average(loss_values, 5)
moving_avg_steps = steps[4:]  # Adjust x-axis for moving average

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('LLM Fine-tuning Training Analysis \n', fontsize=16, fontweight='bold')

# Main plot - Training Loss
ax1.plot(steps, loss_values, 'o-', color='#4A56E2', alpha=0.7, markersize=4, label='Training Loss')
ax1.plot(moving_avg_steps, moving_avg, '-', color='#FF6B6B', linewidth=2, label='5-Step Moving Average')

# Add epoch markers
steps_per_epoch = 20
for epoch in range(1, 4):
    step_num = epoch * steps_per_epoch
    if step_num <= len(steps):
        ax1.axvline(x=step_num, color='gray', linestyle='--', alpha=0.5)
        ax1.text(step_num, 0.1, f'Epoch {epoch}', rotation=90, verticalalignment='bottom', 
                 horizontalalignment='right', color='gray')

# Set up the first subplot
ax1.set_xlabel('Training Step')
ax1.set_ylabel('Loss')
ax1.set_ylim(0, 2.5)
ax1.set_xlim(0, 61)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(loc='upper right')
ax1.set_title('Training Loss Over Time', fontsize=14)

# Annotate important points
ax1.annotate('Initial Loss: 2.20', xy=(1, 2.20), xytext=(5, 2.3),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=9)
ax1.annotate('Final Loss: 0.20', xy=(60, 0.20), xytext=(50, 0.5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=9)
ax1.annotate('Lowest Loss: 0.108', xy=(56, 0.108), xytext=(45, 0.3),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6), fontsize=9)

# Create a table of training metrics in the second subplot
ax2.axis('tight')
ax2.axis('off')

metrics_data = [
    ["Total Training Time", "17.3 minutes"],
    ["Peak Memory Usage", "1.938 GB (13.14% of max)"],
    ["Total Steps", "60"],
    ["Batch Size", "8 (2 per device × 4 accumulation steps)"],
    ["Trainable Parameters", "41,943,040"],
    ["Training Examples", "220"]
]

table = ax2.table(
    cellText=metrics_data,
    colLabels=["Metric", "Value"],
    loc='center',
    cellLoc='left',
    colWidths=[0.4, 0.6]
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)
for (row, col), cell in table.get_celld().items():
    if row == 0:  # Header
        cell.set_text_props(fontproperties=dict(weight='bold'))
        cell.set_facecolor('#e0e0e0')
    elif row % 2 == 1:  # Alternating row colors
        cell.set_facecolor('#f5f5f5')

ax2.set_title('Training Configuration Metrics', fontsize=14)

# Calculate some statistics for the text box
initial_loss = loss_values[0]
final_loss = loss_values[-1]
min_loss = min(loss_values)
min_loss_step = loss_values.index(min_loss) + 1
reduction_pct = ((initial_loss - final_loss) / initial_loss) * 100

# Add a text box with analysis
textstr = '\n'.join([
    'Loss Analysis:',
    f'• Initial Loss: {initial_loss:.2f}',
    f'• Final Loss: {final_loss:.2f}',
    f'• Minimum Loss: {min_loss:.3f} (Step {min_loss_step})',
    f'• Reduction: {reduction_pct:.1f}%',
    '',
    # 'The loss curve indicates successful training with a 91% reduction in error.',
    # 'Training converged well with significant improvements during epoch 2.'
])

props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
ax1.text(0.65, 0.97, textstr, transform=ax1.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.subplots_adjust(hspace=0.3)

# Save the figure 
plt.savefig('llm_training_analysis.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()