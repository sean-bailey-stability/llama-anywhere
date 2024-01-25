#!/usr/bin/env python3

import aws_cdk as cdk

from llama_anywhere.llama_anywhere_stack import LlamaAnywhereStack


app = cdk.App()
# Retrieve the region from the context variables
region = app.node.try_get_context('region')
if region is None:
    raise ValueError("Region must be provided via context variables")

LlamaAnywhereStack(app, "llama-anywhere",env={'region': region})

app.synth()
