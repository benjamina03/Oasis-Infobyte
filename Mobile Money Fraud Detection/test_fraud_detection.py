"""
Test script for the Mobile Money Transaction Anomaly Detection System.
Tests the core functionality without GUI.
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from analyzer import TransactionAnalyzer


def generate_test_dataset():
    """Generate a test dataset."""
    np.random.seed(42)
    n_samples = 100
    
    # Normal transactions
    normal_amounts = np.random.normal(5000, 2000, int(n_samples * 0.9))
    normal_amounts = np.clip(normal_amounts, 100, 15000)
    
    # Anomalous transactions
    anomaly_amounts = np.random.uniform(50000, 200000, int(n_samples * 0.1))
    
    amounts = np.concatenate([normal_amounts, anomaly_amounts])
    np.random.shuffle(amounts)
    
    transaction_types = np.random.choice(
        ['TRANSFER', 'CASH_OUT', 'PAYMENT', 'CASH_IN', 'DEBIT'],
        n_samples
    )
    
    data = pd.DataFrame({
        'step': range(1, n_samples + 1),
        'type': transaction_types,
        'amount': amounts,
        'nameOrig': [f"C{i}" for i in range(n_samples)],
        'oldbalanceOrg': np.random.uniform(1000, 100000, n_samples),
        'newbalanceOrg': np.random.uniform(0, 100000, n_samples),
        'nameDest': [f"M{i}" for i in range(n_samples)],
    })
    
    return data


def test_analyzer():
    """Test the TransactionAnalyzer class."""
    print("=" * 60)
    print("TESTING MOBILE MONEY FRAUD DETECTION SYSTEM")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = TransactionAnalyzer()
    print("\n✓ Analyzer initialized successfully")
    
    # Generate and save test data using cross-platform temp directory
    test_data = generate_test_dataset()
    test_filepath = os.path.join(tempfile.gettempdir(), "test_transactions.csv")
    test_data.to_csv(test_filepath, index=False)
    print(f"✓ Test dataset generated: {len(test_data)} transactions")
    
    # Test dataset loading
    success, message = analyzer.load_dataset(test_filepath)
    assert success, f"Dataset loading failed: {message}"
    print(f"✓ Dataset loaded: {message}")
    
    # Test analysis
    success, results = analyzer.analyze_transactions(contamination=0.1)
    assert success, f"Analysis failed: {results}"
    print(f"\n✓ Analysis completed:")
    print(f"  - Total transactions: {results['total_transactions']}")
    print(f"  - Normal transactions: {results['normal_count']}")
    print(f"  - Flagged transactions: {results['flagged_count']}")
    print(f"  - Flagged percentage: {results['flagged_percentage']:.2f}%")
    
    # Test flagged transactions retrieval
    flagged = analyzer.get_flagged_transactions()
    assert flagged is not None, "Failed to get flagged transactions"
    print(f"\n✓ Retrieved {len(flagged)} flagged transactions")
    
    # Test validation
    if len(flagged) > 0:
        idx = flagged.index[0]
        success, message = analyzer.validate_transaction(idx, is_fraud=True)
        assert success, f"Validation failed: {message}"
        print(f"✓ Transaction validation: {message}")
    
    # Test recommendations
    if len(flagged) > 0:
        idx = flagged.index[0]
        recommendation = analyzer.get_recommendation(idx)
        assert recommendation is not None, "Failed to get recommendation"
        print(f"\n✓ Recommendation generated for transaction {idx}:")
        print("-" * 40)
        print(recommendation[:200] + "..." if len(recommendation) > 200 else recommendation)
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
    
    # Cleanup
    os.remove(test_filepath)
    
    return True


if __name__ == "__main__":
    try:
        test_analyzer()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        sys.exit(1)
