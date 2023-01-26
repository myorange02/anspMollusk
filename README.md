# anspMollusk

This is a repository that saves mollusk API code and web scrapping code using beautifulsoup4 and pandas

"main.py" will be the code to use for scrapping data from BHL. In order to use it, three adjustments are needed before running the code.


First, initial excel file that will be used must have the format that is required to run the program, though format is pretty simple.
In the excel file, there should be two columns, "Genus" column and "Species" column. Their text has to be exactly match or the program would cause an error.
The way program initiate is finding the matching name for each column and append all the data to its local list.

The next two steps are setting correct locations for where initial excel file is sitting, and after runnign the code, the new excel file will be created as the output.
It is important to set the location you want to save at the specific repository.
There will be a line that contains the location of the file, which is look like this:

df = pd.read_excel(r'D:\coding\nameFiltered.xlsx', sheet_name = 'Sheet1')
 
You should change the location based on your desktop or laptop location setting.
You should put the location of the excel file from your pc.
For indicating local drive, for example, it starts with D:, and every time you move in to another folder, you use \ as an indication.
At the end of the line, there is something called sheet_name. You can actually designate specific sheet name from your excel to make sure the program runs the correct file.

When you go to line 154, you will see this code:

df2.to_excel(r'D:\\coding\\test_database.xlsx', index = False)

As you did from previous step, you just need to put appropriate location where file will be saved.
