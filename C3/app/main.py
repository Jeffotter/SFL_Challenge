#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 18:43:16 2022

@author: jeffo

"""

import torch
import io
import string
import time
import os
import numpy as np
from PIL import Image
import uvicorn
from fastapi import FastAPI
import requests


model = torch.jit.load('model_scripted.pt')
model.eval()

def prepare_image(img):
    img = Image.open(img)
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    img = np.expand_dims(img, 0)
    img=255-img
    img = torch.tensor(img)
    img=img[None,:]
    img=img.float()
    return img

output_mapping = {
                 0: "T-shirt/Top",
                 1: "Trouser",
                 2: "Pullover",
                 3: "Dress",
                 4: "Coat", 
                 5: "Sandal", 
                 6: "Shirt",
                 7: "Sneaker",
                 8: "Bag",
                 9: "Ankle Boot"
                 }


def predict_result(img,model=model):
    outputs=model(img)
    predicted = torch.max(outputs, 1)[1]
    return predicted


#from util import *
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#nest_asyncio.apply()




import uvicorn
from fastapi import File, UploadFile, FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {'Message':'Hello world'}

@app.post("/scorefile/")
def create_upload_file(file: UploadFile = File(...)):
    
    k=prepare_image((file.file))
    res=predict_result(k)
    result=output_mapping[int(res)]
    return result

#if __name__ == '__main__':
#    uvicorn.run(app, host='0.0.0.0', port=8000)


