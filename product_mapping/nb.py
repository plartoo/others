# REF: https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
# http://archive.is/l3pqr
# https://web.archive.org/web/20180629014044/https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f?gi=5faf6b6cc8a8
# http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
# https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

X_train, X_test, y_train, y_test = train_test_split(df['Consumer_complaint_narrative'], df['Product'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)