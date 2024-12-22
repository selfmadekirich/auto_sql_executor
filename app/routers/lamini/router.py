from fastapi import APIRouter
from .models import LaminiInput, LaminiOutput
from settings import get_settings

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# IMPORTS FOR TEXT GENERATION PIPELINE CHAIN
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import copy
import os

router = APIRouter(prefix="/lamini")


checkpoint = os.path.abspath(f"{get_settings().MODELS_DIR}{os.sep}lamini")
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint,
    device_map='auto',
    torch_dtype=torch.float32
)


### INITIALIZING PIPELINE WITH LANGCHAIN
llm = HuggingFacePipeline.from_model_id(
    model_id=checkpoint,
    task='text2text-generation',
    model_kwargs={
        "temperature": 0.65,
        "min_length": 30,
        "max_length": 3500,
        "repetition_penalty": 5.0})


@router.post(
        "/predict",
        response_model=LaminiOutput,
        tags=["lamini"])
def predict(input: LaminiInput):
    prompt = PromptTemplate.from_template(
        "Consider this information {info}. Generate SQL")
    prompt.format(info=input.prompt)
    chat = LLMChain(prompt=prompt, llm=llm)
    res = chat.run(input.query)
    result = copy.deepcopy(res)
    print(result)
    return {"generated": result}
