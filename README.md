# Short text corpus with focus on humor detection
This repository was created for publication of the datasets useful for humor recognition in one-liners. This repository contains five datasets and the python code used in the process of gathering the datasets. 
The five datasets are the following:

1. Humorous Oneliners
    Filename: humorous_oneliners
    Filetype: .pickle
    Size: 5251 items
    Sources: Twitter, www.textfiles.com/humor/
    Short description: This dataset contains humorous oneliners (short jokes), which can be used as positive samples for humor recognition tasks. Oneliners that had a Jaccard similarity coefficient higher than or equal to 0.9 were removed from dataset 2 to result in this dataset. Disclaimer: Some of the jokes may be racist, homophobic or insulting in another way.

2. Humorous Oneliners (before removing duplicate jokes)
    Filename: oneliners_incl_doubles
    Filetype: .pickle
    Size: 5416 items
    Sources: Twitter, www.textfiles.com/humor/
    Short description: This dataset contains humorous oneliners (short jokes), which can be used as positive samples for humor recognition tasks. Deduplication has not been applied on this data yet, meaning this dataset includes (near-)duplicate oneliners. Disclaimer: Some of the jokes may be racist, homophobic or insulting in some other way.

3. English Proverbs
    Filename: proverbs
    Filetype: .pickle
    Size: 1019 items
    Sources: http://www.citehr.com/32222-1000-english-proverbs-sayings-love-blind.html, http://www.english-for-students.com/Proverbs.html
    Short description: This dataset contains a large part of existing English proverbs. Deduplication has been applied to remove duplicate proverbs.

4. Reuters Headlines
    Filename: reuters_headlines
    Filetype: .pickle
    Size: 5243 items
    Sources: Twitter
    Short description: This dataset contains headlines tweeted by international press agency Reuters. Retweets were excluded for pre-processing purposes and to ensure the original source is known. Since the Twitter API only allows us to retrieve up to 3200 tweets (including retweets) from a single user account, we scraped tweets from multiple Reuters Twitter accounts: Reuters, ReutersWorld and ReutersUK. The first covers Reuters' top news, the second one news from all over the world and the third one news from the UK. The tweets from Reuters (Top News) were posted between the 4th of January and the 26th of February. The tweets retrieved from Reuters World news date from January 19th to March 2nd. Finally, the Reuters UK news headlines included in the dataset contain tweets sent between December the 24th and March the 3rd.

5. Wikipedia sentences
    Filename: wiki_sentences
    Filetype: .pickle
    Size: 5251 items
    Sources: http://www.cs.pomona.edu/~dkauchak/simplification/
    Short description: Visit source URL
