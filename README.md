# Project_Part_4

We completed a portion of the extra credit project module.

## Setup
Download the files project_bonus.py, copy_files.sh, login.sh, pip_install.sh, and requirements.txt into a folder on your local computer. In order to later log into our EC2 instance, it must be the same folder where the .pem key is located. Run this command to copy the necessary files into our EC2 instance called group19-proj4: 

      bash copy_files.sh
      
 Now login to the EC2 instance from the folder where the .pem key is located:

      bash login.sh
 
 You are inside the EC2 instance now. Use the ls command to make sure the desired files are there. Now install the necessary packages:

      pip install -r requirements.txt
      
 If you get an error saying the command pip is not found, run this command before installing requirements:
 
      bash pip_install.sh
      
 Once you have the necessary packages successfulyl installed, you can run the script with:
 
      python3 project_bonus.py

The script's functions are discussed below. 

      
## Paragraph Scraping
 For the scraping of paragraph data, we utilized the BeautifulSoup and requests python libraries. We start by defining the url variable to hold the web address of the webpage to be scraped, "https://www.abs.gov.au/statistics/health/health-conditions-and-risks/smoking/2020-21".
We then use the function requests.get(url) to send an HTTP GET request to the specified URL and retrieve the webpage's content, which is stored in the variable response. The BeautifulSoup(response.content, "html.parser") line parses the response.content, and we extract all paragraphs using soup.find_all("p"), by finding all the <p> tags within the BeautifulSoup object. the resulting paragraphs list is stored in paragraphs. 

## Paragraph Insertion into DynamoDB
  We connect to dynamodb using AWS' boto3 library, and access the ‘group-19’ table. 
  Next, for each element in the paragraphs list, we create a data object consisting of a primary key ('id'), a content field containing the text of the element, a  url field containing the url of the webpage, and an access_time field that is when the field was being updated. We then insert the data object into the table using table.put_item().
  
## Comparing Previous Data to Paragraphs
  After using our previous code to get the Proportion of current daily smokers by age, 2020-21, we then transpose the 2D list and extract the data column. We then iterate over each number and access DynamoDB to filter the items of the table that contain the number. If the filtered response contains nothing, then we know the number is not referenced in any paragraph.
  
  
## Airflow
  We did not utilize airflow for this assignment, as our previous assignment utilizing airflow used AWS MWAA instead of EC2, so we weren't sure how to get MWAA to be able to use DynamoDB. 
  
  
  
  



