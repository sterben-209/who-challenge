import fiftyone as fo
import fiftyone.brain as fob
import numpy as np
from glob import glob
import json
import os
import pandas
from translate import Translator
# dataset = fo.Dataset.from_images_dir('AIC\\\keyframes', name=None, tags=None, recursive=True)

def get_query():
    translator = Translator(from_lang="vi", to_lang="en")
    query = pandas.read_csv("Danh sách truy vấn.csv",dtype_backend="pyarrow",engine='pyarrow')
    for i in query['Description']:
        # print(i)
        print(translator.translate(i))
    # print(translator.translate("tôi là ai"))



if __name__ == "__main__":
    get_query()
# session = fo.launch_app(dataset,port=5151)

# session.wait() 



