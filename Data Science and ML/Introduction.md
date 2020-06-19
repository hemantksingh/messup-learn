# Machine Learning

Traditional programming is about defining the steps to achieve an outcome.  Machine learning defines the outcome in the data & letting your algorithm learn the steps to get there.

Given a dataset, ML is used to make sense of the data by finding patterns in the data. Patterns could be found by a human just looking at the data if the dataset is small or by using an **algorithm** e.g. linear regression `y = mx + b` to fit points to a line. The values of `m` and `b` are derived mathematically using an algorithm to best fit the line, thus giving you a **model** like `y = 10x + 4` that can recognize patterns. Applications can then supply new data to the model to see if the new data matches this known pattern based on the value of `m` and `b`.

## Machine learning and data science

Data science and machine learning [share a lot of common ground](https://www.analyticsvidhya.com/blog/2019/10/mathematics-behind-machine-learning/) but there are subtle differences in their focus on mathematics. In data science our primary goal is to explore and analyse the data, generate hypotheses and test them. On the other hand, Machine learning focuses more on the concepts of [Linear Algebra](https://www.analyticsvidhya.com/blog/2017/05/comprehensive-guide-to-linear-algebra/?utm_source=blog&utm_medium=mathematics-behind-machine-learning) as it serves as the main stage for all the complex processes to take place. Multivariate calculus, or partial differentiation to be more precise - the driving force behind most machine learning algorithms is used for the mathematical optimisation of a given function (mostly convex).

Mathematical optimization - maximizing or minimizing a real function by systematically choosing input values from within an allowed set and computing the value of the function.

[Derivatives in differential calculus](https://www.youtube.com/watch?v=rAof9Ld5sOg) - rate of change of a function e.g. f(x) = x 2 and finding the slope of a curve.

Broadly there are [3 types](https://www.analyticsvidhya.com/blog/2017/09/common-machine-learning-algorithms/) of machine learning algorithms:

## Supervised

A labelled dataset (with complete class information available) is given to the data model. Each dataset has a set of **feature values** and the value that we want to predict. The model gets feedback on what is correct and what is not. The mapping between the data and the label helps in **classification**.

e.g.

* Predicting the price of a house, houses could be classified into new 2 bedroom houses built after 2010. This classification can then provide a price.
  
```javascript
    {
      price: 98000,
      size: 2255,
      bedrooms: 3,
      yearbuilt: 2010
    }
```

* Detecting fraud in a set of financial transactions.

* Classifying the type of car in an image.

## Unsupervised

Most data is unstructured, complex and unlabelled (with no available class information), so we do not always have the privilege of classification based on labelled data. In unsupervised learning, groups of data that share the same traits are identified. The data model gets no feedback, it has to figure out the structure of the data by itself to perform a given task. This is harder to do but more convenient. [**Regression**](https://en.wikipedia.org/wiki/Regression_analysis) is often used for estimating the relationships amongst data variables.

In supervised learning you get feedback at every move (input/output pairs are present), whereas in the unsupervised approach you do not get feedback at all.

**Clustering** is an unsupervised machine learning technique. Data is grouped into a cluster: a group where all group members are similar in nature in some way and members of one cluster are dissimilar to the members of another cluster. e.g. *gene cluster*. Clustering can be very helpful with unlabelled data. It is used in applications like

* Document classification: Google news uses various clustering techniques to group news, posts and articles on the web.
* City planning, grouping houses by type, value, location.

`Input data + Number of clusters => Learning process => Clustered data`

## Reinforcement

Reinforcement learning is used to train machines to make specific decisions. The machine is exposed to an environment where it trains itself continually using trial and error. It involves finding a balance between exploration (of uncharted territory) and exploitation (of current knowledge).

The model gets feedback only when it has finished its goal. e.g. a machine playing chess would only get feedback if it wins or loses the game. For most part, the machine is trying to make moves that it thinks will win without knowing if they will. It gets zero reward until it finally wins the game. Thus, reinforcement learning is particularly well-suited to problems which include a long-term versus short-term reward trade-off. It has been applied successfully to various problems, including robot control, elevator scheduling, telecommunications and games.

## Deep learning

Neural networks one of the machine learning models/techniques used widely. When we use a neural network that is not just one or two layers but many layers deep to make a prediction we call that deep learning. It is a subset of machine learning that has outperformed almost every other type of model, almost every time on a huge range of tasks, but it needs a relatively large data set as compared to regression and classification.

### Recurrent Neural Network

Google translate used a bit
https://github.com/martin-gorner/tensorflow-rnn-shakespeare

Modify input weights and biases in order to minimise the deviation from the expected output.

### Activation function

* Sigmoid -  (0 to 1)
* Hyperbolic tangent - tanh (-1 to 1)

### LSTM - Long Short term memory

Mitigates the vanishing gradient problem

## ML Cloud APIs

* Speech API - convert speech to a transcript (text)
* Natural Language API - analyse the text
    * Extract entities (nouns) from the text
    * Sentiment analysis, analyse syntax
* Translate API - Google Translate is used by Air B&B to translate postings and reviews submitted in languages other than English.
* Neural Machine Translation - NY times

## Python ML Libraries

![python-ml-libraries.png](../Images/python-ml-libraries.png "Python ml libraries")