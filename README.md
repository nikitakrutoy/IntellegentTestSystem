# Intellegent test system
Test system that can adapt to users by giving questions of varying complexity depending on the answers.  

## Desciption

* When the answer to the question is wrong system increases the number of questios in the test of the same of lesser complexity 

* Number of questions is bounded

* System could memorize rusults of test in order to improve users results in the future tests, by creating set of questions that are more suitible for this user (in progress)


## Technical description
Uses Django, nginx and SQLite database to store usernames and questions  
Hosts on Digital Ocean  
System interface is done with python telegram bot API  
