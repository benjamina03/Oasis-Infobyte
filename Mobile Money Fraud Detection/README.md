# Detection of Anomalous Transactions in Mobile Money Ecosystems

A prototype application for detecting fraudulent activities in mobile money transactions using machine learning.

## Capstone Project Objectives

1. **Upload Dataset**: Upload a mobile money dataset (CSV format) for analysis
2. **Analyze Transactions**: Analyze the dataset against "normal" transaction behaviour using Isolation Forest algorithm
3. **Flag Fraudulent Activities**: Automatically flag transactions that deviate from normal patterns
4. **Manual Validation**: Validate flagged transactions through manual inspection interface
5. **Recommendations**: Get appropriate action recommendations for flagged transactions

## Features

- **Dataset Upload**: Import CSV files containing mobile money transaction data
- **Sample Data Generation**: Generate sample dataset for testing purposes
- **Anomaly Detection**: Uses Isolation Forest algorithm for unsupervised anomaly detection
- **Interactive GUI**: User-friendly Tkinter-based graphical interface
- **Transaction Viewer**: View and inspect individual transactions
- **Validation System**: Mark transactions as confirmed fraud or false positives
- **Action Recommendations**: Risk-based recommendations for handling flagged transactions

## Installation

1. Ensure Python 3.7+ is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python fraud_detection.py
```

### Workflow

1. **Tab 1 - Upload Dataset**: 
   - Click "Browse & Upload Dataset" to load your CSV file
   - Or use "Generate Sample Dataset" for testing

2. **Tab 2 - Analyze Transactions**:
   - Set the expected fraud rate percentage
   - Click "Analyze Transactions" to run the detection algorithm

3. **Tab 3 - Flagged Transactions**:
   - View all transactions flagged as potentially fraudulent
   - Click "Refresh" to update the list after analysis

4. **Tab 4 - Manual Validation**:
   - Enter a transaction index to load details
   - Mark as "Confirmed Fraud" or "False Positive"

5. **Tab 5 - Recommendations**:
   - Enter a transaction index
   - Get risk-based action recommendations

## Dataset Format

The application expects a CSV file with transaction data. Recommended columns:
- `step`: Transaction timestamp/sequence
- `type`: Transaction type (TRANSFER, CASH_OUT, PAYMENT, etc.)
- `amount`: Transaction amount
- `nameOrig`: Sender account ID
- `oldbalanceOrg`: Sender's balance before transaction
- `newbalanceOrg`: Sender's balance after transaction
- `nameDest`: Receiver account ID
- `oldbalanceDest`: Receiver's balance before transaction
- `newbalanceDest`: Receiver's balance after transaction

## Algorithm

The system uses **Isolation Forest**, an unsupervised machine learning algorithm that:
- Identifies anomalies by isolating observations
- Works well with high-dimensional datasets
- Does not require labeled fraud data for training
- Assigns anomaly scores to each transaction

## Dependencies

- pandas >= 1.3.0
- numpy >= 1.21.0
- scikit-learn >= 0.24.0
- tkinter (included with Python)

## License

This project is part of a capstone project for educational purposes.

## Author

Final Year Capstone Project - Detection of Anomalous Transaction in Mobile Money Ecosystems
