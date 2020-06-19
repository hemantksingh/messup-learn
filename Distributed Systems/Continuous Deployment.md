# Separate Deployment from Release

Deployment -> Getting the application artifact on a server and validating the application runs

Release -> Revealing a feature to the end user

Having a clear distinction between deploying a feature and unveiling it to end users allows you to:

* manage deployment risk by deploying smaller changes frequently without necessarily turning on features, in case the changes interfere with other parts of the system or break the system all together
* rollback by switching features off without rolling back the deployment itself
* get quick customer feedback by unveling the feature to a subset of users

The steps to follow in order to get this separation are:

* Deploy your product
* See if it operates in a stable fashion
* Enable your feature for:
    * Segment of users
    * Random selected percentage
    * All
