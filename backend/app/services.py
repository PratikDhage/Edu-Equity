import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from .database import get_db, Base, engine
from .models import District
import joblib
from pathlib import Path

def setup_data():
    try:
        df = pd.read_csv(Path(__file__).parent.parent / 'ml/data/schools.csv', low_memory=False)
    except FileNotFoundError:
        print("Error: schools.csv not found! Using sample data.")
        df = pd.DataFrame([
            {"district_name": "Delhi", "state_code": "DL", "class_rooms": 20, "total_teachers": 15, "latitude": 28.6139, "longitude": 77.2090, "i_students": 100, "ii_students": 80},
            {"district_name": "Mumbai", "state_code": "MH", "class_rooms": 25, "total_teachers": 20, "latitude": 19.0760, "longitude": 72.8777, "i_students": 150, "ii_students": 120},
            {"district_name": "Kolkata", "state_code": "WB", "class_rooms": 18, "total_teachers": 12, "latitude": 22.5726, "longitude": 88.3639, "i_students": 90, "ii_students": 70}
        ])

    df = df.dropna(subset=['district_name', 'state_code', 'latitude', 'longitude', 'class_rooms', 'total_teachers'])
    df['class_students'] = df.filter(like='_students').sum(axis=1) if 'i_students' in df.columns else 300.0
    df['student_teacher_ratio'] = df['class_students'] / df['total_teachers'].replace(0, 1)
    agg_df = df.groupby('district_name').agg({
        'class_rooms': 'mean', 'total_teachers': 'mean', 'class_students': 'mean',
        'student_teacher_ratio': 'mean', 'latitude': 'mean', 'longitude': 'mean', 'state_code': 'first'
    }).reset_index()

    features = ['class_rooms', 'total_teachers', 'class_students', 'student_teacher_ratio']
    X = agg_df[features].fillna(0)
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)

    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    agg_df['cluster'] = clusters

    iso = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso.fit_predict(X_scaled)
    agg_df['anomaly'] = [1 if a == -1 else 0 for a in anomalies]

    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X_scaled, agg_df['class_students'])

    models_dir = Path(__file__).parent.parent / 'ml/models'
    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(kmeans, models_dir / 'kmeans.joblib')
    joblib.dump(rf, models_dir / 'rf.joblib')
    joblib.dump(scaler, models_dir / 'scaler.joblib')
    joblib.dump(iso, models_dir / 'iso.joblib')

    Base.metadata.create_all(engine)
    db = next(get_db())
    db.query(District).delete()
    for _, row in agg_df.iterrows():
        db.add(District(**row.to_dict()))
    db.commit()
    print("Data setup complete!")

def get_clusters(state_code=None):
    db = next(get_db())
    query = db.query(District)
    if state_code:
        query = query.filter(District.state_code == state_code)
    df = pd.read_sql(query.statement, db.bind)
    if len(df) == 0:
        return []
    scaler = joblib.load(Path(__file__).parent.parent / 'ml/models/scaler.joblib')
    kmeans = joblib.load(Path(__file__).parent.parent / 'ml/models/kmeans.joblib')
    features = ['class_rooms', 'total_teachers', 'class_students', 'student_teacher_ratio']
    X = scaler.transform(df[features].fillna(0))
    df['cluster'] = kmeans.predict(X)
    return df.to_dict('records')

def predict_enrollment(features):
    scaler = joblib.load(Path(__file__).parent.parent / 'ml/models/scaler.joblib')
    rf = joblib.load(Path(__file__).parent.parent / 'ml/models/rf.joblib')
    X = np.array([list(features.values())]).reshape(1, -1)
    X_scaled = scaler.transform(X)
    pred = rf.predict(X_scaled)[0]
    return {'predicted_students': float(pred), 'uplift': pred * 1.2}
    
