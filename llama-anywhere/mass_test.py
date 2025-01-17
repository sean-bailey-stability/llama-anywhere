import argparse
import subprocess
import boto3
import random
import traceback
import platform
import boto3
from botocore.exceptions import ClientError



def list_instance_types(numinstances=10, instanceset=None):
    #There doesn't seem to be a quick and easy way to return all the instance types. so I'll just have lists.
    instancedict={
        "gpu_instances" : [
        'g4ad.xlarge',
        'g4ad.2xlarge',
        'g4ad.4xlarge',
        'g4ad.8xlarge',
        'g4ad.16xlarge',
        'g4dn.xlarge',
        'g4dn.2xlarge',
        'g4dn.4xlarge',
        'g4dn.8xlarge',
        'g4dn.12xlarge',
        'g4dn.16xlarge',
        'g4dn.metal',
        'g5.xlarge',
        'g5.2xlarge',
        'g5.4xlarge',
        'g5.8xlarge',
        'g5.16xlarge',
        'g5.48xlarge',
        'inf1.xlarge',
        'inf1.2xlarge',
        'inf1.6xlarge',
        'inf1.24xlarge',
        'p2.xlarge',
        'p2.8xlarge',
        'p2.16xlarge',
        'p3.2xlarge',
        'p3.8xlarge',
        'p3.16xlarge',
        'p3dn.24xlarge',
        'p4d.24xlarge',
        'p4de.24xlarge',
        'p4ov.24xlarge',
        'v100.xlarge',
        'v100.2xlarge',
        'v100.4xlarge',
        'v100.8xlarge'
        ],

        "m_instances" : [
        'm1.small',
        'm1.medium',
        'm1.large',
        'm1.xlarge',
        'm2.xlarge',
        'm2.2xlarge',
        'm2.4xlarge',
        'm3.medium',
        'm3.large',
        'm3.xlarge',
        'm3.2xlarge',
        'm4.large',
        'm4.xlarge',
        'm4.2xlarge',
        'm4.4xlarge',
        'm4.10xlarge',
        'm4.16xlarge',
        'm5.large',
        'm5.xlarge',
        'm5.2xlarge',
        'm5.4xlarge',
        'm5.8xlarge',
        'm5.12xlarge',
        'm5.16xlarge',
        'm5.24xlarge',
        'm5.metal',
        'm5a.large',
        'm5a.xlarge',
        'm5a.2xlarge',
        'm5a.4xlarge',
        'm5a.8xlarge',
        'm5a.12xlarge',
        'm5a.16xlarge',
        'm5a.24xlarge',
        'm5ad.large',
        'm5ad.xlarge',
        'm5ad.2xlarge',
        'm5ad.4xlarge',
        'm5ad.8xlarge',
        'm5ad.12xlarge',
        'm5ad.16xlarge',
        'm5ad.24xlarge',
        'm5d.large',
        'm5d.xlarge',
        'm5d.2xlarge',
        'm5d.4xlarge',
        'm5d.8xlarge',
        'm5d.12xlarge',
        'm5d.16xlarge',
        'm5d.24xlarge',
        'm5d.metal',
        'm5dn.large',
        'm5dn.xlarge',
        'm5dn.2xlarge',
        'm5dn.4xlarge',
        'm5dn.8xlarge',
        'm5dn.12xlarge',
        'm5dn.16xlarge',
        'm5dn.24xlarge',
        'm5n.large',
        'm5n.xlarge',
        'm5n.2xlarge',
        'm5n.4xlarge',
        'm5n.8xlarge',
        'm5n.12xlarge',
        'm5n.16xlarge',
        'm5n.24xlarge',
        'm5zn.large',
        'm5zn.xlarge',
        'm5zn.2xlarge',
        'm5zn.3xlarge',
        'm5zn.6xlarge',
        'm5zn.12xlarge',
        'm6a.large',
        'm6a.xlarge',
        'm6a.2xlarge',
        'm6a.4xlarge',
        'm6a.8xlarge',
        'm6a.12xlarge',
        'm6a.16xlarge',
        'm6a.24xlarge',
        'm6a.32xlarge',
        'm6a.48xlarge',
        'm6a.metal',
        'm6i.large',
        'm6i.xlarge',
        'm6i.2xlarge',
        'm6i.4xlarge',
        'm6i.8xlarge',
        'm6i.12xlarge',
        'm6i.16xlarge',
        'm6i.24xlarge',
        'm6i.32xlarge',
        'm6i.metal'
        ],

        "t_instances" : [
        't1.micro',
        't2.nano',
        't2.micro',
        't2.small',
        't2.medium',
        't2.large',
        't2.xlarge',
        't2.2xlarge',
        't3.nano',
        't3.micro',
        't3.small',
        't3.medium',
        't3.large',
        't3.xlarge',
        't3.2xlarge',
        't3a.nano',
        't3a.micro',
        't3a.small',
        't3a.medium',
        't3a.large',
        't3a.xlarge',
        't3a.2xlarge',
        't4g.nano',
        't4g.micro',
        't4g.small',
        't4g.medium',
        't4g.large',
        't4g.xlarge',
        't4g.2xlarge'
        ],

        "c_instances" : [
        'c1.medium',
        'c1.xlarge',
        'c3.large',
        'c3.xlarge',
        'c3.2xlarge',
        'c3.4xlarge',
        'c3.8xlarge',
        'c4.large',
        'c4.xlarge',
        'c4.2xlarge',
        'c4.4xlarge',
        'c4.8xlarge',
        'c5.large',
        'c5.xlarge',
        'c5.2xlarge',
        'c5.4xlarge',
        'c5.9xlarge',
        'c5.12xlarge',
        'c5.18xlarge',
        'c5.24xlarge',
        'c5.metal',
        'c5a.large',
        'c5a.xlarge',
        'c5a.2xlarge',
        'c5a.4xlarge',
        'c5a.8xlarge',
        'c5a.12xlarge',
        'c5a.16xlarge',
        'c5a.24xlarge',
        'c5ad.large',
        'c5ad.xlarge',
        'c5ad.2xlarge',
        'c5ad.4xlarge',
        'c5ad.8xlarge',
        'c5ad.12xlarge',
        'c5ad.16xlarge',
        'c5ad.24xlarge',
        'c5d.large',
        'c5d.xlarge',
        'c5d.2xlarge',
        'c5d.4xlarge',
        'c5d.9xlarge',
        'c5d.12xlarge',
        'c5d.18xlarge',
        'c5d.24xlarge',
        'c5d.metal',
        'c5n.large',
        'c5n.xlarge',
        'c5n.2xlarge',
        'c5n.4xlarge',
        'c5n.9xlarge',
        'c5n.18xlarge',
        'c6a.large',
        'c6a.xlarge',
        'c6a.2xlarge',
        'c6a.4xlarge',
        'c6a.8xlarge',
        'c6a.12xlarge',
        'c6a.16xlarge',
        'c6a.24xlarge',
        'c6a.32xlarge',
        'c6a.48xlarge',
        'c6a.metal',
        'c6i.large',
        'c6i.xlarge',
        'c6i.2xlarge',
        'c6i.4xlarge',
        'c6i.8xlarge',
        'c6i.12xlarge',
        'c6i.16xlarge',
        'c6i.24xlarge',
        'c6i.32xlarge',
        'c6i.metal'

        ],
        "r_instances" : [
        'r3.large',
        'r3.xlarge',
        'r3.2xlarge',
        'r3.4xlarge',
        'r3.8xlarge',
        'r4.large',
        'r4.xlarge',
        'r4.2xlarge',
        'r4.4xlarge',
        'r4.8xlarge',
        'r4.16xlarge',
        'r5.large',
        'r5.xlarge',
        'r5.2xlarge',
        'r5.4xlarge',
        'r5.8xlarge',
        'r5.12xlarge',
        'r5.16xlarge',
        'r5.24xlarge',
        'r5.metal',
        'r5a.large',
        'r5a.xlarge',
        'r5a.2xlarge',
        'r5a.4xlarge',
        'r5a.8xlarge',
        'r5a.12xlarge',
        'r5a.16xlarge',
        'r5a.24xlarge',
        'r5ad.large',
        'r5ad.xlarge',
        'r5ad.2xlarge',
        'r5ad.4xlarge',
        'r5ad.8xlarge',
        'r5ad.12xlarge',
        'r5ad.16xlarge',
        'r5ad.24xlarge',
        'r5d.large',
        'r5d.xlarge',
        'r5d.2xlarge',
        'r5d.4xlarge',
        'r5d.8xlarge',
        'r5d.12xlarge',
        'r5d.16xlarge',
        'r5d.24xlarge',
        'r5d.metal',
        'r5dn.large',
        'r5dn.xlarge',
        'r5dn.2xlarge',
        'r5dn.4xlarge',
        'r5dn.8xlarge',
        'r5dn.12xlarge',
        'r5dn.16xlarge',
        'r5dn.24xlarge',
        'r5n.large',
        'r5n.xlarge',
        'r5n.2xlarge',
        'r5n.4xlarge',
        'r5n.8xlarge',
        'r5n.12xlarge',
        'r5n.16xlarge',
        'r5n.24xlarge',
        'r6a.large',
        'r6a.xlarge',
        'r6a.2xlarge',
        'r6a.4xlarge',
        'r6a.8xlarge',
        'r6a.12xlarge',
        'r6a.16xlarge',
        'r6a.24xlarge',
        'r6a.32xlarge',
        'r6a.48xlarge',
        'r6a.metal',
        'r6i.large',
        'r6i.xlarge',
        'r6i.2xlarge',
        'r6i.4xlarge',
        'r6i.8xlarge',
        'r6i.12xlarge',
        'r6i.16xlarge',
        'r6i.24xlarge',
        'r6i.32xlarge',
        'r6i.metal'

        ]
        }
    
    returninstances=[]
    selectedlist=[]
    if instanceset == None:
        instanceset = random.choice(list(instancedict.keys()))
    if instanceset is "all":
        for key in instancedict.keys():
            for item in instancedict[key]:
                selectedlist.append(item)
    else:
        selectedlist=instancedict[instanceset]
    random.shuffle(selectedlist)
    for i in range(min(numinstances,len(selectedlist))):
        returninstances.append(selectedlist.pop())
    
    return returninstances

def is_windows():
    return platform.system().lower() == 'windows'

def run_powershell_script(deploytype, port, model, instance_type,hftoken):
    command = ["powershell.exe", ".\\end2endtest.ps1", 
               "-deploytype", deploytype, 
               "-port", str(port), 
               "-model", model, 
               "-instancetype", instance_type,
               '-huggingface_token',hftoken]
    subprocess.check_call(command)



def delete_buckets_with_prefix(prefix):
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']

    for bucket in buckets:
        bucket_name = bucket['Name']
        if bucket_name.startswith(prefix):
            try:
                # Delete all objects in the bucket first
                bucket_resource = boto3.resource('s3').Bucket(bucket_name)
                bucket_resource.objects.all().delete()

                # Delete the bucket
                s3.delete_bucket(Bucket=bucket_name)
                print(f"Deleted bucket: {bucket_name}")
            except ClientError as e:
                print(f"Error deleting bucket {bucket_name}: {e}")



def run_shell_script(deploytype, port, model, instance_type,hftoken,regionvalue):
    command = ["bash", "end2endtest.sh", 
               "-d", deploytype, 
               "-p", str(port), 
               "-m", model, 
               "-i", instance_type,
               '-h',hftoken,
               '-r',regionvalue]
    subprocess.check_call(command)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--foundationmodel",required=False, type=str,default="VMware/open-llama-7b-v2-open-instruct", help="Huggingface transformer compatible repository path (VMware/open-llama-7b-v2-open-instruct)")
    parser.add_argument("--quantizedmodel", required=False, type=str,default="https://huggingface.co/TheBloke/open-llama-7B-v2-open-instruct-GGML/resolve/main/open-llama-7b-v2-open-instruct.ggmlv3.q2_K.bin",help="URL or path to the quantized model (https://huggingface.co/TheBloke/open-llama-7B-v2-open-instruct-GGML/resolve/main/open-llama-7b-v2-open-instruct.ggmlv3.q2_K.bin)")
    parser.add_argument("--instancetype",type=str,default=None,required=False, help="Specify the instance you'd like to test against. Provide a comma delineated list if multiple instances selected." )
    parser.add_argument("--instanceclass",type=str,default=None,required=False, help="Specify the instance class to select from. Selects random at default. Choose from 'gpu_instances','m_instances','t_instances','r_instances','c_instances','all', " )
    parser.add_argument("--instancecount",type=int,default=10,required=False, help="Specify the number of instances you want to pull from the instance class. Default 10" )
    parser.add_argument("--hftoken",type=str,default="",required=False,help="Token for huggingface in order to download private models.")
    parser.add_argument("--region",type=str,default="us-east-1",required=False,help="The region to run this operation in.")

    args = parser.parse_args()
    port = 8080
    if args.instancetype is None:
        instance_types = list_instance_types(args.instancecount,args.instanceclass) 
    else:
        instance_types=args.instancetype.split(",")
        #instance_types=[args.instancetype]

    for instance_type in instance_types:
        try:
            # Run shell script for foundation model and for the quantized model

            if is_windows():
                run_powershell_script('f', port, args.foundationmodel, instance_type,args.hftoken)
                run_powershell_script('q', port, args.quantizedmodel, instance_type,args.hftoken)
            else:
                run_shell_script('f', port, args.foundationmodel, instance_type,args.hftoken,regionvalue=args.region)
                run_shell_script('q', port, args.quantizedmodel, instance_type,args.hftoken,regionvalue=args.region)
        except:
            print(traceback.format_exc())
        delete_buckets_with_prefix('llama-anywhere-bucket')



if __name__ == '__main__':
    main()
