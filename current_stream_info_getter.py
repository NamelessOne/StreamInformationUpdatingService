import urllib.request
import html.parser
import requests


class ImageParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.img = ""

    def handle_starttag(self, tag, attributes):
        if tag == 'img':
            attributes = dict(attributes)
            if 'alt' in attributes and attributes['alt'] == 'Страница автора':
                self.img = attributes['src']


class AboutParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.about = ""
        self.trcount = 0
        self.b = False

    def handle_starttag(self, tag, attributes):
        if tag == 'tr':
            self.trcount += 1
        if tag == 'b' and self.trcount == 3:
            self.b = True

    def handle_endtag(self, tag):
        if tag == 'b':
            self.b = False

    def handle_data(self, data):
        if self.b:
            self.about = data


def send(img, about):
    requests.post('http://192.168.0.104:9000/CurrentStreamInformation', json={'imageURL': img, 'about': about})


def get_stream_info():
    # Image URL
    image_response = urllib.request.urlopen('http://fantasyradio.ru/player.php')
    image_html = str(image_response.read().decode('windows-1251'))
    image_parser = ImageParser()
    image_parser.feed(image_html)
    # About
    about_response = urllib.request.urlopen('http://fantasyradio.ru/player_podrobnee.html')
    about_html = str(about_response.read().decode('windows-1251'))
    about_parser = AboutParser()
    about_parser.feed(about_html)

    send(image_parser.img, about_parser.about)


get_stream_info()
