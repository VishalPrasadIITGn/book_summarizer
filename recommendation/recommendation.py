"""Training and predicting book recommendation"""

import numpy as np
import pandas as pd
import pickle

import warnings
warnings.filterwarnings("ignore")

books = pd.read_csv("book_summarizer/recommendation/dataset/BX-Books.csv", sep=';', encoding="latin-1", on_bad_lines="skip")
users = pd.read_csv("book_summarizer/recommendation/dataset/BX-Users.csv", sep=';', encoding="latin-1", on_bad_lines="skip")
ratings = pd.read_csv("book_summarizer/recommendation/dataset/BX-Book-Ratings.csv", sep=';', encoding="latin-1", on_bad_lines="skip")

print(books.head(3))

books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]
books.rename(columns = {'Book-Title':'title', 'Book-Author':'author', 'Year-Of-Publication':'year', 'Publisher':'publisher'}, inplace=True)
users.rename(columns = {'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
ratings.rename(columns = {'User-ID':'user_id', 'Book-Rating':'rating'}, inplace=True)

x = ratings['user_id'].value_counts() > 200
y = x[x].index  #user_ids
print(y.shape)
ratings = ratings[ratings['user_id'].isin(y)]

rating_with_books = ratings.merge(books, on='ISBN')
rating_with_books.head()

number_rating = rating_with_books.groupby('title')['rating'].count().reset_index()
number_rating.rename(columns= {'rating':'number_of_ratings'}, inplace=True)
final_rating = rating_with_books.merge(number_rating, on='title')
final_rating.shape
final_rating = final_rating[final_rating['number_of_ratings'] >= 50]
final_rating.drop_duplicates(['user_id','title'], inplace=True)


book_pivot = final_rating.pivot_table(columns='user_id', index='title', values="rating")
book_pivot.fillna(0, inplace=True)

from scipy.sparse import csr_matrix
book_sparse = csr_matrix(book_pivot)

from sklearn.neighbors import NearestNeighbors
model = NearestNeighbors(algorithm='brute')
model.fit(book_sparse)

distances, suggestions = model.kneighbors(book_pivot.iloc[250, :].values.reshape(1, -1))

for i in range(len(suggestions)):
  print(book_pivot.index[suggestions[i]])

# dump the model
pickle.dump(model, open("book_summarizer/recommendation/prediction/model_pickle", 'wb')) 
# dump the pickle table
save_data = open('book_summarizer/recommendation/prediction/book_pivot.pickle', 'wb')
pickle.dump(book_pivot, save_data)
save_data.close()
  
# load classifier using pickle 
my_model_clf = pickle.load(open("book_summarizer/recommendation/prediction/model_pickle", 'rb')) 

# load pivot table using 
pickle_data = open('book_summarizer/recommendation/prediction/book_pivot.pickle', 'rb') #rb stands for read bytes 
book_pivot = pickle.load(pickle_data)

# making prediction from loaded model
result_score, suggestions = my_model_clf.kneighbors(book_pivot.iloc[250, :].values.reshape(1, -1))
output = []
for i in range(len(suggestions)):
  print(book_pivot.index[suggestions[i]])
  output.extend(book_pivot.index[suggestions[i]])
pickle_data.close()

print(f"output is: {output}")

  

