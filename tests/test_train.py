from churnguard.data import load_data, preprocess
from churnguard.train import train_model
from churnguard.evaluate import compute_metrics

def test_train_model_returns_fitted_pipeline():
    df = load_data('./data/telco_churn.csv')
    X_train, X_test, y_train, y_test, preprocessed = preprocess(df)

    model = train_model(X_train, X_test, y_train, y_test, preprocessed)

    y_pred = model.predict(X_test)
    assert len(y_pred) == len(y_test)

    y_proba = model.predict_proba(X_test)
    assert y_proba.shape[0] == len(y_test)
    assert y_proba.shape[1] == 2


def test_compute_metrics_returns_expected_keys():
    df = load_data('./data/telco_churn.csv')
    X_train, X_test, y_train, y_test, preprocessed = preprocess(df)

    model = train_model(X_train, X_test, y_train, y_test, preprocessed)

    metrics = compute_metrics(model, X_test, y_test)

    expected_keys = {'accuracy_score', 'precision_score', 'recall_score', 'f1_score', 'roc_auc_score'}

    assert isinstance(metrics, dict)
    assert expected_keys.issubset(metrics.keys())

   