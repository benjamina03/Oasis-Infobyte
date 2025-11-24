"""
Transaction Analyzer Module
===========================
Core functionality for detecting anomalous transactions in mobile money ecosystems.

This module provides the TransactionAnalyzer class that handles:
1. Dataset loading and preprocessing
2. Anomaly detection using Isolation Forest
3. Transaction validation
4. Recommendation generation
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder


class TransactionAnalyzer:
    """Core class for analyzing mobile money transactions."""
    
    def __init__(self):
        self.dataset = None
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.flagged_transactions = None
        self.analysis_results = {}
        
    def load_dataset(self, filepath):
        """
        Load dataset from CSV file.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            self.dataset = pd.read_csv(filepath)
            return True, f"Dataset loaded successfully. {len(self.dataset)} transactions found."
        except FileNotFoundError:
            return False, f"File not found: {filepath}"
        except pd.errors.EmptyDataError:
            return False, "The CSV file is empty."
        except Exception as e:
            return False, f"Error loading dataset: {str(e)}"
    
    def load_dataframe(self, df):
        """
        Load dataset from a pandas DataFrame.
        
        Args:
            df: pandas DataFrame with transaction data
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not isinstance(df, pd.DataFrame):
            return False, "Input must be a pandas DataFrame."
        
        if df.empty:
            return False, "DataFrame is empty."
        
        self.dataset = df.copy()
        return True, f"Dataset loaded successfully. {len(self.dataset)} transactions found."
    
    def preprocess_data(self):
        """
        Preprocess the dataset for analysis.
        
        Returns:
            tuple: (processed_df, feature_columns) or (False, error_message)
        """
        if self.dataset is None:
            return False, "No dataset loaded."
        
        df = self.dataset.copy()
        
        # Identify numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Encode categorical columns
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
        
        # Handle missing values
        df = df.fillna(df.median(numeric_only=True))
        df = df.fillna(0)
        
        return df, numeric_cols + categorical_cols
    
    def analyze_transactions(self, contamination=0.1):
        """
        Analyze transactions to identify anomalies using Isolation Forest.
        
        Args:
            contamination: Expected proportion of anomalies in the dataset (0 < contamination < 0.5)
            
        Returns:
            tuple: (success: bool, results: dict or error_message: str)
        """
        if self.dataset is None:
            return False, "No dataset loaded. Please upload a dataset first."
        
        if not 0 < contamination < 0.5:
            return False, "Contamination must be between 0 and 0.5."
        
        try:
            processed_df, feature_cols = self.preprocess_data()
            
            if processed_df is False:
                return False, feature_cols  # feature_cols contains error message
            
            # Scale features
            features = self.scaler.fit_transform(processed_df[feature_cols])
            
            # Train Isolation Forest model
            self.model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            )
            
            # Predict anomalies (-1 for anomaly, 1 for normal)
            predictions = self.model.fit_predict(features)
            anomaly_scores = self.model.decision_function(features)
            
            # Add predictions to original dataset
            self.dataset['anomaly_prediction'] = predictions
            self.dataset['anomaly_score'] = anomaly_scores
            self.dataset['is_flagged'] = predictions == -1
            
            # Calculate statistics
            total_transactions = len(self.dataset)
            flagged_count = (predictions == -1).sum()
            normal_count = (predictions == 1).sum()
            
            self.analysis_results = {
                'total_transactions': total_transactions,
                'flagged_count': int(flagged_count),
                'normal_count': int(normal_count),
                'flagged_percentage': (flagged_count / total_transactions) * 100
            }
            
            # Store flagged transactions
            self.flagged_transactions = self.dataset[self.dataset['is_flagged']].copy()
            
            return True, self.analysis_results
            
        except Exception as e:
            return False, f"Analysis error: {str(e)}"
    
    def get_flagged_transactions(self):
        """
        Return flagged transactions for manual inspection.
        
        Returns:
            pandas.DataFrame or None: DataFrame containing flagged transactions
        """
        if self.flagged_transactions is None:
            return None
        return self.flagged_transactions
    
    def get_transaction(self, index):
        """
        Get a specific transaction by index.
        
        Args:
            index: Transaction index
            
        Returns:
            pandas.Series or None: Transaction data
        """
        if self.dataset is None:
            return None
        
        if index < 0 or index >= len(self.dataset):
            return None
        
        return self.dataset.iloc[index]
    
    def validate_transaction(self, index, is_fraud):
        """
        Validate a flagged transaction through manual inspection.
        
        Args:
            index: Transaction index
            is_fraud: Boolean indicating if transaction is confirmed fraud
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.dataset is None:
            return False, "No dataset loaded."
        
        if index < 0 or index >= len(self.dataset):
            return False, "Invalid transaction index."
        
        validation_status = 'Confirmed Fraud' if is_fraud else 'False Positive'
        self.dataset.loc[index, 'validation_status'] = validation_status
        
        return True, f"Transaction {index} marked as: {validation_status}"
    
    def get_recommendation(self, transaction_idx):
        """
        Get recommended action for a flagged transaction.
        
        Args:
            transaction_idx: Index of the transaction
            
        Returns:
            str: Recommendation text
        """
        if self.dataset is None or transaction_idx < 0 or transaction_idx >= len(self.dataset):
            return "Unable to generate recommendation."
        
        transaction = self.dataset.iloc[transaction_idx]
        anomaly_score = transaction.get('anomaly_score', 0)
        
        # Generate recommendations based on anomaly severity
        if anomaly_score < -0.3:
            severity = "HIGH"
            recommendations = [
                "IMMEDIATE ACTION REQUIRED",
                "1. Block the account immediately",
                "2. Contact the account holder for verification",
                "3. File a suspicious activity report (SAR)",
                "4. Escalate to fraud investigation team",
                "5. Review all recent transactions from this account"
            ]
        elif anomaly_score < -0.1:
            severity = "MEDIUM"
            recommendations = [
                "MODERATE RISK - ACTION NEEDED",
                "1. Flag account for monitoring",
                "2. Require additional verification for future transactions",
                "3. Contact account holder to verify transaction",
                "4. Review transaction patterns for the past 30 days",
                "5. Consider temporary transaction limits"
            ]
        else:
            severity = "LOW"
            recommendations = [
                "LOW RISK - MONITOR",
                "1. Add to watchlist for routine monitoring",
                "2. Document the transaction for records",
                "3. No immediate action required",
                "4. Review if similar patterns emerge",
                "5. Consider enhanced due diligence if recurring"
            ]
        
        return f"Risk Level: {severity}\n\n" + "\n".join(recommendations)
    
    def export_results(self, filepath):
        """
        Export analysis results to CSV file.
        
        Args:
            filepath: Path to save the CSV file
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if self.dataset is None:
            return False, "No dataset loaded."
        
        try:
            self.dataset.to_csv(filepath, index=False)
            return True, f"Results exported to {filepath}"
        except Exception as e:
            return False, f"Export error: {str(e)}"
