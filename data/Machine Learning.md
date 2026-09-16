# Machine Learning

There are two ways of programming computer systems. The traditional way is by defining the steps to achieve an outcome e.g. providing a recipie to the computer to perform a task. The other way is by providing the computer lots and lots of data and the computer learns to classify this data by ingesting this data. This method didn't catch on until recently because three things were missing: enough data, enough compute (GPUs) and algorithms that train well at scale. With the advent of the smart phones, social media we now collect lots and lots of data. 

Given a dataset, machine learning is used to make sense of  data by finding patterns in the data. Patterns could be found by a human just looking at the data if the dataset is small or by using an **algorithm**, for example fitting a line to points (see [Linear regression](#linear-regression) below), which gives you a **model** like `y = 10x + 4`. Applications can then supply a new `x` to the model to predict `y`.

A model is a mathematical relationship derived from data that an ML system uses to make predictions.

## Machine learning and data science

One framing (from Analytics Vidhya): data science and machine learning [share a lot of common ground](https://www.analyticsvidhya.com/blog/2019/10/mathematics-behind-machine-learning/) but there are subtle differences in their focus on mathematics. In data science our primary goal is to explore and analyse the data, generate hypotheses and test them. On the other hand, machine learning focuses more on the concepts of [Linear algebra](https://www.analyticsvidhya.com/blog/2017/05/comprehensive-guide-to-linear-algebra/?utm_source=blog&utm_medium=mathematics-behind-machine-learning) as it serves as the main stage for all the complex processes to take place. Multivariate calculus, or partial differentiation to be more precise - the driving force behind most machine learning algorithms is used for the mathematical optimisation of a given function (mostly convex).

Mathematical optimization - maximizing or minimizing a real function by systematically choosing input values from within an allowed set and computing the value of the function.

[Derivatives in differential calculus](https://www.youtube.com/watch?v=rAof9Ld5sOg) - rate of change of a function e.g. `f(x) = x²` and finding the slope of a curve.

Broadly there are [3 types](https://www.analyticsvidhya.com/blog/2017/09/common-machine-learning-algorithms/) of machine learning algorithms:

## Supervised

A labelled dataset (with complete class information available) is given to the data model. Each dataset has a set of **feature values** and the value that we want to predict. The model gets feedback on what is correct and what is not. The mapping between the data and the label is used for **classification** (a discrete label) and **regression** (a continuous value).

e.g.

* Regression: predicting the price of a house from its size, number of bedrooms and year built.
  
```json
    {
      price: 98000,
      size: 2255,
      bedrooms: 3,
      yearbuilt: 2010
    }
```

* Classification: detecting fraud in a set of financial transactions, or marking an email as spam.

* Classifying the type of car in an image.

* [Bloomberg](https://www.bloomberg.com/professional/tech-decoded/) reviews vast quantities of previously published news stories and social posts to assign a positive, negative or neutral score to each, giving investors a directional sentiment score, which they can use to understand the impact of the current news story or social post on the price of the security. They use Natural Language Processing (NLP) in making sense of the human language to read and decipher the data contained in words to reveal meaning in the data of the financial world. Sentiment scoring into fixed classes is supervised classification.

[**Regression**](https://en.wikipedia.org/wiki/Regression_analysis) is another supervised machine learning technique which is used to predict continuous values. It is often used for estimating the relationships amongst data variables. The ultimate goal of the regression algorithm is to plot a best-fit line or a curve between the data. See [Linear regression](#linear-regression) below.

## Unsupervised

A supervised approach is given data that contains the correct answer. The model's job is to find connections in the data that produce the correct answer. An unsupervised approach is given data without the correct answer. Its job is to find groupings in the data. In supervised learning the model can get feedback on the predicted value because expected input/output pairs are present, but in the unsupervised approach the model does not get any feedback at all, it has to figure out the structure of the data by itself to perform a given task.

Most data is unstructured, complex and unlabelled (with no available class information), so we do not always have the privilege of classification based on labelled data.

**Clustering** is an unsupervised machine learning technique. Data is grouped into a cluster: a group where all group members are similar in nature in some way and members of one cluster are dissimilar to the members of another cluster. e.g. *gene cluster*. Clustering can be very helpful with unlabelled data. It is used in applications like

* News clustering: Google News uses various clustering techniques to group news, posts and articles on the web into stories.

* City planning, grouping houses by type, value, location.

For k-means: `Input data + Number of clusters => Learning process => Clustered data`. Other algorithms such as DBSCAN or hierarchical clustering do not take the number of clusters as an input.

## Reinforcement

Reinforcement learning is used to train machines to make specific decisions. The machine is exposed to an environment where it trains itself continually using trial and error. It involves finding a balance between exploration (of uncharted territory) and exploitation (of current knowledge).

The model gets a reward signal from the environment. Rewards may be dense (a signal at every step, as in balancing a pole or controlling a robot) or sparse. Chess is a sparse-reward example: a machine playing chess would only get feedback if it wins or loses the game. For most part, the machine is trying to make moves that it thinks will win without knowing if they will. It gets zero reward until it finally wins the game. Thus, reinforcement learning is particularly well-suited to problems which include a long-term versus short-term reward trade-off. It has been applied successfully to various problems, including robot control, elevator scheduling, telecommunications and games.

## Model families

The three types above describe the learning problem. Model families are orthogonal: a neural network, a decision tree ensemble or a linear model can each be used in supervised, unsupervised or reinforcement settings.

### Deep learning

Neural networks one of the machine learning models/techniques used widely. When we use a neural network that is not just one or two layers but many layers deep to make a prediction we call that deep learning. It dominates perception (images, audio) and language tasks, but it needs a relatively large data set, and on tabular data gradient-boosted tree ensembles such as XGBoost and LightGBM remain strong and often match or beat it.

#### Recurrent Neural Network

Processes a sequence one element at a time, carrying a hidden state forward. Google Translate used LSTM-based recurrent networks from 2016 until Transformer models replaced them around 2020.
https://github.com/martin-gorner/tensorflow-rnn-shakespeare

Modify input weights and biases in order to minimise the deviation from the expected output.

#### Activation function

* Sigmoid -  (0 to 1)
* Hyperbolic tangent - tanh (-1 to 1)
* ReLU family - ReLU `max(0, x)` and variants such as GELU and SiLU. The default in deep networks since about 2012 because sigmoid and tanh saturate and cause vanishing gradients in deep stacks.

#### LSTM - Long Short term memory

Mitigates the vanishing gradient problem

#### Transformers

RNNs and LSTMs were the predecessors for sequence tasks. Transformers (2017) replace recurrence with **attention**: every position in the input can weigh every other position directly, so the model sees the whole sequence at once and trains in parallel. Inputs are first mapped to **embeddings**, dense vectors in which similar tokens sit close together. Large language models are transformers pre-trained by **self-supervised learning** on unlabelled text (predicting the next token or a masked token), then fine-tuned for specific tasks.

## ML Cloud APIs

* Speech API - convert speech to a transcript (text)
* Natural Language Processing (NLP) API - textual analysis
  * Extract entities (nouns) from text
  * Sentiment analysis
* Translate API - Google Translate is used by Airbnb to translate postings and reviews submitted in languages other than English.

## Data preparation

### Data transformation

Data transformation is a process of cleaning/preprocessing and transforming the raw data into meaningful information for AI algorithms. This ensures that AI models can learn effectively and produce accurate results without any abnormalities. Tools available for data transformation include:

* Use either Python libraries like `Pandas` (data frames), `NumPy` (scientific computing), `Matplotlib` (2d plotting), or R for data statistical analysis to clean the noisy data you have collected.
* Use libraries like `Scikit-learn` to perform preprocessing functions on the data, such as scaling and encoding or normalisation, while the TensorFlow Data API is great for building data pipelines.
* For supervised learning model development, you would require annotated data. Labelbox, Dataloop, or custom Python libraries are just some examples of data labelling programmes that can generate labelled datasets very effectively.
* Use libraries like `Albumentations` for image data augmentation or NLP augmentation tools for text data to increase model performance.

Keep track of when the data changes or is updated. Use tools such as DVC (Data Version Control) or Git LFS to version the data and ensure reproducibility

### Ensuring Data Quality

Data quality is one of the main factors that contribute to the successful deployment of ML. The better the data, the more efficient the models are to produce accurate and reliable responses. Ensuring data quality involves rigorous validation, consistent updating and thorough vetting of data sources to eliminate errors and biases.

Poor-quality data can lead to inaccurate models and misguided outcomes, undermining the potential benefits of AI.Therefore, it’s crucial to implement data quality management measures to use AI/ML systems more efficiently and securely.

## Linear regression

Regression estimates how a dependent variable `y` changes when independent variables `x` change, for example how sales volume responds to price. With one input it is simple linear regression: find the line `y = m·x + b` that best fits the points.

"Best" means the line that minimises the **sum of squared residuals** over all points, `SSE = Σ (yᵢ − ŷᵢ)²`, where `ŷᵢ` is the line's prediction. Every point counts, not just the outliers; outliers actually distort least squares, which is why robust regression exists.

Two ways to find `m` and `b`:

* **Ordinary least squares** has a closed-form answer (`m = cov(x, y) / var(x)`, `b = ȳ − m·x̄`). No iteration needed for a linear model.
* **Gradient descent** starts from a guess and repeatedly moves `m` and `b` a small step (the learning rate) in the direction that reduces SSE. It is what you use when there is no closed form, or when the data is too large to solve directly.
