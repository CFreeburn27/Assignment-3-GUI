# https://developers.google.com/books/docs/v1/using#PerformingSearch
import requests

# get book info from ocr model predictions
def get_book_details_from_google(title, author):
    bookResponse = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + title + author)           
    jsondict = bookResponse.json()
    firstbookresultdetails = jsondict['items'][0]['volumeInfo']
    print(firstbookresultdetails)
    bookInfomation = {}
    bookInfomation['title'] = (firstbookresultdetails['title'])
    bookInfomation['authors'] = (firstbookresultdetails['authors']) [0]
    bookInfomation['publisher'] = (firstbookresultdetails['publisher'])
    bookInfomation['categories'] = (firstbookresultdetails['categories'][0])
    return bookInfomation
    