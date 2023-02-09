# -*- coding: utf-8 -*-
# @Time    : 2022/12/17 18:49
# @Author  : Hush
# @Email   : crush@tju.edu.cn

from requests_html import HTMLSession
import csv


def download_page(url):
    session = HTMLSession()
    return session.get(url=url).html


def get_content(html, books_info,rank):
    books = html.xpath('//*[@id="content"]/div/div[1]/div/table')
    for book in books:
        book_name = book.xpath('//*[@class="pl2"]/a')[0].attrs['title']

        quote = book.xpath('//*[@class="quote"]/span')
        if len(quote) > 0:
            quote = quote[0].text
        else:
            quote = ''
        book_url = book.xpath('//*[@class="pl2"]/a')[0].attrs['href']
        book_detail = download_page(book_url)
        if book_detail.xpath('//*[@id="info"]//a[1]'):
            book_writer = book_detail.xpath('//*[@id="info"]//a[1]')[0].text
        else:
            book_writer = ''
        book_info = (rank, book_name, book_writer, quote)
        books_info.append(book_info)
        rank = rank + 1
        print(book_info)
        writer.writerow(book_info)
    next_page = html.xpath('//*[@class="paginator"]/span[3]/link')
    if next_page:
        return next_page[0].attrs['href'],rank
    return None,1



if __name__ == "__main__":
    DOWNLOAD_URL = "https://book.douban.com/top250"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9'
    }
    url = DOWNLOAD_URL
    books_info = []
    writer = csv.writer(open('where-is-book-top250.csv', 'w',
                             newline='', encoding='utf-8'))
    fields = ('rank', 'name', 'writer', 'quote')
    writer.writerow(fields)
    rank = 1
    while url:
        html = download_page(url)
        url,rank = get_content(html, books_info,rank)