import pickle
import numpy as np
import get_features

file = open('model/model.pkl', 'rb')
model = pickle.load(file)
file.close()


def phishPrediction(url):
    features = get_features.Features(f'{url}').get_features()
    data = np.array([features]).reshape(1, 29)
    print(data)

    y_pred = model.predict(data)[0]
    y_phishing = model.predict_proba(data)[0, 0]
    y_non_phishing = model.predict_proba(data)[0, 1]

    print("y predict", y_pred)
    print(f"phishing prediction {round(y_phishing*100, 2)}")
    print(f"non phishing prediction {round(y_non_phishing*100, 2)}")

    return y_pred, round(y_phishing*100, 2), round(y_non_phishing*100, 2)

# print(phishPrediction("https://srmvalliammai.ac.in/"))