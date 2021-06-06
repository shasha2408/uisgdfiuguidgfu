# -*- coding: utf-8 -*-
"""Time Series classification PCA & Randf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iKzUmVTR1wDtLcdzdvdaLqIUqL2MiIza
"""

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier 

# Tinme series classification using Support Vector Machine

def PCA_RandF(train,test):
   # information of train and test set
  def dataset_stats(train,test):
    train.info()
    test.info()
    return

   # spliting the train and test data in inputs and outputs. 
    def train_test_split(train,test):  
       x_train = train.iloc[:,1:]
       y_train = train.iloc[:,0]
       x_test = test.iloc[:,1:]
       y_test = test.iloc[:,0]
       print("x_train Shape :: ", x_train.shape)
       print("y_train Shape :: ", y_train.shape)
       print("x_test Shape :: ", x_test.shape)
       print("y_test Shape :: ", y_test.shape)
       return  x_train,x_test,y_train,y_test

    # data scaling of Train nd test variables
       def data_scaling(x_train,x_test):
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_test_scaled  = scaler.fit_transform(x_test)

        return x_train_scaled,x_test_scaled

        def eigenvec_eigenval(data):
          # caslculating mean vector of training datatset

          mean_vec = np.mean(data, axis=0)

          # covariance matrix

          cov_mat = np.cov(data.T)

          eig_vals, eig_vecs = np.linalg.eig(cov_mat)

          # Create a list of (eigenvalue, eigenvector) tuples
          eig_pairs = [ (np.abs(eig_vals[i]),eig_vecs[:,i]) for i in range(len(eig_vals))]

          # Sort the eigenvalue, eigenvector pair from high to low

          eig_pairs.sort(key = lambda x: x[0], reverse= True)

          # Calculation of Explained Variance from the eigenvalues

          tot = sum(eig_vals)

          # Individual explained variance

          var_exp = [(i/tot)*100 for i in sorted(eig_vals, reverse=True)]

          cum_var_exp = np.cumsum(var_exp)  # Cumulative explained variance 

          # Find the eigenvector beyond which 95% of the data is explained

          return cum_var_exp

          #  cummulative explained variance ploting
          def plot_cum_var_exp(cum_var_exp):
            sns.set(style='whitegrid')
            plt.plot(cum_var_exp)
            plt.xlabel('number of components')
            plt.ylabel('cumulative explained variance')
            display(plt.show())
            return

            #calculating the principal components of tha data
            def Prin_components(cum_var_exp):
              p = [ n for n,i in enumerate(cum_var_exp) if i>95 ][0]
              print('no.of principal components', p)
              return p

              #Reducing the train and test dimension to Principal components
              def pca_data(x_train_scaled,x_test_scaled,p):
                pca = PCA(n_components = p)
                pca.fit(x_train_scaled)
                x_train_pca= pca.transform(x_train_scaled)
                pca.fit(x_test_scaled)
                x_test_pca = pca.transform(x_test_scaled)
                print(x_train_pca.shape)
                print(x_test_pca.shape)
                return x_train_pca,x_test_pca,p

                # Model training and evaluation
                def RandF_clf(x_train_pca,y_train):
                  from sklearn.ensemble import RandomForestClassifier
                  Rf = RandomForestClassifier(random_state=1)
                  Rf.fit(x_train_pca,y_train)
                  predictions = Rf.predict(x_test_pca)
                  return Rf, predictions

                  # Evaluating model on test Data
                  def evaluation(y_test,predictions):
                   acc_test = accuracy_score(y_test, predictions)
                   print('Test Accuracy: %.2f' % acc_test)
                   print(classification_report(y_test, predictions)),
                   cm=metrics.confusion_matrix(y_test,predictions)
                   ax= plt.figure(figsize=(8,4))
                   ax= plt.subplot()
                   ax.set_xlabel('Predicted class');ax.set_ylabel('True class'); 
                   ax.set_title('Confusion Matrix__PCA__RandF'); 
                   sns.heatmap(cm, annot=True, fmt='g', ax=ax); 
                   ax.xaxis.set_ticklabels(['Normal', 'Abnormal']); ax.yaxis.set_ticklabels(['Normal', 'Abnormal']);
                   plt.show()
                   return

                   #Crossvalidation and Finding the best parameter using GridSearch
                   def GRid_search(x_train_pca,y_train):
                    Rfc = RandomForestClassifier()
                    scores = cross_validate(Rfc, x_train_pca,y_train, cv=5, scoring=['accuracy'], return_train_score=True)
                    param_grid = { 'n_estimators': [200, 500],'max_depth' : [6,7,8,9,10]}
                    CV_rfc = GridSearchCV(Rfc, param_grid=param_grid, cv= 5)
                    final_model = CV_rfc.fit(x_train_pca, y_train)
                    CV_rfc.best_params_
                    CV_rfc.best_score_
                    print('Train accuracy: ', scores['train_accuracy'])
                    print('Test accuracy: ', scores['test_accuracy'])
                    return final_model