# Bill Splitter

This advanced Streamlit app is designed to facilitate the splitting of bills among a group of people with ease and precision. It allows users to input the names of people and items to generate a detailed Excel sheet that not only calculates the total expenses but also provides flexible methods to split the costs.

## Features

- **Input Management**: Easily input names of people and items.
- **Detailed Calculation**: Once the Excel sheet is generated, input the price for each item and the quantity. The app will automatically calculate the final price.
- **Summarization**: Provides a total sum of all expenses.
- **Flexible Splitting Methods**:
  - **Manual Splitting**: Manually assign a value to each item for each person.
  - **Weighted Sum Splitting**: Use a weighted sum concept to split items proportionally among people. For example, if everyone shared a dish equally, simply fill each cell with '1' to split the cost equally.
- **Validation and Highlighting**: The app checks if the final price of each item is fully split. If fully split, the cell turns green; otherwise, it shows red, indicating that the item still needs splitting.
- **Summary Table**: Reflects the individual shares in a top-right table, showing each person's split, who paid for what, and how much each person owes.

## Setup

### Prerequisites

- Windows OS (for the batch file to work as intended)

### Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/bill_splitter.git
   cd bill_splitter
   ```
2. **Run the Setup Script**

   Double-click the `run_app.bat` file in the project directory. This script will:

   - Check if Python is installed and install it if necessary.
   - Create a virtual environment named `bill_split_venv` if it doesn't already exist.
   - Install the required dependencies (`streamlit` and `openpyxl`).
   - Launch the Streamlit app.

## Usage

1. Fill in the names of people and items in the provided text areas.
2. Click the "Generate Excel" button to create and download the bill split Excel file.
3. Input the price and quantity for each item in the generated Excel sheet.
4. Use the manual or weighted sum splitting methods to distribute the costs.
5. Check the validation colors to ensure all items are fully split.
6. Review the summary table to see the final amounts each person owes and has paid.

## Files

- `app.py`: The main Streamlit app script.
- `requirements.txt`: List of dependencies required for the project.
- `run_app.bat`: Batch file to set up and run the app.
- `.gitignore`: Git ignore file to exclude certain files and directories from being tracked.
- `README.md`: This file, providing information about the project.

## Project Structure

- bill_splitter/
-    ├── .gitignore
-    ├── app.py
-    ├── README.md
-    ├── requirements.txt
-    └── run_app.bat

## Dependencies

The project requires the following Python packages:

- `streamlit`
- `openpyxl`

These dependencies will be installed automatically when you run the `run_app.bat` file for the first time.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For any questions or suggestions, please open an issue in this repository.
