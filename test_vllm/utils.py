import gc

from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
import base64
import requests
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR,draw_ocr
from numpy import asarray

def encode_image(img_pil):
    buffered = BytesIO()
    # img_pil = Image.fromarray(np.uint8(image_np))
    img_pil.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_base64 = img_str.decode('utf-8')
    # img_base64 = f"data:image/png;base64,{img_base64}"

    del buffered 
    del img_pil
    del img_str
    gc.collect()

    return img_base64


def decode_image(image_b64, mode=None):
    # img_encode = image_b64.split(',')[1]
    img_bytes = base64.b64decode(image_b64)
    # img = Image.open(BytesIO(img_bytes))
    if mode is not None:
        img = Image.open(BytesIO(img_bytes)).convert(mode)
    else:
        img = Image.open(BytesIO(img_bytes))
    # img = ImageOps.exif_transpose(img)

    del img_bytes
    gc.collect()

    return img


def get_OCR(img_pil, preprocess=True):
    # img_base64 = encode_image(img_pil)
    try:
        r = requests.post('http://10.124.64.203:10000/infer', json={'base64_image': img_pil}, params=dict(preprocess=preprocess))
        r = r.json()
        print('OK------------------------------------------')    
    except Exception as e:
        # print(str(e))
        # print(r.status_code)
        # print(r.status_code)    
        print('Err----------------------------------------------')    
        return []
    
    return r

def convert_json(data):
    new_d = {
        'image_size': data['image_size']
    }
    phrases = data['phrases']
    new_phs = []
    for phrase in phrases:
        words = phrase['words']
        for word in words:
            new_w = [{
                'text': word['text'],
                'bbox': word['bbox']
            }]
            new_phs.append({
                'words': new_w,
                'text': word['text'],
                'bbox':  word['bbox'],
                # 'label': phrase['label'],
                # 'is_key': phrase['is_key'],
                # 'is_value': phrase['is_value']
            })
    new_d['phrases'] = new_phs
    return new_d
class OCR:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.config = Cfg.load_config_from_name('vgg_transformer')
        self.detector = Predictor(self.config)
    def get_ocr(self, image):
        data = asarray(image)
        image = Image.fromarray(image)

        detect = self.ocr(data, cls = True)
        boxes = [line for line in detect[0]]
        result = ""
        for box in boxes:
            top_left     = (int(box[0][0]), int(box[0][1]))
            bottom_right = (int(box[2][0]), int(box[2][1]))
            bounding_box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
            result += self.detector.predict(image.crop(bounding_box), return_prob=False)
            result += " "
        return result