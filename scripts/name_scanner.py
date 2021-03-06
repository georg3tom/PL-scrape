"""
    This script scans a range from 0 to ID_MAX. For each ID, it sees if there
    is a player with that ID. If there is, store their name and ID to a text 
    file, so during fetching, we only hit those URLs that have valid player 
    information on them.
"""

import requests
import regex
from tqdm import tqdm

ID_MAX = 100000


def main():
    f = open('../outputs/player_names_ids.txt', 'w+')
    for i in tqdm(range(ID_MAX)):
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
    print("Generated player_names_ids.txt")


if __name__ == "__main__":
    main()
