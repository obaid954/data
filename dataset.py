import pandas as pd

# Load the dataset from the CSV file
df = pd.read_csv('online_sales_dataset.csv')

# Display the first few rows of the dataset to understand its structure
print(df.head())

# Print the column names and their respective data types
print('Dataset Columns and Data Types:')
print(df.dtypes)

# Check for missing values in each column
print('Missing Values:')
print(df.isnull().sum())

# Summary statistics of the dataset
# This will provide general statistics like mean, std, min, max, etc., for numerical columns and count for categorical columns
print('Summary Statistics:')
print(df.describe(include='all'))

# Data Preprocessing

# Drop rows where 'CustomerID' is missing since CustomerID is critical for analysis
df = df.dropna(subset=['CustomerID'])

# Fill missing values in 'ShippingCost' with the median value of the 'ShippingCost' column
# This helps to impute missing shipping costs without introducing bias
median_shipping_cost = df['ShippingCost'].median()
df['ShippingCost'] = df['ShippingCost'].fillna(median_shipping_cost)

# Drop rows where 'Quantity' or 'UnitPrice' is less than or equal to zero, as they represent invalid transactions
# These are either errors or non-meaningful data points
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Convert the 'InvoiceDate' column to datetime format for easier manipulation in time-based analysis
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Print the updated dataset information
print('Data Preprocessing Completed:')
# Print the shape of the dataset after preprocessing to see how many rows and columns remain
print('Shape after preprocessing:', df.shape)

# Check for missing values again after preprocessing to ensure no critical columns still have missing data
print('Missing values after preprocessing:')
print(df.isnull().sum())
