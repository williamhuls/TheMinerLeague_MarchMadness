import csv
import pandas as pd

elo_width = 400
k_factor = 64
    
def runSeason():
    teams = pd.read_csv('data/teams.csv')           #every teams elo score was set at 1500 to begin the season
    games = pd.read_csv('data/2021games.csv')       #sorted chronologically already

    for index, row in games.iterrows():
        winnerName = row['win_team']
        loserName = row['lose_team']
        winnerIndex = teams.index[teams['name'] == winnerName].tolist()[0]
        loserIndex = teams.index[teams['name'] == loserName].tolist()[0]

        new_elos = update_elo(teams['elo'][winnerIndex], teams['elo'][loserIndex], teams['rpi'][winnerIndex], teams['rpi'][loserIndex])

        teams.loc[winnerIndex, 'elo'] = new_elos[0]        
        teams.loc[loserIndex, 'elo'] = new_elos[1]
    del teams['rpi']
    rankings = teams.sort_values(by= 'elo', ascending=False)
    rankings.reset_index(drop = True, inplace = True)
    rankings.index += 1 
    rankings.to_csv('results/Elo Ratings.csv')
        
def update_elo(winner_elo, loser_elo, winner_rpi, loser_rpi):
    expected_win = expected_result(winner_elo, loser_elo)
    
    change_in_elo_win = k_factor * (1-expected_win)*(winner_rpi/1000)       #high rpi teams rewarded more for winning
    change_in_elo_lose =  k_factor * (expected_win)*(1 -(loser_rpi/1000))   #low rpi teams  punished more for losing

    winner_elo += change_in_elo_win     #update the winner's elo
    loser_elo -= change_in_elo_lose     #update loser's elo
    return winner_elo, loser_elo

def expected_result(elo_a, elo_b):
    expect_a = 1.0/(1+10**((elo_b - elo_a)/elo_width))      #this expect_a is the probablity that elo_a will win the game
    return expect_a