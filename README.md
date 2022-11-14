# Travel_Bot
Theme:

Telegram-bоt for analysis and parsing api of Hotels.com and search
hotels suitable for the user

Description:
  The project was developed in python, written according to the rules of pep-8, easily portable.
  To develop the project, i user open API Hotels, which is located on
  site rapidapi.com.

The project running from main.py.
  The user, using special bot commands, can perform the following
  actions (get the following information):
  1. Find out the top cheapest hotels in the city (command /lowprice).
  2. Find out the top most expensive hotels in the city (command /highprice).
  3. Find out the top hotels that are most suitable for price and location from the center
  (the cheapest and closest to the center) (command /bestdeal).
  4. Check the hotel search history (command /history)
  Without a running script, the bot does not respond to commands (and to anything else).

Description of the commands:

  lowprice command:
    After entering the command, the user is prompted:
    1. The city where the search will be conducted.
    2. The number of hotels to be displayed as a result (no more
    predetermined maximum).
    3. The need to upload and display photos for each hotel (“Yes / No”)
    a. If yes, the user also enters the quantity
    necessary photographs (no more than a predetermined
    maximum)
    
  highprice command:
    After entering the command, the user is prompted:
    1. The city where the search will be conducted.
    2. The number of hotels to be displayed as a result (no more
    predetermined maximum).
    3. The need to upload and display photos for each hotel (“Yes / No”)
    a. If yes, the user also enters the quantity
    necessary photographs (no more than a predetermined
    maximum)
    
  bestdeal command:
    After entering the command, the user is prompted:
    1. The city where the search will be conducted.
    2. Price range.
    3. The range of the distance at which the hotel is located from the center.
    4. The number of hotels to be displayed as a result (no more
    predetermined maximum).
    5. The need to upload and display photos for each hotel (“Yes / No”)
    a. If yes, the user also enters the quantity of 
    necessary photos (no more than a predetermined maximum)
    
  history command:
    After entering the command, the user is shown the search history of hotels. The story itself
    contains:
    1. The command that the user entered.
    2. Date and time when the command was entered.
    3. Hotels that were found
    
UI:
Description of appearance and UI
The Telegram bot window, which, when running a Python script, should be able to
accept the following commands:
● /help — help with bot commands,
● /lowprice - display the cheapest hotels in the city,
● /highprice - displays the most expensive hotels in the city,
● /bestdeal - displays the most suitable hotels in terms of price and location from
center.
● /history - display the history of hotel search

For the lowprice, highprice and bestdeal commands, the command result message
contain brief information on each hotel. This information is at least
includes:
● hotel name,
● address,
● how far is it from the center,
● price,
● N photos of the hotel (if the user considered it necessary to display them)

Additional files:
[readme.md](https://github.com/iskyshurell/Travel_Bot/files/10005691/readme.md) - bot readme
[requirements.txt](https://github.com/iskyshurell/Travel_Bot/files/10005703/requirements.txt) - requirements
