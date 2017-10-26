# ElasticSearch groupassignment by
Pieter Kronemeijer 11064838<br>
Dico van Leeuwen 11075546<br>
Douwe van der Wal 110422206<br>
Laurens Weitkamp 11011629<br>

# Introduction
For the ElasticSearch assignment we made a searchengine website to search through all the UvA theses. This could be easily expanded with theses


# Link to presentation:
https://docs.google.com/presentation/d/1lkmAWZmtFy3g6WhaI--t2rL-VpRWA0U3klLjeKVphX4/edit?usp=sharing

# Link to live demonstration, available untill the third of november 2017:
http://pindakaas.ga:5000/searchpage 

Searching on this server is a bit slow due to a low end processor and low ram, but it works. 

# SERP page

What you did and why you choose to do it in your special way.

    todo

Examples of what works, and what does not work (very well).

    todo
    
An evaluation of the quality of your work in 3-4 sentences.
    
    todo

Clickable links to a live working demo are highly appreciated.
    
    todo
    
# Advanced search
What you did and why you choose to do it in your special way.

    todo

Examples of what works, and what does not work (very well).

    todo
    
An evaluation of the quality of your work in 3-4 sentences.
    
    todo

Clickable links to a live working demo are highly appreciated.
    
    todo
# Wordclouds
What you did and why you choose to do it in your special way.

    To create wordclouds we used the python library wordcloud. This takes as input a string, and outputs an image of a prespecified size filled with the most common words. We do this with the abstract only, since creating wordclouds is computationally expensive. To prevent common words such as "and" ending up in the wordcloud, we have a special list of words that should be filtered out. We know that a tf-idf approach would have worked better, but this approach consumes to much ram to be able to run the searchengine on our devices. 

Examples of what works, and what does not work (very well).

    Some abstracts are very short, up to merely 1 sentence, resulting in a rather empty wordcloud. For normal abstracts the wordcloud looks good and the main subjects of the thesis are very visible. 
    
An evaluation of the quality of your work in 3-4 sentences.
    
    The wordclouds are pleasing to eye and are created at a reasonable speed (at least for this project). The list of excluded words is an ugly solution to the problem, but it has been thorougly tested and seems to give good results. 

Clickable links to a live working demo are highly appreciated.
    
    When searching the wordclouds are very visable.
# Timeline
What you did and why you choose to do it in your special way.

    todo

Examples of what works, and what does not work (very well).

    todo
    
An evaluation of the quality of your work in 3-4 sentences.
    
    todo

Clickable links to a live working demo are highly appreciated.
    
    todo
# Faceted results
What you did and why you choose to do it in your special way.

    todo

Examples of what works, and what does not work (very well).

    todo
    
An evaluation of the quality of your work in 3-4 sentences.
    
    todo

Clickable links to a live working demo are highly appreciated.
    
    todo
# Kappa score
What you did and why you choose to do it in your special way.

    Our dataset is in both English and Dutch, due to difficulties combining these results we decided to do queries in just one language. 2 of the queries will be in English and 3 in Dutch. The results can be found below. One of the queries in each language will be an easy query and the rest will be a harder query.

Examples of what works, and what does not work (very well).

    N/A
    
An evaluation of the quality of your work in 3-4 sentences.
    
    Computing all the scores worked well and the search engine always returned results to the queries.

Clickable links to a live working demo are highly appreciated.
    
    N/A
