#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 20:31:47 2022

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


model = torch.jit.load('data/model_scripted.pt')
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