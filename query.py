import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = "D:\Web Projects\Query\Employee Timecard Data.csv"  
df = pd.read_csv(file_path)

# Convert 'Time' column to datetime format for calculations
df['Time'] = pd.to_datetime(df['Time'], format='mixed', dayfirst=True)

# Sort the DataFrame by 'Employee Name' and 'Time' columns
df.sort_values(by=['Employee Name', 'Time'], inplace=True)

# Calculate time differences between consecutive rows
df['Time Difference'] = df.groupby('Employee Name')['Time'].diff()

# Convert the "Timecard Hours (as Time)" column to a timedelta format
df['Timecard Hours (as Time)'] = pd.to_timedelta(df['Timecard Hours (as Time)'] + ':00')

# Filter employees who have worked for 7 consecutive days
seven_consecutive_days = df[df['Time Difference'].dt.days == 1].groupby(['Employee Name', 'Position ID']).size()
seven_consecutive_days = seven_consecutive_days[seven_consecutive_days == 6].index

# Filter employees who have less than 10 hours between shifts but greater than 1 hour
shifts_less_than_10_hours = df[(df['Time Difference'].dt.total_seconds() < 36000) &
                                (df['Time Difference'].dt.total_seconds() > 3600)].groupby(['Employee Name', 'Position ID']).size()

# Filter employees who have worked for more than 14 hours in a single shift
shifts_more_than_14_hours = df[df['Timecard Hours (as Time)'] > pd.to_timedelta("14 hours")].groupby(['Employee Name', 'Position ID']).size()

# Print the results
print("Employees who have worked for 7 consecutive days:")
for employee, position in seven_consecutive_days:
    print(f"Employee Name: {employee}, Position ID: {position}")

print("\nEmployees who have less than 10 hours between shifts but greater than 1 hour:")
for (employee, position) in shifts_less_than_10_hours.index:
    print(f"Employee Name: {employee}, Position ID: {position}")

print("\nEmployees who have worked for more than 14 hours in a single shift:")
for (employee, position) in shifts_more_than_14_hours.index:
    print(f"Employee Name: {employee}, Position ID: {position}")
