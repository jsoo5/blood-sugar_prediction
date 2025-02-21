import requests
import numpy as np
import json

def get_endpoint_info(file_name):
    with open(file_name) as f:
        config = json.load(f)
    return config


### Custom Vison API ###
def predict_img(img, times):
    # endpoint
    config = get_endpoint_info('model/config.json')
    endpoint, api_key = config['mld_endpoint_v2'], config['cv_api_key']

    endpoint = config['cv_endpoint']
    headers = {
        'Content-Type' : 'application/octet-stream',
        'Prediction-Key' : api_key
    }
    
    if isinstance(img, str):
        # 파일 경로인 경우
        with open(img, 'rb') as image_file:
            binary_data = image_file.read()
    
    # Numpy 배열인 경우 PIL을 통해 처리
    elif isinstance(img, np.ndarray):
        from PIL import Image
        import io, base64
        
        pil_img = Image.fromarray(img)
        buf = io.BytesIO()
        pil_img.save(buf, format='JPEG')
        binary_data = buf.getvalue()

    response = requests.post(endpoint, headers=headers, data=binary_data)

    # print(response.status_code)
    response_json = response.json()
    # import json
    # print(json.dumps(response_json, indent=4))
    best_pred = response_json['predictions'][times]
    if times < 5:
        return best_pred['tagName']
    else:
        return None



### Machine Learning Designer API ###
def request_gi_prediction(data_list):

    # endpoint
    config = get_endpoint_info('model/config.json')
    endpoint, api_key = config['mld_endpoint_v2'], config['mld_api_key_v2']
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # body
    body = {
        "Inputs": {
            "input1": data_list
        }   
    }

    response = requests.post(endpoint, headers=headers, json=body)

    if response.status_code == 200:
        response_json = response.json()
        # return response_json
        response_data = response_json['Results']['WebServiceOutput0']
        
        return response_data[0]['Scored Labels']

        # for score_gi in response_data:
        #     score = score_gi['Scored Labels']
        #     gi = score_gi['GI']
        #     print(score, gi)
    else:
        return ''
    
