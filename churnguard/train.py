import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from churnguard.evaluate import compute_metrics


models = {
    "logreg": LogisticRegression(max_iter=1000),
    "random_forest": RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
    "gradient_boosting": GradientBoostingClassifier()
}


def train_model(X_train, X_test, y_train, y_test, preprocessed) -> Pipeline:

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("mlops_churnguard")

    best_model = None
    best_score = -1

    for name, clf in models.items():

        with mlflow.start_run(run_name=name):

            model = Pipeline([
                ('prep', preprocessed),
                ('clf', clf),
            ])

            model.fit(X_train, y_train)

            metrics = compute_metrics(model, X_test, y_test)

            for k, v in metrics.items():
                mlflow.log_metric(k, v)

            mlflow.log_param("model_type", name)

            mlflow.sklearn.log_model(model, "model")

            score = metrics["recall_score"] 

            if score > best_score:
                best_score = score
                best_model = model

   
    with mlflow.start_run(run_name="best_model"):

        mlflow.sklearn.log_model(
            best_model,
            "model",
            registered_model_name="churnguard"
        )

   
    client = MlflowClient()

    latest_version = client.get_latest_versions("churnguard")[0]

    client.transition_model_version_stage(
        name="churnguard",
        version=latest_version.version,
        stage="Production",
        archive_existing_versions=True
    )

    return best_model