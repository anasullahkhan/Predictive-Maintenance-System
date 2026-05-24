import numpy as np
import matplotlib.pyplot as plt

# Simulate sensor data
days = 41
readings_per_day = 100
total = days * readings_per_day

# Normal data (30 days)
normal_vib = np.random.normal(2.0, 0.3, total)
normal_temp = np.random.normal(110, 2, total)
normal_curr = np.random.normal(5.0, 0.5, total)

# Create degrading data
test_vib = []
test_temp = []
test_curr = []

for i in range(total):
    day = i // 100
    if day < 30:
        vib = np.random.normal(2.0, 0.3)
        temp = np.random.normal(110, 2)
        curr = np.random.normal(5.0, 0.5)
    elif day < 35:
        severity = (day - 30) / 5
        vib = np.random.normal(2.0 + severity*1.5, 0.3)
        temp = np.random.normal(110 + severity*5, 2)
        curr = np.random.normal(5.0 + severity*0.8, 0.5)
    elif day < 40:
        severity = (day - 35) / 5
        vib = np.random.normal(2.0 + 1.5 + severity*3, 0.3)
        temp = np.random.normal(110 + 5 + severity*10, 2)
        curr = np.random.normal(5.0 + 0.8 + severity*2, 0.5)
    else:
        vib = np.random.normal(6.5, 0.3)
        temp = np.random.normal(125, 2)
        curr = np.random.normal(8.0, 0.5)
    
    test_vib.append(abs(vib))
    test_temp.append(abs(temp) + 50)
    test_curr.append(abs(curr))

test_vib = np.array(test_vib)
test_temp = np.array(test_temp)
test_curr = np.array(test_curr)

# CREATE DASHBOARD IMAGE
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

# Main alert
ax_main = fig.add_subplot(gs[0, :])
ax_main.axis('off')

alert_text = """
EQUIPMENT MONITORING ALERT | Status: CRITICAL 🔴 | Time: 2026-05-24

CURRENT READINGS:
  Vibration: 6.23 mm/s (CRITICAL)  |  Temperature: 179.88°C (CRITICAL)  |  Current: 7.65A (CRITICAL)

⏰ TIME TO FAILURE: 0.0 days  |  🚨 SEVERITY: CRITICAL

RECOMMENDATION: STOP EQUIPMENT IMMEDIATELY - Emergency maintenance required within HOURS
ESTIMATED SAVINGS: ₹50,000 - ₹500,000 (By preventing unexpected failure)
"""

ax_main.text(0.05, 0.5, alert_text, transform=ax_main.transAxes, fontsize=10, 
            verticalalignment='center', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.9, pad=1))

# Vibration
ax1 = fig.add_subplot(gs[1, 0])
ax1.plot(test_vib[-500:], color='green', linewidth=1.5, label='Vibration')
ax1.axhline(y=3.34, color='red', linestyle='--', linewidth=2, label='Critical (3.34)')
ax1.fill_between(range(500), 3.34, max(test_vib[-500:]), alpha=0.2, color='red')
ax1.set_ylabel('Vibration (mm/s)', fontweight='bold')
ax1.set_title('Vibration - Last 5 Days', fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Temperature
ax2 = fig.add_subplot(gs[1, 1])
ax2.plot(test_temp[-500:], color='blue', linewidth=1.5, label='Temperature')
ax2.axhline(y=126.06, color='red', linestyle='--', linewidth=2, label='Critical (126.06)')
ax2.fill_between(range(500), 126.06, max(test_temp[-500:]), alpha=0.2, color='red')
ax2.set_ylabel('Temperature (°C)', fontweight='bold')
ax2.set_title('Temperature - Last 5 Days', fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Current
ax3 = fig.add_subplot(gs[2, 0])
ax3.plot(test_curr[-500:], color='orange', linewidth=1.5, label='Current')
ax3.axhline(y=7.57, color='red', linestyle='--', linewidth=2, label='Critical (7.57)')
ax3.fill_between(range(500), 7.57, max(test_curr[-500:]), alpha=0.2, color='red')
ax3.set_ylabel('Current (A)', fontweight='bold')
ax3.set_xlabel('Hours', fontweight='bold')
ax3.set_title('Current - Last 5 Days', fontweight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend()

# Health score
ax4 = fig.add_subplot(gs[2, 1])
health = 5  # Critical
colors = ['red' if health < 30 else 'orange' if health < 60 else 'green']
ax4.barh(['Equipment Health'], [health], color=colors, height=0.5)
ax4.set_xlim(0, 100)
ax4.text(health/2, 0, f'{health}%\nCRITICAL', va='center', ha='center', 
        fontweight='bold', fontsize=12, color='white')
ax4.set_xlabel('Health %', fontweight='bold')
ax4.set_title('Overall Health', fontweight='bold')

plt.savefig('dashboard_output.png', dpi=150, bbox_inches='tight', facecolor='white')
print("✅ Saved: dashboard_output.png")

# Create anomaly detection image
fig2, axes = plt.subplots(3, 1, figsize=(14, 10))

axes[0].plot(test_vib, color='green', linewidth=0.8, alpha=0.7)
axes[0].axhline(y=2.0, color='darkgreen', linestyle='--', alpha=0.5)
axes[0].fill_between(range(len(test_vib)), 2.0-3*0.3, 2.0+3*0.3, alpha=0.2, color='green')
anomalies_vib = test_vib > 3.34
axes[0].scatter(np.where(anomalies_vib)[0], test_vib[anomalies_vib], color='red', s=30, zorder=5)
axes[0].set_ylabel('Vibration (mm/s)', fontweight='bold')
axes[0].set_title('Anomaly Detection - Vibration (Red dots = Anomalies)', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

axes[1].plot(test_temp, color='blue', linewidth=0.8, alpha=0.7)
axes[1].axhline(y=110, color='darkblue', linestyle='--', alpha=0.5)
axes[1].fill_between(range(len(test_temp)), 110-3*2, 110+3*2, alpha=0.2, color='blue')
anomalies_temp = test_temp > 126.06
axes[1].scatter(np.where(anomalies_temp)[0], test_temp[anomalies_temp], color='red', s=30, zorder=5)
axes[1].set_ylabel('Temperature (°C)', fontweight='bold')
axes[1].set_title('Anomaly Detection - Temperature (Red dots = Anomalies)', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

axes[2].plot(test_curr, color='orange', linewidth=0.8, alpha=0.7)
axes[2].axhline(y=5.0, color='darkorange', linestyle='--', alpha=0.5)
axes[2].fill_between(range(len(test_curr)), 5.0-3*0.5, 5.0+3*0.5, alpha=0.2, color='orange')
anomalies_curr = test_curr > 7.57
axes[2].scatter(np.where(anomalies_curr)[0], test_curr[anomalies_curr], color='red', s=30, zorder=5)
axes[2].set_ylabel('Current (A)', fontweight='bold')
axes[2].set_xlabel('Reading Number', fontweight='bold')
axes[2].set_title('Anomaly Detection - Current (Red dots = Anomalies)', fontsize=12, fontweight='bold')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('anomaly_detection_output.png', dpi=150, bbox_inches='tight', facecolor='white')
print("✅ Saved: anomaly_detection_output.png")
print("\nBoth images generated successfully!")
