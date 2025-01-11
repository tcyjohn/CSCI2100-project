import csv

score = 0


try:
    with open("output/table1.csv", mode="r") as file:
        reader = csv.DictReader(file)
        tab1 = [row for row in reader]
    if len(tab1) == 30:
        score += 5
    else:
        print('incomplete table1')
except:
    print('failed to parse table1')
    tab1 = []

try:
    with open("output/table2.csv", mode="r") as file:
        reader = csv.DictReader(file)
        tab2 = [row for row in reader]
    if len(tab2) == 30:
        score += 5
    else:
        print('incomplete table2')
except:
    print('failed to parse table2')
    tab2 = []

if len(tab1) == 0 or len(tab2) == 0:
    print("tab1 or tab2 is empty")
    print("score: {}".format(score))
    exit(0)

# find if tab1['pointer'] point to id of same stick in tab2

tab2_dict = {row["id"]: row["ticker"] for row in tab2}
for row in tab1:
    if tab2_dict[row["pointer"]] != row["ticker"]:
        print("tab1['pointer'] does not point to id of same stick in tab2")
        print("score: {}".format(score))
        break
score += 15


# check if table1_sorted_a.csv and table1_sorted_b.csv are correct
try:
    with open("output/table1_sorted_a.csv", mode="r") as file:
        reader = csv.DictReader(file)
        tab1_sorted_a = [row for row in reader]
        tab1_sorted_a_ticker = [row["ticker"] for row in tab1_sorted_a]
        if tab1_sorted_a_ticker != sorted(tab1_sorted_a_ticker):
            print("table1_sorted_a.csv is not correct")
            print("score: {}".format(score))
        score += 10
except:
    print('failed to parse table1_sorted_a')

try:
    with open("output/table1_sorted_b.csv", mode="r") as file:
        reader = csv.DictReader(file)
        tab1_sorted_b = [row for row in reader]
        tab1_sorted_b_market_cap = [int(row["market_cap"]) for row in tab1_sorted_b]
        if tab1_sorted_b_market_cap != sorted(tab1_sorted_b_market_cap):
            print("table1_sorted_b.csv is not correct")
            print("score: {}".format(score))
        score += 10
except:
    print('failed to parse table1_sorted_b')

print("total score: {}".format(score))