# -*- coding: utf-8 -*-
from .parser import Parser
from .summarizer import Summarizer

__version__ = '0.0.7'

def summarize(title, text, count=3, summarizer=None):
    if not summarizer:
        summarizer = Summarizer()

    result = summarizer.get_summary(text, title)
    result = summarizer.sort_sentences(result[:count])
    result = [res['sentence'] for res in result]

    return result

