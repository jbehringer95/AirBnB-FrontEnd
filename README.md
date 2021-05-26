# airbnb-plotly-dash-app
This repository hosts the model, the plotly dash application, its assets, and other files necessary for the AirBnb applications production. The [data](https://www.kaggle.com/rudymizrahi/airbnb-listings-in-major-us-cities-deloitte-ml) used to create the model is hosted on Kaggle and the production application can be found [here](https://airbnb-app-tt45.herokuapp.com/)

### File Structure
    .
    ├── airbnb_model
    │   ├── saved_model.pb
    ├── assets
    │   ├── treehouse.jpg
    ├── pages 
    │   ├── index.py
    │   ├── predictions.py
    │   ├── process.py
    ├── pred_lists

   
### Installation

First, you need to clone the repository with the method of you choice (zip download or https). 
Next, in your command line, navigate to the model directory. Then you can install the required packages with the following commands:
```
pipenv install && pipenv shell
```
### Usage

Once you are in the shell, you can run the app locally by 
'''
python run.py
'''