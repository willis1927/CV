import pandas as pd
import math
import json
import requests
import time
from datetime import date, datetime
import os

def main ():
    global input_data
    while True:
        ### Prompt user for filename
        xcl = input(f"Full Team Excel name (with) extension): ")
        #Load file into dataset named input_data     
        try:
            print(xcl)
            input_data = pd.read_excel(xcl, "Order Form", usecols="D:AC", converters={'Item Code': str})
            break
        except:
            print("file not found")
            pass
    global shape
    shape = input_data.shape
    global headers
    headers = input_data.columns.values
    ep = pd.read_excel("excluded postcodes.xls")
    global ExPostcodes
    ExPostcodes = ep[ep.columns[0]].values.tolist()
    global products
    products = pd.read_csv("Product List.csv", encoding='latin-1')

    #print(input_data)
    #print(shape)
    
    #Load Product list into dataset named SKUs
    
    #create blank list for output
    global output
    output = []
    #Loop over each row of sheet 
    if check_Del_methods != None : output.append(check_Del_methods())
    global mode
    while True:
        mode = int(input("Select validation mode (1-4) - \n1. All Rows (average 8 rows/second)\n2. All Rows - no product check\n3. All Rows no product or postcode check (Fastest)\n4. All Rows no postcode check\n").upper())
        if mode > 0 and mode < 5:
            os.system("clear")
            break
        else:
            os.system("clear")
            print("Please enter a number 1 to 4")
    #start timer
    start_time = time.time()
    for x in input_data.index:
    #check each row for any errors 
        test = validate_row(x)
    #If test contains errors add to output list
        if test :
            output.append(test)
    #print(f"row - {x + 1} - {input_data.iloc[x,6]}")

    #Print errors stored in outp ut, if no errors print message saying no errors
    if output[0] == None : output.pop(0)
    #end timer
    end_time=time.time()
    run_time=end_time-start_time
    os.system('clear') 
    print(shape[0], ' rows checked, time taken - ', time.strftime("%H:%M:%S", time.gmtime(run_time)))
    if len(output) > 0  :
        today = date.today()
        curr_time = time.strftime("%M:%S", time.localtime())
        with open(f"{xcl} error summary - {today} - {curr_time}.csv", 'w') as f:
            for error in output:
                f.write(f"{error}\n")
        print(f"{len(output)} rows found with errors, errors saved to output file")
        #df = pd.DataFrame(output)
        #df.to_csv(f"{xcl} error summary - {today} - {curr_time}.csv")
        #print(df)
        #for error in output:
        #    print(error)
    else: 
        print("No Errors detected :)!!")


#Run validations for each column, if validation fails, log column name and spredsheet row number

### validations ####
def validate_row(row_num):
    #create list for rows error with index 0 as the spreadsheet row number
    errors = [f"Row - {row_num+2}"]
    
    #check products have valid product codes
    if mode == 1 or mode == 4:
        if check_product(row_num) : errors.append(check_product(row_num))

    #check if any required columns are empty, if empty add to erros list    
    for col in [2,4,5,6,10,13,18,21]:        
        if check_empty(row_num,col) : errors.append(check_empty(row_num,col))

    #check if 1 of 1 required fields is complete if not add to errors
    #variable to track if 1 of required fields contains data
    address_val=False
    for col in [7,8,9]:
        if not check_empty(row_num,col):
            address_val=True       
        if address_val:
            break    
    if not address_val:errors.append("Company Name/House No/House Name missing")
   
    #check postcode is valide UK postcode
    if mode < 3:
        if check_Postcode(input_data.iloc[row_num,16]): errors.append(check_Postcode(input_data.iloc[row_num,16]))
    
    #check if Country is GB
    if check_Country(row_num,17): errors.append(check_Country(row_num,17))
    #Check if Delivery instructions are POD
    if check_POD(row_num,18): errors.append(check_POD(row_num,18))
    #Check if Phone is 00000
    if check_Phone(row_num,23): errors.append(check_Phone(row_num,23))
    #Check delivery date:
    if check_del_method(row_num): errors.append(check_del_method(row_num))
    
    
    #end of rows validation append summary of errors to output
    if len(errors)>1:
        output.append(errors)
    os.system('clear')
    complete = (row_num/shape[0])*100
    print(f"{row_num} rows checked, {'{:.0f}%'.format(complete)} complete")    
        
    
### check is cell is empty 
def check_empty(row, check_column):
    
    try:
        if math.isnan(input_data.iloc[row,check_column]) :
            result = f"{headers[check_column]} missing"
            return result
    except Exception as e:
        
        pass

### check item code is valid
def check_product(row):
    #print(input_data.iloc[row,1])
    item = products[products["BOM Code"] == str(input_data.iloc[row,1])]
    
    if item.empty:
        return f"Error in Product code" 
    
###pass postcode to API to check if it exists
def check_Postcode (postcode):
    
    data = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
    #if error received assume not valid UK postcode and reutrn error mesage string
    if data.status_code != 200: 
        #print(f"{postcode} returned status {data.status_code}")
        return f"Error in Postcode{postcode}"
    #if Valid UK postcode check postcode agianst list of restricted postcodes
    else:
        pc1 = postcode.split(" ",1)           
        if pc1[0] in ExPostcodes:
            return f"Standard or Delayed Delivery Only to {postcode}"

### Country is equal to "GB"
def check_Country(row, check_column):
    try:
        if input_data.iloc[row,check_column] != "GB" :
            result = f"{headers[check_column]} must be GB"
            return result
    except Exception as e:
            pass

### Instructions is equal to "POD"
def check_POD(row, check_column):
    try:
        if input_data.iloc[row,check_column] != "POD" :
            result = f"{headers[check_column]} must be POD"
            return result
    except Exception as e:
            pass
    

### Validate delivery - Delivery Method is not empty, IF method = DDGI of Flex check delivery date column has date ELSE check date is 0
def check_del_method(row):
    if input_data.iloc[row,21] in ["DDGI","Flex"] and check_empty(row,22) == None : return f"Delivery date missing"
        
        
### Delivery phone = "00000"
def check_Phone(row, check_column):
    try:
        if input_data.iloc[row,check_column] == "00000" :
            result = f"{headers[check_column]} must be 00000"
            return result
    except Exception as e:
            pass
### Check all delivery methods are the same
def check_Del_methods():
    dset= set(input_data["Delivery Method"].tolist())

    if len(dset) > 1 : 
        return "Delivery methods must all be the same"
    else:
        return
if __name__ == "__main__":
    main()
