import gradio as gr
import time, os
from model import connect_api as model
from function.recommend_food import pick_low_gi_food
from function.nutrition_info import get_nutrition_info
from function import blood_sugar

# 현재 파일을 실행한 경로로 이동
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
os.chdir(current_dir)

# CSS 파일 불러오기
with open('data/css_custom.css', 'r') as f:
    css = f.read()


### 버튼 동작 함수 ###
def clear_inputs():
    return gr.update(value=None)


def enable_button(input):
    if input is None:
        return gr.update(interactive=False)
    else:
        return gr.update(interactive=True)


### 웹 UI ###
with gr.Blocks(css=css) as demo:
    page1 = gr.Row(visible=True, elem_classes="nanum-gothic-regular")
    page2 = gr.Column(visible=False, elem_classes="nanum-gothic-regular")

    ### 시작 화면 ###
    with page1:
        gr.Markdown('　　　　　')
        with gr.Column():
            gr.Markdown('## <center><br/><br/>피로는 당 때문이야</center>', elem_classes="orbit-regular")  
            gr.Image('data/logo.png', scale=0.3, show_download_button=False, interactive=False, show_label=False, container=False, show_fullscreen_button=False)
            gr.Markdown('# <center>너의 혈당은<br/><br/></center>', elem_classes="orbit-regular")  
            start_button = gr.Button('시작하기', size='lg', elem_id='button')
        gr.Markdown('　　　　　')
        start_button.click(fn=lambda : (gr.update(visible=False), gr.update(visible=True)), 
                            outputs=[page1, page2])

    ### 입출력 화면 ###
    with page2:
        gr.Markdown('# 너의 혈당은🩸', elem_classes="orbit-regular")
        gr.Markdown('##### 내가 먹은 음식 사진을 업로드 해 혈당이 얼마나 오를지 확인하고 혈당 스파이크를 예방해보세요!')
        
        with gr.Row():
            # 좌측(상단) 탭
            with gr.Tab(label='음식 이미지'):
                img_box = gr.Image(label='사진', value=None, sources=['upload', 'clipboard'])

                with gr.Row():
                    im_del_button = gr.Button('삭제', interactive=False)
                    predict_button = gr.Button('결과 보기', elem_id='button', interactive=False)
            
            # 우측(하단) 탭
            with gr.Column():        
                with gr.Tab(label='결과'):
                    
                    group = gr.Column(visible=False)
                    with group:
                        quest_box = gr.Markdown()
                        answer_radio = gr.Radio(['네', '아니오'], label='답변')
                        cooking_radio = gr.Radio(['날것', '삶음', '조림', '익힘', '찜', '튀김/볶음', '튀김(예:팝콘)', '구움(석쇠·그릴)', '구움(오븐)', 
                                                  '가공', '통조림', '발효', '냉동', '탄산음료'], label='음식 구분', visible=False)
                        result_box = gr.Markdown(elem_classes="nanum-gothic-regular")
                        warning_box = gr.Markdown('<br/></br>⚠️ 본 결과는 기계학습을 통한 예측치이므로 맹목적인 신뢰보다는 참고용으로만 이용해주시기 바랍니다.</br>* 상승 혈당치는 건강한 사람~당뇨 환자 간의 예상 범위를 나타내며, 해당 음식을 100g 섭취했을 때의 기준 값입니다.</br>', visible=False)
                        
                    replay_button = gr.Button('다시 하기', interactive=False)                
                    try_state = gr.State(0)
                    food_name_state = gr.State('')
                    
                    def check_food(img_path, try_times=0):
                        
                        food_name = model.predict_img(img_path, try_times)
                        if food_name != None:                            
                            return food_name, f'#### Q. 드신 음식이 {food_name}이(가) 맞나요?'
                        else:   # 아니오 5번 이상이면 데이터 없음 답변
                            return None, f'#### 죄송하지만 제가 알고 있는 음식이 아닌 것 같아요😭<br/>앞으로 더 많은 음식에 대해 공부해 올게요!'
                    

                    def select_answer(answer, img_path, try_times, food_name):
                        # 반환값: result_box, quest_box, warning_box, answer_radio, cooking_radio, try_state, food_name
                        if answer == '아니오':
                            try_times += 1
                            if try_times >= 5:  # 아니오 5번 이상이면 데이터 없으므로로 답변 비활성화
                                answer_update = gr.update(value=None, visible=False)
                            else:
                                answer_update = gr.update(value=None)
                            new_food_name, recall_check = check_food(img_path, try_times)
                            return '음식을 다시 탐색 중입니다.', recall_check, gr.update(visible=False), answer_update, gr.update(value=None, visible=False), try_times, new_food_name
                        elif answer == '네':
                            return '음식 분류를 선택하면 더 정확하게 예측할 수 있어요.', gr.update(), gr.update(), gr.update(), gr.update(visible=True), try_times, food_name
                        else:
                            return '', gr.update(), gr.update(visible=False), gr.update(value=None), gr.update(value=None, visible=False), try_times, food_name
                        

                    def select_cooking(cooking_method, food_name):

                        if cooking_method != None:
                            return predict_values(food_name, cooking_method)
                        else:
                            return ''


                    def predict_values(food_name, cooking_method):

                        info = get_nutrition_info(food_name, cooking_method)
                        pred_gi = model.request_gi_prediction(info)
                        gi_level, walking_degree = blood_sugar.classify_gi_level(pred_gi)
                        blood_value = blood_sugar.calc_blood_value(pred_gi, info)
                        food_list = pick_low_gi_food(3)
                        return print_results(gi_level, blood_value, walking_degree, food_list, food_name)

        
                    def print_results(gi_level, blood_value, walking_degree, food_list, food_name, gi_textbox):

                        time.sleep(0.5)
                        outputs = ''
                        outputs += f'### <center>`{gi_level}` 식품인 </br>`{food_name}`을(를) 섭취하셨군요!</center>'
                        outputs += f'<center><br/>혈당이 `{blood_value}` 정도<br/>상승할 수 있어요.</center>'
                        outputs += f'<center><br/>혈당 스파이크 예방을 위해<br/>`{walking_degree}` 걸으세요🚶‍♀️🚶‍♂️<br/>고강도 운동은 오히려 혈당을 상승시킬 수 있어요.</center>'
                        outputs += f'<center><br/>다음 식사에는 저혈당지수 식품인<br/>`{food_list}` 등을 섭취하시는 건 어떤가요?😊</center>'
                        return outputs, gr.update(visible=True)


            img_box.change(fn=enable_button, inputs=img_box, outputs=[im_del_button])
            img_box.change(fn=enable_button, inputs=img_box, outputs=[predict_button])
            result_box.change(fn=enable_button, inputs=result_box, outputs=[replay_button])
            answer_radio.change(fn=select_answer, 
                                inputs=[answer_radio, img_box, try_state, food_name_state], 
                                outputs=[result_box, quest_box, warning_box, answer_radio, cooking_radio, try_state, food_name_state])
            cooking_radio.change(fn=select_cooking, inputs=[cooking_radio, food_name_state], outputs=[result_box, warning_box])
            # 결과 확인용
            # cooking_radio.change(fn=select_cooking, inputs=[cooking_radio, food_name_state, gi_textbox], outputs=[result_box, warning_box, gi_textbox])

            predict_button.click(fn=check_food, inputs=[img_box], outputs=[food_name_state, quest_box])
            predict_button.click(fn=lambda : (gr.update(visible=True)), outputs=[group])
            predict_button.click(fn=lambda : (gr.update(visible=True)), outputs=[answer_radio])
            im_del_button.click(fn=lambda : (gr.update(value=None), # img_box
                                             gr.update(value=None), # quest_box
                                             gr.update(value=None), # result_box
                                             gr.update(visible=False),  # warning_box
                                             gr.update(visible=False),  # group
                                             gr.update(value=None, visible=True),   # answer_radio
                                             gr.update(value=None, visible=False),   # cooking_radio
                                             0, ''),    # try_state, food_state
                                outputs=[img_box, quest_box, result_box, warning_box, group, answer_radio, cooking_radio, try_state, food_name_state])
            replay_button.click(fn=lambda : (gr.update(value=None), # img_box
                                             gr.update(value=None), # quest_box
                                             gr.update(value=None), # result_box
                                             gr.update(visible=False),  # warning_box
                                             gr.update(visible=False),  # group
                                             gr.update(value=None, visible=True),   # answer_radio
                                             gr.update(value=None, visible=False),   # cooking_radio
                                             0, ''),    # try_state, food_state
                                outputs=[img_box, quest_box, result_box, warning_box, group, answer_radio, cooking_radio, try_state, food_name_state])