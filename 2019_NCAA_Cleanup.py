import pandas as pd
import numpy as np
import pickle
import time

full_pickle_in = open("/Users/jonahmiller/NCAA-Betting/data.pickle", "rb")
total_team_data = pickle.load(full_pickle_in)
team_pickle_in = open("/Users/jonahmiller/NCAA-Betting/teams.pickle", "rb")
teams = pickle.load(team_pickle_in)

teamwork = total_team_data

Col_Names = ['Team', 'Spread', 'Date', 'Court', 'Rank', 'Opponent', 'Opponent Initials', 'Result', 'Tempo', 'Record',
             'WAB', 'ADJO', 'ADJD', 'O - PPP', 'O - EFG%',
             'O - TO%', 'O - OR%', 'O - FTR', 'O - 2P', 'O - 3P', 'D - PPP', 'D - EFG%',
             'D - TO%', 'D - OR%', 'D -  FTR', 'D -  2P', 'D - 3P', 'G-SC', '+/-']
Team_DataFrame = {}

df = pd.DataFrame(teamwork[teams[0]])

# dropping unusable columns
df = df.drop([5, 6, 12], axis=1)

df.columns = range(df.shape[1])
d = {}
for i in range(29):
    d[i] = Col_Names[i]
df = df.rename(d, axis=1)

d = {}
for j in range(29):
    d[j] = Col_Names[j]

for i in range(len(teamwork)):
    df = pd.DataFrame(teamwork[teams[i]])
    df = df.drop([5, 6, 12], axis=1)
    df.columns = range(df.shape[1])
    df = df.rename(d, axis=1)
    Team_DataFrame[teams[i]] = df

# Cleaning up the 'Spread' string, this is really messy

for j in range(len(teamwork)):
    final_spread = []
    df = Team_DataFrame[teams[j]]
    for i in range(len(df)):
        x = df['Result'][i]
        cat = x.split(',')
        win_loss = cat[0]
        score = cat[1]
        differential = 1
        if win_loss == 'W':
            differential = 1
        else:
            differential = -1

        split = score.split("-")
        same = True

        # Clean up the occasional OT game so that the string can be correctly parsed
        if '2OT' in split[1]:
            split[1] = split[1].replace('2OT', '')
            same = False
        if '3OT' in split[1] and same:
            split[1] = split[1].replace('3OT', '')
            same = False
        if '4OT' in split[1] and same:
            split[1] = split[1].replace('4OT', '')
            same = False
        if 'OT' in split[1]:
            split[1] = split[1].replace('OT', '')
            same = False

        difference = int(split[0]) - int(split[1])
        end_result = difference * differential
        final_spread.append(end_result)
    df['Final Spread'] = final_spread


# Here I check whether the team covered the spread or not
for k in range(len(teamwork)):
    Cover = []
    df = Team_DataFrame[teams[k]]
    for i in range(len(df)):

        # Team strings are messy as a result of the URL format, so I clean them often
        s = df['Spread'][i]
        t1 = (df['Team'][i])
        t2 = (df['Opponent'][i])
        t1 = t1.replace("+", " ")
        t1 = t1.replace("%26", "&")
        t1 = t1.replace("%27", "'")
        t2 = t2.replace("+", " ")
        t2 = t2.replace("%26", "&")
        t2 = t2.replace("%27", "'")
        seperated_spread = []
        favored_team = False
        if t1 in s:
            if t2 in s:
                if len(t2) > len(t1):
                    seperated_spread = s.split(t2)
                    score = seperated_spread[1].split(',')[0]
            else:
                favored_team = True
                seperated_spread = s.split(t1)
                score = seperated_spread[1].split(',')[0]
        else:
            seperated_spread = s.split(t2)
            score = seperated_spread[1].split(',')[0]
        if favored_team:
            # Sometimes there is no spread... really lopsided games

            if '100%' in score:
                score = -50
            if int(df['Final Spread'][i]) > -1 * float(score):
                Cover.append(1)
            else:
                Cover.append(0)
        else:
            if float(score) < int(df['Final Spread'][i]):
                Cover.append(1)
            else:
                Cover.append(0)
    df['Cover'] = Cover

Full_Season = {}

# Here is where the bulk of the work is done, this takes the historical data
# and turns each game into data that can be input into a model
# I weight the three most recent games as 60% of the current value and everything else as 40%

for j in range(len(teamwork)):
    Team = Team_DataFrame[teams[j]]
    Model_Vals = ['Team', 'Spread', 'Court', 'Opponent', 'Rank', 'Tempo', 'ADJO', 'ADJD', 'O - PPP', 'O - EFG%',
                  'D - PPP', 'D - EFG%', 'Cover','Final Spread']

    df_model_ = Team.filter(Model_Vals, axis=1)
    df_mean_ = df_model_[1:len(df_model_) + 1]
    rows = Team.shape[0] - 1
    print(len(df_model_))

    Tempo_, ADJD_, ADJO_, OPPP_, OEFG_, DPPP_, DEFG_ = [], [], [], [], [], [], []

    for i in range(2, len(df_model_) + 1):
        scaling = 0.6
        # 3 Most Recent games will be weighted more
        if i < 5:
            Tempo_.append(df_model_['Tempo'][0:i - 1].astype(float).mean())
            lst_adjd = df_model_.index[df_model_['ADJD'] == '-'].tolist()
            for k in lst_adjd:
                df_model_.drop(k, axis=0, inplace=True)
            ADJD_.append(df_model_['ADJD'][0:i - 1].astype(float).mean())
            ADJO_.append(df_model_['ADJO'][0:i - 1].astype(float).mean())
            OPPP_.append(df_model_['O - PPP'][0:i - 1].astype(float).mean())
            OEFG_.append(df_model_['O - EFG%'][0:i - 1].astype(float).mean())
            DPPP_.append(df_model_['D - PPP'][0:i - 1].astype(float).mean())
            DEFG_.append(df_model_['D - EFG%'][0:i - 1].astype(float).mean())
        else:
            temp = ((df_model_['Tempo'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_temp = ((df_model_['Tempo'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            Tempo_.append((temp + other_temp))

            adjd = ((df_model_['ADJD'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_adjd = ((df_model_['ADJD'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            ADJD_.append(adjd + other_adjd)

            adjo = ((df_model_['ADJO'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_adjo = ((df_model_['ADJO'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            ADJO_.append(adjo + other_adjo)

            oppp = ((df_model_['O - PPP'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_oppp = ((df_model_['O - PPP'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            OPPP_.append(oppp + other_oppp)

            oefg = ((df_model_['O - EFG%'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_oefg = ((df_model_['O - EFG%'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            OEFG_.append(oefg + other_oefg)

            dppp = ((df_model_['D - PPP'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_dppp = ((df_model_['D - PPP'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            DPPP_.append(dppp + other_dppp)

            defg = ((df_model_['D - EFG%'][i - 4:i - 1].astype(float).sum()) * (scaling)) / 3
            other_defg = ((df_model_['D - EFG%'][0:i - 4].astype(float).sum()) * (1 - scaling)) / (i - 4)
            DEFG_.append(defg + other_defg)

    Tempo_, ADJD_, OPPP_ = np.array(Tempo_).reshape(rows), np.array(ADJD_).reshape(rows), np.array(OPPP_).reshape(rows)
    OEFG_, DPPP_, DEFG_ = np.array(OEFG_).reshape(rows), np.array(DPPP_).reshape(rows), np.array(DEFG_).reshape(rows)

    #  Pull The Relevant Columns that have been adjusted (weighted average)
    df_Model = df_mean_.filter(['Cover', 'Final Spread', 'Team', 'Rank', 'Spread', 'Court'], axis=1)
    df_Model['Tempo'], df_Model['ADJO'], df_Model['ADJD'], df_Model['O - PPP'] = Tempo_, ADJD_, ADJO_, OPPP_
    df_Model['O - EFG%'], df_Model['D - PPP'], df_Model['D - EFG%'] = OEFG_, DPPP_, DEFG_
    df_Model['O - EFG%'], df_Model['D - PPP'], df_Model['D - EFG%'] = OEFG_, DPPP_, DEFG_

    Full_Season[teams[j]] = df_Model

df_Full_Season_fp = {}
check_spread = {}
spreads = []
for i in range(len(teamwork)):
    team_1 = teams[i]
    l_t1 = Full_Season[team_1]
    for j in range(1, len(l_t1)):
        spread = l_t1['Spread'][j]
        if spread not in check_spread:
            spreads.append(spread)
        check_spread[spread] = 1
        if spread in df_Full_Season_fp:
            mod = df_Full_Season_fp[spread]
            ins = np.array(l_t1.iloc[j - 1])
            home_away = np.concatenate((mod, ins), axis=0)
            df_Full_Season_fp[spread] = home_away
        else:
            ins = np.array(l_t1.iloc[j - 1])
            df_Full_Season_fp[spread] = ins

fin_spreads = []
df_Full_Season = {}

# Number of Parameters = 12 as of right now
for i in range(len(spreads)):
    if len(df_Full_Season_fp[spreads[i]]) == 13:
        continue
    else:
        fin_spreads.append(spreads[i])
        df_Full_Season[spreads[i]] = df_Full_Season_fp[spreads[i]]

reordered_Full_Season = {}

# Here I reorder the two teams so that the favored team comes first

for i in range(len(fin_spreads)):

    favored_team = df_Full_Season[fin_spreads[i]][2].split('-')[0]
    favored_team = favored_team.replace(' ', '')
    print(i)
    print(df_Full_Season[fin_spreads[i]])
    team_1 = df_Full_Season[fin_spreads[i]][4].split('-')[0]
    team_2 = df_Full_Season[fin_spreads[i]][16].split('-')[0]
    team_1 = team_1.replace('+', '')
    team_1 = team_1.replace('.', '')
    team_2 = team_2.replace('+', '')
    team_2 = team_2.replace('.', '')

    if favored_team == team_2:
        swap = np.array([])
        new_front = df_Full_Season[fin_spreads[i]][13:26]
        new_back = df_Full_Season[fin_spreads[i]][0:13]
        new_entry = np.concatenate([new_front, new_back], axis=0)
        reordered_Full_Season[fin_spreads[i]] = new_entry
    else:
        reordered_Full_Season[fin_spreads[i]] = df_Full_Season[fin_spreads[i]]


Model_Vals = ['Favored Team Cover', 'Favored Final Spread', 'Favored Team', 'Favored Team Rank', 'Spread', 'Fav Court',
              'Fav Tempo', 'Fav ADJO',
              'Fav ADJD', 'Fav O - PPP', 'Fav O - EFG%',
              'Fav D - PPP', 'Fav D - EFG%', 'Underdog Team Cover', 'Underdog Final Spread', 'Underdog Team',
              'Underdog Team Rank',
              'Spread 2', 'Underdog Court', 'Underdog Tempo', 'Underdog ADJO',
              'Underdog ADJD', 'Underdog O - PPP', 'Underdog O - EFG%',
              'Underdog D - PPP', 'Underdog D - EFG%']

model_data = []
for i in fin_spreads:
    model_data.append(reordered_Full_Season[i])


df = pd.DataFrame(model_data)
df.dropna(axis=1, inplace=True)
df.columns = Model_Vals
df.drop('Spread 2', axis=1, inplace=True)

# Convert to csv and load into model
df.to_csv('2019_NCAA.csv')
