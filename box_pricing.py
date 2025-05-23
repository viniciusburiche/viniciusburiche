import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import math

def calculate_pricing():
    try:
        pricing_data_backup = pd.read_csv('pricing_data.csv', encoding='latin1', sep=';')
        rating_pd_backup = pd.read_csv('rating_pd.csv', encoding='latin1', sep=';')

        pricing_data = pricing_data_backup.copy()
        rating_pd = rating_pd_backup.copy()

        input_rating = entry_rating.get().strip()
        input_start_date = entry_start_date.get().strip()
        input_end_date = entry_end_date.get().strip()

        if input_rating not in rating_pd['Global_Rating'].values:
            messagebox.showerror("Error", "Please enter a valid rating.")
            return

        try:
            start_date = datetime.strptime(input_start_date, '%d/%m/%Y')
            end_date = datetime.strptime(input_end_date, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD/MM/YYYY.")
            return

        term = (end_date - start_date).days / 365

        if term > 5.01:
            messagebox.showerror("Error", "Invalid term. Maximum allowed is 5 years.")
            return
        elif term < 1:
            term = math.ceil(term)
        else:
            term = round(term)

        term_str = str(term)

        rating_pd.columns = rating_pd.columns.str.replace('PD_', '').str.strip()

        if term_str not in rating_pd.columns:
            messagebox.showerror("Error", f"'{term_str}' is not a valid column in Rating_PD. Available columns: {', '.join(rating_pd.columns)}")
            return

        rating_lookup = rating_pd[rating_pd['Global_Rating'] == input_rating]
        if not rating_lookup.empty:
            probability_of_default = rating_lookup[term_str].values[0] * 100
        else:
            messagebox.showerror("Error", "Rating not found in the Rating_PD table.")
            return

        pricing_data['PEB'] = (
            pricing_data['STP'] *
            pricing_data['LGD'] *
            pricing_data['ALF'] *
            probability_of_default
        )

        administrative_costs = 0.06
        cost_of_capital = 0.1225
        taxes = 0.01
        acquisition_cost = 0.25
        base_rate = 0.15  # in %

        pricing_data['base_rate'] = base_rate

        pricing_data['gross_rate'] = ((administrative_costs + cost_of_capital + taxes + 1) * pricing_data['PEB'])

        pricing_data['net_rate'] = pricing_data['gross_rate'] / (1 - acquisition_cost)

        pricing_data['final_rate'] = pricing_data[['net_rate', 'base_rate']].max(axis=1)

        pricing_data['final_rate'] = pricing_data['final_rate'].round(2)

        output_file = "pricing_results.csv"
        pricing_data[['Product', 'final_rate']].to_csv(output_file, index=False, sep=';')

        messagebox.showinfo("Success", f"Results saved to '{output_file}'.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("Surety Pricing")
root.geometry("400x300")

tk.Label(root, text="Enter the company rating:").pack(pady=5)
entry_rating = tk.Entry(root, width=30)
entry_rating.pack()

tk.Label(root, text="Enter the start date (DD/MM/YYYY):").pack(pady=5)
entry_start_date = tk.Entry(root, width=30)
entry_start_date.pack()

tk.Label(root, text="Enter the end date (DD/MM/YYYY):").pack(pady=5)
entry_end_date = tk.Entry(root, width=30)
entry_end_date.pack()

btn_calculate = tk.Button(root, text="Calculate", command=calculate_pricing)
btn_calculate.pack(pady=20)

root.mainloop()
