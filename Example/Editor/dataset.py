from string import punctuation
import numpy as np
import torch
import pickle 
import os
class Dataset:
    def __init__(self,text_path,seq_size):
        self.text_path = text_path
        self.georgian_alphabet = 'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
        self.init_dataset()
        self.seq_size = seq_size
        
    def remove_punct(self,line):
        for punct in punctuation:
            line = line.replace(punct, '')
        return line
    def init_dataset(self):
        with open(self.text_path,'r',encoding='utf-8') as f:
            word_set = {}
            for line in f.readlines():
                line = self.remove_punct(line)
                words = line.split()
                for word in words:
                    should = True
                    for ch in word:
                        if ch not in self.georgian_alphabet:
                            should = False
                            break
                    if should:
                        if word in word_set:
                            word_set[word] += 1
                        else:
                            word_set[word] = 1
            word_set = list(sorted(word_set.items(), key=lambda x: x[1], reverse=True))
            self.word_set = list(map(lambda x: x[0], word_set[:499]))
            self.word_set.append("unk")
    
    def get_one_hot_vector(self,word):
        vector = [0] * len(self.word_set)
        is_unk = True
        for i in range(len(self.word_set)):
            if word == self.word_set[i]:
                is_unk = False
                vector[i] = 1
        if is_unk:
            vector[-1] = 1
        return vector
    
    def get_words_from_prediction(self,prediction,number):
        top_values = np.argsort(prediction)[::-1][:number]
        top_words = []
        for i in top_values:
            top_words.append(self.word_set[i])
        return top_words
    def prepare_words(self,words):
        words = [self.remove_punct(word) for word in words]
        tokens = [self.get_one_hot_vector(token) for token in words]
        vector = []
        for token in tokens:
            vector.extend(token)
        vector = torch.tensor(vector, dtype=torch.float32)
        return vector
    
    def save_words_in_pickle(self,words,input_path,output_path):
        input_vector = None
        output_vector = None
        for i in range(len(words)//(self.seq_size+1)):
            curr_input = []
            curr_output = []
            for j in range(self.seq_size):
                curr_input.append(words[i*(self.seq_size+1)+j])
            curr_output.append(words[i*(self.seq_size+1)+self.seq_size])
            curr_input = self.prepare_words(curr_input)
            curr_output = self.prepare_words(curr_output)
            if input_vector is None:
                input_vector = curr_input
                output_vector = curr_output
            else:
                if i == 1:
                    input_vector = torch.cat((input_vector,curr_input)).reshape(2,input_vector.shape[0])
                    output_vector = torch.cat((output_vector,curr_output)).reshape(2,output_vector.shape[0])
                else:
                    input_vector = torch.cat((input_vector.reshape(input_vector.shape[0]*input_vector.shape[1]),curr_input)).reshape(input_vector.shape[0]+1,input_vector.shape[1])
                    output_vector = torch.cat((output_vector.reshape(output_vector.shape[0]*output_vector.shape[1]),curr_output)).reshape(output_vector.shape[0]+1,output_vector.shape[1])
        
        if os.path.exists(input_path):
            prev_input = pickle.load(open(input_path,'rb'))
            prev_output = pickle.load(open(output_path,'rb'))
            input_vector = torch.cat((prev_input.reshape(prev_input.shape[0]*prev_input.shape[1]),input_vector.reshape(input_vector.shape[0]*input_vector.shape[1]))).reshape(input_vector.shape[0]+prev_input.shape[0],input_vector.shape[1])
            output_vector = torch.cat((prev_output.reshape(prev_output.shape[0]*prev_output.shape[1]),output_vector.reshape(output_vector.shape[0]*output_vector.shape[1]))).reshape(output_vector.shape[0]+prev_output.shape[0],output_vector.shape[1])
        pickle.dump(input_vector,open(input_path,'wb'))
        pickle.dump(output_vector,open(output_path,'wb'))
        

    
        
