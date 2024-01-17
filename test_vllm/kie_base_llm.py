import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
hf_token = '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'
from torch import cuda, bfloat16
import transformers
# from langchain.memory import ConversationBufferMemory
from torch import cuda, bfloat16
import transformers
from transformers import  AutoModelForCausalLM, AutoTokenizer
from transformers import TextStreamer, pipeline
import io
import gc
import torch
from langchain_experimental.llms import JsonFormer
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import LLMChain
from langchain import HuggingFacePipeline, PromptTemplate

model_name = "nguyenhuy/mistralai-Code-Instruct-Finetune-test"
tokenizer = "nguyenhuy/mistralai-Code-Instruct-Finetune-test"

bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)
class LLMBase:
    def __init__(self, model_name=model_name, top_k = 20, top_p = 0.95, temperature = 0.01):
        self.model_name = model_name
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name,
                                            trust_remote_code=True,
                                            quantization_config=bnb_config,
                                            token = hf_token,
                                            device_map = 'auto'
                                            )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True, device = "auto", token = hf_token)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            do_sample=False,
            max_new_tokens = 1024,
            temperature = self.temperature,
            top_k = self.top_k,
            top_p = self.top_p,
            repetition_penalty=1.15,
            streamer=self.streamer,
            stop_sequence = ['END','```']
        )
 
        self.default_data_points =  """
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
        # self.json_schema = {
        #     "type": "object",
        #     "properties": {
        #         "current_institute": {"type": "string"},
        #         "patient_name": {"type": "string"},
        #         "gender": {"type": "string"},
        #         "birth": {"type": "string"},
        #         "age": {"type": "string"},
        #         "address": {"type": "string"},
        #         "tel_customer": {"type": "string"},
        #         "id_bhyt": {"type": "string"},
        #         "diagnosis": {"type": "string"},
        #         "drugs": {
        #             "type": "array",
        #             "drugs": {
        #                 "type": "object",
        #                 "properties": {
        #                     "drug_name": {"type": "string"},
        #                     "drug_dose": {"type": "string"},
        #                     "drug_quantity": {"type": "string"}
        #                 }
        #             }
        #         },
        #         "date_in": {"type": "string"},
        #         "doctor_name": {"type": "string"},                
        #     }
        # }
        self.template = """
                You are an AI Assistant in the medical field. Your goal is to provide the Human with information extracted from the Human"s prescription. Think step by step and never skip any step.
                Please try to extract all data points. Do not add or omit any information. If you don"t know, just answer "don"t know" and do not include information that is not in the document in your answer.
                {data_points}
               
                EXAMPLES
                ----
                Human: BỆNH VIỆN VIETT ĐỨC Số toa: 71 Nhà thuốc Bệnh viện Số điện thoại: 02435766328 Năm sinh: 1963 15A-Phương Mai-Đống Đa-Hà Nội PHIÊU THU TIỀN Xuất từ: Quầy Thuốc 1 In: Quầy Thuốc Lần in: 1 Giờ in: 08:15:54 Họ tên bệnh nhân: LÊ NGỌC LAN Mã bệnh nhân: 0029212798 Bác sĩ khám bệnh: Ths.BS TRỊNH MINH TRANG TT Tên mặt hàng ĐVT SL Đơn giá Thành tiền Spulit 100mg Viên 60 17.655 1.059.300 2 Ziaja Med Anti-imperfections Formula Cleansing Body Gel (Gel tắm ngừa khuẩn) 400ml Chai 1 499.460 499.460 3 Notis Antidanruff Shampoo 125ml Chai 2 248.600 497.200 4 Amisea 167mg Viên 30 6.420 192.600 5 Cafunten 10g Tuýp 4 6.527 26.108 Tổng khoản: 5 Tổng tiền: 2.274.668 Bằng chữ: Hai triệu hai trăm bảy mượi bốn nghìn sáu trăm sáu mươi tám đồng. Ngày 26 tháng 04 năm 2022 Người thu tiền Người nhận thuốc ngay trong ngày Lưu Trường hợp khách hàng có đơn tài chính đề nghị lấy (Quá ngày Bệnh viện không với nhân viên (Ký, họ tên) (Ký, họ tên) nhà thuốc để được hướng dẫn) Trân trọng cảm ơn Quý khách đã mua thuốc tại Bệnh viện. NGUYỄN HÀ MY LÊ NGỌC LAN
                AI ASSISTANT: {{"current_institute": "BỆNH VIỆN VIỆT ĐỨC", "name": "LÊ NGỌC LAN", "gender": "", "birth": "1963", "age": "", "address": "", "tel_customer": "", "id_bhyt": "", "diagnosis": "", "drugs": [{{"drug_name": "Spulit 100mg", "drug_dose": "", "drug_quantity": "60 Viên"}}, {{"drug_name": "Ziaja Med Anti-imperfections Formula Cleansing Body Gel (Gel tắm ngừa khuẩn) 400ml", "drug_dose": "", "drug_quantity": "1 Chai"}}, {{"drug_name": "Notis Antidanruff Shampoo 125ml", "drug_dose": "", "drug_quantity": "2 Chai"}}, {{"drug_name": "Amisea 167mg", "drug_dose": "", "drug_quantity": "30 Viên"}}, {{"drug_name": "Cafunten 10g", "drug_dose": "", "drug_quantity": "4 Tuýp"}}], "date_in": "Ngày 26 tháng 04 năm 2022", "doctor_name": "Ths.BS TRỊNH MINH TRANG"}} END
           
                Human: ! Mã BN:2101002494 Số: 211002020 Mã hồ sơ: 2110150077 Kho:110-Kho Ngoại trú ĐƠN THUỐC BẢO HIỂM KKB.43333 Giới tính: Nam Đối tượng: Số thẻ BHYT: CK2383820079366 Địa chỉ: Lê Hoàn 2, Điện Biên, Thành phố Thanh Hóa, Tỉnh Thanh Hóa, Việt Nam Chẩn đoán: E11-Bệnh đái tháo đường không phụ thuộc insuline/ E78-1 Rối loạn chuyển Phòng: Phòng khám 326 Họ tên: LÊ HỒNG KHANH hóa lipoprotein và tình trạng tăng lipid máu khác / Bảo Hiểm Nơi ĐK KCB BĐ: 38280 Ngày sinh: 18/06/1956 Tuổi: 65 SĐT: 0912 660 254 STT Tên thuốc- Cách dùng ĐVT Số lượng BETICAPO 750 SR-750mg (Metformin) Ngày uống 1 viên sau ăn chiều. Viên 60 2 Gliclada 60mg modified- release tablets (Gliclazid) 3 Ngày uống 2 viên trước ăn sáng 30 phút TV. Fenofibrat- 200mg (Fenofibrat) Viên 120 Uống tối 1 viên ngay sau ăn Viên 60 Cộng khoản: 3 loại Lưu Khám lại khi thấy bất thường và khi hết thuốc. Kế toán Thủ kho Người bệnh Ngày 15 tháng 10 năm 2021 Bác sĩ khám (Ký và ghi rõ họ, tên) (Ký và ghi rõ họ, tên) Khih Lê Văn Chinh ISOFH-Người in: Lê Văn Chinh, ngày in: 15/10/2021 08:24
                AI ASSISTANT: {{"current_institute": "", "patient_name": "LÊ HỒNG KHANH",  "gender": "Nam", "birth" : "18/06/1956", "age": "65", "address": "Lê Hoàn 2, Điện Biên, Thành phố Thanh Hóa, Tỉnh Thanh Hóa, Việt Nam", "tel_customer": "0912 660 254", "id_bhyt": "CK2383820079366", "diagnosis": "E11 - Bệnh đái tháo đường không phụ thuộc insuline / E78 - Rối loạn chuyển hóa lipoprotein và tình trạng tăng lipid máu khác", "drugs": [{{"drug_name": "BETICAPO 750 SR-750mg (Metformin)", "drug_dose": "Ngày uống 1 viên sau ăn chiều", "drug_quantity": "60 Viên"}}, {{"drug_name": "Gliclada 60mg modified-release tablets (Gliclazid)", "drug_dose": "Ngày uống 2 viên trước ăn sáng 30 phút", "drug_quantity": "120 viên"}}, {{"drug_name": "Fenofibrat-200mg (Fenofibrat)", "drug_dose": "Uống tối 1 viên ngay sau ăn", "drug_quantity": "60 viên"}}], "date_in": "Ngày 15 tháng 10 năm 2021", "doctor_name": "Lê Văn Chinh"}} END
           
                Human: Tp.HCM Xem tóm tăt bệnh án Bệnh viện Da Liễu ĐT: (028) 39308131 Mã BN: 22368078 P.khám 7 ĐƠN THUỐC ĐT: 0965839049 Họ và tên: TRỊNH PHẠM KIỀU NGA. 18 tháng. Nữ Địa chỉ: ,,Xã Tân Tây,Huyện Gò Công Đông,Tỉnh Tiền Giang Chẩn đoán: (L70;) Trứng cá; Thuốc điều trị: 1 Minocyclin 50mg (Zalenka) 30 Viên Uống, sáng 1 viên, chiều 1 viên 2 L-Cystin 500mg (Elovess) 30 Viên Uống, sáng 1 viên, chiều l viên 3 Cetirizin (10mg) (Cetimed) 15 Viên Uống,, chiều 1 viên 4 Lưu huỳnh 5% (Cream Lưu Huỳnh) 2 Lọ Bôi., sáng 1 lần, tối 1 lần thân cộng:4 khoản Ngày cấp đơn 07 tháng 12 năm 2022 - Tái khám: 1 Bác sĩ điều trị + Khi hết thuốc uống hoặc + Bệnh nặng hơn Bs.CKII Hồ Thị Mỹ Châu BENH VIỆN DA LIEU KHU KHÁM THEO YÊU lọc dinh dưỡng: CN: 53Kg; CC: 156 Cm ;BMI: 21 Kg/m2 ên người đưa trẻ đến khám: Khuyến cáo dinh dưỡng: -Ăn đầy đủ chất dinh dưỡng, đặc biệt vitamin A, C,E, kẽm, omega 3... Hạn chế uống sữa, thức ăn nhiều tinh bột, nhiều đường, nhiều dầu mỡ, tránh căng thẳng. hám lại xin mang theo đơn này Tờ:[1-2]
                AI ASSISTANT: {{"current_institute": "Bệnh viện Da Liễu", "patient_name": "TRỊNH PHẠM KIỀU NGA", "gender": "Nữ", "birth" : "", "age": "18 tháng", "address": "Xã Tân Tây, Huyện Gò Công Đông,Tỉnh Tiền Giang", "tel_customer": "0965839049","id_bhyt": "", "diagnosis": "(L70;) Trứng cá;", "drugs": [{{"drug_name": "Minocyclin 50mg (Zalenka)", "drug_dose": "sáng 1 viên, chiều 1 viên", "drug_quantity": "30 viên"}}, {{"drug_name": "L-Cystin 500mg (Elovess)", "drug_dose": "sáng 1 viên, chiều 1 viên", "drug_quantity": "30 viên"}}, {{"drug_name": "Cetirizin (10mg) (Cetimed)", "drug_dose": "chiều 1 viên", "drug_quantity": "15 viên"}}, {{"drug_name": "Lưu huỳnh 5% (Cream Lưu Huỳnh)", "drug_dose": "bôi sáng 1 lần, tối 1 lần", "drug_quantity": "2 lọ"}}], "date_in": "07 tháng 12 năm 2022", "doctor_name": "Bs.CKII Hồ Thị Mỹ Châu"}} END
               
                ------    
                Human: {content}
                AI ASSISTANT:
    """.strip()
        self.prompt = PromptTemplate(template=self.template, input_variables=['data_points','content'])
        self.llm = HuggingFacePipeline(pipeline = self.text_pipeline)
        self.chain = LLMChain(llm = self.llm, prompt = self.prompt, verbose=True)
    def change_model(self, model_name, top_k = 50, top_p = 0.9, temperature = 0.1):
        try:
            del self.model
            del self.text_pipeline
            del self.builder
            del self.tokenizer
            gc.collect()
            torch.cuda.empty_cache()
        except:
            pass
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True,
                                                       device_map = "auto",
                                                       )

        self.model = AutoModelForCausalLM.from_pretrained(model_name,
                                             trust_remote_code=True,
                                             quantization_config=bnb_config,
                                             device_map = "auto")
        
        self.text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens = 512,
            temperature = self.temperature,
            top_k = self.top_k,
            top_p = self.top_p,
            repetition_penalty=1.15,
            streamer=self.streamer,
        )
        self.builder = JsonFormer(json_schema = self.json_schema, pipeline = self.text_pipeline)
    def response(self, content, data_points):
        return self.chain({"content": content, "data_points": data_points})
        