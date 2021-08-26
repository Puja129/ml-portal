# ml-portal
 - The unified ML UI interface to host a series of ML modeling in DC.

As a first step to provide Machine Learning capability through ml-portal, we explored Streamlit, an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. It provides us capability to use any Machine Learning Algorithm as per our needs. We also have the flexibility to apply multiple classifiers on same data-set or same classifier on multiple data-sets.

To run Streamlit from our system, we just need to install Streamlit using the command:
```
pip install streamlit
```
For ease of use, all the required libraries/dependencies have been provided in **requirements.txt** file. So, all the required dependencies can be installed using a single command as shown below:
```
pip install -r <path-to-requirements.txt>
```

## App to derive Geo-locations from EC Service Logs
This app is designed to provide ability to users to upload EC Service Logs to get the geo-locations of the EC agents. The users can upload the service-logs either through an API endpoint (FastAPI) or through a UI (Streamlit).
Here is the process flow to derive geo-locations from EC Service Logs: ![Geo-Locations_Process_Flow](https://user-images.githubusercontent.com/20440873/131028463-8b78ce59-6dd8-4fbe-939f-f28b568dd896.png)

