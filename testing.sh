  647  python3 mass_test.py --foundationmodel "stabilityai/stablelm-2-zephyr-1_6b" --quantizedmodel "https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf" --hftoken "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" --instancetype "m7g.medium,m7g.large,m7g.xlarge,m7g.2xlarge,m7g.4xlarge,g5g.xlarge,g5g.2xlarge,g5g.4xlarge,g5g.8xlarge,m7g.8xlarge,c7g.medium,c7g.large,c7g.xlarge,c7g.2xlarge,c7g.4xlarge,c7g.8xlarge,g5.xlarge,g5.2xlarge,g5.4xlarge,g5.8xlarge,g5.16xlarge,m7a.medium,m7a.large,m7a.xlarge,m7a.2xlarge,m7a.4xlarge,m7a.8xlarge,m7i.large,m7i.xlarge,m7i.2xlarge,m7i.4xlarge,m7i.8xlarge,g4dn.xlarge,g4dn.2xlarge,g4dn.4xlarge,g4dn.4xlarge,g4dn.8xlarge,r8g.2xlarge,r8g.4xlarge,r8g.8xlarge" --region "us-west-2"
  648  aws sso login
  649  aws sso login
  650  aws configure sso
  651  aws configure sso
  652  aws configure sso
  653  export AWSAdministratorAccess-740929234339
  654  export AWS_PROFILE=AWSAdministratorAccess-740929234339
  655  cdk deploy --require-approval never -c deployType="f" -c portval="8080" -c instanceType="g4dn.4xlarge" -c model="stabilityai/stablelm-2-zephyr-1_6b" -c hftoken="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" -c region="us-west-2"
  656  ls
  657  cd llama-anywhere
  658  ls
  659  cdk deploy --require-approval never -c deployType="f" -c portval="8080" -c instanceType="g4dn.4xlarge" -c model="stabilityai/stablelm-2-zephyr-1_6b" -c hftoken="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" -c region="us-west-2"
  660  cdk destroy --force -c region="us-west-2"
  661  cdk deploy --require-approval never -c deployType="f" -c portval="8080" -c instanceType="g4dn.4xlarge" -c model="stabilityai/stablelm-2-zephyr-1_6b" -c hftoken="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" -c region="us-west-2"
  662  cdk destroy --force -c region="us-west-2"