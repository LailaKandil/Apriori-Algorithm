import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from itertools import combinations
import tkinter as tk
from tkinter import filedialog, messagebox


def read_excel_file():
    data = pd.read_csv(
        "C:\\Users\\DR.Hisham\\Desktop\\Year 4\\Second and Final Semester!!\\Data Mining\\Assignments\\Assignment 1\\Assignment 1\\Assignment(1)\\Groceries data.csv")
    return data


def get_user_input():
    while True:
        amount_of_data = float(input("Enter the amount of data to be processed (e.g., 0.7 for 70%): "))
        if 0 < amount_of_data <= 1:
            break
        else:
            print("Error: Enter a value between 0 and 1 (e.g., 0.7 for 70%).")
    while True:
        try:
            min_support = int(input("Enter the minimum support (absolute count, e.g., 50): "))
            if min_support > 0:
                break
            else:
                print("Error: Please enter a positive integer for minimum support.")
        except ValueError:
            print("Error: Please enter a valid integer for minimum support.")
    while True:
        min_confidence = float(input("Enter the minimum confidence (e.g., 0.7 for 70%): "))
        if 0 < min_confidence <= 1:
            break  # Valid input, break the loop
        else:
            print("Error: Enter a value between 0 and 1.")

    print(
        f"Processing {amount_of_data * 100}% of the data with Min Support: {min_support}, Min Confidence: {min_confidence}")
    return amount_of_data, min_support, min_confidence


def preprocessing_of_data(data, amount_of_data):
    # Sample the data based on user input
    sample_size = int(amount_of_data * len(data))
    sampled_data = data.sample(n=sample_size, random_state=42)
    # Group by 'Member_number' to get all items per transaction
    transactions = sampled_data.groupby('Member_number')['itemDescription'].apply(list).tolist()
    # Apply one hot encoding to transactions
    te = TransactionEncoder()
    encoded_array = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(encoded_array, columns=te.columns_)
    return df_encoded, transactions


def get_1frequency_item_set(df_encoded, min_support):
    item_count = {}
    df_array = df_encoded.to_numpy()
    for row in df_array:
        for idx, item in enumerate(df_encoded.columns):
            if row[idx] == True:  # If the item is present in the transaction
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1

    # Filter the items that meet the minimum support
    frequent_items = {}
    for item, count in item_count.items():
        if count >= min_support:
            frequent_items[(item,)] = count
    return frequent_items


def get_k_frequency_item_set(frequent_items_previous, df_encoded, k, min_support):
    item_set_previous = list(frequent_items_previous)
    item_count = {}
    df_array = df_encoded.to_numpy()
    candidate_item_sets = set()
    for i in range(len(item_set_previous)):
        for j in range(i + 1, len(item_set_previous)):
            candidate = tuple(sorted(set(item_set_previous[i]) | set(item_set_previous[j])))
            if len(candidate) == k:
                candidate_item_sets.add(candidate)

    for candidate in candidate_item_sets:
        count = 0
        for row in df_array:
            is_present = True
            for item in candidate:
                item_index = df_encoded.columns.get_loc(item)
                if not row[item_index]:
                    is_present = False
                    break
            if is_present:
                count += 1
        if count >= min_support:
            item_count[candidate] = count

    return item_count


def get_and_print_frequent_item_sets(df_encoded, min_support):
    all_frequent_item_sets = {}
    frequent_item_sets = get_1frequency_item_set(df_encoded, min_support)
    all_frequent_item_sets[1] = frequent_item_sets
    print(f"Frequent 1-item-sets with minimum support {min_support}:")
    print(frequent_item_sets)
    k = 2
    while True:
        frequent_item_sets_k = get_k_frequency_item_set(list(frequent_item_sets.keys()), df_encoded, k, min_support)
        if not frequent_item_sets_k:
            break
        all_frequent_item_sets[k] = frequent_item_sets_k
        print(f"Frequent {k}-item_sets with minimum support {min_support}:")
        print(frequent_item_sets_k)
        frequent_item_sets = frequent_item_sets_k
        k += 1
    return all_frequent_item_sets


def generate_all_possible_rules(frequent_item_sets):
    all_rules = []
    for item_set, support in frequent_item_sets.items():
        if len(item_set) > 1:
            for i in range(1, len(item_set)):
                for prefix in combinations(item_set, i):
                    suffix = tuple(sorted(set(item_set) - set(prefix)))
                    if len(suffix) > 0:
                        all_rules.append((prefix, suffix, support))
    return all_rules


def calculate_confidence_rule(rule, frequent_item_sets, min_confidence):
    prefix, suffix, support = rule
    prefix_support = frequent_item_sets.get(prefix, 0)
    if prefix_support == 0:
        return None
    confidence = support / prefix_support

    if confidence >= min_confidence:
        return confidence
    else:
        return None


def print_association_rules_with_confidence(rules_with_confidence):
    if not rules_with_confidence:
        print("No association rules found that meet the minimum confidence threshold.")
        return

    print("\nStrong Association Rules:")
    for prefix, suffix, support, confidence in rules_with_confidence:
        print("IF ", end="")
        for item in prefix:
            print(item, end=" ")
        print("THEN ", end="")
        for item in suffix:
            print(item, end=" ")
        print(f"(Support: {support}, Confidence: {confidence:.2f})")


def apriori_algorithm(frequent_item_sets, min_confidence):
    all_rules = generate_all_possible_rules(frequent_item_sets)
    strong_rules = []
    for rule in all_rules:
        confidence = calculate_confidence_rule(rule, frequent_item_sets, min_confidence)
        if confidence is not None:
            prefix, suffix, support = rule
            strong_rules.append((prefix, suffix, support, confidence))
    print_association_rules_with_confidence(strong_rules)


def main():
    data = read_excel_file()
    amount_of_data, min_support, min_confidence = get_user_input()
    df_encoded, transactions = preprocessing_of_data(data, amount_of_data)

    # Get and print frequent item-sets
    all_frequent_item_sets = get_and_print_frequent_item_sets(df_encoded, min_support)

    # Print all the frequent item-sets found
    print("\nAll frequent item-sets found:")
    for level, item_sets in all_frequent_item_sets.items():
        print(f"{level}-item-sets: {item_sets}")

    # Merge all frequent item-sets into one dictionary for rule generation
    combined_frequent_item_sets = {}
    for item_sets in all_frequent_item_sets.values():
        combined_frequent_item_sets.update(item_sets)

    # Generate and print strong association rules using Apriori
    apriori_algorithm(combined_frequent_item_sets, min_confidence)

# main()
