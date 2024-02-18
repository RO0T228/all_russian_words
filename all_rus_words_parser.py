import bs4, requests, time

url = "https://vfrsute.ru/"
responce = requests.get(url)
bs = bs4.BeautifulSoup(responce.text, "lxml")
page_list, allword, cnt = [], [], 0
alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
time1 = time.time()
num_of_words = ''.join(filter(lambda x: x.isdigit(), bs.find("h1").text))

for lett in alphabet:
    url = f"https://vfrsute.ru/слова-на-{lett.lower()}/"
    responce = requests.get(url)
    bs = bs4.BeautifulSoup(responce.text, "lxml")

    pagination = bs.select(".pagination")[1]
    pagination = pagination.find_all('a', {'data-page': True})

    pages = [page_list.append(pg.text) for pg in pagination]
    max_page = page_list[-1]
    for page in range(1, int(max_page)+1):
        # print(f"\n{lett} {page}/{max_page}", end="\r")
        url = f"https://vfrsute.ru/слова-на-{lett.lower()}/{page}"
        responce = requests.get(url)
        bs = bs4.BeautifulSoup(responce.text, "lxml")
        words = bs.find("ul", class_="main-list").find_all("li")
        for i in words:
            allword.append(i.text)
            cnt += 1
            print(f"\r{cnt} / {num_of_words}", end="", flush=True)

with open("all_rus_words.txt", "w", encoding="utf8") as f:
    [f.writelines(f"{word}\n") for word in allword]
    print("\nУспешно!\nЗапись заняла: ", round((time.time() - time1) % 3600, 2), "сек")
    f.close()

file = open("all_rus_words.txt", "r", encoding="utf8")
print("Слов:", len(file.readlines()))
file.close()