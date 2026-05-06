import pandas as pd
from churnguard.data import load_data, preprocess

def test_load_data_returns_dataframe():
    df = load_data('./data/telco_churn.csv')
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0


def test_load_data_has_expected_columns():
    df = load_data('./data/telco_churn.csv')
    assert len(df.columns) == 21


def test_preprocess_returns_features_and_target():
    df = load_data('./data/telco_churn.csv')
    X_train, X_test, y_train, y_test, preprocessed = preprocess(df)

    assert X_train.shape[0] == y_train.shape[0]
    assert 'Churn' not in X_train.columns
    assert y_train.isin([0, 1]).all().all()

def test_preprocess_handles_missing_total_charges():
    df = pd.DataFrame({
        'customerID': ['a', 'b', 'c'],
        'TotalCharges': ['10.5', ' ', '20.1'],
        'tenure': [1, 2, 3],
        'MonthlyCharges': [30, 40, 50],
        'SeniorCitizen': [0, 1, 0],
        'Churn': ['No', 'Yes', 'No']
    })

    X_train, X_test, y_train, y_test, preprocessed = preprocess(df)

    total_len = len(X_train) + len(X_test)
    assert total_len == 2


   