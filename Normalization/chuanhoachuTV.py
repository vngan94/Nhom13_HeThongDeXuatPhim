import re
def remove_html(text):
    return re.sub(r'<.*?>','',text)

def remove_special_character(s):
    return ''.join(item for item in s if item.isalnum() or item == ' ')
def remove_consec_duplicates(s):
    s =  s.strip()
    s = s.lower()
    new_s = ""
    prev = ""
    for c in s:
        if len(new_s) == 0 or c.isnumeric()==True:
            new_s += c
            prev = c
        if c == prev:
            continue
        else:
                new_s += c
                prev = c
    return new_s

if __name__ == '__main__':
    print(remove_consec_duplicates("100000 aaa"))












