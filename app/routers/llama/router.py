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

modelname = 'llama3-1b-trained_cpu'
model_path = os.path.abspath(f"{get_settings().MODELS_DIR}{os.sep}{modelname}")
device = "cuda" if torch.cuda.is_available() else "cpu"


tokenizer = AutoTokenizer.from_pretrained(model_path)


base_model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map={"": 0} if device == "cuda" else {"": "cpu"}
)


@router.post(
        "/predict",
        response_model=LlamaOutput,
        tags=["llama"])
def predict(input: LlamaInput):

    inputs = tokenizer(
        input.prompt, return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = base_model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.5,
            top_p=0.98,
            do_sample=True,
        )

    res = tokenizer.decode(outputs[0], skip_special_tokens=True)
    result = copy.deepcopy(res)
    print(result)
    return {"generated": result}
