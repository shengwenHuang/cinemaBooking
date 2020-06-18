# cinemaBooking

This is a cinema booking management system with the following capacities:


1. The management system was implemented as a command-line application.


2. The system handles two different profiles; the cinema employee and ordinary customers. Both types of users need to login before being able to use the management system
Note: Don’t over complicate the registration process. You can simply check the user’s credentials by reading a manually created file containing username/password pairs.


3. Since, there are two types of users, your application should display a different text-based options menu depending on the logged-in user.


### Cinema employee profile


4. The cinema employee should be able to login to the cinema management system using a username/password pair.


5. The cinema employee can add films with their respective dates and screening times. A film is represented by a title and a brief description.


6. For a given film/date/time, your application should provide an up-to-date textual representation of the cinema room setting. It should distinguish between booked seats and available ones (consider using different text labels).


7. The employee text view also shows basic information about the total number of seats, booked ones and available ones for a given film/date/time.


8. The employee can export a list of films (i.e. titles), dates, times and number of booked and available seats. The list is a comma separated values text file.


9. The cinema employee can logout from the application.


### Cinema customer profile


10. After login, a customer should be able to update his/her profile to use for future bookings. The profile is composed of basic information such as name and email address. There is also booking history that is updated automatically when the user makes a booking or delete an existing one.


11. He/she can pick up a date, get a list of films available on the selected date with their respective information and available screening times.


12. The customer can book a seat (for a given film/date/time) for example by typing ‘book’ with film details in the terminal.


13. When booking is confirmed, a summary of his booking is displayed and the booking added to his history.


14. A customer can delete an existing booking from his list if it is a future booking only, otherwise an error message is displayed.


15. The cinema customer can logout from the application.
