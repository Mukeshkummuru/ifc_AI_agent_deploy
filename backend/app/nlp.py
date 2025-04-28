import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

 
nltk.data.path.append('./backend/nltk_data') 

lemmatizer = WordNetLemmatizer()

def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized

def identify_intent(tokens):
    tokens_set = set(tokens)

    
    casual_keywords = ['hello', 'hi', 'hey', 'thanks', 'please', 'good', 'morning', 'evening']
    if any(word in tokens_set for word in casual_keywords) and not {'wall', 'door', 'slab', 'plaster', 'volume', 'material', 'count','cost'}.intersection(tokens_set):
        return 'greeting'

    
    if 'slab' in tokens_set and 'volume' in tokens_set:
        return 'slab_volume'
    if 'wall' in tokens_set and 'volume' in tokens_set:
        return 'wall_volume'
    if 'wall' in tokens_set and ('area' in tokens_set or 'surface' in tokens_set):
        return 'wall_area'
    if 'wall' in tokens_set and any(w in tokens_set for w in ['count', 'how', 'many', 'number']):
        return 'wall_count'
    if 'door' in tokens_set and any(w in tokens_set for w in ['count', 'how', 'many', 'number']):
        return 'door_count'
    if 'plaster' in tokens_set or 'plastering' in tokens_set or 'plastered' in tokens_set:
        return 'plastering_area'
    if 'material' in tokens_set and any(w in tokens_set for w in ['names', 'used', 'materials','list']):
        return 'material_names'

    return 'unknown'