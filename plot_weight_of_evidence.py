import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# import file

loan_data_backup = pd.read_csv('loan_data.csv', dtype={'desc': str})
loan_data = loan_data_backup.copy()

# preprocessing 

loan_data['emp_length_float'] = loan_data['emp_length'].str.replace('+ years', '')
loan_data['emp_length_float'] = loan_data['emp_length_float'].str.replace('< 1 year',str(0))
loan_data['emp_length_float'] = loan_data['emp_length_float'].str.replace('n/a',str(0))
loan_data['emp_length_float'] = loan_data['emp_length_float'].str.replace(' years','')
loan_data['emp_length_float'] = loan_data['emp_length_float'].str.replace(' year','')
loan_data['emp_length_float'] = pd.to_numeric(loan_data['emp_length_float'])

loan_data['term_float'] = loan_data['term'].str.replace(' months','')
loan_data['term_float'] = pd.to_numeric(loan_data['term_float'])

loan_data['earliest_cr_line_date'] = pd.to_datetime(loan_data['earliest_cr_line'],format= '%b-%y')

loan_data.loc[loan_data['earliest_cr_line_date'] > pd.Timestamp.today(), 'earliest_cr_line_date'] -= pd.DateOffset(years=100)

today = pd.Timestamp.today()

loan_data['age_earliest_cr_line_date'] = (today - loan_data['earliest_cr_line_date']).dt.days
loan_data['age_earliest_cr_line_date'] = loan_data['age_earliest_cr_line_date'] / 365.25

loan_data['issue_date'] = pd.to_datetime(loan_data['issue_d'], format='%b-%y')

loan_data['age_issue_date'] = (today - loan_data['issue_date']).dt.days
loan_data['age_issue_date'] = round(loan_data['age_issue_date'] / 365.25,2)

# dummies

loan_data_dummies = [

pd.get_dummies(loan_data['grade'], prefix='grade', prefix_sep=': '),
pd.get_dummies(loan_data['sub_grade'], prefix='sub_grade',prefix_sep=': '),
pd.get_dummies(loan_data['home_ownership'], prefix='home_ownership',prefix_sep=': '),
pd.get_dummies(loan_data['verification_status'], prefix='verification_status',prefix_sep=': '),
pd.get_dummies(loan_data['loan_status'], prefix='loan_status',prefix_sep=': '),
pd.get_dummies(loan_data['purpose'], prefix='purpose',prefix_sep=': '),
pd.get_dummies(loan_data['addr_state'], prefix='addr_state',prefix_sep=': '),
pd.get_dummies(loan_data['initial_list_status'], prefix='initial_list_status',prefix_sep=': ')

]

loan_data_dummies = pd.concat(loan_data_dummies, axis=1)

loan_data = pd.concat([loan_data,loan_data_dummies], axis=1)

# null treatment

loan_data['total_rev_hi_lim'] = loan_data['total_rev_hi_lim'].fillna(loan_data['funded_amnt'])
loan_data['annual_inc'] = loan_data['annual_inc'].fillna(loan_data['annual_inc'].mean())
loan_data['age_issue_date'] = loan_data['age_issue_date'].fillna(0)
loan_data['acc_now_delinq'] = loan_data['acc_now_delinq'].fillna(0)
loan_data['total_acc'] = loan_data['total_acc'].fillna(0)
loan_data['pub_rec'] = loan_data['pub_rec'].fillna(0)
loan_data['open_acc'] = loan_data['open_acc'].fillna(0)
loan_data['inq_last_6mths'] = loan_data['inq_last_6mths'].fillna(0)
loan_data['delinq_2yrs'] = loan_data['delinq_2yrs'].fillna(0)
loan_data['emp_length_float'] = loan_data['emp_length_float'].fillna(0)

# training/testing 

loan_data['good_bad'] = np.where(loan_data['loan_status'].isin(['Charged Off', 'Default', 'Does not meet the credit policy. Status:Charged Off', 'Late (31-120 days)']), 0, 1)

loan_data_inputs_train, loan_data_inputs_test, loan_data_targets_train, loan_data_targets_test = train_test_split(loan_data.drop('good_bad', axis=1),loan_data ['good_bad'], test_size=0.2, random_state=42)

# data preparation function

df_inputs_prepr = loan_data_inputs_train
df_targets_prepr = loan_data_targets_train

def woe_discrete (frame, disc_var_name, good_bad_parameter):

    frame = pd.concat([frame[disc_var_name],good_bad_parameter], axis=1)    
    
    frame_count_obs = frame.groupby(frame.columns.values[0], as_index=False)[frame.columns.values[1]].count()
    frame_mean_obs = frame.groupby(frame.columns.values[0], as_index=False)[frame.columns.values[1]].mean()
    
    frame = pd.concat([frame_count_obs,frame_mean_obs], axis=1)
    
    frame = frame.iloc[:,[0,1,3]]
    
    frame.columns = [frame.columns.values[0], 'count_obs','mean_obs']
    frame['prop_n_obs'] = frame['count_obs'] / frame['count_obs'].sum()
    frame['n_good'] = frame['mean_obs'] * frame['count_obs']
    frame['n_bad'] = (1-frame['mean_obs']) * frame['count_obs']
    frame['prop_n_good'] = frame['n_good'] / frame['n_good'].sum()
    frame['prop_n_bad'] = frame['n_bad'] / frame['n_bad'].sum()
    frame['WoE'] = np.log(frame['prop_n_good'] / frame['prop_n_bad'])
    
    frame = frame.sort_values(disc_var_name,ascending=False)
    frame = frame.reset_index(drop = True)
   
    frame['diff_mean_obs'] = frame['mean_obs'].diff().abs()
    frame['diff_WoE'] = frame['WoE'].diff().abs()
    frame['Information Value'] = (frame['prop_n_good'] - frame['prop_n_bad']) * frame['WoE']
    frame['Information Value'] = frame['Information Value'].sum()

    return frame

template_frame = woe_discrete(df_inputs_prepr,'grade',df_targets_prepr)

# plot function

def plot_Woe(df_Woe, rotation_x_axis=0):
    
    x = np.array(df_Woe.iloc[:,0].apply(str))
    y = df_Woe['WoE']
    
    plt.figure(figsize= (18,6))
    plt.plot(x,y,marker = 'o', linestyle= '--', color = 'k')
    plt.xlabel(df_Woe.columns[0])
    plt.ylabel('Weight of Evidence')
    plt.title(str('Weight of evidence by ' + df_Woe.columns[0]))
    plt.xticks(rotation = rotation_x_axis)
    plt.axhline()
    plt.axvline()
    
    plt.show()

plot_frame = plot_Woe(template_frame)

print(plot_frame)
