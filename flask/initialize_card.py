import csv

CARD_NAME = 0

with open('gamecard.csv', 'r') as file:
    reader = csv.reader(file, delimiter='\t')  # タブ区切りのCSVとして読み込む

    row = next(reader)
    i = 0
    for col in row:
        if col == "カード名3":
            CARD_NAME = i
        i = i + 1

    for row in reader:
        if row[CARD_NAME] == "メラゴースト":
            print(row)
