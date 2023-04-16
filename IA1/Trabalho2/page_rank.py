# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 22:48:19 2023

@author: sergi
"""

import numpy as np

def pagerank(texts, word):
    n = len(texts)
    M = np.zeros((n, n))
    for i in range(n):
        total_words = len(texts[i].split())
        word_count = texts[i].count(word)
        M[i, :] = word_count / total_words
        M[i, :] /= M[i, :].sum()  # normalize row i
    v = np.full(n, 1/n)
    d = 0.85
    epsilon = 0.0001
    while True:
        v_new = d * np.matmul(M, v) + (1-d)/n
        if np.abs(v_new - v).sum() < epsilon:
            break
        v = v_new
    print(v)
    return np.argsort(v)[::-1]

texts = ["This text the first text.", "This is the second text.", "The third text is different.", 
         "This is a text about programming.", "The fifth text is quite short.", 
         "The sixth text is longer than the fifth.", "The seventh text is the longest.",
         "This is a text about text.", "Text text text text text text text."]
word = "text"
ranking = pagerank(texts, word)
print(ranking)