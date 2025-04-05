# Apriori Algorithm - Association Rule Mining

This project implements the **Apriori algorithm** for **association rule mining** using a grocery transactions dataset. The goal is to identify frequent itemsets and generate strong association rules based on the user-defined minimum support and confidence thresholds.

## Project Structure

The project is divided into several key functions that handle different parts of the process:

1. **Reading the Data**: The dataset is loaded from a CSV file, where each transaction is represented by the items purchased by a customer.
2. **Data Preprocessing**: The data is preprocessed to convert it into a format suitable for the Apriori algorithm. This includes sampling the data and encoding transactions using one-hot encoding.
3. **Frequent Itemset Generation**: The algorithm generates frequent itemsets of varying sizes based on a user-defined minimum support.
4. **Association Rule Generation**: Strong association rules are generated based on the frequent itemsets, with their confidence values compared against a user-defined threshold.
5. **Printing Results**: The frequent itemsets and strong association rules are printed to the console.

## Features

- **Data Sampling**: The user can specify the proportion of the dataset to be processed.
- **Minimum Support and Confidence**: The user can input the minimum support (absolute count) and minimum confidence for rule generation.
- **Frequent Itemset Extraction**: Identifies frequent itemsets using the Apriori algorithm.
- **Association Rule Generation**: Generates strong association rules based on frequent itemsets.
- **Print Results**: Displays frequent itemsets and association rules along with their support and confidence values.

## Requirements

- **Python 3.x**
- **Pandas**: For data manipulation and preprocessing.
- **mlxtend**: For the `TransactionEncoder` to handle one-hot encoding of the transactions.
- **Tkinter** For GUI implementation
