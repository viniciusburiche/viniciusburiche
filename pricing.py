import pandas as pd
import math
from datetime import datetime

# Load datasets
pricing_data_backup = pd.read_csv('Pricing_Data.csv', encoding='latin1', sep=';')
rating_pd_backup = pd.read_csv('Rating_PD.csv', encoding='latin1', sep=';')

# Create copies to work with
pricing_data = pricing_data_backup.copy()
rating_pd = rating_pd_backup.copy()

# Input rating with validation
while True:
    input_rating = input('Enter the company rating: ')
    if input_rating in rating_pd['Global_Rating'].values:
        break
    else:
        print('Please enter a valid rating.')

# Input and validate dates
while True:
    input_start_date = input('Enter the start date (DD/MM/YYYY): ')
    input_end_date = input('Enter the end date (DD/MM/YYYY): ')
    
    try:
        start_date = datetime.strptime(input_start_date, '%d/%m/%Y')
        end_date = datetime.strptime(input_end_date, '%d/%m/%Y')

        rating_pd.columns = rating_pd.columns.str.replace('PD_', '').str.strip()

        term = (end_date - start_date).days / 365
        if term > 5:
            print('Invalid term: exceeds 5 years.')
            continue
        elif term < 1:
            term = math.ceil(term)
        else:
            term = round(term)

        term = str(term)

        if term in rating_pd.columns:
            break
        else:
            print('Please enter a valid term.')
    except ValueError as ve:
        print(f'Invalid input. Please check the dates entered. {ve}')

# Retrieve probability of default
if term in rating_pd.columns:
    rating_lookup = rating_pd[rating_pd['Global_Rating'] == input_rating]

    if not rating_lookup.empty:
        probability_of_default = rating_lookup[term].values * 100
    else:
        print("No matching rows found for the specified rating.")
else:
    print(f"'{term}' is not a valid column in the Rating_PD dataset.")

# Pricing calculation
pricing_data['PEB'] = (pricing_data['STP'] * pricing_data['LGD'] * pricing_data['ALF'] * probability_of_default)

# Fixed parameters
administrative_costs = 0.10
cost_of_capital = 0.08
taxes = 0.00
acquisition_cost = 0.33
base_rate = 0.5  # in %

pricing_data['base_rate'] = base_rate

pricing_data['gross_rate'] = ((administrative_costs + cost_of_capital + taxes + 1) * pricing_data['PEB'])

pricing_data['net_rate'] = pricing_data['gross_rate'] / (1 - acquisition_cost)

pricing_data['final_rate'] = pricing_data[['net_rate']].apply(lambda x: max(x['net_rate'], base_rate), axis=1)

pricing_data['final_rate'] = pricing_data['final_rate'].round(2)

print(pricing_data[['Product', 'final_rate']])
