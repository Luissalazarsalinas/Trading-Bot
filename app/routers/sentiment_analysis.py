import numpy as np
from fastapi import APIRouter, status
import tensorflow as tf
from pathlib import Path
from app.schemas import Deeplearningin
# Instance of the router
router = APIRouter(
    prefix="/sentiment",
    tags=["Deep_learning Sentiment Analysis"]
)


# Import model
BASEPATH = Path(__file__).resolve(strict=True).parent

def get_model():
    model = tf.keras.models.load_model(f"{BASEPATH}/dl_model-0.0.1")
    return model

# Preprocessing data
def tokenizer(data):

    # Tokenizer
    token = tf.keras.preprocessing.text.Tokenizer(
        num_words = 2000,
        filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower = True,
        oov_token = "<OOV>"
    )

    # Fit the tokenizer
    token.fit_on_texts(data)

    # Text to sequence and padding
    data_seq = token.texts_to_sequences(data)
    data_padded = tf.keras.preprocessing.sequence.pad_sequences(
        data_seq, maxlen = 200, padding = "post", truncating = "post"
    )

    # Convent to an array
    data = np.array(data_padded)

    return data


# Add the path or endpoint 
@router.post("/", status_code= status.HTTP_201_CREATED)
def inference(data: Deeplearningin):

    # Data sentences
    data_sentence  = list(data.Teewts)
    
    # model
    model = get_model()
    try:
        data_tf = tokenizer(data_sentence)
    except Exception as e:
        raise print(e)

    # Inference 
    y_pred = model.predict(data_tf).argmax()

    # Result
    if y_pred == 0:
        return "Negative"
    
    elif y_pred == 1:
        return "Positive"
    
    else:
        return "Neutro"
