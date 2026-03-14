import dateparser

def parse_date(text):

    d = dateparser.parse(text)

    if d:
        return d.strftime("%Y-%m-%d")

    return None