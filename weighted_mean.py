import numpy as np

while True:
    margin_factor = input('Enter the margin factor: ')
    try:
        margin_factor = float(margin_factor)
        break
    except ValueError:
        print('Please enter a valid margin factor.')

while True:
    liquidity_factor = input('Enter the liquidity factor: ')
    try:
        liquidity_factor = float(liquidity_factor)
        break
    except ValueError:
        print('Please enter a valid liquidity factor.')

while True:
    leverage_factor = input('Enter the leverage factor: ')
    try:
        leverage_factor = float(leverage_factor)
        break
    except ValueError:
        print('Please enter a valid leverage factor.')

while True:
    return_factor = input('Enter the return factor: ')
    try:
        return_factor = float(return_factor)
        break
    except ValueError:
        print('Please enter a valid return factor.')

# Define weights
weights = [0.185, 0.29, 0.33, 0.195]

# Calculate quantitative grade
quantitative_grade = round(
    np.average(
        [margin_factor, liquidity_factor, leverage_factor, return_factor],
        weights=weights
    ),
    2
)

print(f'The quantitative grade is: {quantitative_grade}')
