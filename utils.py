import os
import pickle
from corus import load_lenta
from functools import partial
from pymystem3 import Mystem
from multiprocessing import Manager
from tqdm.contrib.concurrent import process_map



def get():
    return len(os.listdir('data'))


def parce(shered_list, sentence):
    m=Mystem()
    analis=m.analyze(sentence)
    new_sent=[]
    for aa in analis:
        if 'analysis' in aa and aa['analysis']:
            gr=aa['analysis'][0]['gr']
            if gr:
                part=gr.split('=')[0].split(',')[0]
                if part in('A','S','V'):
                    new_sent.append(aa['analysis'][0]['lex'])  
    shered_list.append(new_sent)
    return shered_list          

path='lenta-ru-news.csv.gz'
records=load_lenta(path)


if __name__=='__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    manager=Manager()
    
    max_count=get()
    i=0
    while True:
        sentences=[]
        for _ in range(10):
            record=next(records)
            if i <= max_count:
                i+=1
                continue
            sentences += [sentence.strip() for sentence in record.text.replace('\xa0',' ').split('.')]
        if i <= max_count:
            i+=1
            continue
        shared_list=manager.list()
        r=process_map(partial(parce,shared_list), sentences,max_workers=8,chunksize=1)
        print(r)
        with open(f'data/chunck_{i}.pickle','wb') as f:
            pickle.dump(list(shared_list),f)
        i+=1


















