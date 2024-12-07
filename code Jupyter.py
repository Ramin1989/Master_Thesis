import pandas as pd
import openpyxl
import seaborn as sns
import matplotlib.pyplot as plt
import glob
from IPython.display import display
import os
import sys
from datetime import date,timedelta
import json
import numpy as np
import time
from math import cos, sin
from os import path

from scipy.special import gammaln
import math

from sklearn.metrics import r2_score
from scipy.stats import circmean






# Read the Excel file into a pandas DataFrame
df = pd.read_excel("sorted_data2.xlsx")




df.head()




# Drop unnecessary columns
to_drop = ['CASE', 'REF', 'PI09', 'SC01', 'TIME001', 'TIME002',
           'MAILSENT', 'TIME_SUM', 'LASTDATA', 'FINISHED', 'Q_VIEWER', 'LASTPAGE', 'MAXPAGE', 'PS_EMAIL',
           'PS_PHONE', 'PS_UID', 'MISSING', 'TIME_RSI', 'DEG_TIME', 'MISSREL']
df = df.drop(to_drop, axis=1)



#Filter the DataFrame to include only rows with 'type' values 'A' or 'B'
#df['QUESTNNR'].replace({'A2': 'Science', 'B': 'Media'}, inplace=True)
#filtered_df = df[df['QUESTNNR'].isin(['A2', 'B'])]









# List of column names 'SQ1', 'SQ2', ..., 'SQ22'
sq_columns = df.columns[11:37]

print(sq_columns)






# Melt the dataframe to create the 'item' column
melted_df = pd.melt(df, id_vars=['QUESTNNR', 'Nationality', 'SERIAL', 'Gender', 'Edu_level', 'Age'], value_vars=sq_columns,
                    var_name='item', value_name='score')
print(melted_df)




# Fill the missing gender values with the last non-missing value for each serial number
melted_df['Gender'] = melted_df.groupby('SERIAL')['Gender'].transform('ffill')
melted_df['Edu_level'] = melted_df.groupby('SERIAL')['Edu_level'].transform('ffill')
melted_df['Age'] = melted_df.groupby('SERIAL')['Age'].transform('ffill')
print(melted_df)




# Filter the DataFrame to include only rows with 'type' values 'A' or 'B'
melted_df['QUESTNNR'].replace({'A2': 'Science', 'B': 'Media'}, inplace=True)




#it counts the number of unique Nationalities per item
#F = melted_df.groupby('item')['Nationality'].nunique()




melted_df = melted_df[melted_df['QUESTNNR'].isin(['Science', 'Media'])]
melted_df['Gender'].replace({1: 'Male', 2: 'Female', 3: 'Other'}, inplace=True)
melted_df




melted_df.to_excel('/Users/rahimforoughisaeidabadi/Documents/Thesis/Thesis- data analysis/data.xlsx', index=False)




#output_file_path = '/Users/rahimforoughisaeidabadi/Documents/Thesis/Thesis- data analysis/New-data.xlsx'  # Specify the desired output file path

#new_df.to_excel(output_file_path, index=False)  # Save the DataFrame to the new Excel file




# Iterate over unique SERIAL values and calculate differences
new_df = pd.DataFrame(columns=['SERIAL', 'Gender', 'Age', 'Nationality'] + [f'Difference_{i}' for i in range(1, 23)])

for serial in df['SERIAL'].unique():
    participant_df = df[df['SERIAL'] == serial]
    a2_answers = participant_df.loc[participant_df['QUESTNNR'] == 'A2', 'SQ01':'SQ22'].values
    b_answers = participant_df.loc[participant_df['QUESTNNR'] == 'B', 'SQ01':'SQ22'].values
    if len(a2_answers) > 0 and len(b_answers) > 0:  # Check if A2 and B answers exist
        differences = np.abs(a2_answers[0] - b_answers[0])
        participant_data = {
            'SERIAL': serial,
            'Gender': participant_df['Gender'].iloc[0],
            'Age': participant_df['Age'].iloc[0],
            'Nationality': participant_df['Nationality'].iloc[0],
            **{f'Difference_{i}': diff for i, diff in enumerate(differences, 1)}
        }
        new_df = pd.concat([new_df, pd.DataFrame(participant_data, index=[0])], ignore_index=True)



# Set the threshold value
threshold = 1

# Calculate the mean difference for each participant
mean_values = new_df.loc[:, 'Difference_1':'Difference_22'].mean(axis=1)

# Categorize the mean differences
new_df['Category'] = np.where(mean_values >= threshold, 'Strong', 'Weak')

# Plot the scatter plot with different colors for weak and strong categories
plt.scatter(new_df.index, mean_values, c=new_df['Category'].map({'Weak': 'blue', 'Strong': 'red'}))

# Plot the threshold line
plt.axhline(y=threshold, color='black', linestyle='--')

# Add labels and title
plt.xlabel('Participants')
plt.ylabel('Mean Difference')
plt.title('Mean Difference by Participants')

# Show the plot
plt.show()

# Create a DataFrame with mean values (using existing calculation)
mean_df = pd.DataFrame({'Columns': mean_values.index, 'Mean': mean_values.values})

# Plot the mean values as a scatter plot with a line connecting the points
plt.figure(figsize=(30, 10))  # Adjust the width and height as desired
plt.plot(mean_df['Columns'], mean_df['Mean'], marker='o', linestyle='-', color='blue')
plt.xlabel('Columns')
plt.ylabel('Mean')
plt.title('Mean of questions')
plt.xticks(rotation=45)
plt.show()





