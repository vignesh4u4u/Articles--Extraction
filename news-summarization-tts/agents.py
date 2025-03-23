from api import Model
import os
def initial_prompt(list_of_articles, POSITIVE, NEGATIVE,cleaned_text):
    return f"""
You are a senior data analyst with 15+ years of expertise in comparative analysis. Your task is to analyze multiple articles from the given list and generate a structured **JSON summary** that highlights key differences, patterns, and sentiment insights.

### **Input Data:**  
- **Articles:** {list_of_articles} 


### Complete contents of the articles: 
{cleaned_text} 

### **Task Requirements:**  
1. **Identify Key Differences:**  
   - Highlight the **strongest contrasting viewpoints** or **highest topic overlap** among the articles.  

2. **Generate a Structured JSON Output:**  
   - **Coverage Differences:** Identify variations in focus across articles.  
   - **Impact Analysis:** Explain how these differences affect audience perception.  

3. **Perform Sentiment Analysis:**  
   - Generate a summary based on the sentiment distribution.  


### **Sentiment Overview:**  
- **Positive Mentions:** {POSITIVE}  
- **Negative Mentions:** {NEGATIVE}  
 
"""

prompt1 = """
### **Expected JSON Output Format:**  
{  
  "Coverage Differences": [  
    {  
      "Comparison": "{Article_X} focuses on {Key_Topic_X}, while {Article_Y} highlights {Key_Topic_Y}.",  
      "Impact": "{Effect_of_the_different_focuses_on_audience_perception}."  
    },  
    {  
      "Comparison": "{Article_X} emphasizes {Aspect_X}, whereas {Article_Y} discusses {Aspect_Y}.",  
      "Impact": "{Potential_market_or_public_reaction}."  
    },  
    {  
      "Comparison": "{Article_X} presents {Perspective_X}, but {Article_Y} contrasts this with {Perspective_Y}.",  
      "Impact": "{Implications_of_the_conflicting_perspectives}."  
    }  
  ],  
  "Topic Overlap": {  
    "Common Topics": ["{Common_Topic_1}", "{Common_Topic_2}"],  
    "Unique Topics in {Article_X}": ["{Unique_Topic_X_1}", "{Unique_Topic_X_2}"],  
    "Unique Topics in {Article_Y}": ["{Unique_Topic_Y_1}", "{Unique_Topic_Y_2}"]  
  },  
  "Final Sentiment Analysis": "{Overall_sentiment_summary (Positive/Negative/Neutral) with a brief explanation}",
  "Overall_Sentiment_Ssummarizing_Report" :"Complete contents of the articles content summarizing into give clean format." 
}  

### **Instructions:**  
- **Strictly** follow this JSON structure in your output.  
- Do **not** include any additional text besides the JSON.  
"""



def generate_response(list_of_articles,POSITIVE,NEGATIVE,clean_text):
    prompt = initial_prompt(list_of_articles,POSITIVE,NEGATIVE,clean_text) + "\n\n"+ prompt1
    answer_text= Model.OPENAI_MODEL(prompt)
    start_index_square = answer_text.find('[')
    start_index_curly = answer_text.find('{')
    if start_index_square != -1 and (start_index_curly == -1 or start_index_square < start_index_curly):
        start_index = start_index_square
        end_char = ']'
    elif start_index_curly != -1 and (start_index_square == -1 or start_index_curly < start_index_square):
        start_index = start_index_curly
        end_char = '}'
    else:
        return ("Error: JSON data not found.")
        extracted_json = None
    end_index = answer_text.rfind(end_char)
    if start_index != -1 and end_index != -1:
        extracted_json = answer_text[start_index:end_index + 1]
        return (extracted_json)



