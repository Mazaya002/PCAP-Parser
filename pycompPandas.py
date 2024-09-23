import csv  # Import csv module
import pandas as pd

def read_csv_to_dict(file_path):
    packets = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            packets[row['tcp_payload']] = row  # Use payload as the key
    return packets

def compare_packets(file1, file2, output_file):
    packets_file1 = read_csv_to_dict(file1)
    packets_file2 = read_csv_to_dict(file2)

    matching_packets = {payload: packets_file1[payload] for payload in packets_file1 if payload in packets_file2}
    unique_to_file1 = {payload: packets_file1[payload] for payload in packets_file1 if payload not in packets_file2}
    unique_to_file2 = {payload: packets_file2[payload] for payload in packets_file2 if payload not in packets_file1}

    # Convert dict_values to list of dictionaries
    matching_list = list(matching_packets.values())
    unique_to_file1_list = list(unique_to_file1.values())
    unique_to_file2_list = list(unique_to_file2.values())

    # Create DataFrames
    matching_df = pd.DataFrame(matching_list)
    unique_to_file1_df = pd.DataFrame(unique_to_file1_list)
    unique_to_file2_df = pd.DataFrame(unique_to_file2_list)

    # Write to an Excel file with different sheets
    with pd.ExcelWriter(output_file) as writer:
        matching_df.to_excel(writer, sheet_name='Matching Packets', index=False)
        unique_to_file1_df.to_excel(writer, sheet_name='Unique to File 1', index=False)
        unique_to_file2_df.to_excel(writer, sheet_name='Unique to File 2', index=False)

    print(f"Results written to {output_file}")

if __name__ == "__main__":
    compare_packets('file1.csv', 'file2.csv', 'comparison_results.xlsx')
