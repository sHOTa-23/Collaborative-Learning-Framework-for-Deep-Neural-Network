from string import punctuation
import numpy as np
class Dataset:
    def __init__(self,text_path):
        self.text_path = text_path
        self.georgian_alphabet = 'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
        self.init_dataset()
        
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
    
        
