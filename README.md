# Math 390 Final Project

## Introduction
With the recent rise of rest days in the NBA, I have noticed an increasing number of game day additions to Injury Reports. This late additions tend to cause big swings in the betting lines for given games. Top NBA players like Joel Embiid, Stepth Curry, and Giannis Antetokounmpo being ruled out can cause line shifts of upwards of 5 points. However, often times, this doesn't seem like enough to capture the true value of the player to his respective team. Just 4 weeks ago a Sixers team missing Tobias Harris and Ben Simmons was favored against the Knicks by 4.5 points. That was before, however, Joel Embiid was ruled out for rest. Afterwards the line shifted to Knicks -2. Against a roster with very little tallent that line stuck out to me as weirdly low. Ultimatley the Knicks ended up winning the game 103-97, covering the new spread. This sparked an interest in seeing if there was anything that could be learned from this game for future games.

## Research Question
To properly analyze if the events on November 8th were just a one off occurance or part of a larger pattern surrounding NBA lines not shifting enough to compensate for the loss of key players I intended to answer a key question: Did NBA teams cover spreads at a disporportionate rate when their openent was missing a key player?

## Method
To answer my question I gathered data from sportsbookreviewsonline.com which contained the opening and closing lines for nba games as well as the outcome. From there I began to analyze that data to help me answer my question. The first thing I looked at was the distibution of line shifts. Then I calculated the cover percentage of teams when a line shifted by a certain number of points. While teams covered at a higher percentage than expected this did not capture the true intent of my question, analyzing betting trends when a key player was injured. I attempted to use Twitters API's to accesss tweets from various accounts that I know to cover NBA injury news but was uncessful due to the complex nature of the Twitter API, my sub par coding skills, and the limits on how many Tweets could be sourced. I then found the `NBA_API` package which contained box scores for every game including inactive players. Since the box scores were only accessible by game ID number I first had to generate a list of all games from the package so that I could then merge them with my existing odds data frame and be able to create a new column for all the inactive players. The was a very tedious process as the `NBA_API` package only let me access around 100 games at a time without creating an error message. As a work around I downloaded the information for around 100 games at a time and created csvs containing the games players missed. From there, I created a new column(`Key Player Out`) which checked if any of the inactive players were in the top 50 in BPM, sourced from basketball reference. I then ran the same analysis seeing the performance of teams against the spread when a key player was missing from there opponent given a shift of a certain number of points. This produced very significant results. When a key player was out there was a 55.7% success rate of team covering spreads that had shifted 2+ points worse (a team going from -4 to -6 for example). While I was happy with that result given the profitably threshold on standard -110 lines is 52.38%, I was left to wonder what would happen if I could issolate only the games where I player was ruled out on game day. While I theorized that a key play being out in conjunction with a line shift would likely capture this effect, since the teams performed much better when taking 'Key Player Out' into affect I attempted to better estimate when a player was ruled out on game day by only looking for players who missed the prior game. To do this I had to determe which row in my dateframe contained the previous game for a team. This was something I struggled with since half for half the games for a team were in the `Away Team` column and the other half in the `Home Team` column. I created two seperate dataframes and then added a new column `Team` which had the name of the home or road team for each dataset respectively. I merged the two data sets which allowed me to find the previous game for all teams. From there I used the shift function to have a new column called `Prev Out` which was the players out in the previous game for the team. I then created the `New Out` column to see which players that had played in the previous were innactive for the following game. I also changed the criteria of a Key Player to top 40 in BPM after some trial and error. I then ran the same analysis checking the performace and much to my delight taking into account only when a key player played the game before but not the current game, a better proxy for late innactives, when the line shifted 2+ points teams covered the new spread at a 58.2% rate.

## Questions for further Analysis 
While I was very happy with my results there are still a few things I would like to further investigate. First, while I believe a line shift in conjuction with a player who didn't play the game before is a good proxy for a game day innactive I would like to be able to get the correct data of when I player was ruled out. Furthermore, one possible bias within my model was I used the end of season BPM for each year. This could introduce bias since if you were actually betting based on this system you would only have access to the current BPM numbers not future ones for the rest of the season. I did check what would happened if I used the prior season's BPM number and the model was still sucessful (55.9%). I also would like to know how the system worked in prior seasons. Since the data was not easily accessible I only generated the inactive players information for the prior two seasons. I also would like to look into the right way to define a Key NBA player. While I tried using different cutoff points and also using the best player on a team there are still plenty of more options to check.

## Conclusion
Despite my lingering questions, I ultimately feel confident concluding that my inital hypothesis, the shift in lines is not enough to make up for the loss of a key player, was correct. Not only do lines not shift enough but they allow for the bettor to gain a significant edge. Using this system a bettor can profit 11% on their bets.
