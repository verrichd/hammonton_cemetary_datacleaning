import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read in DOB, DOD, and Sex columns from data files
df = pd.read_csv("data\halloween2019b.csv",usecols=[2,3,4])
df1 = pd.read_csv("data\halloween2019c.csv",usecols=[1,2,3])

# Delete any rows that contain NA or equivalent values
df.dropna(how='any',inplace=True)
df1.dropna(how='any',inplace=True)

# Remove any spaces in column names
df.columns = df.columns.str.replace(' ', '')

# Format DOB and DOD to hold only the year
df['DOB'] = df['DOB'].astype(str).str[-4:]
df['DOD'] = df['DOD'].astype(str).str[-4:]
df1['DOB'] = df1['DOB'].astype(str).str[-4:]
df1['DOD'] = df1['DOD'].astype(str).str[-4:]

# Format Sex -- Remove all whitespace, make lowercase, and keep only first letter
df['Sex'] = df['Sex'].astype(str).str.lower().str.strip().str[0]
df1['Sex'] = df1['Sex'].astype(str).str.lower().str.strip().str[0]

# Cast formatted year columns to integers for future calculations
df['DOB'] = df['DOB'].astype(int)
df['DOD'] = df['DOD'].astype(int)
df1['DOB'] = df1['DOB'].astype(int)
df1['DOD'] = df1['DOD'].astype(int)

# Create new column subtracting DOB from DOD to get lifespan
df['lifespan'] = df['DOD'] - df['DOB']
df1['lifespan'] = df1['DOD'] - df1['DOB']

# Drop rows with negative values for lifespan
df.drop(df[df.lifespan < 0].index, inplace=True)
df1.drop(df1[df1.lifespan < 0].index, inplace=True)

# Merge unified data to one common data frame
df = pd.concat([df,df1],ignore_index=True)

print(df)

# Use groupby() to group DOB (decades) showing average lifespan for each Sex
df_grouped_by_gender = df.groupby([pd.cut(df["DOB"], np.arange(1810, 2010, 10)),'Sex'])['lifespan'].mean().unstack()

print(df_grouped_by_gender)

# Year labels on x axis
labels = np.arange(1810, 2000, 10)

# Creating lists of data for male and female average lifespan by year
male_avg = df_grouped_by_gender['m'].tolist()
fem_avg = df_grouped_by_gender['f'].tolist()

# Setting label locations on x axis
x = np.arange(len(labels))  
# will represent width of bars in chart
width = 0.45 

# Create figure with two bar plots using male_avg and fem_avg
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, male_avg, width, label='Men')
rects2 = ax.bar(x + width/2, fem_avg, width, label='Women')

# Adding labels for title and axes
ax.set_ylabel('Lifespan')
ax.set_xlabel('Year')
ax.set_title('Lifespan by year and gender')

# Add tick marks on x axis labels
ax.set_xticks(x, labels)

# Add legend
ax.legend()

# Display created bar chart
fig.tight_layout()
plt.show()
