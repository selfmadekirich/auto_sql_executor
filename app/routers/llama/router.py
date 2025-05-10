from fastapi import APIRouter
from .models import LlamaInput, LlamaOutput
from settings import get_settings

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

import copy
import os

router = APIRouter(prefix="/llama")

modelname = 'llama3-1b-trained'
model_path = os.path.abspath(f"{get_settings().MODELS_DIR}{os.sep}{modelname}")
device = "cuda" if torch.cuda.is_available() else "cpu"


tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForCausalLM.from_pretrained(modelname)

base_model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map={"": 0} if device == "cuda" else {"": "cpu"}
)


@router.post(
        "/predict",
        response_model=LlamaOutput,
        tags=["llama"])
def predict(input: LlamaInput):

    inputs = tokenizer.encode(
        input.prompt, return_tensors="pt"
    ).to(device)

    outputs = model.generate(**inputs)

    res = tokenizer.decode(outputs[0], skip_special_tokens=True)
    result = copy.deepcopy(res)
    print(result)
    return {"generated": result}
