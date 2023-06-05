from sklearn.metrics import mean_squared_error, r2_score, make_scorer

class RConfig:
    def __init__(self):
        self.params = {'estimator__hidden_layer_sizes': [(64, 32, 16), (128, 64, 32)],
                       'estimator__alpha': [.0001, .001, .00001],
                       'estimator__batch_size': [16, 32],
                       #'estimator__learning_rate': 'adaptive',
                       'estimator__learning_rate_init': [.001, .01, .1]}
        
        self.scores = {'mse': make_scorer(mean_squared_error),
                       'r2': make_scorer(r2_score)}