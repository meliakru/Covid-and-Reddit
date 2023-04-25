import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Load Reddit API post data from CSV file
data = pd.read_csv(r'./post_covid_datasets/mentalhealthreddit_data.csv')

# Filter data to only include posts that mention desired keyword
keyword = 'Covid'
filtered_data = data[data['Title'].str.contains(keyword, case=False) | data['Content'].str.contains(keyword, case=False)]
filtered_data.reset_index(inplace=True, drop=True)  # reset the index to remove any gaps

## Preprocess text data
stop_words = set(stopwords.words('english'))
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(filtered_tokens)
filtered_data.loc[:, 'clean_Title'] = filtered_data['Title'].apply(preprocess_text) 
filtered_data.loc[:, 'clean_Content'] = filtered_data['Content'].apply(preprocess_text)


# Compute TF/IDF scores for each word in filtered posts
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(filtered_data['clean_Title'] + filtered_data['clean_Content'])
feature_names = {v: k for k, v in vectorizer.vocabulary_.items()}
tfidf_scores = tfidf_matrix.toarray()

# Identify most commonly used words by sorting by TF/IDF score
word_scores = [(word, score) for word, score in zip(feature_names.values(), tfidf_scores.sum(axis=0))]
word_scores.sort(key=lambda x: x[1], reverse=True)
top_words = [word for word, score in word_scores[:10]]

returnstr:str ='\n The top 10 words are: '
for i in range(0, len(top_words)):
    scoretuples = [t for t in word_scores if t[0] == top_words[i]]
    returnstr += scoretuples[0][0] + ' (score: ' + str(round(scoretuples[0][1], 5)) + '), '
returnstr = returnstr[0:len(returnstr)-2]
print(returnstr)
