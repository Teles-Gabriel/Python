from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

def language_analysis(text):
    
    document = client.document_from_text(text)
    sent_analysis = document.analyze_sentiment()
    print(dir(sent_analysis))
    sentiment = sent_analysis.sentiment
    ent_analysis = document.analyze_entities()
    entities = ent_analysis.entities
    return sentiment, entities

exemple_text = "Isn't it obvious that I love you?"

sentiment, entities = language_analysis(exemple_text)
print(sentiment.score, sentiment.magnitude)

for e in entities:
    print(e.name, e.entity_type, e.metadata, e.salience)