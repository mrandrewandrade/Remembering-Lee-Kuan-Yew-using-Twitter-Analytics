#Quick and dirty way of find the frequency of tweets from a csv of just tweet content
library("plyr")
data <- read.csv("2015-03-29.csv")
df<- data.frame(data$Posted.Content)
#regex to find all URLs in tweets
#testing <-gsub("\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))", "", df$data.Posted.Content)
#regex to find times in tweets
#\d{2}:\d{2}
freq_tweets<- ddply(df,.(data.Posted.Content),nrow)
newdata <- freq_tweets[order(-freq_tweets$V1),] 
write.csv(newdata,file="2015-03-29 tweet_freq.csv")
