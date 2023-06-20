#!/usr/bin/env python
# coding: utf-8

# # Implementation of SVM _linear

# In[1]:


# Run this cell to get preprocessed data
get_ipython().run_line_magic('run', 'Dimension_Reduction.ipynb')


# In[3]:


# splitting dataset into training and testing part
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV
test_data_ratio=[0.3,0.25,0.2,0.15,0.1,0.05]
for i in test_data_ratio:
    print("******************Start of iteration******************\n")
    print("For rati0 ",i)
    X_train, X_test, y_train, y_test=train_test_split(final_data.iloc[:,:80],final_data['label'],test_size=i,shuffle=True)

    params_grid = [{'kernel': ['linear'], 'C': [1,5, 10, 100]}]
    svm_model = GridSearchCV(SVC(), params_grid, cv=5)
    svm_model.fit(X_train.iloc[:,0:80],y_train)
    print('Best score for training data:', svm_model.best_score_,"\n") 

    # View the best parameters for the model found using grid search
    print('Best C:',svm_model.best_estimator_.C,"\n") 
    print('Best Kernel:',svm_model.best_estimator_.kernel,"\n")
    print('Best Gamma:',svm_model.best_estimator_.gamma,"\n")
    final_model = svm_model.best_estimator_
    Y_pred = final_model.predict(X_test)
    print(confusion_matrix(y_test,Y_pred))
    print("\n")
    print(classification_report(y_test,Y_pred))
    print("Training set score for SVM_linear: %f" % final_model.score(X_train , y_train))
    print("Testing  set score for SVM_linear: %f" % final_model.score(X_test  , y_test ))
    print("******************End of iteration******************\n")

