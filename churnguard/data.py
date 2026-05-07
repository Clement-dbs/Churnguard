import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

def load_data(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

def preprocess(df:pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df = df.dropna()
    df = df.drop(columns=['customerID'])

    y = (df['Churn'] == 'Yes').astype(int)
    X = df.drop(columns=['Churn'])

    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
    cat_cols = [c for c in X.columns if c not in num_cols]

    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
    cat_cols = [c for c in X.columns if c not in num_cols]

    preprocessed = ColumnTransformer([
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols),
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    return X_train, X_test, y_train, y_test, preprocessed

