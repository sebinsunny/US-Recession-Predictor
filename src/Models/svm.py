from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


def plot_confusion_matrix(y_true, y_pred, label,
                          cmap=plt.cm.Blues):
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data

    print(cm)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=label, yticklabels=label,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


import pandas as pd

c = [1, 10, 100, 1000]
gamma = [1e-3, 1e-4]
features = ['Date', 'Payrolls_3mo_vs_12mo', 'Effective_Fed_Funds_12_chg', 'CPI_All_Items_3_mo_annualised',
            '10Y_Treasury_Rate_12_chg', '3M_10Y_Treasury_Spread', 'S&P_500_Index_12_chg']
cv_predictions_by_output = {}
df = pd.read_csv('/Users/sebin/Desktop/companyandngo/Data/final_features.csv')[::-1]
df_features = df[features]
df_features.join(pd.get_dummies(df['Recession']))

X_train, X_test, y_train, y_test = train_test_split(df_features, df['Recession_in_12mo'], test_size=0.30)

# dictionary for saving f1-score
svm_ac = {}
key = {'Payrolls_3mo_vs_12mo': 'S&P_500_Index_12_chg'}
# finding best c and gamma from the list of parameters
for x, y in [(x, y) for x in c for y in gamma]:
    k = x, y
    # initalize the'model' and passing the SVM Classifier with respect to C and gamma value
    model = svm.SVC(C=x, kernel='rbf', gamma=y, probability=True,
                    tol=1e-3, random_state=123,
                    class_weight='balanced')
    scaler = StandardScaler()
    scaler.fit(X_train.loc[:, key])
    training_x_scaled = scaler.transform(X_train.loc[:, key])
    accuracy = cross_val_score(model, training_x_scaled, y_train, cv=10, scoring='accuracy')
    svm_ac[k] = np.mean(accuracy)
    print("\n{:20} {:25}".format('Parameter', 'Average accuracy'))
    print('{}\t{:25}'.format(k, np.mean(accuracy)))

acc_score = max(svm_ac, key=svm_ac.get)
svc_model = svm.SVC(C=acc_score[0], kernel='rbf', gamma=acc_score[1], probability=True,
                    tol=1e-3, random_state=123,
                    class_weight='balanced')
scaler = StandardScaler()
scaler.fit(X_test.loc[:, key])
testing_scaled = scaler.transform(X_test.loc[:, key])
# fitting the model with training data
svc_model.fit(training_x_scaled, y_train)
# predicting the model with the test data
y_predict = svc_model.predict(testing_scaled)

# evaluating the accuracy with the ground truth and predicted value
model_acc = accuracy_score(y_test, y_predict)

print("Model Accuracy is: {}".format(model_acc))
predicted_probs = pd.DataFrame(svc_model.predict_proba(testing_scaled))
# classification_report((y_true, y_pred)
print("\nPerformance table")
print(f"\n{classification_report(y_test, y_predict)}")
# confusion matrix
print("\nConfusion matrix")
plot_confusion_matrix(y_test, y_predict, features)
print(
    "\nThe diagonal elements represent the total number of predicted value is equal to the true label and off-diagonal elements are mislabelled by the classifier")
