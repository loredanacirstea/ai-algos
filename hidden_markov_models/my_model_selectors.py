import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        
        best_score = np.float('Inf') 
        best_model = None
        
        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                logL = model.score(self.X, self.lengths)
                
                # Number of features
                features = len(self.X[0])
                
                # Number of parameters
                # transistion probs = n*n
                # means = n*features
                # covars = n*features
                p = n**2 + 2 * n * features - 1
                # p = n*(n-1)+2*features*n
          
                # self.X.shape[0] = number of data points
                score = (- 2 * logL) + (p * np.log(self.X.shape[0]))
                
                # Take the lowest BIC score
                if score < best_score:
                    best_score, best_model = score, model                
            except:
                pass
            
        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        
        best_score = np.float('-inf')
        best_model = None
        
        for n in range(self.min_n_components, self.max_n_components+1):
            model = self.base_model(n)
            
            try:
                # Current word log likelihood
                current_logL = model.score(self.X, self.lengths)

                # Sum of the log likelihoods for all the other words 
                logL_sum = 0  
                for word in self.words:
                    if word == self.this_word: 
                        continue
                    X, lengths = self.hwords[word]
                    logL_sum += model.score(X, lengths)

                # DIC score is the difference between the current word logL
                # and the average logL of all other words
                score = current_logL - logL_sum / (len(self.words) - 1)
                
                # Choose the biggest score because we want the model to not overfit,
                # therefore it should output different logL for the other words
                if score >= best_score:
                    best_score, best_model = score, model
            except:
                pass

        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_model = None
        best_logL = np.float('-inf')
        # Cannot have number of splits greater than the number of samples
        # k-fold cross-validation requires at least one train/test split by setting n_splits=2 or more
        splits = 3 if len(self.sequences) >= 3 else len(self.sequences)
        if splits == 1:
            return self.base_model(self.n_constant)
        split_method = KFold(splits)
        # Array of log likelihoods
        logL = []
        # Best number of hidden states
        best_n = self.min_n_components
        
        for n in range(self.min_n_components, self.max_n_components+1):
            scores = []
            
            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                # Combine subsets based on the indices given for the folds
                train_X, train_lengths = combine_sequences(cv_train_idx, self.sequences)
                test_X, test_lengths = combine_sequences(cv_test_idx, self.sequences)
                
                try:
                    model = GaussianHMM(n_components=n, covariance_type="diag", n_iter=1000, random_state=self.random_state, verbose=False).fit(train_X, train_lengths)
                    
                    # Calculate log likelihood
                    logL = model.score(test_X, test_lengths)
                    scores.append(logL)
                except:
                    pass
                     
            # Average log-likelihood
            average = np.average(scores) if len(scores) > 0 else float("-inf")
            
            # Update best log likelihood and best number of hidden states
            if average > best_logL:
                best_logL = average
                best_n = n
        
        # Build the model with the number of hidden states that gave the best log likelihood
        return self.base_model(best_n)
        