DATABASE = 'micro_p4'

def create_table(fname, db, cur, small = False, DATABASE = DATABASE):
    
    fpath = fname + '.csv'  # determine the file path.
    
    # Step1: grab some general information from csv
    # Save the basic information (header, nrows and ncols) and pick a example row. 
    # Figure out the maximum element length of each row, which updated as eleLen.
    # Delete all the spaces of each header element. 
    # The words should be linked by underline, like ' patient id  ' should be replaced by 'patient_id'.
    
    nrows = 0  # The total rows counter
    for i, row in enumerate(read_file(fpath)):
        thisRow = [x.strip() for x in list(row)]
        if i == 0:
            header = ['_'.join(x.split(' '))[:60] for x in thisRow]  #Remove the spaces in header; Control the maximum length of title
            ncols = len(header)
        
        # Bulid a exmaple row from the file
        if i == 1:
            exampleRow = thisRow
            eleLen = [len(exampleRow[i]) for i in range(ncols)]
        if i > 1:
            for i in range(ncols):
                if len(exampleRow[i]) < len(thisRow[i]):
                    eleLen[i] = len(thisRow[i])
                if not exampleRow[i]:
                    exampleRow[i] = thisRow[i]
        nrows += 1

        
    # Create the datatype of exampleRow. 0 for varchar, 1 for int, 2 for float, -1 for NULL, then 0 for other type as char.
    dataType = []
    for i, ele in enumerate(exampleRow):
        
        # Auto delete all-NULL column
        if not ele:    
            header.pop(i)
            ncols -= 1 
            
        # Set the datatype
        dataType.append(0)   # Defult is varchar
        if ele[-1] == '%': dataType[-1] = 2  # Precentage should be float 
        elif ele[0].isdigit() or ele[0] == '$':  # Digit or currency to int or float
            if '.' in ele: dataType[-1] = 2
            else: dataType[-1] = 1

    print('Example: ', exampleRow)
    print('Maximum element length: ', eleLen)

    
    # Step2: create the table head in SQL
    # Set the table header commands in SQL commands
    cols_cmd = []
    cols_cmd.append('`auto_id` int(11) NOT NULL AUTO_INCREMENT,')
    for i, typ in enumerate(dataType):
        result = '`%s` ' %(header[i])
        if typ == 0:
            eleLen[i] = eleLen[i] * 2 + 1
            tempStr = 'varchar(%d),' %(eleLen[i])
        if typ == 1:
            eleLen[i] = eleLen[i] + 1
            tempStr = 'int(%d),' %(eleLen[i])
        if typ == 2:
            tempStr = 'double(%d,%d),' %(eleLen[i], 2)
        result = result + tempStr
        cols_cmd.append(result)
    primary_cmd = 'PRIMARY KEY (`auto_id`)'

    # The command line to create the table
    table_create_cmd = 'CREATE TABLE `%s` (%s) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;' %(fname, ''.join(cols_cmd) + primary_cmd)  
    print('\n Table create command: \n', table_create_cmd, '\n')
    
    # Create the database and execute the table create command
    cur.execute('DROP DATABASE IF EXISTS `%s`' %(DATABASE))
    cur.execute('CREATE DATABASE `%s`' %(DATABASE))
    cur.execute('USE `%s`' %(DATABASE))
    cur.execute(table_create_cmd)
    
    
    # Step3: Insert All the rows
    for i, row in enumerate(read_file(fpath)):
        if small and i == 10000: break
        if i == 0: continue  # Skip the head row
        thisRow = list(row)
        if not any(thisRow): continue   # Skip the all-NULL row
        for j in range(ncols):
            
            # Cut the redundant spaces, dollar sign and percentage sign
            thisRow[j] = thisRow[j].strip().lstrip('$').rstrip('%')
            
            # Decide the values we want to insert.
            if not thisRow[j]:  # If thisRow[j] is empty, set the value to NULL.
                thisRow[j] = 'NULL'
            elif dataType[j] >0:  # If thisRow[j] is int or float, delete the commas. 
                thisRow[j] = ''.join(thisRow[j].split(','))
            elif dataType[j] == 0:  # If thisRow[j] is a string, add quotes around it.
                thisRow[j] = '\'' + thisRow[j] + '\''
        
        # Combine the insert commands together
        insert_cmd = 'INSERT INTO `%s` VALUES (%s,%s);' %(fname, str(i), ','.join(thisRow))
        
        # Print the example
        if i == 1: print('Line Insert Command Example: \n', insert_cmd, '\n')
            
        # Execute the command in SQL
        cur.execute(insert_cmd)
    
    return [nrows, ncols, header, exampleRow, eleLen]