# -*- coding: utf-8 -*-
"""reccomendersystem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_d_T4InEnZLSmHYh9xN-IC66KeFk8xwn

# Mount to Drive
"""

from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

cd "/content/gdrive/MyDrive/1-Academics/CS383/Final_Project"

"""# Import Modules and Data"""

import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

data = pd.read_csv("u1.base", sep='\t',usecols=(0, 1, 2), names=["user id", "item_id", "rating"])

# datatest = pd.read_csv("u1.test", sep='\t',usecols=(0, 1, 2), names=["user id", "item_id", "rating"])
# mattest = datatest.pivot(*datatest.columns)

genre = pd.read_csv("u.genre", sep='|', names=["genre", "id"])

movies = pd.read_csv("u.item", sep='|', encoding = "ISO-8859-1", usecols=(0, 1, 2), names=["movie_id", "Title", "Year"])

movies

demo = pd.read_csv("u.user", sep='|', names=["user id", "age", "gender", "profession", "zipcode"])

mat = data.pivot(*data.columns)

mat = mat.fillna(0)

mat

R = np.array(mat)

"""# Functions"""

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):

    error_track = []
    Q = Q.T
    
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:

                    # Calculate error
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])

                    # Step weights
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        eR = np.dot(P,Q)
        e = 0

        # Calculate total error
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )

        print("Step:", step, "Error:", e)
        error_track.append(e)

        # Early stopping
        if e < 0.001:
            break
    return P, Q.T, error_track

# Top N predicted user error
def topNerror(N, nR, R):
  prederror = 0

  for i, ratings in enumerate(nR[:5]):
    ratingidx = np.where(R[i] != 0)

    prederror = prederror + (R[i][ratingidx] - ratings[ratingidx]).sum()

  return prederror

def returnpredictions(movies, R, nR, userid):
  userid = userid-1

  # Get Movie Index of previously rated movies
  userpred = R[userid] #[np.where(R[userid] != 0)]
  toppredidx = np.argsort(userpred)[-10:]

  # Get Movie Index of newly rated movies
  recs = nR[userid].copy()
  recs[np.where(R[userid] != 0)] = 0
  nonpredidx = np.argsort(recs)[-10:]

  # Return top 10 ratings (previously selected)
  favorites = movies.loc[toppredidx, :]

  # Return top 10 ratings (reccomended)
  reccomendations = movies.loc[nonpredidx, :]

  return favorites, reccomendations

"""# Predict Movie Recommendations

- Train Varied Dataset Sizes
- Predict same users over different tests, comment on similarity
- Record per-user accuracy

### 5-user, 50-item Factorization
"""

# Train and plot curves
R1 = R[0:5, 0:50]

N = len(R1)
M = len(R1[0])
K = 2

P = np.random.rand(N,K)
Q = np.random.rand(M,K)

start = time.time()
nP, nQ, error = matrix_factorization(R1, P, Q, K)
end = time.time()
print("Elapsed Time:", end - start)

nR1 = np.dot(nP, nQ.T)

steps = np.arange(0, 5000, 1)
plt.plot(steps, error)
plt.xlabel('Step')
plt.ylabel('Error')
plt.title('Training Loss - 5 users, 50 items')

topNerror(5, nR1, R1)

toprated, reccomended = returnpredictions(movies, R1, nR1, 1)

toprated

reccomended

"""### 5-user, 150-item Factorization


"""

# Train and plot curves
R2 = R[0:5, 0:150]

N = len(R2)
M = len(R2[0])
K = 2

P = np.random.rand(N,K)
Q = np.random.rand(M,K)

start = time.time()
nP, nQ, error = matrix_factorization(R2, P, Q, K)
end = time.time()
print("Elapsed Time:", end - start)

nR2 = np.dot(nP, nQ.T)

steps = np.arange(0, 5000, 1)
plt.plot(steps, error)
plt.xlabel('Step')
plt.ylabel('Error')
plt.title('Training Loss - 5 users, 150 items')

topNerror(5, nR2, R2)

toprated, reccomended = returnpredictions(movies, R2, nR2, 1)

toprated

reccomended

"""### 30-user, 50-item Factorization


"""

# Train and plot curves
R3 = R[0:30, 0:50]

N = len(R3)
M = len(R3[0])
K = 2

P = np.random.rand(N,K)
Q = np.random.rand(M,K)

start = time.time()
nP, nQ, error = matrix_factorization(R3, P, Q, K)
end = time.time()
print("Elapsed Time:", end - start)

nR3 = np.dot(nP, nQ.T)

steps = np.arange(0, 5000, 1)
plt.plot(steps, error)
plt.xlabel('Step')
plt.ylabel('Error')
plt.title('Training Loss - 30 users, 50 items')

topNerror(5, nR3, R3)

toprated, reccomended = returnpredictions(movies, R3, nR3, 1)

toprated

reccomended

"""### 30-user, 150-item Factorization


"""

# Train and plot curves
R4 = R[0:30, 0:150]

N = len(R4)
M = len(R4[0])
K = 2

P = np.random.rand(N,K)
Q = np.random.rand(M,K)

start = time.time()
nP, nQ, error = matrix_factorization(R4, P, Q, K)
end = time.time()
print("Elapsed Time:", end - start)

nR4 = np.dot(nP, nQ.T)

steps = np.arange(0, 5000, 1)
plt.plot(steps, error)
plt.xlabel('Step')
plt.ylabel('Error')
plt.title('Training Loss - 30 users, 150 items')

topNerror(5, nR4, R4)

toprated, reccomended = returnpredictions(movies, R4, nR4, 1)

toprated

reccomended

"""# Demographic Clustering
- Take a couple users and find their closest matches (before and after factorization), compare demographic
"""

target = R3[0]
similarity = []

for i in R3:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]

target = nR3[0]
similarity = []

for i in nR3:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]

target = nR3[6]
similarity = []

for i in nR3:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]

target = R3[6]
similarity = []

for i in R3:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]

target = R4[0]
similarity = []

for i in R4:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]

target = nR4[0]
similarity = []

for i in nR4:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]



target = nR4[2]
similarity = []

for i in nR4:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]

target = R4[6]
similarity = []

for i in R4:
  similarity.append(abs(i-target).sum())

top5 = np.argsort(similarity)

demo.iloc[top5[:10]]