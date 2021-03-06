import os
import requests
from bs4 import BeautifulSoup


def scrape_greatestadventurers():
    sitemap_link = "https://greatestadventurers.com/site-map/"

    sitemap_page = requests.get(sitemap_link)
    soup = BeautifulSoup(sitemap_page.content, "html.parser")

    categories = soup.find_all("strong", class_="wsp-category-title")

    # create folder where everything goes
    output_folder = "greatestadventurers"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # go through every category and create folder for it
    for category in categories:
        category_link = category.find("a")["href"]

        category_folder = "greatestadventurers/" + category.text.split(" ")[1]
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        category_page = requests.get(category_link)
        category_soup = BeautifulSoup(category_page.content, "html.parser")
        books = category_soup.find_all("h2", class_="entry-title")

        # when we are on the category page, open the site for the book and
        # download the pdf
        for book in books:
            book_link = book.find("a")["href"]
            book_page = requests.get(book_link)
            book_soup = BeautifulSoup(book_page.content, "html.parser")

            book_name = book_link.split("/")[3]

            # the link to download the pdf has no css id/class
            # so this is an easy way to get the link
            for a_tag in book_soup.find_all('a'):
                if ("pdf" in a_tag.get("href")):
                    book_pdf = a_tag.get("href")

            book_download = requests.get(book_pdf)

            with open(f"{category_folder}/{book_name}.pdf", 'wb') as f:
                f.write(book_download.content)

            print(f"Downloaded: {book_name}")

if __name__ == "__main__":
    scrape_greatestadventurers()
