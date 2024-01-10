import os
#os.environ["CUDA_VISIBLE_DEVICES"]="0"
import wandb
from dataclasses import dataclass, field
from typing import Optional
import torch
import torch.nn as nn
from accelerate import Accelerator
from datasets import load_dataset,DatasetDict
from peft import AutoPeftModelForCausalLM, LoraConfig, get_peft_model_state_dict
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, HfArgumentParser, TrainingArguments

from trl import SFTTrainer
from trl.trainer import ConstantLengthDataset
from random import randrange
os.environ["WANDB_LOG_MODEL"] = "checkpoint"  # log all model checkpoints
os.environ["WANDB_PROJECT"] = "medical"  # name your W&B project
wandb.login()
import json
from rich import (inspect, print, pretty)
from rich.console import Console
from rich.syntax import Syntax
pretty.install()
import ast
from torch.utils.data import Dataset
class CustomInvoiceDataset(Dataset):
    def __init__(self, json_folder, text_folder):
        self.text_files = [os.path.join(text_folder, file) for file in os.listdir(text_folder)]
        self.json_files = [os.path.join(json_folder, file) for file in os.listdir(json_folder)]
        self.text_files.sort()
        self.json_files.sort()

        assert len(self.text_files) == len(self.json_files), "Mismatch in number of files"


    def __len__(self):
        return len(self.text_files)
    
    def __getitem__(self, index):
        with open(self.text_files[index],'r') as file:
            text_content = file.read()
            lines  = text_content.splitlines()
            list_of_lists = [ast.literal_eval(line) for line in lines]

        with open(self.json_files[index], 'r') as file:
            json_content = json.load(file)
        return list_of_lists, str(json_content)
    @property
    def features(self):
        return ('text','json')
    @property
    def num_rows(self):
        return len(self)
data = CustomInvoiceDataset("/home/huynv43/langchain_rag/data/json", "/home/huynv43/langchain_rag/data/txt_dataset_with_coor")
import torch
from torch.utils.data import DataLoader, random_split
total_size = len(data)
print(total_size)
train_ratio = 0.8
valid_ratio = 0.1
test_ratio = 0.1
train_size = int(total_size * train_ratio)
valid_size = int(total_size * valid_ratio)
test_size = total_size - train_size - valid_size 
train_dataset, valid_dataset, test_dataset = random_split(data, [train_size, valid_size, test_size])
def format_train_instruction(sample):
    return f"""### Instruction:
You are medical expert, and medical data engineer with many years on working with complex medical receipt structure. 
I need you parse, detect, recognize and convert following medical receipt OCR image result into structure medical receipt format. 
the outout mus be a well-formed json object.```json

### Input:
{sample[0]}

### Output:
{sample[1]}"""
def chars_token_ratio(dataset, tokenizer, nb_examples=400):
    """
    Estimate the average number of characters per token in the dataset.
    """
    total_characters, total_tokens = 0, 0
    for _, example in tqdm(zip(range(nb_examples), iter(dataset)), total=nb_examples):
        text = format_train_instruction(example)
        total_characters += len(text)
        if tokenizer.is_fast:
            total_tokens += len(tokenizer(text).tokens())
        else:
            total_tokens += len(tokenizer.tokenize(text))

    return total_characters / total_tokens


def create_datasets(tokenizer,train_data, test_data, valid_data ,data_dir=None,seq_length=2048,num_workers=6,streaming=False,size_valid_set=10,shuffle_buffer=1000):
    train_data = train_data
    valid_data = valid_data
    chars_per_token = chars_token_ratio(train_data, tokenizer)
    print(f"The character to token ratio of the dataset is: {chars_per_token:.2f}")

    train_dataset = ConstantLengthDataset(
        tokenizer,
        train_data,
        formatting_func=format_train_instruction,
        infinite=True,
        seq_length=seq_length,
        chars_per_token=chars_per_token,
    )
    valid_dataset = ConstantLengthDataset(
        tokenizer,
        valid_data,
        formatting_func=format_train_instruction,
        infinite=False,
        seq_length=seq_length,
        chars_per_token=chars_per_token,
    )
    return train_dataset, valid_dataset
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
hf_token = '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'

use_flash_attention = False
# Hugging Face model id
#model_id = "NousResearch/Llama-2-7b-hf" # non-gated "meta-llama/Llama-2-7b-hf
#model_id="PY007/TinyLlama-1.1B-intermediate-step-240k-503b"
model_id = "mistralai/Mistral-7B-v0.1" 

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
##quantization_config=bnb_config, 
# Load model and tokenizer
model_8bit = AutoModelForCausalLM.from_pretrained(model_id, 
                                             #load_in_8bit=True,      
                                             quantization_config=bnb_config,  
                                             trust_remote_code=True,                                                  
                                             device_map="auto",
                                             token = hf_token )

base_tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
base_tokenizer.pad_token = base_tokenizer.eos_token
base_tokenizer.padding_side = "right"
def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

print_trainable_parameters(model_8bit)
## frezee the model
for param in model_8bit.parameters():
  param.requires_grad = False  # freeze the model - train adapters later
  if param.ndim == 1:
    # cast the small parameters (e.g. layernorm) to fp32 for stability
    param.data = param.data.to(torch.float32)

model_8bit.gradient_checkpointing_enable()  # reduce number of stored activations
model_8bit.enable_input_require_grads()

class CastOutputToFloat(nn.Sequential):
  def forward(self, x): return super().forward(x).to(torch.float32)
model_8bit.lm_head = CastOutputToFloat(model_8bit.lm_head)
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model

peft_config = LoraConfig(
    r=64, 
    lora_alpha=16,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"], # skip this time
    bias="none",
    task_type="CAUSAL_LM",
)

## prepare model for training
model = prepare_model_for_kbit_training(model_8bit)
base_model = get_peft_model(model, peft_config)
base_model.print_trainable_parameters()
os.environ["WANDB_PROJECT"] = "Vietnamese_medical1"  # name your W&B project
os.environ["WANDB_LOG_MODEL"] = "checkpoint"  # log all model checkpoints
from transformers import TrainingArguments

OUTPUT_DIR = "./results/mistral7b_ocr_to_json_10epoch2"
NUM_TRAIN_EPOCHS = 10
BATCH_SIZE=128
PER_DEVICE_TRAIN_BATCH_SIZE=3
PER_DEVICE_EVAL_BATCH_SIZE=1
GRADIENT_ACCUMULATION_STEPS = BATCH_SIZE // PER_DEVICE_TRAIN_BATCH_SIZE
SAVE_STEPS=20
LOGGING_STEPS=10
LEARNING_RATE=2e-4 #3e-4
TRAIN_STEPS=150  #300
#WARM_UP_STEPS=50  or ratio 
max_seq_length = 2048 # max sequence length for model and packing of the dataset
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=NUM_TRAIN_EPOCHS,
    per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
    per_device_eval_batch_size=PER_DEVICE_EVAL_BATCH_SIZE,        
    gradient_accumulation_steps=2, ## GRADIENT_ACCUMULATION_STEPS,
    gradient_checkpointing=True,        
    optim="paged_adamw_32bit",  
    logging_steps=LOGGING_STEPS,    
    save_total_limit=2,  
    save_strategy="epoch",    
    learning_rate=2e-4,            ## LEARNING_RATE,    
    fp16=True,
    # tf32=True,        
    max_grad_norm=0.3,
    warmup_ratio=0.03,             ## warmup_steps=WARM_UP_STEPS,    
    lr_scheduler_type="constant",  ##"cosine"   
    disable_tqdm=True,              # disable tqdm since with packing values are in correct    
    #max_steps=TRAIN_STEPS,
    report_to="wandb",
    #save_steps=SAVE_STEPS,
    #group_by_length=False,
    #remove_unused_columns=False,
    evaluation_strategy="epoch",  #steps
    run_name="sft_mistral7b_colorist",

)
train_dataset, eval_dataset = create_datasets(base_tokenizer, train_dataset, test_dataset, valid_dataset, seq_length=max_seq_length)
from trl import SFTTrainer,DataCollatorForCompletionOnlyLM

trainer = SFTTrainer(
    model=base_model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=peft_config,
    packing=True,  ## make sure group_by_length=False
    max_seq_length=max_seq_length,
    tokenizer=base_tokenizer,
    args=training_args,

)
base_model.config.pretraining_tp = 1
base_model.config.use_cache = False  # silence the warnings. Please re-enable for inference!

## pytorch optimization 
old_state_dict = base_model.state_dict
base_model.state_dict = (
    lambda self, *_, **__: get_peft_model_state_dict(
        self, old_state_dict()
    )
).__get__(base_model, type(base_model)) 
base_model = torch.compile(base_model)

# Enable cuDNN auto-tuner - NVIDIA cuDNN supports many algorithms to compute a convolution. 
torch.backends.cudnn.benchmark = True
trainer.train() # there will not be a progress bar since tqdm is disabled
# save model
trainer.save_model(OUTPUT_DIR)