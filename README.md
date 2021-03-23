# DATABASE MODULE DEMO FOR Python

Most software programs often have to access and transact with the database to perform at least RUD (Retrieve, Update, Delete) mass data manipulation operations.

And many programming languages offer built-in modules that connects, interacts, transfer, modify & exchange data to and from the database.

Python has a MySQL Data Connector module that is a good framework for the Python software to interact with MySQL database.

There are other database connectors available for Python as well.

As the MySQL Data Connector is structured as either class or a functional module, 
it could be used directly by any calling objects that require database data transactions.

However, it would be better to be in control with your code and your software project by creating a facade Database class that has a Database class and a Database cursor.

In this way, we would not be overwhelmed by the numerous and large features of the MySQL Data Connector and we would only use what we need from its methods and properties.

This simple software demo project demonstrates how to use Python's MySQL Data Connector to interact with the database.

The module is tested through PyUnit test case that (although not recommended) connects to a MySQL server installed within the computer where this Python module would run.

This demo contains the following:

- database_records.py which is the database access module itself.
- test_database_records.py which are series of PyUnit tests that describes how to use the database_records.py
- CreateFruitsTableInDemoDatabase.sql which contains SQL commands to create the demo_database and its fruits table that shall be used by the test_dataase_records.py to test the database_records.py....AND
- database_demo.yaml which is the configuration file that contains user credentials and server settings used to connect to the test MySQL server.

This Python software demo on database access shall be compared with its corresponding PHP and Raku Perl software demos.

For more inquiries, please feel free to e-mail me at marcanthonyconcepcion@gmail.com.
Thank you.
