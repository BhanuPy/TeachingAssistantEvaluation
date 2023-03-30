import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib



# Load the dataset
df = pd.read_csv('data.csv', header=None)

# Assign column names to the dataset
df.columns = ['native_english_speaker', 'course_instructor', 'course', 'semester', 'class_size', 'score']

# Convert categorical features into numerical features using LabelEncoder
le = LabelEncoder()
df['course_instructor'] = le.fit_transform(df['course_instructor'])
df['course'] = le.fit_transform(df['course'])

# Split the dataset into features and target
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Scale the features using StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print("line 38")

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a logistic regression model
logistic_model = LogisticRegression(multi_class='auto', solver='lbfgs', max_iter=1000)

# Use cross-validation to optimize hyperparameters
scores = cross_val_score(logistic_model, X_train, y_train, cv=5)
print('Cross-validation scores:', scores)
print('Average score:', scores.mean())




# Train the logistic regression model on the training set
logistic_model.fit(X_train, y_train)

# Save the trained model to a file
filename = 'logistic_regression_model.joblib'
joblib.dump(logistic_model, filename)


# Load the saved model from the file
loaded_model = joblib.load(filename)


# Predict new data using the loaded model
# new_data = [[5.1, 3.5, 1.4, 0.2]]
# loaded_model.predict(new_data)


# Evaluate the model on the testing set
y_pred = logistic_model.predict(X_test)

# Calculate accuracy, precision, recall, and F1-score
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1-score:', f1)



# # Train the logistic regression model on the training set
# logistic_model.fit(X_train, y_train)

# # Save the trained model to a file
# filename = 'logistic_regression_model.joblib'
# joblib.dump(logistic_model, filename)
