from churnguard.data import load_data, preprocess
from churnguard.train import train_model
from churnguard.evaluate import compute_metrics


def main():
    df = load_data("./data/telco_churn.csv")
    X_train, X_test, y_train, y_test, preprocessed = preprocess(df)

    model = train_model(X_train, X_test, y_train, y_test, preprocessed)
    compute_metrics(model, X_test, y_test)


if __name__ == "__main__":
    main()
