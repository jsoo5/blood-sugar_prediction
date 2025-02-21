def get_info():
    input_data = [{
                    "name": "", # Acorns
                    "GI": 25,
                    "proteins": 6,
                    "carbohydrates": 41,
                    "fats": 24,
                    "monosaccharide": 0.5,
                    "category": "nuts_and_seeds",
                    "dietary fiber": 9,
                    "cooking_method": "raw"
                }]
    return input_data

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