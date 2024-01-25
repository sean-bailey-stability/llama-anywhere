#!/bin/bash

deploytype="q"
port="8080"
instancetype="t4g.xlarge"
model="https://huggingface.co/TheBloke/Llama-2-7B-GGML/resolve/main/llama-2-7b.ggmlv3.q2_K.bin"
huggingface_token=""
region="us-east-1"
while getopts ":d:p:i:m:h:r:" opt; do
  case $opt in
    d)
      deploytype=$OPTARG
      ;;
    p)
      port=$OPTARG
      ;;
    i)
      instancetype=$OPTARG
      ;;
    m)
      model=$OPTARG
      ;;
    h)
      huggingface_token=$OPTARG
      ;;
    r)
      region=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
echo $model
echo $port
echo $instancetype
echo $deploytype
echo $region

function cleanup {
    cdk destroy --force -c region=$region
    deactivate
    rm -rf tempvenv
}

trap cleanup EXIT
python3 -m venv tempvenv
source tempvenv/bin/activate 
pip3 install -r requirements.txt
# use variables in context 
cdk deploy --require-approval never -c deployType=$deploytype -c portval=$port -c instanceType=$instancetype -c model=$model -c hftoken=$huggingface_token -c region=$region

python3 final_file_upload.py --region $region
