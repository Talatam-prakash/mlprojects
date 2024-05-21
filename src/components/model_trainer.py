import os 
import sys
from dataclasses import dataclass

from sklearn.ensemble import(
    AdaBoostRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.neighbors  import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import r2_score

from src.logger import logging
from src.exception import CustomException

from src.utils import save_object,evalute_model


@dataclass 
class ModelTrainerConfig:
    trainer_model_file_path=os.path.join("artifact","model.pkl")
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
        
    def intiate_model_trainer(self,train_data,test_data):
        
        try:
            
            logging.info("Splitting the data ")
            x_train,y_train,x_test,y_test= (
                train_data[:,:-1],
                train_data[:,-1],
                test_data[:,:-1],
                test_data[:,-1]
            )
            models={
               "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                
            }
            model_report:dict=evalute_model(X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,
                                             models=models)
            
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model=models[best_model_name]
            
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info("Best model found ")
            
            save_object(
                file_path=self.model_trainer_config.trainer_model_file_path,
                obj=best_model
            )
            
            predicted=best_model.predict(x_test)
            r2=r2_score(y_test,predicted)
             
            return r2
        except Exception as e:
            raise CustomException(e,sys)