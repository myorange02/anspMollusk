# anspMollusk

The purpose of creating this program is to get the basis of records of combinations that haven't updated to MolluskaBase and upload them to MolluskaBase. This program will surf through Biodiversity Heritage Library to find any potential sources for basis of records, giving maximum of ten sources to each combination.

"bhl_gen_2.py" and "bhl_gen_3.py" are the programs that are used for scrapping data from BHL. "bhl_gen_2.py" contains all the functions that are used for the programming, and the file itself works as a module. "bhl_gen_3.py" will use "bhl_gen_2.py" as a module to run the actual algorithm. If you want to modifiy searching process, you can edit "bhl_gen_3.py." If you want to edit, add, or delete any functions, you can do that on "bhl_gen_2.py."

In order to use it, three adjustments are needed before running the code.

First, initial excel file that will be used must have the format that is required to run the program, though format is pretty simple.
In the excel file, there should be four columns, "Genus", "Subgenus", "Species", and "Subspecies." Their text has to be exactly match or the program would cause an error. Even if you don't have any subgenus or subspecies name, you still need to include columns as parts of the data.
The way program work is finding the matching name for each column and append all the data to its local list.

The next two steps are setting correct locations for where initial excel file is sitting, and after runnign the code, the new excel file will be created as the output.
It is important to set the location you want to save at the specific repository.
In "bhl_gen_3.py", there will be a variable that contains the location of the file, which is look like this:

fileLoc = r'D:\coding\Sample_names.xlsx'
 
You should change the location based on your desktop or laptop location setting, and put the location of the excel file from your pc.
For indicating local drive, for example, it starts with D:, and every time you move in to another folder, you use \ as an indication.
Under the "fileLoc" variable, there will be a variable "sheetName." You need to designate specific sheet name from your excel to make sure the program runs the correct file.

When you go to line 47 from "bhl_gen_3.py", you will see this code:

exportLoc = r'D:\coding\test_database.xlsx'

You asl need to assign your exporting location to this  "exportLoc" variable, including the file name.
