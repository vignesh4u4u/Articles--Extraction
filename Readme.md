# News Summarization and Text-to-Speech Application

A web-based application that extracts news articles for a given company, performs sentiment analysis, conducts comparative analysis, and generates a Hindi text-to-speech (TTS) output. Built with Python, Gradio, and deployed on Hugging Face Spaces.

## Objective
This project develops a tool to:
- Extract key details from 10+ news articles about a specified company.
- Analyze sentiment (positive, negative, neutral) for each article.
- Compare sentiment across articles for deeper insights.
- Summarize findings and convert them into Hindi audio output.

## Features
- **News Extraction**: Scrapes article titles, summaries, and metadata using BeautifulSoup.
- **Sentiment Analysis**: Classifies article sentiment using a pre-trained NLP model.
- **Comparative Analysis**: Highlights differences in news coverage across articles.
- **Text-to-Speech**: Generates playable Hindi audio summarizing the sentiment report.
- **Web Interface**: Simple UI built with Gradio for user interaction.
- **API Integration**: Backend-frontend communication via custom APIs.
- **Deployment**: Hosted on Hugging Face Spaces.

## Project Structure
```
news-summarization-tts/
├── app.py              # Main Gradio application script
├── api.py             # API definitions for backend communication
├── utils.py           # Utility functions (scraping, sentiment, TTS)
├── requirements.txt   # Dependencies list
├── README.md          # Project documentation
└── assets/            # Optional: Store generated audio files or images
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (e.g., `venv` or `conda`)

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/news-summarization-tts.git
   cd news-summarization-tts
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application Locally**
   ```bash
   python app.py
   ```

5. Open your browser and go to the URL provided by Gradio (e.g., `http://127.0.0.1:7860`) to access the app.

## Usage
1. Launch the application (locally or via Hugging Face Spaces).
2. Enter a company name (e.g., "Tesla") in the text input field.
3. Click "Submit" to fetch news articles and generate the report.
4. View the structured report:
   - Article titles, summaries, sentiments, and topics displayed as text.
   - Comparative sentiment analysis as text output.
   - Playable Hindi TTS audio file summarizing the findings.

## Deployment
The application is deployed on Hugging Face Spaces, which natively supports Gradio. Access it here:  
[**Live Demo Link**](#) *(Replace with your actual Hugging Face Spaces URL once deployed)*

## Dependencies
Listed in 
```
newspaper3k
lxml_html_clean
googlesearch-python
duckduckgo-search
tensorflow
nltk
scikit-learn
googletrans
gradio
groq
spacy
python-dotenv
textblob
gtts
cohere
protobuf==4.25.3
transformers==4.38.2

```

## Model Details
- **Sentiment Analysis**: Uses `cardiffnlp/twitter-roberta-base-sentiment-latest` for classifying sentiment.
- **Text-to-Speech**: Implements `gTTS` (Google Text-to-Speech) with Hindi language support (`lang='hi'`).

## Assumptions & Limitations
- **Assumptions**:
  - News articles are available via non-JS websites scrapable with BeautifulSoup.
  - Internet connection is required for fetching articles and TTS generation.
- **Limitations**:
  - Limited to 10 articles due to scraping constraints.
  - Sentiment analysis accuracy depends on the pre-trained model’s training data.
  - Hindi TTS output quality relies on the `gTTS` library.

## Evaluation Notes
- **Correctness**: Extracts and processes data accurately from supported websites.
- **Efficiency**: Optimized with caching (if implemented) for repeated queries.
- **Robustness**: Handles invalid inputs and scraping errors gracefully.
- **Code Quality**: Follows PEP8 guidelines, with comments and modular design.

## Submission
- **GitHub Repository**: [https://github.com/your-username/news-summarization-tts](#) *(Replace with your repo link)*
- **Hugging Face Spaces**: [https://huggingface.co/spaces/vicky4s4s/News-Summarizer](#) *(Replace with your deployment link)*


## Bonus Features (Optional)
- Detailed comparative analysis with visualizations (e.g., sentiment distribution chart using Gradio’s plotting components).
- Query system allowing users to search within extracted articles.

---

### Notes for You:
1. **Gradio-Specific Adjustments**:
   - Gradio uses a different approach than Streamlit. Your `app.py` will define a function (e.g., `process_company(company_name)`) and pass it to `gr.Interface()` to create the UI.
   - Example: `gr.Interface(fn=process_company, inputs="text", outputs=["text", "audio"], title="News Summarizer")`.
   - Update the "Usage" section if you add a dropdown or other UI elements.

2. **Deployment**:
   - Hugging Face Spaces works seamlessly with Gradio. Simply push your repo with `app.py` as the entry point, and it will auto-detect the Gradio app.

3. **Customization**:
   - Replace placeholders (e.g., GitHub URL, Hugging Face link) with your actual links.
   - If you use different models or libraries, update the "Model Details" and `requirements.txt` sections.
   - Add any challenges or extra features in the "Assumptions & Limitations" or "Bonus Features" sections.

4. **Testing**:
   - Test the README instructions locally to ensure they work before uploading to GitHub.

