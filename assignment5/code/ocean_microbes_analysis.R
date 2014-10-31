library(ggplot2)
library(caret)
library(rpart)
library(randomForest)
library(e1071)
library(dplyr)

# Load the data
seaflow_dat <- read.csv("seaflow_21min.csv")

summary(seaflow_dat)

# Split the data into training and test sets
groups <- createDataPartition(seaflow_dat$pop, 2)
train_dat <- seaflow_dat[groups[[1]], ]
test_dat <- seaflow_dat[groups[[2]], ]

summary(train_dat)
summary(test_dat)

# Plot pe against chl_small and color by pop
ggplot(data = train_dat, aes(x = chl_small, y = pe)) +
    geom_point(aes(colour = pop))

# Train a decision tree
fol <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)

model <- rpart(fol, method = "class", data = train_dat)
print(model)

# Test the decision tree
yhat <- predict(model, newdata = test_dat, type = "class")
sum(yhat == test_dat$pop)/length(test_dat$pop)
tree_table <- table(yhat, test_dat$pop)
tree_table

# Train a random forest model
model <- randomForest(fol, method = "class", data = train_dat, nodesize = 10)
print(model)

# Test the random forest model
yhat <- predict(model, type = "class", newdata = test_dat)
sum(yhat == test_dat$pop)/length(test_dat$pop)
rf_table <- table(yhat, test_dat$pop)
rf_table

# Train an SVM model
model <- svm(fol, data = train_dat)

# Test the SVM model
yhat <- predict(model, newdata = test_dat)
sum(yhat == test_dat$pop)/length(test_dat$pop)
svm_table <- table(yhat, test_dat$pop)
svm_table

# Remove data for file_id 208
seaflow_new <- seaflow_dat %>% filter(file_id != 208)

groups <- createDataPartition(seaflow_new$pop, 2)
train_new <- seaflow_new[groups[[1]], ]
test_new <- seaflow_new[groups[[2]], ]

# Retrain SVM
model_new <- svm(fol, data = train_new)

# Retest SVM
yhat <- predict(model_new, newdata = test_new)
sum(yhat == test_new$pop)/length(test_new$pop) - 0.922
