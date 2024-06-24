# -*- coding: utf-8 -*-
import os
import json
from collections import defaultdict

from nltk.tokenize import punkt

from .sentence_tokenizer import SentenceTokenizer

class Parser(object):
    def __init__(self, ideal=20.0, stop_words=None, tokenizer=None):
        self.ideal = 20.0
        if not stop_words:
            stop_words = self._get_stop_words()
        self.stop_words = stop_words

        if not tokenizer:
            fname = os.path.dirname(os.path.abspath(__file__)) + '/trainer/english.json'
            with open(fname, 'r') as fp:
                data = json.load(fp)

            self.training = self.load_training(
                set(data['AbbrevTypes']),
                set(data['Collocations']),
                set(data['SentStarters']),
                defaultdict(int, data['OrthoContext'])
            )

            tokenizer = SentenceTokenizer()
            tokenizer._params = self.training

        self.tokenizer = tokenizer

    def load_training(self, abbrev_types, collocations, sent_starters, ortho_context):
        """ Manually supply training data instead of using nltk's default pickle.
        This will allow us to extend PunktSentenceTokenizer to fix its warts or
        add data to our training data. """
        training = punkt.PunktParameters()
        training.abbrev_types = abbrev_types
        training.collocations = collocations
        training.sent_starters = sent_starters
        training.ortho_context = ortho_context
        return training

    def _get_stop_words(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/trainer/stop_words.txt') as file:
            words = file.readlines()

        return [word.replace('\n', '') for word in words]

    def get_keywords(self, text):
        text = self.remove_punctations(text)
        words = self.words(text)
        words = self.remove_stop_words(words)
        unique_words = list(set(words))

        keywords = [{'word': word, 'count': words.count(word)} for word in unique_words]
        keywords = sorted(keywords, key=lambda x: -x['count'])

        return (keywords, len(words))

    def get_sentence_length_score(self, sentence):
        return (self.ideal - abs(self.ideal - len(sentence))) / self.ideal

    # Jagadeesh, J., Pingali, P., & Varma, V. (2005). Sentence Extraction Based Single Document Summarization. International Institute of Information Technology, Hyderabad, India, 5.
    def get_sentence_position_score(self, i, sentence_count):
        normalized = i / (sentence_count * 1.0)

        if normalized > 0 and normalized <= 0.1:
            return 0.17
        elif normalized > 0.1 and normalized <= 0.2:
            return 0.23
        elif normalized > 0.2 and normalized <= 0.3:
            return 0.14
        elif normalized > 0.3 and normalized <= 0.4:
            return 0.08
        elif normalized > 0.4 and normalized <= 0.5:
            return 0.05
        elif normalized > 0.5 and normalized <= 0.6:
            return 0.04
        elif normalized > 0.6 and normalized <= 0.7:
            return 0.06
        elif normalized > 0.7 and normalized <= 0.8:
            return 0.04
        elif normalized > 0.8 and normalized <= 0.9:
            return 0.04
        elif normalized > 0.9 and normalized <= 1.0:
            return 0.15
        else:
            return 0

    def get_title_score(self, title, sentence):
        title_words = self.remove_stop_words(title)
        sentence_words = self.remove_stop_words(sentence)
        matched_words = [word for word in sentence_words if word in title_words]
        return len(matched_words) / (len(title) * 1.0)

    def sentences(self, text):
        return self.tokenizer.tokenize(text)

    def tokens(self, text):
        """ Get a list of annotated tokens instead of a list of sentences """
        tokens = self.tokenizer._tokenize_words(text)
        annotated_tokens = self.tokenizer._annotate_tokens(tokens)
        return annotated_tokens

    def words(self, sentence):
        return sentence.lower().split()

    def remove_punctations(self, text):
        return ''.join(t for t in text if t.isalnum() or t == ' ')

    def remove_stop_words(self, words):
        return [word for word in words if word not in self.stop_words]

