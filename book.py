##
# Read PDF, MOBI, EPUB and TXT by scraping the text found within each.
# Books are a list of strings.
#

class Book():
    def __init__(self,file_path):
        # init book file
        self._file_path = file_path
        # list of strings
        self._content = []
        pass

    def read_book(file_path):
        pass

    def parse_mobi(self):
        pass

    def parse_epub(self):
        pass

    def parse_pdf(self):
        pass

    def parse_txt(self):
        pass

    def get_content(self):
        return self._content