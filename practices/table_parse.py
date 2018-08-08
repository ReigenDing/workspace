import lxml.html


def parse_table(table):
    table_dict = {}
    table = table[0] if table else None
    rows = table.xpath('.//tr')
    return table_dict


if __name__ == '__main__':
    with open('../tmp/table1.html') as fp:
        root = lxml.html.fromstring(fp.read())
        print(root.xpath('//title/text()')[0])
    t = root.xpath("//div[@class='table']/table")
    td = parse_table(t)

