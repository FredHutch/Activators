import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from hydrophobicities_range import *
from assign_scores import *
import pandas as pd

#digits = load_digits()
#X,y = digits.data, digits.target
#y_cat = to_categorical(y,10)

#from sklearn.model_selection import train_test_split
#Xtrain, Xtest, ytrain, ytest = train_test_split(X, y_cat, test_size=0.3)

#######################################################################################################
# assign promoter and get the data encoded for DL

m = pd.read_csv('./arg3_ALLcentroids_reads.csv', index_col=0)
promoter='ARG3'
scores = assign_score(promoter)
input_data = pd.concat([iupred_long, hydroph_df, np.log(m.scores)], axis=1, sort=True).dropna()
input_data.columns = [str(i)+'iupred'for i in range(30)] + [str(i)+'hydroph' for i in range(30)]+['scores']
input_data = input_data.astype(float)
'''
# normalize the data!
normalize = lambda x: (x-np.mean(x)) / np.std(x)

# Try classification since regression is not learning enough
scores = scores[scores.iloc[:,:5].sum(axis=1)>=5]  # first filter on number of total reads
positives = scores[scores[['bin3','bin4']].sum(axis=1) > \
             scores[['pres','bin1','bin2']].sum(axis=1)*2].index
negatives = scores[scores[['bin2','bin3','bin4']].sum(axis=1)*2<scores['pres']].index

# now get intersection of scores index with positives and negatives indexes
positives = list( set(positives).intersection(set(input_data.index)) )
negatives = list( set(negatives).intersection(set(input_data.index)) )

print('{} positives and {} negatives makes a {} ratio of negat/posit'.format(\
      len(positives), len(negatives), float(len(negatives))/len(positives)))

# Genereate a set of only positive and negative samples, and let all rest of data aside 
input_data = input_data.loc[positives+negatives]
input_data.loc[:,'TAD']=0
input_data.loc[positives,'TAD']=1
#gete rid of scores in input_data
input_data = input_data.drop('scores', axis=1)

# get a stack of disorder and hydrophobicities in 4 dimensions.
X = input_data.iloc[:,:-1].values.reshape(input_data.shape[0],3,20,1)
y = input_data.iloc[:,-1].values
#y = normalize(y)
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)
'''

print(input_data.sample(5))
print(input_data.columns)
#gete rid of scores in input_data
X = input_data.drop('scores', axis=1)
y = input_data.scores
from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.1)
#######################################################################################################


from sklearn.model_selection import learning_curve
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import to_categorical
import keras.backend as K
from keras.callbacks import EarlyStopping

K.clear_session()

model = Sequential()
model.add(Dense(500, input_shape=(Xtrain.shape[1],), activation='relu'))
model.add(Dense(250, activation='relu'))
model.add(Dense(60, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])

# store initial random weights
initial_weights = model.get_weights()

# proposed 4 training sets for the learning curve
train_sizes = (len(Xtrain) * np.linspace(0.1, 0.999, 7)).astype(int)

train_scores = []
test_scores = []

for train_size in train_sizes:
    Xtrain_frac, _, ytrain_frac, _ = train_test_split(Xtrain, ytrain, train_size=train_size)

    # at each iteration reset the weights of the model to the initial random weights
    model.set_weights(initial_weights)

    h = model.fit(Xtrain_frac, ytrain_frac, verbose=0, batch_size=50, epochs=100, callbacks=[EarlyStopping(monitor='loss', patience=1)])

    r = model.evaluate(Xtrain_frac, ytrain_frac, verbose=0)
    train_scores.append(r[-1])

    e = model.evaluate(Xtest, ytest, verbose=0)
    test_scores.append(e[-1])

    print("Done size: ",train_size)

print('train_scores = ',train_scores)
print('test_scores = ', test_scores)

plt.plot(train_sizes, train_scores, 'o-', label='Training score')
plt.plot(train_sizes, test_scores, 'o-', label='Test score')
plt.legend(loc='best')
plt.savefig('test_learn_curve.jpg', dpi=300)


