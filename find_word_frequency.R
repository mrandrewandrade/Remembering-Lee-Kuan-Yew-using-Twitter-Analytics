#Find the frequency of words to use in word cloud

library(RCurl)
library(RJSONIO)
library(stringr)
library(tm)
library(wordcloud)
library(SnowballC)

data <- read.csv("tweets_cleaned.csv")
data$Date <- as.Date( as.character(data$Date), "%d/%m/%Y")
initial_date = min(data$Date)
end_date = max(data$Date)

days <- seq(from=initial_date, to=end_date,by='days' )
for ( iii in seq_along(days) )
{
    folder_name <- paste(toString(days[iii]),"/", sep = "")
    tweet_content <- Corpus (DirSource(folder_name))
    tweet_content <- tm_map(tweet_content, stripWhitespace)
    tweet_content <- tm_map(tweet_content, PlainTextDocument)
    
    #day_1 <- tm_map(day_1, removeWords, stopwords("english"))
    #day_1 <- tm_map(day_1, stemDocument)
    
    a.dtm1 <- TermDocumentMatrix(tweet_content, control = list(wordLengths = c(3,10)))
    findFreqTerms(a.dtm1, 10)
    m <- as.matrix(a.dtm1)
    v <- sort(rowSums(m), decreasing=TRUE)
    file_name<- paste(toString(days[iii]),"_word_freq.csv", sep = "")
    write.csv(v,file=file_name)
}
