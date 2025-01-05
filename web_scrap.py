import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape course data from a given page URL
def scrape_courses_from_page(page_number):
    url = f'https://courses.analyticsvidhya.com/collections?page={page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all course items
    course_items = soup.find_all('li', class_='products__list-item')

    courses = []
    for item in course_items:
        course = {}

        # Get course title
        title_tag = item.find('h3')
        course['title'] = title_tag.text.strip() if title_tag else None

        # Get lesson count
        lesson_tag = item.find('span', class_='course-card__lesson-count')
        course['lessons'] = lesson_tag.text.strip() if lesson_tag else None

        # Get course rating
        rating_tag = item.find('span', class_='stars__rating')
        course['rating'] = rating_tag.text.strip() if rating_tag else None

        # Get course link
        link_tag = item.find('a', class_='course-card')
        course['link'] = link_tag.get('href') if link_tag else None

        courses.append(course)

    return courses

# Collect data from pages 1 to 9
all_courses = []
for page_number in range(1, 10):
    courses = scrape_courses_from_page(page_number)
    all_courses.extend(courses)

# Write the data to a CSV file
with open('analytics_vidhya_courses.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'lessons', 'rating', 'link'])
    writer.writeheader()
    writer.writerows(all_courses)

print("Data scraped and saved to 'analytics_vidhya_courses.csv'")
