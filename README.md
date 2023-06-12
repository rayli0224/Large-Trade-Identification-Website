# Introduction

## What is the Stock Tracker?

This app is a tool for stock traders to track statistically large trades of various stocks. 
The tool has the following functionality:
1. Users can input the desired stock ticker.  
2. Users can manage which stocks they are tracking.
3. Users are notified through email whenever a large trade is placed with information about the size of the trade and who executed the trade.   
4. Users can create an account using their email address.

For more details, view the full project proposal [here](https://docs.google.com/document/d/14OYDM5gOmXMALanmBgJUMHj2VP-7JzOIuRCciTij-aU/edit#heading=h.5nyf95t1y4zs).

# Technical Architecture
![image](https://user-images.githubusercontent.com/55147322/236515575-e64d8386-c46c-42d7-a29a-1304c747b693.png)

# Developers
- **George Ma**: Worked on frontend website development
- **Vijay Shah** Developed the Django Server
- **Ray Li** Developed the large trade detector 
- **Larry Liao** Worked on the frontend website development


# Installation and Setup
1. Install Required Python Packages:
 - Django for the server hosting
 - Pandas, Numpy, Matplotlib, AlpacaTrade for trade backend
 - Smtplib for emails
2. Create a .env folder and put email credentials in there to setup the email client
3. Run python manage.py migrate to initialize the databses 
4. Run python manage.py runserver to start the server. 
