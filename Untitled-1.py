import fiftyone as fo
import fiftyone.brain as fob
import numpy as np
from glob import glob
import json
import os
dataset = fo.Dataset.from_images_dir('D:\\AIC\\\keyframes', name=None, tags=None, recursive=True)


session = fo.launch_app(dataset,port=5151)

session.wait() 



