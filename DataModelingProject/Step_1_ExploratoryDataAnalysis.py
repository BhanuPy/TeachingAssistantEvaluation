import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data.csv', header=None)

# Assign column names to the dataset
df.columns = ['native_english_speaker', 'course_instructor', 'course', 'semester', 'class_size', 'score']

# Display the first few rows of the dataset
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Get summary statistics of the dataset
print(df.describe())

# Plot histograms of the features
df.hist(bins=20, figsize=(10,10))
plt.savefig('histograms_of_the_features.png')
plt.show()
plt.close()


# Plot a correlation matrix of the features
corr = df.corr()
plt.figure(figsize=(8,8))
plt.imshow(corr, cmap='Blues', interpolation='none', aspect='auto')
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation='vertical')
plt.yticks(range(len(corr)), corr.columns);
plt.savefig('correlation_matrix_of_the_features.png')
plt.show()
plt.close()