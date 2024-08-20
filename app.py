from flask import Flask, request, render_template, jsonify
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Azure Text Analytics Configuration
endpoint_url = "https://ksentimentanalysis.cognitiveservices.azure.com/"
secret_key = "89995415ce064fb98ec2513248c7a9ed"

def get_client():
    credentials = AzureKeyCredential(secret_key)
    analytics_client = TextAnalyticsClient(endpoint=endpoint_url, credential=credentials)
    return analytics_client

client = get_client()

def evaluate_sentiment(client, texts):
    results = client.analyze_sentiment(documents=texts)
    analysis_results = []
    for i, result in enumerate(results):
        analysis_results.append({
            "text": texts[i],
            "sentiment": result.sentiment,
            "confidence_scores": {
                "positive": result.confidence_scores.positive,
                "neutral": result.confidence_scores.neutral,
                "negative": result.confidence_scores.negative
            }
        })
    return analysis_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-review', methods=['POST'])
def submit_review():
    review_text = request.json.get('review', '')
    
    if not review_text:
        return jsonify({"error": "No review provided"}), 400
    
    sentiment_results = evaluate_sentiment(client, [review_text])
    
    return jsonify(sentiment_results)

if __name__ == '__main__':
    app.run(debug=True)
