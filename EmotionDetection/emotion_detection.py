
import requests
import json

# Creating the emotion_detector function to validate text from input arguments
def emotion_detector(text_to_analyse):

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json_obj = { "raw_document": { "text": text_to_analyse } }
    
    # Send the request to the API
    response = requests.post(url, json=input_json_obj, headers=headers)
    
    # Step 1: Handle the response status codes
    if response.status_code != 200:
        return {'error': f'Invalid text! Please try again!. {response.status_code}'}
    
    # Step 2: Convert the response text into a dictionary
    converted_response = json.loads(response.text)
    
    # Step 3: Extract required set of emotions and their scores
    predictions = converted_response.get("emotionPredictions", [])
    if not predictions:
        return {'error': 'No emotion predictions found in the response'}
    
    emotions = predictions[0].get("emotion", {})
    
    anger_score = emotions.get("anger", 0)
    disgust_score = emotions.get("disgust", 0)
    fear_score = emotions.get("fear", 0)
    joy_score = emotions.get("joy", 0)
    sadness_score = emotions.get("sadness", 0)
    
    # Step 4: Find the dominant emotion
    emotion_list = [anger_score, disgust_score, fear_score, joy_score, sadness_score]
    emotion_keys = ["anger", "disgust", "fear", "joy", "sadness"]
    
    if any(emotion_list):  
        # Ensure there are non-zero emotion scores
        dominant_emotion_index = emotion_list.index(max(emotion_list))
        dominant_emotion_key = emotion_keys[dominant_emotion_index]
    
    # Step 7: Error handling
    elif response.status_code == 400:
        anger_score = None
        disgust_score = None
        fear_score = None
        joy_score = None
        sadness_score = None
        dominant_emotion_key = None
    
    elif(dominant_emotion_key == None):
        #dominant_emotion_key = None
        print("Invalid text! Please try again!.") 
    
    # Step 5: Return the required output format
    result = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion_key
    }
    return result  

# Example usage
print(emotion_detector(" "))