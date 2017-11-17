reddit <- read.csv('reddit.csv')
levels(reddit$income.range)

install.packages('ggplot2')
library(ggplot2)
tShirts <- factor(c('medium', 'small', 'large', 'medium', 'large', 'large'), levels = c('medium','small','large'))
tShirts
qplot(x = tShirts)
tShirts <- ordered(tShirts, levels = c('small', 'medium', 'large'))
tShirts
qplot(x = tShirts)

qplot(x = reddit$age.range)
reddit$age.range <- ordered(reddit$age.range, c('Under 18', '18-24', '25-34', '45-54', '55-64', '65 or Above'))
qplot(x = reddit$age.range)