'''
For imbalanced classes we cannot use accuracy as a metric to analyze the model performance.
Metrics F1, precision, and recall have been removed from Keras.
So we will use a custom metric function:
'''

from keras import backend as K

def F1(y_true, y_pred):

    def precision(y_true, y_pred):
        """ Batch-wise average precision calculation

        Calculated as tp / (tp + fp), i.e. how many selected items are relevant
        Added epsilon to avoid the Division by 0 exception
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def recall(y_true, y_pred):
        """ Batch-wise average recall calculation

        Computes the Recall metric, or Sensitivity or True Positive Rate
        Calculates as tp / (tp + fn) i.e. how many relevant items are selected

        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall


    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2* (precision * recall) / (precision + recall + K.epsilon())
