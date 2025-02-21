import requests
import numpy as np
import json

### Custom Vison API ###
def predict_img(img, times):
    # endpoint - 현재 iteration13 사용
    endpoint = 'https://korms6tfirstproject4team-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/4b2acd23-4aee-4403-a306-255d6fbfac5a/classify/iterations/Iteration20/image'
    headers = {
        'Content-Type' : 'application/octet-stream',
        'Prediction-Key' : '22nCuj5dSly9FfIxCpKcwAxYYtcnXLyulD7wyIc0fgdn88cSKNUfJQQJ99BBACHYHv6XJ3w3AAAIACOGVIsM'
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
    if times < 3:
        return best_pred['tagName']
    else:
        return None


### Machine Learning Designer API ###
def request_gi_prediction(data_list):
    
    def get_mld_endpoint_info(file_name):
        with open(file_name) as f:
            config = json.load(f)

        return config['mld_endpoint'], config['mld_api_key']

    # endpoint
    endpoint, api_key = get_mld_endpoint_info('./config.json')
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
    
