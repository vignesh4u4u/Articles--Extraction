import json
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nlp = spacy.load("en_core_web_sm")
from transformers import pipeline,set_seed
from utils import extract_data
from agents import generate_response
from gtts import gTTS
import gradio as gr
import os
import asyncio
from googletrans import Translator

set_seed(42)

def eng_to_hindi(text):
    translator = Translator()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    translated_text = loop.run_until_complete(translator.translate(text, src="en", dest="hi"))
    return translated_text.text

def text_to_voice(text,complete_text):
    output_audio = r"assets/output.mp3"
    output_text = r"assets/output.txt"
    hindi_text = eng_to_hindi(text)
    tts = gTTS(text=hindi_text, lang="hi")
    tts.save(output_audio)
    with open(output_text, "w", encoding="utf-8") as f:
        f.write(complete_text)
    return output_audio, output_text

def compare_articles(articles):
    docs = [nlp(article) for article in articles]
    entities_list = [set(doc.ents) for doc in docs]
    keywords_list = [set(chunk.text.lower() for chunk in doc.noun_chunks) for doc in docs]
    topic_overlap = {
        f"Article {i + 1} & Article {j + 1}": {
            "Common Topics": list(keywords_list[i] & keywords_list[j]),
            "Unique to Article {}".format(i + 1): list(keywords_list[i] - keywords_list[j]),
            "Unique to Article {}".format(j + 1): list(keywords_list[j] - keywords_list[i])
        }
        for i in range(len(articles))
        for j in range(i + 1, len(articles))
    }

    vectorizer = TfidfVectorizer().fit_transform(articles)
    similarity_matrix = cosine_similarity(vectorizer)

    similarity_scores = {
        f"Article {i + 1} & Article {j + 1}": similarity_matrix[i][j]
        for i in range(len(articles))
        for j in range(i + 1, len(articles))
    }

    output = {
        "Topic Overlap": topic_overlap,
        "Similarity Scores": similarity_scores
    }

    return output


def sentiment_analysis(input_text):
    model_id = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=model_id,
        tokenizer=model_id,
    )
    data = extract_data(input_text)
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    summary_list = []
    all_articles = []
    for sublist in data:
        for item in sublist:
            summary_text = item['summary']
            summary_list.append(summary_text)
            results = sentiment_pipeline(summary_text)
            sentiment_label = results[0]['label'].upper()
            sentiment_counts[sentiment_label] += 1
            all_articles.append({
                "Title": item['title'],
                "Summary": summary_text,
                "Sentiment": sentiment_label,
                "Topics": item['topics']
            })

    comparison_result1 = compare_articles(summary_list)
    clean_text = ""
    for item in summary_list:
        clean_text += item + " \n"
    response = generate_response(summary_list,
                                 sentiment_counts["POSITIVE"],
                                 sentiment_counts["NEGATIVE"],
                                 clean_text)
    response_dict = json.loads(response)
    coverage_differences = response_dict.get("Coverage Differences", [])
    Topic_Overlap = response_dict.get("Topic Overlap", [])
    Final_Sentiment_Analysis = response_dict.get("Final Sentiment Analysis", [])
    summarizing_report = response_dict.get("Overall_Sentiment_Ssummarizing_Report", [])
    final_output = {
        "Company": input_text,
        "Articles": all_articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": {
                "Positive": sentiment_counts["POSITIVE"],
                "Negative": sentiment_counts["NEGATIVE"],
            }
        },
        "Coverage Differences": coverage_differences,
        "Topic Overlap":Topic_Overlap,
        "Final Sentiment Analysis": Final_Sentiment_Analysis,
        "Overall sentiment summarizing report": summarizing_report
    }

    return final_output


def main(input_text):
    final_answer = sentiment_analysis(input_text)
    clean_text = json.dumps(final_answer, indent=4)
    output_audio, output_text = text_to_voice(final_answer["Overall sentiment summarizing report"],clean_text)
    return output_audio, output_text

interface = gr.Interface(
    fn=main,
    inputs=gr.Textbox(label="Enter the input"),
    outputs=[
        gr.Audio(label="Hindi Audio Output"),
        gr.File(label="complete summarization report")
    ],
    title="News Summarizer",
    description="Enter text in English, and get a pure Hindi speech output along with a downloadable text file."
)

interface.launch()




