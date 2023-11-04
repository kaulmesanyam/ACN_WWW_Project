import json

user_stats_file = 'user_statistics.json'
def get_total_access_count(user_stats_file):
    website_counts = {}
    for data in   user_stats_file.values():
        website_access_count = data.get("website_access_count", {})
        for website, count in website_access_count.items():
            website_counts[website] = website_counts.get(website, 0) + count
    return website_counts

def loadData(user_stats_file):
    with open(user_stats_file, 'r') as json_file:
        loaded_data = json.load(json_file)
        # Print the loaded data
        print(f'data loaded from file - {loaded_data}')
        return loaded_data
def plot():
    data = loadData(user_stats_file)
    site_access_count_map = get_total_access_count(data)

if __name__ == '__main__':
    plot()