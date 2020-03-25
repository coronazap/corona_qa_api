from bert_serving.client import BertClient
import numpy as np
import json
import time

category_to_number = {
    'prevencao' = 0,
    'sintomas' = 1,
    'transmissao' = 2,
    'tratamento' = 3
}

number_to_category = {
    0 = 'prevencao',
    1 = 'sintomas',
    2 = 'transmissao', 
    3 = 'tratamento'
}

context_to_questions = get_context_dict()

category_to_questions = get_category_questions()

def get_similarity(category, question):
    # Ambos virão da request
    # Inicialização de variáveis
    bc = BertClient(port=5555, port_out=5556)
    topk = 3
    query_vec = bc.encode([query])[0]

    # "tópico" e "query" vão chegar pela request

    questions = get_category_questions(category)

    doc_vecs = bc.encode(questions)


    # Caso seja apenas a pergunta #1 (top pergunta)
    #---------------------------------------------------
    if topk == 1:
        score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
        topk_idx = np.argsort(score)[::-1][:topk]
        topQuestion = questions[max(topk_idx)]

        for key in contextDict.keys():
            if topQuestion in contextDict[key]:
                context = key
                return format(context)
    #------------------------------------------------------


    # Caso sejam N top perguntas
    #-------------------------------------------------------
    if topk > 1:
        score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
        topk_idx = np.argsort(score)[::-1][:topk]
        topQuestions = []
        # contexts = set()
        contexts = []

        for idx in topk_idx:
            topQuestions.append(questions[idx])

        for key in contextDict.keys():
            
            for topQuestion in topQuestions:
                
                if topQuestion in contextDict[key]:
                    contexts.append(key)
                                        
        context = max(set(contexts), key=contexts.count)
        return format(context)
                
        # print("Número de contextos únicos encontrados: {}".format(contexts))
        # print("Número de contextos: {}".format(len(contexts)))


def get_categories_questions():
    '''
        Retorna uma lista de perguntas 
    '''

    with open("./covid-train2.json") as file:
        dataset = json.load(file)

    data = dataset["data"][category_to_number[category]]

    results = {}

    for index, item in enumerate(dataset["data"]): 

        pre_list = []
        for item in data:
            pre_list.append(item['qas'])

        questions = []

        for i in range(len(pre_list)):
            for j in range(len(pre_list[i])):
                questions.append(pre_list[i][j]['question'])

        
        result[number_to_category[i]] = questions

    return results


def get_context_dict(): 
    ''' 
        Retorna um dicionário mapeando contextos à uma lista perguntas
    '''

    with open("./covid-train2.json") as train_file:
        dataset = json.load(train_file)

    data = dataset['data'][category_to_number[category]]['paragraphs']

    context_to_questions = {}
    
    for i in range(len(data)):
        context_to_questions[data[i]['context']] = []
        for j in range(len(data[i]['qas'])):
            context_to_questions[data[i]['context']].append(data[i]['qas'][j]['question'])

   return context_to_questions