import os
import json
import boto3
from transformers import AutoModelForCausalLM
from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from pydantic import BaseModel, validator
from typing import Optional, List, Union
from typing import Dict, Optional
from typing import Union, Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel
import traceback
from typing import ClassVar
from pydantic import BaseModel
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
from typing import Optional, List, ClassVar
from pydantic import BaseModel, validator
#in here we need to instead use huggingface transformers, using a model of the users selection.

MODEL_TYPE=os.environ.get("MODEL_TYPE")
SAVEPATH=os.environ.get("SAVE_PATH")
STAGE = os.environ.get('STAGE', None)
#OPENAPI_PREFIX = f"/{STAGE}" if STAGE else "/"
HF_AUTH_TOKEN=os.environ.get('HF_AUTH_TOKEN')

app = FastAPI(title="Sagemaker Endpoint LLM API for HuggingFace Models")#, openapi_prefix=OPENAPI_PREFIX)


if HF_AUTH_TOKEN is not None:
    if len(HF_AUTH_TOKEN) <1:
        os.environ['HF_AUTH_TOKEN']=None
        HF_AUTH_TOKEN = os.environ.get(HF_AUTH_TOKEN)
#Initial config 
TOKENIZER=None
MODEL = None
try:
    TOKENIZER = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=MODEL_TYPE,cache_dir=SAVEPATH, use_auth_token=HF_AUTH_TOKEN,trust_remote_code=True)
    MODEL = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=MODEL_TYPE,cache_dir=SAVEPATH,use_auth_token=HF_AUTH_TOKEN,trust_remote_code=True)
except Exception as e:
    print(e) #I'm doing a lazy way of handling initial configuration, just in case the user does not provide an initial model and instead wishes to provide it in configuration later.

print(MODEL_TYPE)
print(SAVEPATH)

class ModelConfig(BaseModel):
    pretrained_model_name_or_path: Union[str, Path]
    use_auth_token:Optional[str]=os.environ.get('HF_AUTH_TOKEN')
    trust_remote_code:Optional[bool]=True
    config_file_name: Optional[Union[str, Path]] = "generation_config.json"
    cache_dir: Optional[Union[str, Path]] = SAVEPATH
    force_download: Optional[bool] = False
    resume_download: Optional[bool] = False
    proxies: Optional[Dict[str, str]] = None
    token: Optional[Union[str, bool]] = None
    revision: Optional[str] = "main"
    # return_unused_kwargs: Optional[bool] = False  # Remove this line
    subfolder: Optional[str] = ""
    kwargs: Optional[Dict[str, Any]] = None  # If this dict contains 'return_unused_kwargs', ensure it's not duplicated




class ModelArguments(BaseModel):
    input_text: str
    # Length control parameters
    max_length: ClassVar[int] = 20
    max_new_tokens: Optional[int] = None
    min_length: int = 0
    min_new_tokens: Optional[int] = None
    early_stopping: bool = False
    max_time: Optional[float] = None

    # Generation strategy parameters
    do_sample: bool = False
    num_beams: int = 1
    num_beam_groups: int = 1
    penalty_alpha: Optional[float] = None
    use_cache: bool = True

    # Logit manipulation parameters
    temperature: float = 0.7
    top_k: int = 40
    top_p: float = 0.95
    typical_p: float = 1.0
    epsilon_cutoff: float = 0.0
    eta_cutoff: float = 0.0
    diversity_penalty: float = 0.0
    repetition_penalty: float = 1.1
    encoder_repetition_penalty: float = 1.1
    length_penalty: float = 1.0
    no_repeat_ngram_size: int = 0
    bad_words_ids: Optional[List[int]] = None
    force_words_ids: Optional[List[int]] = None
    renormalize_logits: bool = False
    constraints: Optional[str] = None
    forced_bos_token_id: Optional[int] = None
    forced_eos_token_id: Optional[int] = None
    remove_invalid_values: Optional[bool] = None
    exponential_decay_length_penalty: Optional[bool] = None
    suppress_tokens: Optional[List[int]] = None
    begin_suppress_tokens: Optional[List[int]] = None
    forced_decoder_ids: Optional[List[int]] = None
    sequence_bias: Optional[float] = None
    guidance_scale: Optional[float] = None

    # Output variables parameters
    num_return_sequences: int = 1
    output_attentions: bool = False
    output_hidden_states: bool = False
    output_scores: bool = False
    return_dict_in_generate: bool = False

    # Encoder-decoder exclusive parameters
    encoder_no_repeat_ngram_size: int = 0
    decoder_start_token_id: Optional[int] = None

class RoutePayload(BaseModel):
    configure: bool
    inference: bool
    args: dict

def download_from_s3(bucket: str, key: str, local_path: str):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, local_path)

@app.post("/")
async def route(payload: RoutePayload):
    if payload.configure:
        llama_model_args = ModelConfig(**payload.args)
        return await configure(llama_model_args)
    elif payload.inference:
        model_args = ModelArguments(**payload.args)
        return await invoke(model_args)
    else:
        raise HTTPException(status_code=400, detail="Please specify either 'configure' or 'inference'")



@app.get("/ping")
async def ping():
    return Response(status_code=200)


@app.post("/invoke")
async def invoke(model_args: ModelArguments):
    try:
        model_args=model_args.dict()
        input_text=model_args.pop("input_text",None)
        inputs=TOKENIZER.encode(input_text,return_tensors="pt")
        outputs=MODEL.generate(inputs,**model_args)
        finaloutdata={}
        for i, outdata in enumerate(outputs):
            print(f"{i}: {TOKENIZER.decode(outdata)}")
            finaloutdata[i]=TOKENIZER.decode(outdata)
        output=finaloutdata
        output["model_args"]=str(model_args)

    except:
        output={"traceback_err":str(traceback.format_exc()),"model_args":str(model_args)}
    return output

@app.post("/configure")
async def configure(model_config_args: ModelConfig):
    try:
        global TOKENIZER
        global MODEL
        # Filter out any kwargs that are not recognized by `from_pretrained`
        recognized_args = {k: v for k, v in model_config_args.dict().items() if k in ['pretrained_model_name_or_path', 'cache_dir', 'force_download', 'resume_download', 'proxies', 'use_auth_token', 'revision','trust_remote_code']}
        TOKENIZER = AutoTokenizer.from_pretrained(**recognized_args)
        MODEL = AutoModelForCausalLM.from_pretrained(**recognized_args)
        
        return {"status": "success"}
    except:
        return {"traceback_err":str(traceback.format_exc())}

