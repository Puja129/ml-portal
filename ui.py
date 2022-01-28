import streamlit as st
import re
import os
import json

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# construct UI layout
st.set_option('deprecation.showPyplotGlobalUse', False)
def main():
    html_temp = """
    <div style="background-color:white;"><p style="color:black;font-size:30px;padding:10px"><img width="54" alt="ec-logo" src="https://user-images.githubusercontent.com/20440873/131534094-13f07dd0-8245-49b3-8199-ba3b0424b4b2.png">View Agent Geo-Locations from Service Logs</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    menu = ["About", "Upload EC Service Logs", "View EC-Agent Geo Locations"]
    choice = st.sidebar.selectbox("Menu",menu)
    a_file = open("geoloc.json", "r")
    v = json.load(a_file)

    a_file = open("plot.json", "w")
    json.dump(plot_data, a_file)
    a_file.close()

    if choice == "About":
    	st.subheader("About")
    	st.info("This app is designed to provide ability to users to upload EC Service Logs to get the geo-locations of the EC agents.")
    	st.image("geo_loc_process_flow.png")
    	st.text("by EC Team")

    elif(choice == 'Upload EC Service Logs'):
        st.subheader("Upload EC Service Logs")
        oauth2_token =  st.text_input("OAuth2 Token")
        svc_id = st.text_input("Service ID")
        docx_file = st.file_uploader("Upload File",type=['txt','docx'])
        if st.button("Process"):
            if docx_file.type == "text/plain":
                file_details = {"ServiceId":svc_id,"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
                st.info(file_details)
                oauth2_token = oauth2_token.replace('=','%3D')
                oauth2_token = oauth2_token.replace('+','%2B')

                url = "http://localhost/uploadfile/"+svc_id+"?oauth2_token="+oauth2_token
                filenm = docx_file.name
                with open(docx_file.name, 'wb') as fh:
                    fh.write(docx_file.getbuffer())

                files = {'file': (filenm, open(filenm, 'rb'), 'text/plain', {'Expires': '0'})}
                res = requests.post(url, files=files)
                res.status_code
                if res.status_code != 200:
                    error = {"error_message": "invalid values provided in the request."}
                    st.error(error)
                else:
                    st.success(res.text)
            else:
                error_msg = {"error_message": "please upload ec-service logs in text/plain format."}
                st.error(error_msg)

    else:
    	st.subheader("View EC-Agent Geo Locations")
    	svc_id = st.selectbox("Select Service-Id from the drop-down", options=list(v.values()))
    	st.info("You Selected: {}" .format(svc_id))

    	df = pd.read_json('plot.json')


    	if st.checkbox("Show Dataset"):
    		st.dataframe(df.head())

    	# Show Columns
    	if st.button("Column Names"):
    		st.write(df.columns)

    	# Show Shape
    	if st.checkbox("Shape of Dataset"):
    		data_dim = st.radio("Show Dimension By ",("Rows","Columns"))
    		if data_dim == 'Rows':
    			st.text("Number of Rows")
    			st.write(df.shape[0])
    		elif data_dim == 'Columns':
    			st.text("Number of Columns")
    			st.write(df.shape[1])
    		else:
    			st.write(df.shape)

    	# Select Columns
    	if st.checkbox("Select Columns To Show"):
    		all_columns = df.columns.tolist()
    		selected_columns = st.multiselect("Select",all_columns)
    		new_df = df[selected_columns]
    		st.dataframe(new_df)

    	# Show Values
    	if st.button("Value Counts"):
    		st.text("Value Counts By Target/Class")
    		st.write(df.iloc[:,-1].value_counts())


    	# Show Datatypes
    	if st.button("Data Types"):
    		st.write(df.dtypes)


    	# Show Summary
    	if st.checkbox("Summary"):
    		st.write(df.describe().T)

    	## Plot and Visualization

    	st.subheader("Data Visualization")

    	# Plot Map
    	if st.checkbox("Map"):
    		st.text("Map")
    		airports = df.head()[['lat', 'lon']][0:100]
    		st.map(airports)

    	# Correlation
    	# Seaborn Plot
    	if st.checkbox("Correlation Plot[Seaborn]"):
    		st.write(sns.heatmap(df.corr(),annot=True))
    		st.pyplot()

    	# Pie Chart
    	if st.checkbox("Pie Plot"):
    		all_columns_names = df.columns.tolist()
    		if st.button("Generate Pie Plot"):
    			st.success("Generating A Pie Plot")
    			st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
    			st.pyplot()

    	# Count Plot
    	if st.checkbox("Plot of Value Counts"):
    		st.text("Value Counts By Target")
    		all_columns_names = df.columns.tolist()
    		primary_col = st.selectbox("Primary Columm to GroupBy",all_columns_names)
    		selected_columns_names = st.multiselect("Select Columns",all_columns_names)
    		if st.button("Plot"):
    			st.text("Generate Plot")
    			if selected_columns_names:
    				vc_plot = df.groupby(primary_col)[selected_columns_names].count()
    			else:
    				vc_plot = df.iloc[:,-1].value_counts()
    			st.write(vc_plot.plot(kind="bar"))
    			st.pyplot()


    	# Customizable Plot

    	st.subheader("Customizable Plot")
    	all_columns_names = df.columns.tolist()
    	type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
    	selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

    	if st.button("Generate Plot"):
    		st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

    		# Plot By Streamlit
    		if type_of_plot == 'area':
    			cust_data = df[selected_columns_names]
    			st.area_chart(cust_data)

    		elif type_of_plot == 'bar':
    			cust_data = df[selected_columns_names]
    			st.bar_chart(cust_data)

    		elif type_of_plot == 'line':
    			cust_data = df[selected_columns_names]
    			st.line_chart(cust_data)

    		# Custom Plot
    		elif type_of_plot:
    			cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
    			st.write(cust_plot)
    			st.pyplot()

    	if st.button("Thanks"):
    		st.balloons()

    os.remove('plot.json')


if __name__ == '__main__':
	main()
