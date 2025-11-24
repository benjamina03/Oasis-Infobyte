"""
Mobile Money Transaction Anomaly Detection System
==================================================
A prototype for detecting anomalous transactions in mobile money ecosystems.

Objectives:
1. Upload a mobile money dataset for analysis
2. Analyse the dataset against "normal" transaction behaviour
3. Flag fraudulent activities in mobile money transactions
4. Validate flagged transactions through manual inspection
5. Recommend appropriate actions for flagged transactions

Author: Capstone Project
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import os
import tempfile

# Import the core analyzer module
from analyzer import TransactionAnalyzer


class FraudDetectionApp:
    """GUI Application for Mobile Money Fraud Detection."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mobile Money Transaction Anomaly Detection System")
        self.root.geometry("1200x800")
        
        self.analyzer = TransactionAnalyzer()
        self.current_transaction_idx = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_container, 
            text="Detection of Anomalous Transactions in Mobile Money Ecosystems",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Upload Dataset
        self.upload_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.upload_tab, text="1. Upload Dataset")
        self.setup_upload_tab()
        
        # Tab 2: Analysis
        self.analysis_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.analysis_tab, text="2. Analyze Transactions")
        self.setup_analysis_tab()
        
        # Tab 3: Flagged Transactions
        self.flagged_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.flagged_tab, text="3. Flagged Transactions")
        self.setup_flagged_tab()
        
        # Tab 4: Validation
        self.validation_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.validation_tab, text="4. Manual Validation")
        self.setup_validation_tab()
        
        # Tab 5: Recommendations
        self.recommendations_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.recommendations_tab, text="5. Recommendations")
        self.setup_recommendations_tab()
        
    def setup_upload_tab(self):
        """Setup the dataset upload tab."""
        # Instructions
        instructions = ttk.Label(
            self.upload_tab,
            text="Upload a mobile money transaction dataset (CSV format) for analysis.",
            font=('Helvetica', 12)
        )
        instructions.pack(pady=20)
        
        # File path display
        self.filepath_var = tk.StringVar()
        filepath_frame = ttk.Frame(self.upload_tab)
        filepath_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filepath_frame, text="Selected File:").pack(side=tk.LEFT)
        ttk.Entry(filepath_frame, textvariable=self.filepath_var, width=80, state='readonly').pack(side=tk.LEFT, padx=10)
        
        # Browse button
        browse_btn = ttk.Button(
            self.upload_tab, 
            text="Browse & Upload Dataset",
            command=self.upload_dataset
        )
        browse_btn.pack(pady=20)
        
        # Dataset info display
        self.dataset_info = scrolledtext.ScrolledText(self.upload_tab, height=15, width=100)
        self.dataset_info.pack(pady=10)
        
        # Generate sample dataset button
        sample_btn = ttk.Button(
            self.upload_tab,
            text="Generate Sample Dataset (for testing)",
            command=self.generate_sample_dataset
        )
        sample_btn.pack(pady=10)
        
    def setup_analysis_tab(self):
        """Setup the analysis tab."""
        # Instructions
        instructions = ttk.Label(
            self.analysis_tab,
            text="Analyze the uploaded dataset to identify anomalous transactions.",
            font=('Helvetica', 12)
        )
        instructions.pack(pady=20)
        
        # Contamination parameter
        param_frame = ttk.Frame(self.analysis_tab)
        param_frame.pack(pady=10)
        
        ttk.Label(param_frame, text="Expected Fraud Rate (%):").pack(side=tk.LEFT)
        self.contamination_var = tk.StringVar(value="10")
        contamination_entry = ttk.Entry(param_frame, textvariable=self.contamination_var, width=10)
        contamination_entry.pack(side=tk.LEFT, padx=10)
        
        # Analyze button
        analyze_btn = ttk.Button(
            self.analysis_tab,
            text="Analyze Transactions",
            command=self.analyze_transactions
        )
        analyze_btn.pack(pady=20)
        
        # Results display
        self.analysis_results = scrolledtext.ScrolledText(self.analysis_tab, height=20, width=100)
        self.analysis_results.pack(pady=10)
        
    def setup_flagged_tab(self):
        """Setup the flagged transactions tab."""
        # Instructions
        instructions = ttk.Label(
            self.flagged_tab,
            text="View all transactions flagged as potentially fraudulent.",
            font=('Helvetica', 12)
        )
        instructions.pack(pady=10)
        
        # Treeview for flagged transactions
        columns = ('Index', 'Score', 'Details')
        self.flagged_tree = ttk.Treeview(self.flagged_tab, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.flagged_tree.heading(col, text=col)
            self.flagged_tree.column(col, width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.flagged_tab, orient=tk.VERTICAL, command=self.flagged_tree.yview)
        self.flagged_tree.configure(yscrollcommand=scrollbar.set)
        
        self.flagged_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        refresh_btn = ttk.Button(
            self.flagged_tab,
            text="Refresh Flagged Transactions",
            command=self.refresh_flagged_list
        )
        refresh_btn.pack(pady=10)
        
    def setup_validation_tab(self):
        """Setup the manual validation tab."""
        # Instructions
        instructions = ttk.Label(
            self.validation_tab,
            text="Manually inspect and validate flagged transactions.",
            font=('Helvetica', 12)
        )
        instructions.pack(pady=10)
        
        # Transaction selector
        selector_frame = ttk.Frame(self.validation_tab)
        selector_frame.pack(pady=10)
        
        ttk.Label(selector_frame, text="Transaction Index:").pack(side=tk.LEFT)
        self.transaction_idx_var = tk.StringVar(value="0")
        idx_entry = ttk.Entry(selector_frame, textvariable=self.transaction_idx_var, width=10)
        idx_entry.pack(side=tk.LEFT, padx=10)
        
        load_btn = ttk.Button(selector_frame, text="Load Transaction", command=self.load_transaction_for_validation)
        load_btn.pack(side=tk.LEFT, padx=10)
        
        # Transaction details display
        self.transaction_details = scrolledtext.ScrolledText(self.validation_tab, height=15, width=100)
        self.transaction_details.pack(pady=10)
        
        # Validation buttons
        validation_frame = ttk.Frame(self.validation_tab)
        validation_frame.pack(pady=20)
        
        confirm_fraud_btn = ttk.Button(
            validation_frame,
            text="✓ Confirm as Fraud",
            command=lambda: self.validate_transaction(True)
        )
        confirm_fraud_btn.pack(side=tk.LEFT, padx=10)
        
        false_positive_btn = ttk.Button(
            validation_frame,
            text="✗ Mark as False Positive",
            command=lambda: self.validate_transaction(False)
        )
        false_positive_btn.pack(side=tk.LEFT, padx=10)
        
        # Validation status
        self.validation_status = ttk.Label(self.validation_tab, text="", font=('Helvetica', 12))
        self.validation_status.pack(pady=10)
        
    def setup_recommendations_tab(self):
        """Setup the recommendations tab."""
        # Instructions
        instructions = ttk.Label(
            self.recommendations_tab,
            text="Get recommended actions for flagged transactions.",
            font=('Helvetica', 12)
        )
        instructions.pack(pady=10)
        
        # Transaction selector
        selector_frame = ttk.Frame(self.recommendations_tab)
        selector_frame.pack(pady=10)
        
        ttk.Label(selector_frame, text="Transaction Index:").pack(side=tk.LEFT)
        self.rec_idx_var = tk.StringVar(value="0")
        rec_idx_entry = ttk.Entry(selector_frame, textvariable=self.rec_idx_var, width=10)
        rec_idx_entry.pack(side=tk.LEFT, padx=10)
        
        get_rec_btn = ttk.Button(selector_frame, text="Get Recommendations", command=self.get_recommendations)
        get_rec_btn.pack(side=tk.LEFT, padx=10)
        
        # Recommendations display
        self.recommendations_display = scrolledtext.ScrolledText(self.recommendations_tab, height=20, width=100)
        self.recommendations_display.pack(pady=10)
        
    def upload_dataset(self):
        """Handle dataset upload."""
        filepath = filedialog.askopenfilename(
            title="Select Mobile Money Transaction Dataset",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if filepath:
            self.filepath_var.set(filepath)
            success, message = self.analyzer.load_dataset(filepath)
            
            self.dataset_info.delete(1.0, tk.END)
            self.dataset_info.insert(tk.END, f"{message}\n\n")
            
            if success:
                # Display dataset preview
                self.dataset_info.insert(tk.END, "Dataset Preview:\n")
                self.dataset_info.insert(tk.END, "-" * 80 + "\n")
                self.dataset_info.insert(tk.END, f"Columns: {list(self.analyzer.dataset.columns)}\n\n")
                self.dataset_info.insert(tk.END, "First 10 rows:\n")
                self.dataset_info.insert(tk.END, self.analyzer.dataset.head(10).to_string())
                self.dataset_info.insert(tk.END, "\n\n")
                self.dataset_info.insert(tk.END, "Dataset Statistics:\n")
                self.dataset_info.insert(tk.END, self.analyzer.dataset.describe().to_string())
                
                messagebox.showinfo("Success", "Dataset uploaded successfully!")
            else:
                messagebox.showerror("Error", message)
                
    def generate_sample_dataset(self):
        """Generate a sample dataset for testing."""
        # Create sample mobile money transaction data
        np.random.seed(42)
        n_samples = 1000
        
        # Normal transactions
        normal_amounts = np.random.normal(5000, 2000, int(n_samples * 0.9))
        normal_amounts = np.clip(normal_amounts, 100, 15000)
        
        # Anomalous transactions (potential fraud)
        anomaly_amounts = np.random.uniform(50000, 200000, int(n_samples * 0.1))
        
        amounts = np.concatenate([normal_amounts, anomaly_amounts])
        np.random.shuffle(amounts)
        
        # Generate other features
        transaction_types = np.random.choice(
            ['TRANSFER', 'CASH_OUT', 'PAYMENT', 'CASH_IN', 'DEBIT'],
            n_samples,
            p=[0.35, 0.25, 0.20, 0.15, 0.05]
        )
        
        # Generate sender and receiver IDs
        sender_ids = [f"C{np.random.randint(100000, 999999)}" for _ in range(n_samples)]
        receiver_ids = [f"M{np.random.randint(100000, 999999)}" for _ in range(n_samples)]
        
        # Balance before and after
        old_balance = np.random.uniform(1000, 100000, n_samples)
        new_balance = old_balance - amounts * np.random.uniform(0.8, 1.0, n_samples)
        new_balance = np.clip(new_balance, 0, None)
        
        # Create DataFrame
        sample_data = pd.DataFrame({
            'step': range(1, n_samples + 1),
            'type': transaction_types,
            'amount': amounts,
            'nameOrig': sender_ids,
            'oldbalanceOrg': old_balance,
            'newbalanceOrg': new_balance,
            'nameDest': receiver_ids,
            'oldbalanceDest': np.random.uniform(0, 50000, n_samples),
            'newbalanceDest': np.random.uniform(0, 100000, n_samples),
        })
        
        # Save to temp file using cross-platform temp directory
        sample_filepath = os.path.join(tempfile.gettempdir(), "sample_mobile_money_data.csv")
        sample_data.to_csv(sample_filepath, index=False)
        
        # Load the sample dataset
        self.filepath_var.set(sample_filepath)
        success, message = self.analyzer.load_dataset(sample_filepath)
        
        self.dataset_info.delete(1.0, tk.END)
        self.dataset_info.insert(tk.END, "Sample Dataset Generated Successfully!\n\n")
        self.dataset_info.insert(tk.END, f"{message}\n\n")
        
        if success:
            self.dataset_info.insert(tk.END, "Dataset Preview:\n")
            self.dataset_info.insert(tk.END, "-" * 80 + "\n")
            self.dataset_info.insert(tk.END, f"Columns: {list(self.analyzer.dataset.columns)}\n\n")
            self.dataset_info.insert(tk.END, "First 10 rows:\n")
            self.dataset_info.insert(tk.END, self.analyzer.dataset.head(10).to_string())
            
        messagebox.showinfo("Success", "Sample dataset generated and loaded!")
        
    def analyze_transactions(self):
        """Analyze transactions for anomalies."""
        try:
            contamination = float(self.contamination_var.get()) / 100
            if contamination <= 0 or contamination >= 0.5:
                messagebox.showerror("Error", "Expected fraud rate must be between 0 and 50%")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for expected fraud rate")
            return
        
        success, results = self.analyzer.analyze_transactions(contamination)
        
        self.analysis_results.delete(1.0, tk.END)
        
        if success:
            self.analysis_results.insert(tk.END, "=" * 60 + "\n")
            self.analysis_results.insert(tk.END, "TRANSACTION ANALYSIS RESULTS\n")
            self.analysis_results.insert(tk.END, "=" * 60 + "\n\n")
            
            self.analysis_results.insert(tk.END, f"Total Transactions Analyzed: {results['total_transactions']}\n")
            self.analysis_results.insert(tk.END, f"Normal Transactions: {results['normal_count']}\n")
            self.analysis_results.insert(tk.END, f"Flagged Transactions: {results['flagged_count']}\n")
            self.analysis_results.insert(tk.END, f"Flagged Percentage: {results['flagged_percentage']:.2f}%\n\n")
            
            self.analysis_results.insert(tk.END, "-" * 60 + "\n")
            self.analysis_results.insert(tk.END, "ANALYSIS COMPLETE\n")
            self.analysis_results.insert(tk.END, "-" * 60 + "\n\n")
            
            self.analysis_results.insert(tk.END, "The Isolation Forest algorithm has identified potentially\n")
            self.analysis_results.insert(tk.END, "anomalous transactions based on deviation from normal patterns.\n\n")
            
            self.analysis_results.insert(tk.END, "Next Steps:\n")
            self.analysis_results.insert(tk.END, "1. Go to 'Flagged Transactions' tab to view suspicious transactions\n")
            self.analysis_results.insert(tk.END, "2. Use 'Manual Validation' tab to verify each flagged transaction\n")
            self.analysis_results.insert(tk.END, "3. Check 'Recommendations' tab for suggested actions\n")
            
            # Auto-refresh flagged transactions list
            self.refresh_flagged_list()
            
            messagebox.showinfo("Analysis Complete", f"Found {results['flagged_count']} potentially fraudulent transactions!")
        else:
            self.analysis_results.insert(tk.END, f"Analysis Failed: {results}\n")
            messagebox.showerror("Error", str(results))
            
    def refresh_flagged_list(self):
        """Refresh the list of flagged transactions."""
        # Clear existing items
        for item in self.flagged_tree.get_children():
            self.flagged_tree.delete(item)
        
        flagged = self.analyzer.get_flagged_transactions()
        
        if flagged is not None and len(flagged) > 0:
            for idx, row in flagged.iterrows():
                score = row.get('anomaly_score', 'N/A')
                # Create a summary of the transaction details with safe formatting
                amount = row.get('amount', 'N/A')
                amount_str = f"{amount:.2f}" if isinstance(amount, (int, float)) else str(amount)
                details = f"Type: {row.get('type', 'N/A')}, Amount: {amount_str}"
                score_str = f"{score:.4f}" if isinstance(score, (int, float)) else str(score)
                self.flagged_tree.insert('', tk.END, values=(idx, score_str, details))
        else:
            messagebox.showinfo("Info", "No flagged transactions found. Please run analysis first.")
            
    def load_transaction_for_validation(self):
        """Load a specific transaction for manual validation."""
        try:
            idx = int(self.transaction_idx_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid transaction index")
            return
        
        if self.analyzer.dataset is None:
            messagebox.showerror("Error", "No dataset loaded. Please upload a dataset first.")
            return
        
        if idx < 0 or idx >= len(self.analyzer.dataset):
            messagebox.showerror("Error", f"Invalid index. Must be between 0 and {len(self.analyzer.dataset) - 1}")
            return
        
        transaction = self.analyzer.dataset.iloc[idx]
        
        self.transaction_details.delete(1.0, tk.END)
        self.transaction_details.insert(tk.END, "=" * 60 + "\n")
        self.transaction_details.insert(tk.END, f"TRANSACTION #{idx} DETAILS\n")
        self.transaction_details.insert(tk.END, "=" * 60 + "\n\n")
        
        for col, value in transaction.items():
            self.transaction_details.insert(tk.END, f"{col}: {value}\n")
        
        # Show if flagged
        if 'is_flagged' in transaction:
            status = "⚠️ FLAGGED AS SUSPICIOUS" if transaction['is_flagged'] else "✓ Normal"
            self.transaction_details.insert(tk.END, f"\nStatus: {status}\n")
        
        # Show validation status if exists
        if 'validation_status' in transaction and pd.notna(transaction['validation_status']):
            self.transaction_details.insert(tk.END, f"Validation: {transaction['validation_status']}\n")
            
    def validate_transaction(self, is_fraud):
        """Validate a transaction as fraud or false positive."""
        try:
            idx = int(self.transaction_idx_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid transaction index")
            return
        
        success, message = self.analyzer.validate_transaction(idx, is_fraud)
        
        if success:
            status = "CONFIRMED FRAUD" if is_fraud else "FALSE POSITIVE"
            self.validation_status.config(text=f"Transaction {idx}: {status}")
            messagebox.showinfo("Validation Complete", message)
            
            # Reload transaction details
            self.load_transaction_for_validation()
        else:
            messagebox.showerror("Error", message)
            
    def get_recommendations(self):
        """Get recommendations for a flagged transaction."""
        try:
            idx = int(self.rec_idx_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid transaction index")
            return
        
        if self.analyzer.dataset is None:
            messagebox.showerror("Error", "No dataset loaded. Please upload and analyze a dataset first.")
            return
        
        if idx < 0 or idx >= len(self.analyzer.dataset):
            messagebox.showerror("Error", f"Invalid index. Must be between 0 and {len(self.analyzer.dataset) - 1}")
            return
        
        recommendations = self.analyzer.get_recommendation(idx)
        
        self.recommendations_display.delete(1.0, tk.END)
        self.recommendations_display.insert(tk.END, "=" * 60 + "\n")
        self.recommendations_display.insert(tk.END, f"RECOMMENDATIONS FOR TRANSACTION #{idx}\n")
        self.recommendations_display.insert(tk.END, "=" * 60 + "\n\n")
        self.recommendations_display.insert(tk.END, recommendations)
        self.recommendations_display.insert(tk.END, "\n\n")
        self.recommendations_display.insert(tk.END, "-" * 60 + "\n")
        self.recommendations_display.insert(tk.END, "Note: These recommendations are based on the anomaly\n")
        self.recommendations_display.insert(tk.END, "score calculated during analysis. Final decisions should\n")
        self.recommendations_display.insert(tk.END, "be made by qualified fraud investigators.\n")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = FraudDetectionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
