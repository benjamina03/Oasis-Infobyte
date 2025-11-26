// ===== DOM Elements =====
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const uploadSection = document.getElementById('upload-section');
const resultsSection = document.getElementById('results-section');
const resultsPlaceholder = document.getElementById('resultsPlaceholder');
const loadingOverlay = document.getElementById('loadingOverlay');

// ===== Sample Data =====
const sampleTransactions = [
    { id: 'TXN-2025-001', amount: 181000.00, oldBalance: 181000.00, newBalance: 0.00, type: 'TRANSFER', ifScore: 0.92, lofScore: 0.88, aeScore: 0.034, probability: 94.2, status: 'Fraud' },
    { id: 'TXN-2025-002', amount: 9839.64, oldBalance: 9839.64, newBalance: 0.00, type: 'CASH_OUT', ifScore: 0.89, lofScore: 0.91, aeScore: 0.028, probability: 91.5, status: 'Fraud' },
    { id: 'TXN-2025-003', amount: 339682.13, oldBalance: 339682.13, newBalance: 0.00, type: 'TRANSFER', ifScore: 0.95, lofScore: 0.93, aeScore: 0.041, probability: 96.8, status: 'Fraud' },
    { id: 'TXN-2025-004', amount: 1250.00, oldBalance: 5420.50, newBalance: 4170.50, type: 'PAYMENT', ifScore: 0.12, lofScore: 0.08, aeScore: 0.003, probability: 8.2, status: 'Valid' },
    { id: 'TXN-2025-005', amount: 45678.90, oldBalance: 45678.90, newBalance: 0.00, type: 'CASH_OUT', ifScore: 0.87, lofScore: 0.84, aeScore: 0.025, probability: 88.7, status: 'Fraud' },
    { id: 'TXN-2025-006', amount: 520.00, oldBalance: 12340.00, newBalance: 11820.00, type: 'DEBIT', ifScore: 0.05, lofScore: 0.06, aeScore: 0.001, probability: 4.1, status: 'Valid' },
    { id: 'TXN-2025-007', amount: 892345.67, oldBalance: 892345.67, newBalance: 0.00, type: 'TRANSFER', ifScore: 0.98, lofScore: 0.96, aeScore: 0.052, probability: 98.4, status: 'Fraud' },
    { id: 'TXN-2025-008', amount: 78.50, oldBalance: 3421.75, newBalance: 3343.25, type: 'PAYMENT', ifScore: 0.02, lofScore: 0.03, aeScore: 0.001, probability: 2.3, status: 'Valid' },
    { id: 'TXN-2025-009', amount: 156789.00, oldBalance: 156789.00, newBalance: 0.00, type: 'CASH_OUT', ifScore: 0.91, lofScore: 0.89, aeScore: 0.031, probability: 92.8, status: 'Fraud' },
    { id: 'TXN-2025-010', amount: 2500.00, oldBalance: 18750.00, newBalance: 16250.00, type: 'TRANSFER', ifScore: 0.15, lofScore: 0.11, aeScore: 0.004, probability: 11.5, status: 'Valid' },
];

// ===== File Upload Handling =====
let selectedFile = null;

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
        alert('Please upload a CSV file.');
        return;
    }
    
    selectedFile = file;
    fileName.textContent = `Selected: ${file.name}`;
}

// ===== Button Event Listeners =====
analyzeBtn.addEventListener('click', () => {
    runAnalysis();
});

clearBtn.addEventListener('click', () => {
    clearAll();
});

function runAnalysis() {
    // Show loading overlay
    loadingOverlay.classList.remove('hidden');
    
    // Simulate analysis delay
    setTimeout(() => {
        loadingOverlay.classList.add('hidden');
        showResults();
    }, 2000);
}

function clearAll() {
    selectedFile = null;
    fileName.textContent = '';
    fileInput.value = '';
    
    // Hide results and show placeholder
    resultsSection.classList.add('hidden');
    resultsPlaceholder.classList.remove('hidden');
    
    // Destroy charts if they exist
    if (window.confusionChart) {
        window.confusionChart.destroy();
        window.confusionChart = null;
    }
    if (window.distributionChart) {
        window.distributionChart.destroy();
        window.distributionChart = null;
    }
    if (window.comparisonChart) {
        window.comparisonChart.destroy();
        window.comparisonChart = null;
    }
}

function showResults() {
    // Hide placeholder and show results
    resultsPlaceholder.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    
    // Generate random metrics (simulating real analysis)
    updateMetrics();
    
    // Populate table
    populateTransactionsTable();
    
    // Create charts
    createCharts();
}

function updateMetrics() {
    // Slight random variations to simulate real analysis
    const randomize = (base, variance) => (base + (Math.random() - 0.5) * variance).toFixed(1);
    
    document.getElementById('if-accuracy').textContent = randomize(97.8, 2) + '%';
    document.getElementById('if-precision').textContent = randomize(95.2, 3) + '%';
    document.getElementById('if-recall').textContent = randomize(89.4, 4) + '%';
    
    document.getElementById('lof-accuracy').textContent = randomize(96.5, 2) + '%';
    document.getElementById('lof-precision').textContent = randomize(93.8, 3) + '%';
    document.getElementById('lof-recall').textContent = randomize(87.2, 4) + '%';
    
    document.getElementById('ae-score').textContent = (0.02 + Math.random() * 0.01).toFixed(4);
    
    // Update summary stats
    const totalTxn = Math.floor(1000000 + Math.random() * 100000);
    const fraudTxn = Math.floor(totalTxn * (0.007 + Math.random() * 0.003));
    const validTxn = totalTxn - fraudTxn;
    const fraudRate = ((fraudTxn / totalTxn) * 100).toFixed(2);
    
    document.getElementById('total-transactions').textContent = totalTxn.toLocaleString();
    document.getElementById('fraudulent-transactions').textContent = fraudTxn.toLocaleString();
    document.getElementById('valid-transactions').textContent = validTxn.toLocaleString();
    document.getElementById('fraud-rate').textContent = fraudRate + '%';
}

function populateTransactionsTable() {
    const tbody = document.getElementById('transactionsBody');
    tbody.innerHTML = '';
    
    sampleTransactions.forEach(txn => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${txn.id}</td>
            <td>$${txn.amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>$${txn.oldBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>$${txn.newBalance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>${txn.type}</td>
            <td>${txn.ifScore.toFixed(2)}</td>
            <td>${txn.lofScore.toFixed(2)}</td>
            <td>${txn.aeScore.toFixed(3)}</td>
            <td>${txn.probability}%</td>
            <td><span class="status-badge status-${txn.status.toLowerCase()}">${txn.status}</span></td>
        `;
        tbody.appendChild(row);
    });
}

function createCharts() {
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') {
        // Show fallback charts
        showFallbackCharts();
        return;
    }
    
    try {
        // Destroy existing charts
        if (window.confusionChart) window.confusionChart.destroy();
        if (window.distributionChart) window.distributionChart.destroy();
        if (window.comparisonChart) window.comparisonChart.destroy();
        
        // Chart.js default configuration
        Chart.defaults.color = '#a0a0c0';
        Chart.defaults.borderColor = 'rgba(77, 208, 225, 0.1)';
        
        // Hide fallback charts, show canvas
        hideFallbackCharts();
        
        // Confusion Matrix Chart
        const confusionCtx = document.getElementById('confusionMatrixChart').getContext('2d');
        window.confusionChart = new Chart(confusionCtx, {
            type: 'bar',
            data: {
                labels: ['True Positive', 'True Negative', 'False Positive', 'False Negative'],
                datasets: [
                    {
                        label: 'Isolation Forest',
                        data: [7823, 1032145, 423, 1185],
                        backgroundColor: 'rgba(179, 136, 255, 0.7)',
                        borderColor: '#B388FF',
                        borderWidth: 1
                    },
                    {
                        label: 'LOF',
                        data: [7456, 1031890, 678, 1552],
                        backgroundColor: 'rgba(77, 208, 225, 0.7)',
                        borderColor: '#4DD0E1',
                        borderWidth: 1
                    },
                    {
                        label: 'Autoencoder',
                        data: [7650, 1032012, 556, 1358],
                        backgroundColor: 'rgba(224, 64, 251, 0.7)',
                        borderColor: '#E040FB',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(77, 208, 225, 0.1)'
                        },
                        ticks: {
                            callback: function(value) {
                                if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M';
                                if (value >= 1000) return (value / 1000).toFixed(0) + 'K';
                                return value;
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
        
        // Distribution Pie Chart
        const distributionCtx = document.getElementById('distributionChart').getContext('2d');
        window.distributionChart = new Chart(distributionCtx, {
            type: 'doughnut',
            data: {
                labels: ['Non-Fraud Transactions', 'Fraud Transactions'],
                datasets: [{
                    data: [99.22, 0.78],
                    backgroundColor: [
                        'rgba(77, 208, 225, 0.8)',
                        'rgba(255, 71, 87, 0.8)'
                    ],
                    borderColor: [
                        '#4DD0E1',
                        '#ff4757'
                    ],
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '%';
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
        
        // Model Comparison Chart
        const comparisonCtx = document.getElementById('comparisonChart').getContext('2d');
        window.comparisonChart = new Chart(comparisonCtx, {
            type: 'bar',
            data: {
                labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                datasets: [
                    {
                        label: 'Isolation Forest',
                        data: [97.8, 95.2, 89.4, 92.2],
                        backgroundColor: 'rgba(179, 136, 255, 0.7)',
                        borderColor: '#B388FF',
                        borderWidth: 2,
                        borderRadius: 8
                    },
                    {
                        label: 'Local Outlier Factor',
                        data: [96.5, 93.8, 87.2, 90.4],
                        backgroundColor: 'rgba(77, 208, 225, 0.7)',
                        borderColor: '#4DD0E1',
                        borderWidth: 2,
                        borderRadius: 8
                    },
                    {
                        label: 'Autoencoder',
                        data: [97.1, 94.5, 88.3, 91.3],
                        backgroundColor: 'rgba(224, 64, 251, 0.7)',
                        borderColor: '#E040FB',
                        borderWidth: 2,
                        borderRadius: 8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 80,
                        max: 100,
                        grid: {
                            color: 'rgba(77, 208, 225, 0.1)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.warn('Chart.js error, using fallback charts:', error);
        showFallbackCharts();
    }
}

function showFallbackCharts() {
    // Hide canvas elements
    document.getElementById('confusionMatrixChart').style.display = 'none';
    document.getElementById('distributionChart').style.display = 'none';
    document.getElementById('comparisonChart').style.display = 'none';
    
    // Show fallback charts
    document.getElementById('confusionFallback').classList.remove('hidden');
    document.getElementById('distributionFallback').classList.remove('hidden');
    document.getElementById('comparisonFallback').classList.remove('hidden');
}

function hideFallbackCharts() {
    // Show canvas elements
    document.getElementById('confusionMatrixChart').style.display = 'block';
    document.getElementById('distributionChart').style.display = 'block';
    document.getElementById('comparisonChart').style.display = 'block';
    
    // Hide fallback charts
    document.getElementById('confusionFallback').classList.add('hidden');
    document.getElementById('distributionFallback').classList.add('hidden');
    document.getElementById('comparisonFallback').classList.add('hidden');
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    // Initial state is already set in HTML
    console.log('Mobile Money Fraud Detection Dashboard initialized');
});
