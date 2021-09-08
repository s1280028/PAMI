**[CLICK HERE](index.html)** to access the PAMI manual.

#Statistical details of a transactional database

The performance of a mining algorithm primarily depends on the following two key factors: 
1. Distribution of items' frequencies and 
1. Distribution of transaction length

Thus, it is important to know the statistical details of a database. PAMI provides inbuilt classes and functions methods to 
get the statistical details of a database.   In this page, we provide the details of methods to get statistical details from 
a transactional database. 

### Executing transactionalDatabaseStats program

The transactionalDatabaseStats.py program is located in PAMI.extras.dbStats folder. Thus, execute the below lines to run the program.

    #import the program
    import PAMI.extras.dbStats.transactionalDatabaseStats as tds
          
    
    #initialize the program
    obj = tds.transactionalDatabaseStats(inputFile)
    #obj = tds.transactionalDatabaseStats(inputFile,sep=',') #override default tab seperator
    #execute the program
    obj.run()
    
Once the program is executed, users can call different methods to get the statistical details of a database. We now describe the available methods.

#### getDatabaseSize()
    
   This method outputs the total number of transactions in a database.  
   
    print(f'Database size : {obj.getDatabaseSize()}')

#### getMinimumTransactionLength()

   This method  outputs the length of the small transaction in a database. In other words, this function outputs the minimum number of items in a transaction.
   
    print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')

#### getAverageTransactionLength()

   This method  outputs the length of an average transaction in a database. In other words, this function outputs the average number of items in a transaction.
   
    print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
   
#### getMaximumTransactionLength()
   This method outputs the length of the largest transaction in a database. In other words, this function outputs the maximum number of items in a transaction. 

    print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
    
#### getStandardDeviationTransactionLength()
   This method outputs the standard deviation of the lengths of transactions in database.

    print(f'Standard Deviation Transaction Size : {obj.getStandardDeviationTransactionLength()}')

#### getMinimumUtility()
  This method returns the minimum utility of all items in a database.
   
    print(f'Minimum utility : {obj.getMinimumUtility()}')    

#### getAverageUtility()
  This method returns the average utility of all items in a database.
   
    print(f'Average utility : {obj.getAverageUtility()}')    
    
#### getMaximumUtility()
  This method returns the maximum utility of all items in a database.
   
    print(f'Maximum utility : {obj.getMaximumUtility()}')    
        
#### getSortedListOfItemFrequencies()
   This method returns a sorted dictionary of items and their frequencies in the database. The format of this dictionary is {item:frequency} 
   The items in this dictionary are sorted in frequency descending order. 
   
    itemFrequencies = obj.getSortedListOfItemFrequencies()

#### getTransanctionalLengthDistribution()
   This method returns a sorted dictionary of transaction lengths and their occurrence frequencies in the database. 
   The format of this dictionary is {transactionalLength:frequency}.
   The transaction lengths in this dictionary are sorted in ascending order of their transactional lengths.
   
    transactionLength = obj.getTransanctionalLengthDistribution()

#### getSortedUtilityValuesOfItem()
   This method returns the sorted dictionary of items and their sum of utility values in a database.
   The format of this dictionary is {item:sumOfItsUtilities}.
   
     utility = obj.getSortedUtilityValuesOfItem()
         
#### storeInFile(dictionary, returnFileName)
   This method stores the dictionary in a file. In the output file, the key value pairs of the dictionary are separated by a tab space. 
   
    obj.storeInFile(itemFrequencies, 'itemFrequency.csv')
    obj.storeInFile(transactionLength, 'transactionSize.csv')       
    obj.storeInFile(utility, 'utility.csv')  
    
## Sample code 

    import PAMI.extras.dbStats.utilityDatabaseStats as uds
            
    obj = uds.utilityDatabaseStats(inputFile)
    #obj = uds.utilityDatabaseStats(inputFile,sep=',') #override default tab separator
    obj.run()
    print(f'Database size : {obj.getDatabaseSize()}')
    print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')
    print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
    print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
    print(f'Total utility : {obj.getTotalUtility()}')
    print(f'Minimum utility : {obj.getMinimumUtility()}')
    print(f'Average utility : {obj.getAverageUtility()}')
    print(f'Maximum utility : {obj.getMaximumUtility()}')
    itemFrequencies = obj.getSortedListOfItemFrequencies()
    transactionLength = obj.getTransanctionalLengthDistribution()
    utility = obj.getSortedUtilityValuesOfItem()
    obj.storeInFile(itemFrequencies, 'itemFrequency.csv')
    obj.storeInFile(transactionLength, 'transactionSize.csv')
    obj.storeInFile(utility, 'utility.csv')   




