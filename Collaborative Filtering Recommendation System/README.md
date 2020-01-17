# What is it
just is a simple case of recommendation , completed by the method 'collaborative filtering recommendation'. It could be treated by as entry-level model in the recommendation field.

# Overview
#### Item-based collaborative filtering recommendation
- 0.one hot encoding process
- 1.cal the similarity between items
- 2.search the related items viewed by users in the past 
- 3.cal the similarity between the viewed items and related items

#### User-based collaborative filtering recommendation
- 0.got the user-item matrix first
- 1.acorrding to the neighbours of the Target Customer，cal the similarity
- 2.got the items list of the neighbours 
- 3.cal the similarity by calculating the items similarity of the Target Customer's items 

# Demodata
[u1.base](https://github.com/sladesha/machine_learning/tree/master/data)

# Dependencies
- math
