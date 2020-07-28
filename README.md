# Final Report

### Introduction

Our group developed an online flight reservation system, which mimics the ticket booking system in the real world such as Priceline. The system cantains both user interface and manager interface. As a manager, it is easy to use the system to add new airlines and new tickets. As a passenger, you can search for the flights basing on departure/arrival city and time. The system provides convenience for travelers to compare tickets from different airlines with different price, and book whatever you like! We combine the Amazon SNS service with our register part so that when users register they can receice welcome email from us. Also, there is a background process which releases the manager from manually adding and deleting the flights from database everyday. It automatically runs once a day to delete old flights and add up-to-date flights with default parameters.

***

### User Guide

#### Our Website

[Online Ticket Reservation System](https://lvprrym0x4.execute-api.us-east-1.amazonaws.com/dev)

URL: https://lvprrym0x4.execute-api.us-east-1.amazonaws.com/dev

Notice: the server has been shut down considering the cost of continuously running. You can view the application by the following screenshots.

#### As a Manager

1. Enter the URL to go to the homepage of our website, and click **Admin System** to log in as a manager. The default admin account is:

   > username: admin
   >
   > password: 123456

![](https://github.com/maybe8240/airticket/blob/master/images/signin.png)

  <center>sign in page for admin</center>

2. **Permission management** : Add new admin account by setting an username and password and submit. The new manager account will be listed above.

![](https://github.com/maybe8240/airticket/blob/master/images/permission.png)

   <center>permission management</center>

3. **Airline management** : Add new airline by filling in the IATA code and callsign of an airline/company, and the new airline will be listed above. Notice: You can only choose from the aviliable airlines when adding flight, therefore, it is necessary to add at least one airline before adding flights.
![](https://github.com/maybe8240/airticket/blob/master/images/adding_airlines.png)

   <center>adding airlines</center>

4. **Adding new flight**: Add new flight once a time by completing the form, and the new flight will be saved in the system for travelers to search and book.

![](https://github.com/maybe8240/airticket/blob/master/images/adding_flights.png)

  <center>adding flights</center>

5. **Order management** : The manager is able to view all the orders, and read the passenger information and delete the order.
![](https://github.com/maybe8240/airticket/blob/master/images/order_management.png)  

    <center>order management</center>



#### As a Passenger

1. **Ticket Searching** : A passenger can use the flight searching function on the homepage of our website Search for a satisfying flight by choosing the departure and arrival city and departure date and click search.


![](https://github.com/maybe8240/airticket/blob/master/images/homepage.png)

   <center>homepage</center>

2. **Ticket Booking** : After clicking search, the passenger will be redirected to a new page of results. If there are avilable tickets, it will be shown in the result table. It is easy to make a reservation by clicking book.

![](https://github.com/maybe8240/airticket/blob/master/images/search_result.png)

   <center>search result</center>

3. **Log in/Register** : After clicking book, the passenger will be redirected to the log in page. He/She can choose to log in or register. Of course, if he/she has already logged in, he/she will jump directly  to the order confirmation page.If you are first time to register you will receive our welcome email.


![](https://github.com/maybe8240/airticket/blob/master/images/login.png)

   <center>log in page</center>

![](https://github.com/maybe8240/airticket/blob/master/images/register.png)

   <center>register page</center>

![](https://github.com/maybe8240/airticket/blob/master/images/email.png)

   <center>welcome email</center>

4. **Order Confirmation** : If a logged-in passenger clicked book button, he/she will be redirected to the order confirmation page. In this page, some information is automatically filled in by system, and the passenger must provide avilable email address and ID to make the reservation.

![](https://github.com/maybe8240/airticket/blob/master/images/confirmation.png)

   <center>order confirmation</center>

5. **Personal Center** : After confirmming the order, the passenger will be redirected to his/her personal center, where all his/her reservations are shown. He/She can also edit personal information in the personal center.

![](https://github.com/maybe8240/airticket/blob/master/images/reservation.png)

   <center>my reservation page</center>

![](https://github.com/maybe8240/airticket/blob/master/images/personal_info.png)

   <center>personal information page</center>

***

### Architecture

#### File Scheme

```python
----airticket\   #project name
    |----airplane.py   #run the application
    |----app\
    |    |----__init__.py
    |    |----config.py
    |    |----forms\   #data for building the interface
    |    |    |----auth.py
    |    |    |----search_order.py
    |    |    |----admin.py
    |    |    |----base.py
    |    |----web\   #main functions for passengers
    |    |    |----auth.py
    |    |    |----search_order.py
    |    |    |----__init__.py
    |    |    |----main.py
    |    |----admin\   #main function for managers
    |    |    |----auth.py
    |    |    |----__init__.py
    |    |    |----ticket_manage.py
    |    |    |----main.py
    |    |----static\   #static files
    |    |----templates\   #html files
    |    |    |----web\
    |    |    |----admin\
    |    |----data\   #database interaction
    |    |    |----ticket.py
    |    |    |----order.py
    |    |    |----admin.py
```

#### Application Architecture


![](https://github.com/maybe8240/airticket/blob/master/images/general.png)

<center>general architecture</center>


The graph above is the general architecture of our project with functions of AWS. The code is deployed to **Lambda** using Zappa, which automatically upload the code to **S3** first. The static files are also in S3 bucket for Lambda to call. Users use the URL given by **API Gateway** to interact with the web application. Data is saved in **Dynamodb**, and we use **SNS** to send email to users. Also, the **background process** is deployed seperately in another Lambda function, which interacts with Dynamodb to update the data. It is set to run once a day by **Cloudwatch**.

#### Program Architecture

##### administrator

![](https://github.com/maybe8240/airticket/blob/master/images/manager.jpg)

##### user

![](https://github.com/maybe8240/airticket/blob/master/images/user.jpg)
