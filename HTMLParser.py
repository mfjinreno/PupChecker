import re


def parse_html(text):
    substring = re.findall(r'<\s*a[^>]*>(.*?)<\s*/\s*a>', str(text))

    name_list = []
    for item in substring:
        if re.search(r'<\s*img[^>]*(.*?)\s*>', item) and not re.search(r'@@', item):
            print("Link: " + item)

        elif not re.search(r'@@', item):
            name_list.append(item)

    return name_list


