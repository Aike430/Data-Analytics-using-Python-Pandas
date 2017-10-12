# Download the zip file and extract it.
# Install the dependencies using the following command
# make sure the files requirements.txt, states.py, source1.csv & source2.csv file is in the same folder as report.py
# states.py file contains a dictionary of state codes as keys and full names as values
# In order to simplify the execution input file paths were hard coded and should be included in the same folder as report.py

pip install --upgrade -r requirements.txt

# Run the report.py script

python -B report.py 

#Note: -B to avoid generating .pyc files

Successful execution of script generates a report.pdf file


5. What was the total cost per view for all video ads, truncated to two decimal places?
Note: Calculated as ration of total cost for all the video ads to total views for the video ads
      (total cost for video ads / total views for video ads)


7. What combination of state and hair color had the best CPM?
Note: grouped the data based on state_hair-color combo and calculated the cpm based on all the 
campaigns_ids in that group
cpm = (total costs / total impression) * 1000

