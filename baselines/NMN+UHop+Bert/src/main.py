import argparse
import os
import numpy as np
#from UHop import UHop
#from Baseline import Baseline
from Framework import Framework
from data_utilities import load_bert_from_tf, load_lan_vocab, PerQuestionDatasetMLPQ
import utility
import json
import torch

torch.manual_seed(1126)

parser = argparse.ArgumentParser()
parser.add_argument('--model', action='store', type=str, default=None) # HR-BiLSTM, ABWIM, MVM
parser.add_argument('--framework', action='store', type=str, default='UHop') # UHop, baseline

train_parser = parser.add_mutually_exclusive_group(required=True)   # train + test | test only
train_parser.add_argument('--train', action='store_true')
train_parser.add_argument('--test', action='store_true')

parser.add_argument('--emb_size', action='store', type=int)
parser.add_argument('--path', action='store', type=str, default=None) # for test mode, specify model path
parser.add_argument('--epoch_num', action='store', type=int, default=1000)
parser.add_argument('--hidden_size', action='store', type=int, default=256)
parser.add_argument('--num_filters', action='store', type=int, default=150)
parser.add_argument('--neg_sample', action='store', type=int, default=2048)
parser.add_argument('--dropout_rate', action='store', type=float, default=0.0)
parser.add_argument('--learning_rate', action='store', type=float, default=0.001)
parser.add_argument('--learning_rate_bert', action='store', type=float, default=0.00001)
parser.add_argument('--optimizer', action='store', type=str, default='adam')
parser.add_argument('--l2_norm', action='store', type=float, default=0.0)
parser.add_argument('--earlystop_tolerance', action='store', type=int, default=10)
parser.add_argument('--margin', action='store', type=float, default=0.5)
parser.add_argument('--train_step_1_only', action='store', type=bool, default=False)
parser.add_argument('--train_rela_choose_only', action='store', type=bool, default=False)
parser.add_argument('--show_result', action='store', type=bool, default=False)
parser.add_argument('--train_embedding', action='store', type=bool, default=False)
parser.add_argument('--log_result', action='store', type=bool, default=False)
parser.add_argument('--dataset', action='store', type=str) #sq, wq, wq_train1_test2
parser.add_argument('--saved_dir', action='store', type=str, default='saved_model')
parser.add_argument('--hop_weight', action='store', type=float, default=1)
parser.add_argument('--task_weight', action='store', type=float, default=1)
parser.add_argument('--acc_weight', action='store', type=float, default=1)
parser.add_argument('--stop_when_err', action='store_true')
parser.add_argument('--step_every_step', action='store_true')
parser.add_argument('--dynamic', action='store', type=str, default='flatten')
parser.add_argument('--only_one_hop', action='store_true')
parser.add_argument('--reduce_method', action='store', type=str, default='dense')
parser.add_argument('--pretrained_bert', action='store', type=str, default='bert-base-multilingual-cased')
parser.add_argument('--PerQuestionDataset', action='store', type=str, default='lstm')
parser.add_argument('--q_representation', action='store', type=str, default='bert')
parser.add_argument('--use_nmn', action='store', type=bool, default=False)

args = parser.parse_args()
print(f'args: {args}')

import_model_str = 'from model.{} import Model as Model'.format(args.model)
exec(import_model_str)
if args.train == True:
    args.path = utility.find_save_dir(args.saved_dir, args.model) if args.path == None else args.path
    with open(os.path.join(args.path, 'args.txt'), 'w') as f:
        json.dump(vars(args), f, indent=4, ensure_ascii=False)

#baseline_path, UHop_path = path_finder.path_finder()
#wpq_path = path_finder.WPQ_PATH()

args.Model = Model
if args.framework == 'baseline':
    if args.dataset.lower() == 'wq':
        with open('../data/baseline/KBQA_RE_data/webqsp_relations/rela2id.json', 'r') as f:
            rela2id = json.load(f)
        with open('../data/WQ/main_exp/rela2id.json', 'r') as f:
            rela_token2id =json.load(f)
    elif args.dataset.lower() == 'sq':
        with open('../data/baseline/KBQA_RE_data/sq_relations/rela2id.json', 'r') as f:
            rela2id = json.load(f)
        with open('../data/SQ/rela2id.json', 'r') as f:
            rela_token2id =json.load(f)
    elif args.dataset.lower() == 'exp4':
        with open('../data/PQ/exp4/rela2id.json', 'r') as f:
            rela_token2id = json.load(f)
        with open('../data/PQ/exp4/concat_rela2id.json', 'r') as f:
            rela2id = json.load(f)
    elif 'pq' in args.dataset.lower():
        with open(f'../data/PQ/baseline/{args.dataset.upper()}/concat_rela2id.json', 'r') as f:
            rela2id = json.load(f)
        with open(f'../data/PQ/baseline/{args.dataset.upper()}/rela2id.json', 'r') as f:
            rela_token2id =json.load(f)
    else:
        raise ValueError('Unknown dataset')
elif args.framework == 'UHop':
    if args.dataset == 'wq' or args.dataset == 'WQ':
        with open('../data/WQ/main_exp/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset == 'sq' or args.dataset == 'SQ':
        with open('../data/SQ/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'wq_train1test2':
        with open('../data/WQ/train1test2_exp/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'exp4':
        with open('../data/PQ/exp4/rela2id.json', 'r') as f:
            rela2id = json.load(f)
    elif 'wpq' in args.dataset.lower():
        with open('../data/PQ/exp3/UHop/rela2id.json', 'r') as f:
            rela2id = json.load(f)
    elif args.dataset.lower() == 'pq':
        with open('../data/PQ/PQ/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pq1':
        with open('../data/PQ/PQ1/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pq2':
        with open('../data/PQ/PQ2/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pq3':
        with open('../data/PQ/PQ3/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pql':
        with open('../data/PQ/PQL/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pql1':
        with open('../data/PQ/PQL1/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pql2':
        with open('../data/PQ/PQL2/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    elif args.dataset.lower() == 'pql3':
        with open('../data/PQ/PQL3/rela2id.json', 'r') as f:
            rela2id =json.load(f)
    # NEW DATASETS
    elif 'mlpq-en-fr' in args.dataset.lower():
        if "nmn" not in args.dataset.lower():
            with open('../data/MLPQ/en-fr/total/rela2id.json', 'r') as f:
                rela2id =json.load(f)
        else:
            with open('../data/MLPQ/en-fr/total_NMN/rela2id.json', 'r') as f:
                rela2id =json.load(f)
    elif 'mlpq-en-zh' in args.dataset.lower():
        if "nmn" not in args.dataset.lower():
            with open('../data/MLPQ/en-zh/total/rela2id.json', 'r') as f:
                rela2id =json.load(f)
        else:
            with open('../data/MLPQ/en-zh/total_NMN/rela2id.json', 'r') as f:
                rela2id =json.load(f)
    elif 'mlpq-zh-fr' in args.dataset.lower():
        if "nmn" not in args.dataset.lower():
            with open('../data/MLPQ/zh-fr/total/rela2id.json', 'r') as f:
                rela2id =json.load(f)
        else:
            with open('../data/MLPQ/zh-fr/total_NMN/rela2id.json', 'r') as f:
                rela2id =json.load(f)
    else:
        raise ValueError('Unknown dataset.')

#print(rela2id)
#print(rela2id['scientist'])
#exit()
word2id_path = '../data/glove.300d.word2id.json' if args.emb_size == 300 else '../data/glove.50d.word2id.json' 
word_emb_path = '../data/glove.300d.word_emb.npy' if args.emb_size == 300 else '../data/glove.50d.word_emb.npy'
with open(word2id_path, 'r') as f:
    word2id = json.load(f)
word_emb = np.load(word_emb_path)
args.word_embedding = word_emb
if args.framework == 'UHop': 
    args.rela_vocab_size = len(rela2id)
if args.framework == 'baseline':
    args.rela_vocab_size = len(rela_token2id)

# Should introduce UHop here!

bert_model, bert_tokenizer, bert_config = load_bert_from_tf(args.pretrained_bert)

fr_to_en_vocab = load_lan_vocab("../data/MLPQ/vocab/rel_words_fr", "../data/MLPQ/vocab/rel_words_fr_to_en")
zh_to_en_vocab = load_lan_vocab("../data/MLPQ/vocab/rel_words_zh", "../data/MLPQ/vocab/rel_words_zh_to_en")
mapping_vocab = fr_to_en_vocab.copy()
mapping_vocab.update(zh_to_en_vocab)

if args.framework == 'UHop':
    uhop = Framework(args, word2id, rela2id, mapping_vocab, bert_tokenizer)
    if args.train == True:
        model = Model(args, bert_model, bert_config).cuda()
        model = uhop.train(model)
        print("-----------------------------------------------------------------------------------------------------")
        loss, acc, scores, labels = uhop.evaluate(model=None, bert_model=bert_model, bert_config=bert_config,
                                                  mode='test', dataset=None, output_result=True)
        print()
        lans = ["en", "fr", "zh"]
        hops = ["2h", "3h"]
        nmn = ""
        if args.use_nmn:
            nmn = "nmn"
        for lan in lans:
            for hop in hops:
                uhop.args.dataset = args.dataset.split("_")[0] + "_" + nmn + "_" + lan + "-" + hop
                print("-----------------------------------------------------------------------------------------------------")
                loss, acc, scores, labels = uhop.evaluate(model=None, bert_model=bert_model, bert_config=bert_config,
                                                          mode='test', dataset=None, output_result=True)
                print()

    if args.test == True:
        loss, acc, scores, labels = uhop.evaluate(model=None, bert_model=bert_model, bert_config=bert_config,
                                                  mode='test', dataset=None, output_result=True)

elif args.framework == 'baseline':
    baseline = Framework(args, word2id, rela_token2id)
    model = Model(args).cuda()
    if args.train == True:
        model = baseline.train(model)
        baseline.evaluate(model=None, mode='test', dataset=None, output_result=True)
    if args.test == True:
        baseline.evaluate(model=None, mode='test', dataset=None)
