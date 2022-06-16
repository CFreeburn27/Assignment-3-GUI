# https://developers.google.com/books/docs/v1/using#PerformingSearch
import requests

# get book info from ocr model predictions
def get_book_details_from_google(title, author):
    bookResponse = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + title + author)           
    jsondict = bookResponse.json()
    firstbookresultdetails = jsondict['items'][0]['volumeInfo']
    print(firstbookresultdetails)
    print(firstbookresultdetails['infoLink'])
    bookInfomation = {}
    bookInfomation['Title'] = (firstbookresultdetails['title'])
    bookInfomation['Authors'] = (firstbookresultdetails['authors']) [0]
    bookInfomation['Publisher'] = (firstbookresultdetails['publisher'])
    bookInfomation['Categories'] = (firstbookresultdetails['categories'][0])
    bookInfomation['InfoLink'] = (firstbookresultdetails['infoLink'])
    return bookInfomation
    
    
if __name__ == '__main__':
    get_book_details_from_google('why nations fail', 'Daron Acemoglu')