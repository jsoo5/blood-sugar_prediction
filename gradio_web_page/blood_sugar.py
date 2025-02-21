def classify_gi_level(gi):
    gi = round(float(gi))
    if gi <= 55:
        return '저혈당지수', '10분 간 가볍게'
    elif 55 < gi < 70:
        return '중혈당지수', '20분 간 빠르게'
    else:
        return '고혈당지수', '30분 간 빠르게'

def calc_blood_value(gi, info):
    gi = round(float(gi))
    
    carbo = info[0]['carbohydrates']
    gl = (gi * carbo) / 100
    
    normal = 2.5
    abnormal = 5

    min_value = gl * normal
    max_value = gl * abnormal
    
    return f'{min_value} ~ {max_value}'

# 혈당부하지수 = (혈당지수 × 1회 섭취분량에 함유된 탄수화물 양) ÷ 100
# 분류 10 이하: 저혈당부하지수, 11~19: 중혈당부하지수, 20 이상: 고혈당부하지수