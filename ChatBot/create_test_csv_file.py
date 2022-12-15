import pandas as pd
from itertools import permutations
import csv

price_permutation = pd.read_csv("create_price_chat_data.csv")
price_talk = []
for idx in range(len(price_permutation.question)):
    lis = list(price_permutation.question[idx].split())
    permute = permutations(lis)
    for i in permute:
        permuteList = list(i)
        price_talk.append([" ".join(permuteList), "PRICE"])

vol_permutation = pd.read_csv("create_vol_surface_chat_data.csv")
for idx in range(len(vol_permutation.question)):
    lis = list(vol_permutation.question[idx].split())
    permute = permutations(lis)
    for i in permute:
        permuteList = list(i)
        price_talk.append([" ".join(permuteList), "VOL"])

header = ['question', 'answer']

with open('test_data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(price_talk)

print("Successfully created test_data.csv")
