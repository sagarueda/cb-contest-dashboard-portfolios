# cb-contest-dashboard-portfolios
# README
  
### Requirements for running locally
This code create different plots containing information from the historical contest, mainly showing the best projects based on the best contestant and the historical of best contestant.

- check that you have installed python 3.x preferibly 3.8 and beyond
    
- check that you have installed `pipenv`, otherwise:

    ```shell
    pip3 install pipenv
    ```
     
- check that you have installed `plotly`, otherwise:

    ```shell
    pip3 install  plotly
    ```
    plotly may be installed using pip:
  ```conda:
  $ conda install -c plotly
  
- To create a new virtual environment write in a command line being at the `contests` directory: 
  
    ```shell
    pipenv shell
    ```
- Once the environment is created, you have to install the dependencies described in pipfile:

    ```shell
    pipenv install
    ```


 - The script run differents queries to MySQL Database and then calculate the historical contestant uptoday.
 And also it creates a bar plot showing the best projects that were chosen by the best participants who are in the current contest.
 This scripts use the next tables 
 - `contests_historical_rank`
 - `users`
 - `projects`
    
 - to connect to the database, you have to set the ENVIRONMENT VARIABLES in your shell, e.g :
    
    ```shell
    export MYSQL_USER=[your_SQL_user] && export MYSQL_PASSWORD=[your_SQL_password] && export MYSQL_DATABASE=[your_SQL_database] && export MYSQL_SERVER=[your_SQL_SERVER] && export MYSQL_SERVER=[your_SQL_SERVER]
    ```

    'MYSQL_PORT'--> optional, just if you use a different port than the default
    
### Running the code

For running the code, you need to provide two different arguments in the command line or in input parameters:
[TOP_ENTRY, TOP_PROJECTS]

- `TOP_ENTRY` is the number of contestant that will be taken into account to the processing.

- `TOP_PROJECTS` is the number of projects that we want to see ordered by scored based in the frecuency that they were choose and the percentage in each portfolio.

### Output program

 This program generates two plots and one table with the main information of the current contest.
 The main parameter is the number TOP_ENTRY which is the number of best contestant to be taken into account in the processing.
In case you didn't enter eny top_entry, the program will use TOP_ENTRY = 10
The output of the program are three .html containing this plots

-   PLOT 1:
A bar plot of the TOP_ENTRY best historical contestant until today, ranked based on the acumulated total points, which was calculated based in the position in each contest a
and with an extra bonus based in how many times the contestant arrived in the top contest.

-  Plot 2:
A bar plot of the best TOP_PROJECTS projects based on the portfolios of the best historical contestant which are in the current contest.
The best projects were order by the total points per slug.
-   Plot 3:
It is A table containing the main information of the current contest
