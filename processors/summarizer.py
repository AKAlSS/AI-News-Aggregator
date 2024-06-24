from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_texts(items):
    summarized_items = []
    for item in items:
        if 'summary' in item and item['summary']:
            text_to_summarize = item['summary']
        elif 'text' in item:
            text_to_summarize = item['text']
        else:
            text_to_summarize = item['title']

        summary = summarizer(text_to_summarize, max_length=60, min_length=30, do_sample=False)
        
        summarized_items.append({
            'title': item['title'],
            'summary': summary[0]['summary_text'],
            'link': item['link'],
            'source': item['source']
        })
    
    return summarized_items