import pdb
# REF:
# http://scikit-learn.org/stable/auto_examples/text/document_classification_20newsgroups.html#sphx-glr-auto-examples-text-document-classification-20newsgroups-py
# https://www.kaggle.com/adamschroeder/countvectorizer-tfidfvectorizer-predict-comments | http://archive.is/RZ23f

# https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
# http://archive.is/l3pqr
# https://web.archive.org/web/20180629014044/https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f?gi=5faf6b6cc8a8
# http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

# Tensor Flow: http://www.riptutorial.com/tensorflow/example/30750/math-behind-1d-convolution-with-advanced-examples-in-tf


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns

import heuristic


def predict_nb(str, model, cnt_vect):
    print(model.predict(cnt_vect.transform([str])))


def predict_svc(str, model, vectorizer, category_dict):
    vectorized_str = vectorizer.transform([str])
    predicted_cat_id = model.predict(vectorized_str)[0]
    print(category_dict[predicted_cat_id])


query_name = 'mapped_items'
print('Loading data from remote database using query:', heuristic.QUERIES[query_name])
df = heuristic.get_dataframe_from_query(query_name)


# ## First try the quick and dirty: Multi-nomial Naive Bayes
# dfx = (df['GM_ADVERTISER_NAME'].apply(heuristic.tokenize) + df['GM_SECTOR_NAME'].apply(heuristic.tokenize) \
#       + df['GM_SUBSECTOR_NAME'].apply(heuristic.tokenize) + df['GM_CATEGORY_NAME'].apply(heuristic.tokenize) \
#       + df['GM_BRAND_NAME'].apply(heuristic.tokenize) + df['GM_PRODUCT_NAME'].apply(heuristic.tokenize)).apply(' '.join)
# dfy = df[['CP_SUBCATEGORY_NAME']]
# dfy.columns = ['CP_SUBCATEGORY_NAME']
# x_train, x_test, y_train, y_test = train_test_split(dfx, dfy, random_state = 0)
# cnt_vect = CountVectorizer()
# x_train_counts = cnt_vect.fit_transform(x_train)
# tfidf_transformer = TfidfTransformer()
# x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
# clf = MultinomialNB().fit(x_train_tfidf, y_train)
# # predict('Dial Kids : Hair & Body Wash', clf, cnt_vect)
# # pdb.set_trace()
# print('ha')


## Let's try to see how other models stack up compared to Multinomial NB
# models = [
#     #RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
#     LinearSVC(),
#     MultinomialNB(),
#     LogisticRegression(random_state=0),
# ]
# CV = 5 # 5 fold cross validation
# cv_df = pd.DataFrame(index=range(CV * len(models)))
# entries = []
# tfidf = TfidfVectorizer(
#                         sublinear_tf=True, # TODO: we can remove this if log scale doesn't work out
#                         min_df=1,
#                         norm='l2', # L2 norm
#                         encoding='utf-8',
#                         ngram_range=(1, 2),
#                         stop_words='english'
#         )
# dfx = (df['GM_ADVERTISER_NAME'].apply(heuristic.tokenize) + df['GM_SECTOR_NAME'].apply(heuristic.tokenize) \
#       + df['GM_SUBSECTOR_NAME'].apply(heuristic.tokenize) + df['GM_CATEGORY_NAME'].apply(heuristic.tokenize) \
#       + df['GM_BRAND_NAME'].apply(heuristic.tokenize) + df['GM_PRODUCT_NAME'].apply(heuristic.tokenize)).apply(' '.join)
# features = tfidf.fit_transform(dfx)
#
# dfy = df[['CP_SUBCATEGORY_NAME']]
# dfy.columns = ['CP_SUBCATEGORY_NAME'] # assign column name
# dfy['category_id'] =  dfy['CP_SUBCATEGORY_NAME'].factorize()[0]
# category_id_df = dfy[['CP_SUBCATEGORY_NAME', 'category_id']].drop_duplicates().sort_values('category_id')
# category_to_id = dict(category_id_df.values)
# id_to_category = dict(category_id_df[['category_id', 'CP_SUBCATEGORY_NAME']].values)
# labels = dfy.category_id
#
# for model in models:
#     print(model)
#     model_name = model.__class__.__name__
#     accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
#     # accuracies = cross_val_score(model, dfx, dfy, scoring='accuracy', cv=CV)
#     for fold_idx, accuracy in enumerate(accuracies):
#         entries.append((model_name, fold_idx, accuracy))
#
# cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
# sns.boxplot(x='model_name', y='accuracy', data=cv_df)
# sns.stripplot(x='model_name', y='accuracy', data=cv_df,
#               size=8, jitter=True, edgecolor="gray", linewidth=2)
# plt.show()



## After finding out that the best model is LinearSVC, we build confusion matrix to see where it falls short
entries = []
tfidf_vectorizer = TfidfVectorizer(
                        sublinear_tf=True, # TODO: we can remove this if log scale doesn't work out
                        min_df=1,
                        norm='l2', # L2 norm
                        encoding='utf-8',
                        ngram_range=(1, 2),
                        stop_words='english'
        )

dfx = (df['GM_ADVERTISER_NAME'].apply(heuristic.tokenize) + df['GM_SECTOR_NAME'].apply(heuristic.tokenize) \
      + df['GM_SUBSECTOR_NAME'].apply(heuristic.tokenize) + df['GM_CATEGORY_NAME'].apply(heuristic.tokenize) \
      + df['GM_BRAND_NAME'].apply(heuristic.tokenize) + df['GM_PRODUCT_NAME'].apply(heuristic.tokenize)).apply(' '.join)
features = tfidf_vectorizer.fit_transform(dfx)

dfy = df[['CP_SUBCATEGORY_NAME']]
dfy.columns = ['CP_SUBCATEGORY_NAME'] # assign column name
dfy = dfy.copy() # to avoid getting 'SettingWIthCopyWarning'
dfy['category_id'] =  dfy['CP_SUBCATEGORY_NAME'].factorize()[0]
category_id_df = dfy[['CP_SUBCATEGORY_NAME', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'CP_SUBCATEGORY_NAME']].values)
labels = dfy.category_id

model = LinearSVC() # API Reference: http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features,
                                                                                 labels,
                                                                                 df.index,
                                                                                 test_size=0.33,
                                                                                 random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# here is where magic happens
predict_svc('Dettol Liquid Soap Dist', model, tfidf_vectorizer, id_to_category)
predict_svc('D262.0 Solid & Roll-On Deodorants & Antiperspirants', model, tfidf_vectorizer, id_to_category)


# cnt_vect = CountVectorizer()
# x_train_counts = cnt_vect.fit_transform(X_train)
# tfidf_transformer = TfidfTransformer()
# x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)


from sklearn.metrics import confusion_matrix
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.CP_SUBCATEGORY_NAME.values,
            yticklabels=category_id_df.CP_SUBCATEGORY_NAME.values
            # vmax=conf_mat.max(),
            # square=True,
            # cmap='cubehelix',
            # linewidths=1.0,
            )

## Trying to make confusion matrix look readable
## REF: https://stackoverflow.com/questions/35127920/overlapping-yticklabels-is-it-possible-to-control-cell-size-of-heatmap-in-seabo
# fontsize_pt = 10 # plt.rcParams['ytick.labelsize'] does not return a numeric value, so I set it to '10'
# dpi = 72.27
# matrix_height_pt = fontsize_pt * conf_mat.shape[0]
# matrix_height_in = matrix_height_pt / dpi
# top_margin = 0.04
# bottom_margin = 0.04
# figure_height = matrix_height_in / (1 - top_margin - bottom_margin)
# fig, ax = plt.subplots(figsize=(20, figure_height),
#                        gridspec_kw=dict(top=(1-top_margin), bottom=bottom_margin))
# ax = sns.heatmap(conf_mat, ax=ax, annot=True, cmap="cubehelix")

plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

## We can pickle the trained model and reload it like this below:
# Save classifier to a file
# save_classifier = open("Tfidf_LogR_3.pickle", 'wb') #wb= write in bytes.
# pickle.dump(grid3, save_classifier) #use pickle to dump the grid3 we trained, as 'Tfidf_LogR.pickle' in wb format
# save_classifier.close()
# Retrieve the saved file and uplaod it to an object

# vec = open("Tfidf_LogR_3.pickle", 'rb') # rb= read in bytes
# grid3 = pickle.load(vec)
# vec.close()