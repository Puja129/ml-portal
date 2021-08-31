# ml-portal
 - The unified ML UI interface to host a series of ML modeling in DC.

As a first step to provide Machine Learning capability through ml-portal, we explored Streamlit, an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. It provides us capability to use any Machine Learning Algorithm as per our needs. We also have the flexibility to apply multiple classifiers on same data-set or same classifier on multiple data-sets.

To run Streamlit from our system, we just need to install Streamlit using the command:
```
pip install streamlit
```
and then run the app using 
```
streamlit run <app-name>
```

For ease of use, all the required libraries/dependencies have been provided in **requirements.txt** file. So, all the required dependencies can be installed using a single command as shown below:
```
pip install -r requirements.txt
```

## App to derive Geo-locations from EC Service Logs
This app is designed to provide ability to users to upload EC Service Logs to get the geo-locations of the EC agents. The users can upload the service-logs either through an API endpoint (FastAPI) or through a UI (Streamlit). 

**FastAPI** is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. FastAPI supports data validation via pydantic and automatic API documentation as well. It is a modern, async alternative to Flask with the capability of supporting asynchronous function handlers.

**Streamlit**, meanwhile, is an application framework that makes it easy for data scientists and machine learning engineers to create powerful user interfaces that interact with machine learning models.

Here is the process flow to derive geo-locations from EC Service Logs:
<img width="935" alt="geo_loc_process_flow" src="https://user-images.githubusercontent.com/20440873/131532775-167e8933-15b6-48b0-b122-bd624a7bbaa1.png">




