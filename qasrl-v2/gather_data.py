import os
import json
from pprint import pprint
import random
from IPython import embed
from collections import defaultdict

def gather_data(ds):
    with open(f'./orig/{ds}.jsonl', 'r') as f:
        dataset = [json.loads(ln) for ln in f]
    return dataset

def data_stats(dataset):
    for i, x in enumerate(dataset):
        for verb in x['verbEntries'].values():
            verb_idxs = verb['verbIndex']
            for question, entry in verb['questionLabels'].items():
                slots = []
                ans = []
                lr = []
                for aj in entry['answerJudgments']:
                    if aj['isValid']:
                        for span in aj['spans']:
                            if tuple(span) not in ans:
                                ans.append(tuple(span))
                                if span[0] < verb_idxs:
                                    lr.append('L')
                                else:
                                    lr.append('R')
                for slot, value in entry['questionSlots'].items():
                    slots.append(value)

            x = '\t'.join(slots + lr)
            print(x)
              
    #embed()
    assert False

def save_data(dataset):
    new_dataset = []

    for i, x in enumerate(dataset):
        sentence = x['sentenceTokens']
        verbs = []
        etc = []
        
        print('NEW SOURCE SENTENCE')
        #print(sentence)
        
        for vkey in x['verbEntries'].keys():
            z = x['verbEntries'][vkey]['questionLabels']
            verbs.append([sentence[int(vkey)]])
            for qkey in z.keys():
                verbs[-1].append([qkey])
                for qa in z[qkey]['answerJudgments']:
                    if qa['isValid']:
                        verbs[-1][-1].append(qa['spans'][0])
                        
        pprint.pprint(verbs)
        print(sentence)
        
        print()
        if i == 3:
            break


def question_stats(fname):
    wh_count = defaultdict(int)
    lr_dict = defaultdict(lambda: defaultdict(int))
    with open(fname) as f:
        for line in f:
            line = line.rstrip().split('\t')
            wh_count[line[0]] += 1
            lr_dict[line[0]][line[-1]] += 1

    print('wh-word\tcount')
    for k, v in wh_count.items():
        print('\t'.join([k, str(v)]))
    print()
    print('wh-word\tleft-right\tpercentage')
    for k, v in lr_dict.items():
        for lr, count in v.items():
            print('\t'.join([k, lr, str(count)]))


if __name__ == '__main__':
    question_stats('./train_dev_questions.csv')
    #for ds in ['train', 'dev']:
    #    dataset = gather_data(ds)
    #    data_stats(dataset)
    #random.shuffle(dataset)
    #save_data(dataset)
