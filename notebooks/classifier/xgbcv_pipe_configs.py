from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

class Config:
    def __init__(self):
        self.params = {'estimator__learning_rate': [.2, .1],
                       'estimator__n_estimators': [200, 150],
                       'estimator__max_depth': [4, 5],
                       'estimator__min_samples_leaf': [.1, .2],
                       'estimator__max_features': [2, 4],
                       'estimator__min_samples_split': [.7, .6]}
        
        self.scores = {'precision': make_scorer(precision_score, average='macro'),
                       'recall': make_scorer(recall_score, average='macro'),
                       'f1': make_scorer(f1_score, average='macro')}