import json
import os
from pymongo import MongoClient

def refine_nutrition_info(info, cooking_method):
    # cooking_method 추가
    info[0]['cooking_method'] = cooking_method
    # 오류 발생시키는 데이터 삭제 및 추가
    info[0]['GI'] = 0
    del(info[0]['_id'])
    del(info[0]['NO'])
    return info

def get_nutrition_info(food_name, cooking_method):

    def get_db_endpoint_info(file_name):
        with open(file_name) as f:
            config = json.load(f)

        return config['mongodb_user'], config['mongodb_key'], config['mongodb_endpoint']
    user, key, endpoint = get_db_endpoint_info('model/config.json')

    import warnings
    warnings.filterwarnings("ignore", message="You appear to be connected to a CosmosDB cluster")

    def connect_azure_cosmosdb(user, key, endpoint):
        client = MongoClient(f'mongodb+srv://{user}:{key}@{endpoint}')
        db = client['team4']
        coll = db['foods']
        return coll

    coll = connect_azure_cosmosdb(user, key, endpoint)
    response = coll.find({'name':food_name})
    result = list(response)

    adding_method = trans_cooking_method(cooking_method)
    info = refine_nutrition_info(result, adding_method)
    print(info)
    return info

'''
[{'_id': ObjectId('67b8036b38cb606118e8df34'),
  'NO': 2,
  'name': '훈제오리',
  'calory': 318.86, 
  'proteins': '17.22', 
  'fats': '25.63', 
  'carbohydrates': '4.83', 
  'monosaccharide': '0.11', 
  'GI_Class': 1, 
  'category': 'meat', 
  'dietary_fiber': 0.0}]
'''


# def get_info():
#     input_data = [{
#                     "name": "", # Acorns
#                     "GI": 25,
#                     "proteins": 6,
#                     "carbohydrates": 41,
#                     "fats": 24,
#                     "monosaccharide": 0.5,
#                     "category": "nuts_and_seeds",
#                     "dietary fiber": 9,
#                     "cooking_method": "raw"
#                 }]
#     return input_data


def trans_cooking_method(method):
    if method == '날것':
        return 'raw'
    elif method == '가공':
        return 'processed'
    elif method == '삶음':
        return 'boiled'
    elif method == '조림':
        return 'braised'
    elif method == '익힘':
        return 'cooked'
    elif method == '통조림':
        return 'canned'
    elif method == '튀김/볶음':
        return 'fried'
    elif method == '석쇠·그릴에 구움':
        return 'grilled'
    elif method == '찜':
        return 'steamed'
    elif method == '오븐에 구움':
        return 'baked'
    elif method == '탄산음료':
        return 'carbonated'
    elif method == '발효':
        return 'fermented'
    elif method == '튀김(예:팝콘)':
        return 'popped'
    elif method == '냉동':
        return 'frozen'