import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the file path for user statistics
user_stats_file = 'user_statistics.json'

# Function to calculate total access count for each website
def get_total_access_count(user_stats_file):
    website_counts = {}
    for data in user_stats_file.values():
        website_access_count = data.get("website_access_count", {})
        for website, count in website_access_count.items():
            website_counts[website] = website_counts.get(website, 0) + count
    return website_counts

# Function to load data from a JSON file
def loadData(user_stats_file):
    with open(user_stats_file, 'r') as json_file:
        loaded_data = json.load(json_file)
        # Print the loaded data
        print(f'data loaded from file - {loaded_data}')
        return loaded_data

# Function to get website access counts within a specified date range
def get_website_counts_in_range(start_date, end_date, data):
    website_counts = {}

    for client_data in data.values():
        accessed_websites = client_data.get("accessed_websites", [])
        for website_info in accessed_websites:
            access_date = website_info.get("access_date")
            if start_date <= access_date <= end_date:
                website = website_info.get("website")
                website_counts[website] = website_counts.get(website, 0) + 1
    return website_counts

# Function to get user-specific website access counts within a specified date range
def get_user_website_counts_in_range(start_date, end_date, data):
    user_website_counts = {}

    for client_address, client_data in data.items():
        accessed_websites = client_data.get("accessed_websites", [])
        total_access_count = 0
        website_counts = {}

        for website_info in accessed_websites:
            access_date = website_info.get("access_date")
            if start_date <= access_date <= end_date:
                website = website_info.get("website")
                total_access_count += 1
                website_counts[website] = website_counts.get(website, 0) + 1

        if total_access_count > 0:
            user_website_counts[client_address] = {
                "total_access_count": total_access_count,
                "website_counts": website_counts
            }

    return user_website_counts

# Function to plot bar chart showing total access counts for each user
def plot_user_website_counts(user_website_counts):
    user_ips = list(user_website_counts.keys())
    total_access_counts = [data["total_access_count"] for data in user_website_counts.values()]

    plt.figure(figsize=(10, 6))
    plt.bar(user_ips, total_access_counts, color='skyblue')
    plt.xlabel('User IP')
    plt.ylabel('Total Access Count')
    plt.title('Total Websites visited by each user')
    plt.xticks(rotation=0)
    plt.show()

# Function to plot pie chart showing distribution of total website access counts
def plot_total_site_counts(website_counts):
    labels = list(website_counts.keys())
    sizes = list(website_counts.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    # Display the pie chart
    plt.show()

# Function to get website access counts within a specified date range
def get_website_counts_in_range(start_date, end_date, data):
    website_counts = {}

    for client_data in data.values():
        accessed_websites = client_data.get("accessed_websites", [])
        for website_info in accessed_websites:
            access_date = website_info.get("access_date")
            if start_date <= access_date <= end_date:
                website = website_info.get("website")
                website_counts[website] = website_counts.get(website, 0) + 1
    return website_counts

# Function to get the start and end dates of the current week
def get_week_range(date_str):
    date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
    start_of_week = date_obj - timedelta(days=date_obj.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

# Function to get the start and end dates of the current month
def get_month_range(date_str):
    date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
    start_of_month = date_obj.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return start_of_month, end_of_month

# Function to plot line graphs showing total site access counts
def plot_line_graphs():
    data = loadData(user_stats_file)
    user_website_count_in_range = get_user_website_counts_in_range('2023-11-01', '2023-11-02', data)

    # Get daily, weekly, and monthly total counts
    today_date = datetime.today().date()
    yesterday_date = today_date - timedelta(days=1)
    yesterday_date = str(yesterday_date)
    daily_counts = get_website_counts_in_range(str(today_date), str(yesterday_date), data)
    start_of_week, end_of_week = get_week_range(today_date)
    weekly_counts = get_website_counts_in_range(start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d"),
                                                data)
    start_of_month, end_of_month = get_month_range(today_date)
    monthly_counts = get_website_counts_in_range(start_of_month.strftime("%Y-%m-%d"), end_of_month.strftime("%Y-%m-%d"),
                                                 data)

    # Prepare data for plotting
    dates = ['Daily', 'Weekly', 'Monthly']
    total_counts = [len(daily_counts), len(weekly_counts), len(monthly_counts)]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, total_counts, marker='o')
    plt.xlabel('Time Period')
    plt.ylabel('Total Count')
    plt.title('Total Sites Visited (Time period on x-axis is relative to today')
    plt.grid(True)
    plt.show()

# Main function to execute various functions
def plot():
    data = loadData(user_stats_file)
    site_access_count_map = get_total_access_count(data)
    site_hits_in_dynamic_range = get_website_counts_in_range('2023-11-01', '2023-11-02', data)
    user_website_count_in_range = get_user_website_counts_in_range('2023-11-01', '2023-11-02', data)
    print(f'site_access_count_map - {site_access_count_map}')
    print(f'site_hits_in_dynamic_range - {site_hits_in_dynamic_range}')
    print(f'user website count in range - {user_website_count_in_range}')

    plot_user_website_counts(user_website_count_in_range)
    plot_total_site_counts(site_access_count_map)
    plot_line_graphs()

if __name__ == '__main__':
    plot()
