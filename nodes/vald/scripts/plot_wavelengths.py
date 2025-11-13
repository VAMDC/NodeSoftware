#!/usr/bin/env python
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('vald_dev.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT wave FROM transitions')
wavelengths = np.array([row[0] for row in cursor.fetchall()])
conn.close()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

bins = np.logspace(np.log10(wavelengths.min()), np.log10(wavelengths.max()), 150)
ax1.hist(wavelengths, bins=bins, edgecolor='black', linewidth=0.5)
ax1.set_xscale('log')
ax1.set_xlabel('Wavelength (Å, log scale)')
ax1.set_ylabel('Number of transitions')
ax1.set_title(f'Full wavelength distribution (N={len(wavelengths):,}, log scale)')
ax1.grid(alpha=0.3)

normal = wavelengths[wavelengths <= 100000]
outliers = wavelengths[wavelengths > 100000]
ax2.hist(normal, bins=100, edgecolor='black', linewidth=0.5)
ax2.set_xlabel('Wavelength (Å)')
ax2.set_ylabel('Number of transitions')
ax2.set_title(f'Normal range (≤100,000 Å): {len(normal):,} transitions | Outliers (>100,000 Å): {len(outliers):,}')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('wavelength_histogram.png', dpi=150)
print(f'Total: {len(wavelengths):,} transitions')
print(f'Range: {wavelengths.min():.2f} - {wavelengths.max():.2e} Å')
print(f'Normal (≤100k Å): {len(normal):,} transitions ({len(normal)/len(wavelengths)*100:.1f}%)')
print(f'Outliers (>100k Å): {len(outliers):,} transitions ({len(outliers)/len(wavelengths)*100:.1f}%)')
print('Saved to wavelength_histogram.png')
