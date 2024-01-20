# importing the modules

""" importing machine learning modules """
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

""" importing necessary modules """
import pandas as pd
import pickle

# reading the dataset
data = pd.read_csv('dataset/phishing.csv')
data = data.drop(['Index', 'WebsiteTraffic'], axis=1)

# splitting x and y
x = data.drop(["class"], axis=1)
y = data["class"]

# testing and training dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# model for LogisticRegression
model_logisticRegression = LogisticRegression()
model_logisticRegression.fit(x_train, y_train)
print(f"\n\nLogistic Regression (testing): {model_logisticRegression.score(x_test, y_test)}")
print(f"Logistic Regression (training): {model_logisticRegression.score(x_train, y_train)}")

# model for SVC
model_SVC = SVC()
model_SVC.fit(x_train, y_train)
print(f"\n\nSupport Vector Classifier (testing): {model_SVC.score(x_test, y_test)}")
print(f"Support Vector Classifier (training): {model_SVC.score(x_train, y_train)}")

# model for DecisionTree
model_tree = DecisionTreeClassifier(max_depth=10)
model_tree.fit(x_train, y_train)
print(f"\n\nDecision Tree (testing): {model_tree.score(x_test, y_test)}")
print(f"Decision Tree (training): {model_tree.score(x_train, y_train)}")

# model for RandomForestClassifier
model_RFC = RandomForestClassifier(n_estimators=100)
model_RFC.fit(x_train, y_train)
print(f"\n\nRandom Forest Classifier (testing): {model_RFC.score(x_test, y_test)}")
print(f"Random Forest Classifier (training): {model_RFC.score(x_train, y_train)}")

# model for Gradient Boosting Classifier
model_GBC = GradientBoostingClassifier(max_depth=7, learning_rate=0.6790)
model_GBC.fit(x_train, y_train)
print(f"\n\nGradient Boosting Classifier (testing): {model_GBC.score(x_test, y_test)}")
print(f"Gradient Boosting Classifier (training): {model_GBC.score(x_train, y_train)}")


pickle.dump(model_GBC, open('model/model.pkl', 'wb'))
