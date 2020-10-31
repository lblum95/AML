import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.decomposition import KernelPCA
from sklearn.ensemble import StackingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from imblearn.pipeline import Pipeline

import numpy as np

x_train = pd.read_csv("data/X_train.csv", index_col=0, header=0)
y_train = pd.read_csv("data/y_train.csv", index_col=0, header=0)
x_test = pd.read_csv("data/X_test.csv", index_col=0, header=0)

cv = StratifiedKFold(n_splits=5)

estimators = [
    ('svc_sig', SVC(kernel='sigmoid', random_state=42)),
    ('svc_rbf', SVC(kernel='rbf', random_state=42)),
    ('svc_poly', SVC(kernel='poly', random_state=42))
]

over = SMOTE(random_state=42)
under = RandomUnderSampler(random_state=42)
feature_sel = KernelPCA(kernel='rbf', random_state=42)
model = StackingClassifier(estimators=estimators, final_estimator=SVC(random_state=42))

param_grid = {
    'feature__n_components': np.linspace(start=100, stop=600, num=2),
    'classification__svc_sig__C': [1],
    'classification__svc_rbf__C': [1],
    'classification__svc_poly__C': [1],
    'classification__final_estimator__C': [1]
}

steps = [('feature', feature_sel), ('over', over), ('under', under), ('classification', model)]
pipeline = Pipeline(steps=steps)

import pprint as pp

pp.pprint(sorted(pipeline.get_params().keys()))

search = GridSearchCV(pipeline, param_grid,scoring='balanced_accuracy', cv=cv, n_jobs=-1, verbose=10)
search.fit(x_train, y_train.values.ravel())

print("Best parameter (CV score=%0.3f):" % search.best_score_)
print(search.best_params_)
print(search.cv_results_)

y_pred = search.predict(x_test)

df = pd.DataFrame(y_pred)
df.to_csv('data/y_pred.csv', header=['y'], index_label='id')