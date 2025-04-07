import tkinter as tk
from tkinter import simpledialog, scrolledtext
import io
import sys
import main as dm


def main():
    data = dm.read_excel_file()
    amount_of_data = simpledialog.askfloat("Input", "Enter the amount of data to be processed (e.g., 0.7 for 70%):",
                                           minvalue=0.01, maxvalue=1.0)
    min_support = simpledialog.askinteger("Input", "Enter the minimum support (absolute count, e.g., 50):", minvalue=1)
    min_confidence = simpledialog.askfloat("Input", "Enter the minimum confidence (e.g., 0.7 for 70%):", minvalue=0.01,
                                           maxvalue=1.0)
    df_encoded, transactions = dm.preprocessing_of_data(data, amount_of_data)
    all_frequent_itemsets = dm.get_and_print_frequent_itemsets(df_encoded, min_support)

    # Display frequent itemsets in the text widget
    text_widget.insert(tk.END, "\nAll frequent itemsets found:\n")
    for level, itemsets in all_frequent_itemsets.items():
        text_widget.insert(tk.END, f"{level}-itemsets: {itemsets}\n")

    combined_frequent_itemsets = {}
    for itemsets in all_frequent_itemsets.values():
        combined_frequent_itemsets.update(itemsets)

    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    dm.apriori_algorithm(combined_frequent_itemsets, min_confidence)
    sys.stdout = old_stdout
    text_widget.insert(tk.END, mystdout.getvalue())


def show_main_page():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="mint cream")
    frame.pack(pady=20)
    btn_load = tk.Button(frame, text="Load Data", command=main, font=("Helvetica", 14), bg="light blue")
    btn_load.pack(side=tk.LEFT, padx=10)
    global text_widget
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, bg="mint cream")
    text_widget.pack(pady=20)


def show_welcome_page():
    for widget in root.winfo_children():
        widget.destroy()

    welcome_frame = tk.Frame(root, bg="mint cream")
    welcome_frame.pack(pady=20)
    welcome_label = tk.Label(welcome_frame, text="Welcome to the Apriori Algorithm GUI", font=("Helvetica", 24),
                             bg="mint cream")
    welcome_label.pack(pady=10)
    start_button = tk.Button(welcome_frame, text="Start", command=show_main_page, font=("Helvetica", 18),
                             bg="light blue")
    start_button.pack(pady=10)


def run_gui():
    global root
    root = tk.Tk()
    root.title("Apriori Algorithm GUI")
    root.geometry("800x600")
    root.configure(bg="mint cream")
    show_welcome_page()
    root.mainloop()


if __name__ == "__main__":
    run_gui()
