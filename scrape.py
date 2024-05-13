import requests
from bs4 import BeautifulSoup
import pprint

# Get the HTML content of the first page of Hacker News
res = requests.get('https://news.ycombinator.com/news')
# Get the HTML content of the second page of Hacker News
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

# Selecting all the story links from both pages
links = soup.select('.titleline > a')
links2 = soup2.select('.titleline > a')

# Selecting the subtext (which contains points and comments) for each story from both pages
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

# Combining links and subtext from both pages
mega_links = links + links2
mega_subtext = subtext + subtext2

# Function to sort the stories by the number of votes they received
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Function to create a custom Hacker News list with only stories having more than 99 points
def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        # Selecting the score (points) of each story
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    # Return sorted list of stories by votes
    return sort_stories_by_votes(hn)

# Print the list of stories with more than 99 points, sorted by the number of votes
pprint.pprint(create_custom_hn(mega_links, mega_subtext))
