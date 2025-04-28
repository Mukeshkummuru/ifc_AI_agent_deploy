import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure necessary NLTK data packages are downloaded
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized

def identify_intent(tokens):
     
    intents = {
        'plastering_area': ['plaster', 'plastering'],
        'wall_volume': ['wall', 'volume'],
        'slab_volume': ['slab', 'volume'],
        'wall_area': ['wall', 'surface', 'area'],
        'wall_count': ['wall', 'count', 'how', 'many', 'number'],
    }

  
    for intent, keywords in intents.items():
        if all(keyword in tokens for keyword in keywords):
            return intent

   
    max_overlap = 0
    selected_intent = 'unknown'

    for intent, keywords in intents.items():
        overlap = len(set(tokens).intersection(set(keywords)))
        if overlap > max_overlap:
            max_overlap = overlap
            selected_intent = intent

    return selected_intent if max_overlap > 0 else 'unknown'
