import requests
import regex
from tqdm import tqdm


def main():
    f = open('./names.txt', 'w+')
    for i in tqdm(range(100000)):
        response = requests.get(f'https://www.premierleague.com/players/{i}')
        if response.status_code != 200:
            continue
        elif response.text.find('<div class="name t-colour">') == -1:
            continue
        else:
            name = regex.search(
                r'(?<=\<div class\="name t\-colour"\>)(.*?)\<\/div>', response.text).group(1)
            print(f"{i}: {name}", file=f)

    f.close()


if __name__ == "__main__":
    main()
