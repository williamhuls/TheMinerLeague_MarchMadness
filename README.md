# TheMinerLeague_MarchMadness

###### A submission for MinneAnalytics Madness (Student Data Science Challenge co-hosted by the UST Data Science & Analytics Club).  http://minneanalytics.org/minnemudac-spring-2021/ 
####
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [About the Model](#about-the-model)

## General info

This project was created as a submission to the MinneMudac Student Data Science Challenge. The goal of the challenge was to create a predictive model for the 2021 March Madness Tournament.  Our model can be run with everything contained in this repository. 
	
## Technologies
Project is created with:
* Python version: 3.9.0
* Pandas version: 1.1.4
	
## Setup
To run this project, install it locally into a folder. Open a python terminal with the folder as the working directory and run:

```
$import march
```
To calculate the Elo scores for each team and export them to a csv, run:
```
$march.runSeason()
```
The csv file will be titled "Elo Ratings.csv" and will be located in the results folder.

  
## About the Model

We created a variation of an Elo rating system. All teams started with the same rating at the beginning of the season. After each game throughout the season, the team's rating was updated. The severity and direction of the update varied depending on the outcome(W/L), the Elo rating of their opponent, and the team's end of season RPI. To select the head-to-head matchups in the March Madness tournament, we compared the two teams' Elo ratings and picked whichever was higher.  
  
We picked this model because it is both powerful and easy for anyone to understand. If a team wins, they should be upgraded, and downgraded if they lose. A bad team should not be downgraded as much if they lose to a good team, while a good team should be downgraded more if they lose to a bad team. Strength of schedule is very important when predicting college basketball, because the level of skill varies widely from conference to conference. Our model is based around both of those ideas: weighted winning/losing (traditional Elo) & strength of schedule (RPI calculated by the NCAA). This model is a good way to evaluate past performance and will likely be a good predictor for future performance.  
  
### How the Ratings work:

#### The Data:
The model uses data from two tables.  
* [data/teams.csv](data/teams.csv)
  *  Located in the data folder, it lists every Division I (DI) team (plus some).  If a DI team played a non-DI team, that non-DI team exists in this table.  A row represents a team.  Attached to each team is two values:
    *  Their preseason Elo rating. Every teams starts the season at 1500.
    *  Their RPI on 3/18/2021 * 1000 (https://www.teamrankings.com/ncb/rpi/?date=2021-03-18).  The value range is 1-1000.  Any non-DI team in the table was assigned a 1. RPI is a way to factor in the strength of a teams schedule.  More information on how RPI is calculated here: https://en.wikipedia.org/wiki/Rating_percentage_index.  
  
  
| Column Name   | Type          | Description | 
| ------------- | ------------- | ------------|
| name          | string        | the name of the team |
| elo           | int           |  all initialized at 1500|
| rpi           | int (1-1000)  | NCAA RPI score on 3/18/2021|

* [data/2021games](data/2021games.csv)
  *  Located in the data folder, it contains the outcome of of every game in the 2020-2021 season.  A row represents a game.  A game contains a date, a winner and a loser. The game data was found here: https://www.masseyratings.com/scores.php?s=320158&sub=11590&all=1.
  
| Column Name   | Type          | Description |
| ------------- | ------------- | ------------|
| date   | string   | day of the game |
| win_team | string  |  the name of the team that won  |
| lose_team | string | the name of the team that lost |
  
#### The Calculation:
* [march.py](march.py)
  * Running runSeason() calculates the Elo scores for each team.  It does this by iterating through every game found in 2021games.csv. Both team's Elo scores are updated after each game.  The calculation for the winning team is different than the losing team, and this is conceptually the hardest part of the model.  For the winning team:
    * new_elo = old_elo + [k * (1 - expected_win) * (winner_rpi/1000)]
  * For the losing team:
    * new_elo = old_elo - [k * (expected_win) * (1- (loser_rpi/1000))]
  * This equation contains the traditional Elo system equation, and pro-rates the amount it changes based on RPI.  A tradition Elo system only changes old_elo by (k * (expected_win)) and (k * (1 - expected_win).  More on a traditional Elo system can be found here: https://en.wikipedia.org/wiki/Elo_rating_system.  A winning team's Elo will always rise after a win.  How much it rises depends on the probability of them winning (expected_win).  Our model also factors in strength of schedule in the form of RPI, pulled from teams.csv and the number does not change throughout this model.  Here, a winning team's Elo is affected greater if their RPI is higher.  On the flipside, a losing team's Elo decreases more if they have a low RPI.
  *  Our variable expected_win is calculated like a traditional Elo system.  It gives the expected probability for an outcome.  A good team will have a higher expected_win against a bad team.  Their opponents probability of winning is (1 - expected_win).  expected_win is calculated as: 
     * expected_win = 1/ [ 1 + 10 ^ (elo_loseing_team - elo_winning_team)/(elo_width)]
  *  Other variables used are somewhat arbitrary- all Elo scores are relative specifically to this system. The values alues used in this model are:  
  
| variable   | value          | Description | 
| ------------- | ------------- | ------------|
| initial elo   | 1500   | starting point for all teams |
| k | 64  |  the maximum amount at which a team's rating can change from one outcome  |
| elo_width | 400 | TODO | 

#### The Results
  
  * 'Elo Ratings.csv'
    * The results of the Elo rating calculations are put into a csv file.  This file is created after running the runSeason() method in [march.py](march.py).  The teams are sorted by the best Elo rating to the worst. There are three columns:
  
| Column        | Type          | Description |
| ------------- | ------------- | ------------|
| #1 (unnamed)  | int           | team rank (1 being the best) |
| team          | string        |  the name of the team  |
| elo           | double        | the calculated elo rating (no units) |
  
  
  *  [results/bracket.pdf](results/bracket.pdf)
     * To select the winner of each matchup in the tournament, we compared the team's Elo ratings.  The team with the higher rating won that head-to-head matchup.  This pdf shows the bracket resulting from our methodology. 
