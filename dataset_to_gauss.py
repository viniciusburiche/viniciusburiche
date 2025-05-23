import numpy as np
from sklearn.preprocessing import QuantileTransformer
import pandas as pd
import matplotlib.pyplot as plt

csv_file = pd.read_csv(r'')

gross_set = csv_file[csv_file.columns[0]].values.reshape(-1, 1)

normal_set = QuantileTransformer(output_distribution='normal', random_state=0)
normal_set = normal_set.fit_transform(gross_set)

plt.figure(figsize=(10, 5))
plt.hist(normal_set.flatten(), bins=50, color='black', edgecolor='black')
plt.title('Distribuição normal')
plt.xlabel('Valor')
plt.ylabel('Frequência')
plt.grid(True)
plt.show()
