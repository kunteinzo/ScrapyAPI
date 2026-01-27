from re import search

with open('browsers.jsonl', 'r') as f, open('ua.json', 'w') as ua:
    data = []
    while line := f.readline():
        if 'os": "Mac' in line:
            print(search(r'',line).group())
        if 'os": "Windows' in line:
            print(line)