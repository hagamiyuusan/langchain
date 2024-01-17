import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
from threading import Thread
import transformers
from torch import cuda, bfloat16
import time
from PIL import Image
import numpy as np
import requests
from resources import birth_schema, birth_examples, examples_passport, schema_passport
from utils import get_OCR, OCR
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)
ocr = OCR()
import io
import base64
count = 0



data_points = """
        {
        "current_institute": "name of the hospital or clinic issuing the prescription",
        "name": "patient full name",
        "gender": "patient gender",
        "birth": "date of birth",
        "age": "patient age",
        "address": "patient address",
        "tel_customer": "patient phone number",
        "id_bhyt": "health insurance card number",
        "diagnosis": "diagnosis",
        "drugs": [{
            "drug_name": "drug name",
            "drug_dose": "drug dosage, usage and instructions",
            "drug_quantity": "drug duantity"
        }],
        "date_in": "issued date",
        "doctor_name": "doctor full name",
        }
        """
examples = """
                Human: BỆNH VIỆN VIETT ĐỨC Số toa: 71 Nhà thuốc Bệnh viện Số điện thoại: 02435766328 Năm sinh: 1963 15A-Phương Mai-Đống Đa-Hà Nội PHIÊU THU TIỀN Xuất từ: Quầy Thuốc 1 In: Quầy Thuốc Lần in: 1 Giờ in: 08:15:54 Họ tên bệnh nhân: LÊ NGỌC LAN Mã bệnh nhân: 0029212798 Bác sĩ khám bệnh: Ths.BS TRỊNH MINH TRANG TT Tên mặt hàng ĐVT SL Đơn giá Thành tiền Spulit 100mg Viên 60 17.655 1.059.300 2 Ziaja Med Anti-imperfections Formula Cleansing Body Gel (Gel tắm ngừa khuẩn) 400ml Chai 1 499.460 499.460 3 Notis Antidanruff Shampoo 125ml Chai 2 248.600 497.200 4 Amisea 167mg Viên 30 6.420 192.600 5 Cafunten 10g Tuýp 4 6.527 26.108 Tổng khoản: 5 Tổng tiền: 2.274.668 Bằng chữ: Hai triệu hai trăm bảy mượi bốn nghìn sáu trăm sáu mươi tám đồng. Ngày 26 tháng 04 năm 2022 Người thu tiền Người nhận thuốc ngay trong ngày Lưu Trường hợp khách hàng có đơn tài chính đề nghị lấy (Quá ngày Bệnh viện không với nhân viên (Ký, họ tên) (Ký, họ tên) nhà thuốc để được hướng dẫn) Trân trọng cảm ơn Quý khách đã mua thuốc tại Bệnh viện. NGUYỄN HÀ MY LÊ NGỌC LAN
                AI ASSISTANT: {"current_institute": "BỆNH VIỆN VIỆT ĐỨC", "name": "LÊ NGỌC LAN", "gender": "", "birth": "1963", "age": "", "address": "", "tel_customer": "", "id_bhyt": "", "diagnosis": "", "drugs": [{"drug_name": "Spulit 100mg", "drug_dose": "", "drug_quantity": "60 Viên"}, {"drug_name": "Ziaja Med Anti-imperfections Formula Cleansing Body Gel (Gel tắm ngừa khuẩn) 400ml", "drug_dose": "", "drug_quantity": "1 Chai"}, {"drug_name": "Notis Antidanruff Shampoo 125ml", "drug_dose": "", "drug_quantity": "2 Chai"}, {"drug_name": "Amisea 167mg", "drug_dose": "", "drug_quantity": "30 Viên"}, {"drug_name": "Cafunten 10g", "drug_dose": "", "drug_quantity": "4 Tuýp"}], "date_in": "Ngày 26 tháng 04 năm 2022", "doctor_name": "Ths.BS TRỊNH MINH TRANG"} END
           
                Human: ! Mã BN:2101002494 Số: 211002020 Mã hồ sơ: 2110150077 Kho:110-Kho Ngoại trú ĐƠN THUỐC BẢO HIỂM KKB.43333 Giới tính: Nam Đối tượng: Số thẻ BHYT: CK2383820079366 Địa chỉ: Lê Hoàn 2, Điện Biên, Thành phố Thanh Hóa, Tỉnh Thanh Hóa, Việt Nam Chẩn đoán: E11-Bệnh đái tháo đường không phụ thuộc insuline/ E78-1 Rối loạn chuyển Phòng: Phòng khám 326 Họ tên: LÊ HỒNG KHANH hóa lipoprotein và tình trạng tăng lipid máu khác / Bảo Hiểm Nơi ĐK KCB BĐ: 38280 Ngày sinh: 18/06/1956 Tuổi: 65 SĐT: 0912 660 254 STT Tên thuốc- Cách dùng ĐVT Số lượng BETICAPO 750 SR-750mg (Metformin) Ngày uống 1 viên sau ăn chiều. Viên 60 2 Gliclada 60mg modified- release tablets (Gliclazid) 3 Ngày uống 2 viên trước ăn sáng 30 phút TV. Fenofibrat- 200mg (Fenofibrat) Viên 120 Uống tối 1 viên ngay sau ăn Viên 60 Cộng khoản: 3 loại Lưu Khám lại khi thấy bất thường và khi hết thuốc. Kế toán Thủ kho Người bệnh Ngày 15 tháng 10 năm 2021 Bác sĩ khám (Ký và ghi rõ họ, tên) (Ký và ghi rõ họ, tên) Khih Lê Văn Chinh ISOFH-Người in: Lê Văn Chinh, ngày in: 15/10/2021 08:24
                AI ASSISTANT: {"current_institute": "", "patient_name": "LÊ HỒNG KHANH",  "gender": "Nam", "birth" : "18/06/1956", "age": "65", "address": "Lê Hoàn 2, Điện Biên, Thành phố Thanh Hóa, Tỉnh Thanh Hóa, Việt Nam", "tel_customer": "0912 660 254", "id_bhyt": "CK2383820079366", "diagnosis": "E11 - Bệnh đái tháo đường không phụ thuộc insuline / E78 - Rối loạn chuyển hóa lipoprotein và tình trạng tăng lipid máu khác", "drugs": [{"drug_name": "BETICAPO 750 SR-750mg (Metformin)", "drug_dose": "Ngày uống 1 viên sau ăn chiều", "drug_quantity": "60 Viên"}, {"drug_name": "Gliclada 60mg modified-release tablets (Gliclazid)", "drug_dose": "Ngày uống 2 viên trước ăn sáng 30 phút", "drug_quantity": "120 viên"}, {"drug_name": "Fenofibrat-200mg (Fenofibrat)", "drug_dose": "Uống tối 1 viên ngay sau ăn", "drug_quantity": "60 viên"}], "date_in": "Ngày 15 tháng 10 năm 2021", "doctor_name": "Lê Văn Chinh"} END
           
                Human: Tp.HCM Xem tóm tăt bệnh án Bệnh viện Da Liễu ĐT: (028) 39308131 Mã BN: 22368078 P.khám 7 ĐƠN THUỐC ĐT: 0965839049 Họ và tên: TRỊNH PHẠM KIỀU NGA. 18 tháng. Nữ Địa chỉ: ,,Xã Tân Tây,Huyện Gò Công Đông,Tỉnh Tiền Giang Chẩn đoán: (L70;) Trứng cá; Thuốc điều trị: 1 Minocyclin 50mg (Zalenka) 30 Viên Uống, sáng 1 viên, chiều 1 viên 2 L-Cystin 500mg (Elovess) 30 Viên Uống, sáng 1 viên, chiều l viên 3 Cetirizin (10mg) (Cetimed) 15 Viên Uống,, chiều 1 viên 4 Lưu huỳnh 5% (Cream Lưu Huỳnh) 2 Lọ Bôi., sáng 1 lần, tối 1 lần thân cộng:4 khoản Ngày cấp đơn 07 tháng 12 năm 2022 - Tái khám: 1 Bác sĩ điều trị + Khi hết thuốc uống hoặc + Bệnh nặng hơn Bs.CKII Hồ Thị Mỹ Châu BENH VIỆN DA LIEU KHU KHÁM THEO YÊU lọc dinh dưỡng: CN: 53Kg; CC: 156 Cm ;BMI: 21 Kg/m2 ên người đưa trẻ đến khám: Khuyến cáo dinh dưỡng: -Ăn đầy đủ chất dinh dưỡng, đặc biệt vitamin A, C,E, kẽm, omega 3... Hạn chế uống sữa, thức ăn nhiều tinh bột, nhiều đường, nhiều dầu mỡ, tránh căng thẳng. hám lại xin mang theo đơn này Tờ:[1-2]
                AI ASSISTANT: {"current_institute": "Bệnh viện Da Liễu", "patient_name": "TRỊNH PHẠM KIỀU NGA", "gender": "Nữ", "birth" : "", "age": "18 tháng", "address": "Xã Tân Tây, Huyện Gò Công Đông,Tỉnh Tiền Giang", "tel_customer": "0965839049","id_bhyt": "", "diagnosis": "(L70;) Trứng cá;", "drugs": [{"drug_name": "Minocyclin 50mg (Zalenka)", "drug_dose": "sáng 1 viên, chiều 1 viên", "drug_quantity": "30 viên"}, {"drug_name": "L-Cystin 500mg (Elovess)", "drug_dose": "sáng 1 viên, chiều 1 viên", "drug_quantity": "30 viên"}, {"drug_name": "Cetirizin (10mg) (Cetimed)", "drug_dose": "chiều 1 viên", "drug_quantity": "15 viên"}, {"drug_name": "Lưu huỳnh 5% (Cream Lưu Huỳnh)", "drug_dose": "bôi sáng 1 lần, tối 1 lần", "drug_quantity": "2 lọ"}], "date_in": "07 tháng 12 năm 2022", "doctor_name": "Bs.CKII Hồ Thị Mỹ Châu"} END
               
"""
template = """
                You are an AI Assistant in general field. Your goal is to provide the Human with informations extracted from the Human's document. Think step by step and never skip any step.
                Please try to extract all data points. Do not add or omit any information. If you don't know, just answer "don't know" and do not include information that is not in the document in your answer.
                {data_points}
               
                EXAMPLES
                ----
                {examples}
                ------    
                Human: {content}
                AI ASSISTANT:
    """.strip()
def update_data_points(input_text):
    global data_points
    data_points = input_text
def update_examples(input_text):
    global examples
    examples = input_text
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1",
                                            trust_remote_code=True,
                                            quantization_config=bnb_config,
                                            device_map = 'auto',
                                            do_sample=False )
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", torch_dtype=torch.float16, use_fast = True, device = 'auto')
def image_to_base64(image):
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    result_ocr = get_OCR(img_str)
    content = get_text(result_ocr)
    return content

def get_text(ocr_res):
    text = ''
    phrases = ocr_res["phrases"]
    for phrase in phrases:
        text += phrase['text'] + '\n'
    return text

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [1, 21288, 2]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

def predict(message, history):

    # history_transformer_format = history + [[message, ""]]
    stop = StopOnTokens()
    global data_points
    global examples
    global template
    formatted_template = template.format(data_points = data_points, examples = examples, content = message)
    print(formatted_template)
    # messages = "".join(["".join(["\n<human>:"+item[0], "\n<bot>:"+item[1]])  #curr_system_message +
    #             for item in history_transformer_format])
    model_inputs = tokenizer([formatted_template], return_tensors="pt").to("cuda")
    streamer = TextIteratorStreamer(tokenizer, timeout=10., skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=1024,
        do_sample=False,
        top_p=0.95,
        top_k=20,
        temperature=1.0,
        num_beams=1,
        repetition_penalty = 1.15,
        stopping_criteria=StoppingCriteriaList([stop])
        )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    start = time.time()
    partial_message  = ""
    global count
    count = 0
    for new_token in streamer:
        if new_token != '<' and new_token !='END':
            count+=1
            partial_message += new_token
            yield partial_message
    end = time.time()
    print(end-start)
    print(f"""{count/(end-start)} tokens per second""")
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(label="Upload Image")
            convert_button = gr.Button("Get OCR Text")
            output_textbox = gr.Textbox(label="OCR Result", interactive=False, show_copy_button = True)
            convert_button.click(fn=ocr.get_ocr, inputs=image_input, outputs=output_textbox)

        
        with gr.Column(scale=2):
            data_points_input = gr.Textbox(label="Enter your Schema", value=data_points)
            data_points_button = gr.Button("Update Data Points")
            data_points_button.click(fn=update_data_points, inputs=data_points_input, outputs=None)


            examples_input = gr.Textbox(label="Enter your Examples", value=examples)
            examples_button = gr.Button("Update Examples")
            examples_button.click(fn=update_examples, inputs=examples_input, outputs=None)
            
            
            gr.Examples(
            [[schema_passport, examples_passport], [data_points, examples],[birth_schema, birth_examples]],
            [data_points_input, examples_input])
            gr.ChatInterface(predict)
demo.launch()