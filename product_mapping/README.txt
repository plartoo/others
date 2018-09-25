Files included:
1. map_subcategories.py
2. map_variants.py
3. mapping_utils.py
4. queries.py

#1 and #2 above are the files you need to run. To learn how to run them, you can type for example:
>> python map_subcategories.py -h

When running the code and if the program responds something like below:
""ModuleNotFoundError: No module named 'scipy'""
you are missing the Python library/module. You can install the missing library like below:
>> pip install <missing library's name>

The proper way to run the automated mapping is as follows:
1. Run the subcategory mapping code. 
>> python map_subcategories.py -c "UNITED STATES"

OR
>> python map_subcategories.py -c "UNITED STATES" -m <mapping model file>
if you generated a model file recently and don't want to wait the code to generate
a new model from scratch (takes only about 10 minutes max for subcategory mapping though,
so you probably don't need to use this option that often)

OR
>> python map_subcategories.py -c "UNITED STATES" -m <mapping model file> -t 1
if you want the output to be a TSV file.

Note: Before running #1, you need to make sure that [GM_CP_MASTER_PRODUCT_MAPPING] table 
is loaded with rows that have CP_SUBCATEGORY_NAME not mapped (meaning, they are NULL). 
That will allow the code to suck in the unmapped values and generate automated mapping 
for them.


2. Running subcategory mapping above will generate an output file with the name like this:
mapped_subcategories_1537536953.xlsx
Now you should double check the results in CP_SUBCATEGORY_NAME and CP_SUBCATEGORY_ID
and fix what you need. After that, move that modified file to the input folder.


3. Run the variant mapping code.
>> python map_variants.py -c "UNITED STATES" -i <mapped_subcategories_1537536953.xlsx for example>

This code will take ~15 minutes on a powerful laptop to generate the machine learning model
and do the automated mapping. After that, it'll generate the output file with the name like:
mapped_variants_1537471819.xlsx

Please double check on the results and modify them as needed. Remember that there are thousands 
of variant names, so the accuracy of variant mapping is going to be lower than that of subcategories.
But at least, this process will help you pace quicker in manual mapping process (that's the hope).










