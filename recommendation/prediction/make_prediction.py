"""Make prediction for book recommendation"""
import pickle

def predict(user_id: int) -> list:
  """Predict book recommendation for user"""
  # load classifier using pickle 
  my_model_clf = pickle.load(open("book_summarizer/recommendation/prediction/model_pickle", 'rb')) 

  # load pivot table using 
  pickle_data = open('book_summarizer/recommendation/prediction/book_pivot.pickle', 'rb') #rb stands for read bytes 
  book_pivot = pickle.load(pickle_data)

  output = []

  # making prediction from loaded model
  _, suggestions = my_model_clf.kneighbors(book_pivot.iloc[user_id, :].values.reshape(1, -1)) 
  for i in range(len(suggestions)):
    output.extend(book_pivot.index[suggestions[i]])
    
  pickle_data.close()
  return output
