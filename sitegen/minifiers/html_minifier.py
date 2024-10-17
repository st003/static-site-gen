from html.parser import HTMLParser

# see: https://docs.python.org/3/library/html.parser.html

class HTMLMinifier(HTMLParser):

    ILLEGAL = set(['\n', '\r'])

    def __init__(self):
        self._tokens = []
        super().__init__()

    def get_minified(self):
        return ''.join(self._tokens)

    def handle_starttag(self, tag, attrs):

        self._tokens.append('<')
        self._tokens.append(tag)

        if len(attrs) > 0:
            self._tokens.append(' ')

        for key, value in attrs:
            self._tokens.append(f'{key}="{value}"')

        self._tokens.append('>')

    def handle_endtag(self, tag):
        self._tokens.append(f'</{tag}>')

    def handle_data(self, data):
        for char in data:
            if char in self.ILLEGAL:
                continue
            self._tokens.append(char)


sample_html: str = '<html  lang="en">\n    <body>\n        <h1>HTML Minifier Test!</h1>\n    </body>\n</html>'

minifier = HTMLMinifier()
minifier.feed(sample_html)

print(sample_html)
print()
print(minifier.get_minified())
