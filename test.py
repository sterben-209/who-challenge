
import pandas
from translate import Translator
import os 


def get_query():
    translator = Translator(from_lang="vi", to_lang="en") #setup translate 
    query = pandas.read_csv("Danh sách truy vấn.csv",dtype_backend="pyarrow",engine='pyarrow') # use pyarrow to read csv faster 
    for i in query['Description']:
        print(translator.translate(i))


def delete_similar() :
    
if __name__ == "__main__":
    get_query()




