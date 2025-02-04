# CLine - CSV Data Reader

This project contains a Python script `read_csv_data.py` that efficiently reads large CSV files in chunks using the pandas library. It also automatically detects file encoding using the chardet library to handle different character encodings.

## 功能

- Efficiently reads large CSV files in chunks to minimize memory usage.
- Automatically detects CSV file encoding using the chardet library.
- Provides a function `read_large_csv` that can be used in other Python scripts for CSV data processing.

## 使用方法

1. Make sure you have Python installed.
2. Install the required libraries:
   ```bash
   pip install pandas chardet
   ```
3. Run the `read_csv_data.py` script to test CSV file reading:
   ```bash
   python read_csv_data.py
   ```

## 檔案

- `read_csv_data.py`: Python script for reading large CSV files.
- `requirements.txt`: Lists the Python libraries required for this project.
- `README.md`: This file, providing a description of the project.

## 作者

[Your Name/Organization]