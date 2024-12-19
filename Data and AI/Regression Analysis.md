# Regression analysis

[Regression analysis](https://www.youtube.com/watch?v=zPG4NjIkCjc) is a set of statistical processes for estimating the relationships among variables in a dataset. It helps us study how the value of a *dependent variable* changes when any one of the *independent variables* or *explanatory variable* is varied. e.g. how profit on sales of a good changes on changing the good's profit margin or price.

[Linear Regression](https://towardsdatascience.com/multiple-linear-regression-with-math-and-code-c1052f3c7446) models the relationship between a scalar *dependent variable* `y` and one or more *independent variables* `x`. If there is only one *independent variable* it is called [Simple Linear Regression](https://en.wikipedia.org/wiki/Simple_linear_regression)

Linear regression entails finding the best line for your data based on the equation `y = mx + b` where `m` is the slope and `b` is the line's *y-intercept*. Some of the data points will fit closely with this line whereas there may be few outliers. The idea is to minimise the error between the outliers and the line (estimated value) using a *minimising function*.

Sum of Squares Error (SSE) = Sum(y - y^)2 where y = actual y^ = estimated

## Least square method

https://www.youtube.com/watch?v=JvS2triCgOY

## Gradient Descent

Calculate the error for a set of points from the best line the points (data) can be plotted upon. Each iteration will update `m` and `b` to a line that yields slightly lower error than the previous iteration.

https://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression
