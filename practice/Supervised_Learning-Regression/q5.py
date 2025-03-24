import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

#from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression

# sklearn의 KFold 모듈 불러오기
from sklearn.model_selection import KFold

"""
1. 사이킷런에 존재하는 데이터를 불러오고, 
   불러온 데이터를 학습용 데이터와 테스트용 데이터로 
   분리하여 반환하는 함수를 구현합니다.
"""
def load_data():
    # 데이터 URL에서 로드
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep=r"\s+", skiprows=22, header=None)

    # 입력 변수(X)와 타겟 변수(y) 설정
    X = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    y = raw_df.values[1::2, 2]

    # feature names 추가
    feature_names = np.array(['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 
                              'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT'], dtype='<U7')

    # 데이터 분할 (80% train, 20% test)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=100)

    print("데이터의 입력값(X)의 개수 :", train_X.shape[1])

    return train_X, test_X, train_y, test_y
    

"""
2. K-fold 교차 검증을 통한 
   모델 학습 및 예측 수행을 진행할 함수를 구현합니다.
"""
def kfold_regression(train_X, train_y):
    
    # 반복문 내에서 횟수를 표시하기 위한 변수 설정하기
    n_iter = 0
    
    # 각 fold 마다 모델 검증 점수를 저장하기 위한 빈 리스트 생성하기
    model_scores = []
    
    kfold = KFold(n_splits=5)
    
    for train_idx, val_idx in kfold.split(train_X):
        
        X_train, X_val = train_X[train_idx], train_X[val_idx]
        y_train, y_val = train_y[train_idx], train_y[val_idx]
        
        # 동일한 가중치 사용을 위해 각 fold 마다 모델 초기화 하기
        model = LinearRegression()
        
        model.fit(X_train, y_train)
        
        # 각 Iter 별 모델 평가 점수 측정
        score = model.score(X_val, y_val)
        
        # 학습용 데이터의 크기를 저장합니다.
        train_size = X_train.shape[0]
        val_size = X_val.shape[0]
    
        print("Iter : {0} Cross-Validation Accuracy : {1}, Train Data 크기 : {2}, Validation Data 크기 : {3}"
              .format(n_iter, score, train_size, val_size))
    
        n_iter += 1
        
        # 전체 모델 점수를 저장하는 리스트에 추가하기
        model_scores.append(score)
        
    return kfold, model, model_scores
        
        
def main():
    
    # 학습용 데이터와 테스트 데이터 불러오기
    train_X, test_X, train_y, test_y = load_data()
    
    # KFold 교차 검증을 통한 학습 결과와 회귀 모델을 반환하는 함수 호출하기
    kfold, model, model_scores = kfold_regression(train_X, train_y)
    
    # 전체 성능 점수의 평균 점수 출력
    print("\n> 평균 검증 모델 점수 : ", np.mean(model_scores))
    

    
if __name__ == "__main__":
    main()