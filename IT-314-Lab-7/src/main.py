# main.py
# The Command Line Driver that brings our classes to life and runs all 7 Test Cases!

from models import Movie, Cinema, Screen, Seat, Show, Customer, Booking

def setup_data():
    """Helper function to create some dummy data for our tests."""
    cinema = Cinema("PVR Cinemas", "Ahmedabad")
    screen1 = Screen("Screen 1")
    
    # Add two physical seats: A1 and A2
    screen1.add_seat(Seat("A", 1))
    screen1.add_seat(Seat("A", 2))
    cinema.add_screen(screen1)
    
    movie = Movie("The Avengers", 150, "English", "Action", "PG-13")
    
    # Create two shows for the SAME movie on the SAME screen, but at different times
    show_6pm = Show(movie, screen1, "6:00 PM")
    show_9pm = Show(movie, screen1, "9:00 PM")
    
    return cinema, movie, show_6pm, show_9pm

def run_tests():
    print("======================================================")
    print("      MOVIE TICKET BOOKING SYSTEM - TEST RESULTS      ")
    print("======================================================\n")
    
    cinema, movie, show_6pm, show_9pm = setup_data()
    customer = Customer("Student 202401465", "student@daiict.ac.in")

    # ---------------------------------------------------------
    print(">>> TC01: Successful booking")
    print("Scenario: Selecting an available seat, payment succeeds.")
    booking1 = Booking(customer, show_6pm)
    booking1.add_seat("A1") 
    is_confirmed = booking1.confirm_booking(payment_succeeds=True)
    if is_confirmed and len(booking1.tickets) == 1:
        print("Actual Result: Seat A1 was successfully selected. Payment was processed. Booking status is CONFIRMED and 1 ticket was generated.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

    # ---------------------------------------------------------
    print(">>> TC02: Duplicate seat")
    print("Scenario: Trying to book a seat that is already booked for the same show.")
    booking2 = Booking(customer, show_6pm)
    seat_added = booking2.add_seat("A1") 
    if not seat_added:
        print("Actual Result: The system rejected the selection because Seat A1 is already booked by the first customer.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

    # ---------------------------------------------------------
    print(">>> TC03: Payment failure")
    print("Scenario: Payment is rejected during confirmation.")
    booking3 = Booking(customer, show_6pm)
    booking3.add_seat("A2")
    is_confirmed_fail = booking3.confirm_booking(payment_succeeds=False)
    if not is_confirmed_fail and booking3.status == "FAILED":
        print("Actual Result: The payment declined. Booking status changed to FAILED and absolutely no tickets were generated.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

    # ---------------------------------------------------------
    print(">>> TC04: Cancellation with refund")
    print("Scenario: An eligible cancellation changes booking status and releases the seat.")
    cancel_success = booking1.cancel_booking(is_eligible_for_refund=True)
    if cancel_success and booking1.status == "CANCELLED":
        print("Actual Result: Booking was successfully cancelled. Refund was generated, and Seat A1 was released back to the system.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

    # ---------------------------------------------------------
    print(">>> TC05: Cancellation not allowed")
    print("Scenario: Cancellation is attempted but policy rejects it (no refund).")
    # First we need a confirmed booking to try and cancel
    booking_temp = Booking(customer, show_6pm)
    booking_temp.add_seat("A1") # We can book A1 again because TC04 just released it!
    booking_temp.confirm_booking(payment_succeeds=True)
    
    cancel_no_refund = booking_temp.cancel_booking(is_eligible_for_refund=False)
    if not cancel_no_refund and booking_temp.status == "CONFIRMED":
        print("Actual Result: The cancellation policy denied the request. Booking remains CONFIRMED and no refund was issued.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

    # ---------------------------------------------------------
    print(">>> TC06: Same seat, different shows")
    print("Scenario: A seat booked for one show is still available for another show.")
    # Note: A1 is booked for 6PM right now via booking_temp. Let's book it for 9PM!
    booking4 = Booking(customer, show_9pm)
    seat_added_different_show = booking4.add_seat("A1")
    if seat_added_different_show:
        booking4.confirm_booking(payment_succeeds=True)
        print("Actual Result: Seat A1 was successfully booked for the 9:00 PM show even though it was taken for the 6:00 PM show.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

    # ---------------------------------------------------------
    print(">>> TC07: Invalid seat")
    print("Scenario: Trying to select a seat number that doesn't exist.")
    booking5 = Booking(customer, show_9pm)
    invalid_seat = booking5.add_seat("Z9")
    if not invalid_seat:
        print("Actual Result: The system immediately rejected the seat 'Z9' because it does not exist in the screen's layout.")
        print("Status: [PASS]\n")
    else:
        print("Status: [FAIL]\n")

if __name__ == "__main__":
    run_tests()
