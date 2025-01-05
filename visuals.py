import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('online_sales_dataset.csv')

# Convert 'InvoiceDate' to datetime format for easier manipulation
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 3. Geographic Distribution - Sales by Country
plt.figure(figsize=(10, 6))

# Group by 'Country' and sum 'Quantity' for each country, then sort the results
country_sales = df.groupby('Country')['Quantity'].sum().sort_values(ascending=True)

# Generate a color palette for the bars, with darker shades for higher quantities
colors = sns.color_palette('YlGnBu', len(country_sales))

# Normalize the values for color gradient
norm = plt.Normalize(vmin=country_sales.min(), vmax=country_sales.max())

# Create a bar plot with custom color mapping
sns.barplot(x=country_sales.values, y=country_sales.index, palette=colors)
plt.title('Sales by Country')
plt.xlabel('Total Quantity Sold')
plt.tight_layout()

# Save and display the plot
plt.savefig('geographic_distribution.png')
plt.show()

# Calculate revenue (taking discount into account)
df['Revenue'] = df['Quantity'] * df['UnitPrice'] * (1 - df['Discount'])

# Create a new 'Year' column based on the 'InvoiceDate' for easier yearly analysis
df['Year'] = df['InvoiceDate'].dt.year

# Aggregate yearly data (Revenue, unique InvoiceNo, and Quantity sold)
yearly_sales = df.groupby('Year').agg({
    'Revenue': 'sum',  # Sum revenue per year
    'InvoiceNo': 'nunique',  # Count unique invoices (orders)
    'Quantity': 'sum'  # Sum quantity sold
}).round(2)

# Create subplots for multiple line charts (Revenue, Orders, Quantity)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 15))

# Plot Yearly Revenue Trend
ax1.plot(yearly_sales.index, yearly_sales['Revenue'], marker='o', linewidth=2, color='blue')
ax1.set_title('Yearly Revenue Trend')
ax1.set_ylabel('Total Revenue ($)')
ax1.grid(True)
# Annotate each point with its value
for i, v in enumerate(yearly_sales['Revenue']):
    ax1.text(yearly_sales.index[i], v, f'${v:,.0f}', ha='center', va='bottom')

# Plot Yearly Number of Orders
ax2.plot(yearly_sales.index, yearly_sales['InvoiceNo'], marker='s', linewidth=2, color='green')
ax2.set_title('Yearly Number of Orders')
ax2.set_ylabel('Number of Orders')
ax2.grid(True)
# Annotate each point with its value
for i, v in enumerate(yearly_sales['InvoiceNo']):
    ax2.text(yearly_sales.index[i], v, f'{v:,.0f}', ha='center', va='bottom')

# Plot Yearly Quantity Sold
ax3.plot(yearly_sales.index, yearly_sales['Quantity'], marker='^', linewidth=2, color='red')
ax3.set_title('Yearly Quantity Sold')
ax3.set_ylabel('Total Quantity')
ax3.grid(True)
# Annotate each point with its value
for i, v in enumerate(yearly_sales['Quantity']):
    ax3.text(yearly_sales.index[i], v, f'{v:,.0f}', ha='center', va='bottom')

# Adjust layout for better spacing and display/save the plot
plt.tight_layout()
plt.savefig('yearly_sales_analysis.png')
plt.show()

# 1. Sales patterns by hour and day of week
# Extract hour and day of the week from 'InvoiceDate' for heatmap analysis
df['Hour'] = df['InvoiceDate'].dt.hour
df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek

# Create a pivot table to calculate revenue by hour and day of the week
hourly_daily_sales = df.pivot_table(
    values='Revenue',
    index='Hour',  # Rows represent hour of the day
    columns='DayOfWeek',  # Columns represent days of the week
    aggfunc='sum'
).fillna(0)  # Fill any NaN values with 0 for missing data

# Rename columns to actual day names for better readability
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hourly_daily_sales.columns = day_names

# Create a heatmap to visualize sales by hour and day of the week
plt.figure(figsize=(12, 8))
sns.heatmap(hourly_daily_sales, cmap='YlOrRd', annot=True, fmt='.0f', 
            cbar_kws={'label': 'Revenue'})  # Add a color bar for better context
plt.title('Sales Heatmap: Hour of Day vs Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Hour of Day')
plt.tight_layout()

# Save and display the heatmap
plt.savefig('sales_time_heatmap.png')
plt.show()

# 2. Category and Sales Channel Performance
# Pivot table to analyze revenue by Category and Sales Channel
category_channel_sales = df.pivot_table(
    values='Revenue',
    index='Category',  # Rows represent product categories
    columns='SalesChannel',  # Columns represent sales channels
    aggfunc='sum'
).fillna(0)  # Fill NaN with 0

# Create the group bar chart
category_channel_sales.plot(kind='bar', figsize=(12, 8), width=0.8)

# Adding title and labels
plt.title('Revenue by Category and Sales Channel')
plt.xlabel('Category')
plt.ylabel('Revenue')
plt.xticks(rotation=45, ha='right')

# Display the group bar chart
plt.tight_layout()
plt.savefig('category_channel_group_bar_chart.png')
plt.show()

# Print Key Insights from Heatmap Analysis
print("\nKey Insights from Heatmap Analysis:")
print("\n1. Best Performing Time Slots:")
# Identify the best-performing hour and day
best_hour = hourly_daily_sales.sum(axis=1).idxmax()
best_day = hourly_daily_sales.sum(axis=0).idxmax()
print(f"Peak Hour: {best_hour}:00")
print(f"Best Performing Day: {best_day}")

print("\n2. Category Performance:")
# Identify the top-performing category
best_category = category_channel_sales.sum(axis=1).idxmax()
print(f"Top Performing Category: {best_category}")
print(f"Revenue: ${category_channel_sales.sum(axis=1).max():,.2f}")

print("\n3. Return Rate Analysis:")
# Pivot table for return rates
return_rate_matrix = df.pivot_table(
    values='ReturnStatus',
    index='Category',  # Rows represent categories
    columns='SalesChannel',  # Columns represent sales channels
    aggfunc=lambda x: (x == 'Returned').mean() * 100  # Calculate return rate as percentage
).fillna(0)  # Fill NaN with 0

# Print categories with lowest return rates
print("\nCategories with Lowest Return Rates:")
return_rate_lowest = return_rate_matrix.mean(axis=1).sort_values().head(3)
print(return_rate_lowest)

# Print yearly sales statistics in table format
print("\nYearly Sales Statistics:")
print(yearly_sales)


