import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import ticker
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re

figure, axs = plt.subplots(nrows=3, ncols=1, figsize=(10,10))
figure.suptitle('Rank-Frequency of Top 10 words from Post-Covid period Covid-Related Posts')

# note: assumes that the file being read is in subfolder
def generateRankFrequancy(period:str, filename:str, ax:plt.Axes):
    # Load the Reddit API post data from the .csv file
    folder = 'preCovid/datasets' if period == 'before' else 'duringCovid/datasets' if period =='during' else 'postCovid/datasets'
    data = pd.read_csv(rf"./{folder}/{filename}")

    # Filter the data to include only posts that mention a specific keyword
    keyword = 'Covid'
    filtered_data = data[data['Title'].str.contains(keyword, case=False) | data['Content'].str.contains(keyword, case=False)]

    # Concatenate the title and body columns and preprocess the text data
    filtered_data['text'] = filtered_data['Title'].fillna('') + ' ' + filtered_data['Content'].fillna('')
    filtered_data['text'] = filtered_data['text'].str.replace('[^\w\s]','')
    filtered_data['text'] = filtered_data['text'].str.lower()

    # Tokenize the text data into individual words
    filtered_data['tokens'] = filtered_data['text'].apply(word_tokenize)

    # Filter out stopwords
    stop_words = set(stopwords.words('english'))
    filtered_data['tokens'] = filtered_data['tokens'].apply(lambda x: [word for word in x if word not in stop_words])

    # Tag the tokens with parts of speech
    filtered_data['pos_tags'] = filtered_data['tokens'].apply(pos_tag)

    # Filter the word list to include only nouns, adjectives, verbs, and adverbs
    allowed_pos = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'RB', 'RBR', 'RBS']
    word_list = []
    for tags in filtered_data['pos_tags']:
        word_list += [tag[0] for tag in tags if tag[1] in allowed_pos]

    # Filter out words with special characters using regular expressions
    word_list = [word for word in word_list if re.match(r'^[a-zA-Z0-9]+$', word)]


    # Calculate the frequency of each word using the Counter class
    word_counts = Counter(word_list)

    total_words = sum(word_counts.values())

    # Sort the word frequency counts in descending order to create a ranked list of words
    ranked_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Extract the top 10 words and their frequencies
    top_10_words = [word for word, count in ranked_words[:10]]
    top_10_frequencies = [count/total_words for word, count in ranked_words[:10]]

    # Plot the rank of each word against its frequency
    
    ax.set(xlabel='Word Rank(1-10 Left-Right)', ylabel = 'Frequency')
    ax.set_xticks(range(1, len(top_10_words)+1), top_10_words)
    yticks = ticker.MaxNLocator(10)
    ax.yaxis.set_major_locator(yticks)
    subreddit = "r/Anxiety" if filename.__contains__("Anxiety") else "r/depression" if filename.__contains__("depression") else "r/mentalhealth"
    title = rf'{subreddit} Top 10 words in Covid-related Posts'
    ax.set_title(title)
    ax.scatter(range(1, len(top_10_words)+1), top_10_frequencies)

#input args: 
#period: "before", "during" or "after"
#filename: the name of the file in the subfolder
#can be changed as needed to calculate for different periods
generateRankFrequancy("after", 'Anxietyreddit_data.csv', axs[0])
generateRankFrequancy("after", 'depressionreddit_data.csv',axs[1])
generateRankFrequancy("after", 'mentalhealthreddit_data.csv', axs[2])
figure.subplots_adjust(hspace=0.5)
plt.show()
