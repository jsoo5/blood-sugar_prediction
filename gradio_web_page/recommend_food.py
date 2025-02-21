import pandas as pd
import random

def pick_low_gi_food(pick_count): 

    low_gi_food_list = pd.read_csv('low_gi_foods_re.csv')
    low_gi_food_list.head()

    categorized = low_gi_food_list.groupby('카테고리')['음식명'].apply(list)
    select_idx = random.sample(range(categorized.count()), pick_count)
    foods = []

    for idx in select_idx:
        foods.append(random.choice(categorized[idx]))

    return foods