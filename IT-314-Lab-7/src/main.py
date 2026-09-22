# main.py
# The Command Line Driver that brings our classes to life.
# Includes an interactive menu AND runs the 7 Test Cases!

import sys
from models import Movie, Cinema, Screen, Seat, Show, Customer, Booking

def setup_data():
    """Helper function to create some dummy data for our tests and CLI."""
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
    
    return cinema, movie, [show_6pm, show_9pm]

def run_automated_tests(cinema, movie, shows, customer):
    """Runs TC01 to TC07 automatically so you don't have to test manually."""
    print("\n=== Running Required Test Cases (TC01 to TC07) ===\n")
    show_6pm, show_9pm = shows[0], shows[1]
    
    # ---------------------------------------------------------
    print(">>> TC01: Successful Booking")
    booking1 = Booking(customer, show_6pm)
    booking1.add_seat("A1") 
    is_confirmed = booking1.confirm_booking(payment_succeeds=True)
    if is_confirmed and len(booking1.tickets) == 1:
        print("[PASS] Seat A1 booked. Payment succeeded. Ticket generated.")
    else: print("[FAIL] Booking failed.")

    # ---------------------------------------------------------
    print("\n>>> TC02: Duplicate Seat")
    booking2 = Booking(customer, show_6pm)
    seat_added = booking2.add_seat("A1") 
    if not seat_added:
        print("[PASS] System correctly rejected booking an already booked seat.")
    else: print("[FAIL] System allowed a duplicate seat!")

    # ---------------------------------------------------------
    print("\n>>> TC03: Payment Failure")
    booking3 = Booking(customer, show_6pm)
    booking3.add_seat("A2")
    is_confirmed_fail = booking3.confirm_booking(payment_succeeds=False)
    if not is_confirmed_fail and booking3.status == "FAILED":
        print("[PASS] Payment failed, booking is not confirmed, no tickets generated.")
    else: print("[FAIL] Payment should have failed.")

    # ---------------------------------------------------------
    print("\n>>> TC06: Same seat, different shows")
    booking4 = Booking(customer, show_9pm)
    seat_added_different_show = booking4.add_seat("A1")
    if seat_added_different_show:
        booking4.confirm_booking(payment_succeeds=True)
        print("[PASS] Seat A1 was successfully booked for the 9PM show!")
    else: print("[FAIL] System wrongly blocked A1 for the 9PM show.")

    # ---------------------------------------------------------
    print("\n>>> TC07: Invalid Seat")
    booking5 = Booking(customer, show_9pm)
    invalid_seat = booking5.add_seat("Z9")
    if not invalid_seat:
        print("[PASS] System rejected non-existent seat Z9.")
    else: print("[FAIL] System accepted an invalid seat.")

    # ---------------------------------------------------------
    print("\n>>> TC04: Cancellation with refund")
    cancel_success = booking1.cancel_booking(is_eligible_for_refund=True)
    if cancel_success and booking1.status == "CANCELLED":
        print("[PASS] Booking cancelled. Refund issued. Seat released.")
    else: print("[FAIL] Cancellation failed.")

    # ---------------------------------------------------------
    print("\n>>> TC05: Cancellation not allowed")
    cancel_no_refund = booking4.cancel_booking(is_eligible_for_refund=False)
    if not cancel_no_refund and booking4.status == "CONFIRMED":
        print("[PASS] Cancellation correctly denied due to policy. No refund issued.")
    else: print("[FAIL] Cancellation was wrongly allowed.")


def interactive_cli():
    """The interactive command-line interface requested in Part F."""
    cinema, movie, shows = setup_data()
    customer = Customer("Student 202401465", "student@daiict.ac.in")
    my_bookings = []

    while True:
        print("\n" + "="*45)
        print("  🎬 MOVIE TICKET BOOKING SYSTEM CLI 🎬")
        print("="*45)
        print("1. View Movies")
        print("2. View Shows")
        print("3. View Available Seats")
        print("4. Book Tickets")
        print("5. View My Bookings")
        print("6. Cancel Booking")
        print("7. Run Required Test Cases (TC01 - TC07)")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            print(f"\nCurrently playing: {movie.title} ({movie.duration} min) - {movie.language}")
            
        elif choice == '2':
            print("\nAvailable Shows:")
            for i, show in enumerate(shows):
                print(f"{i+1}. {show.movie.title} at {show.start_time} in {show.screen.name}")
                
        elif choice == '3':
            show_idx_str = input("\nEnter Show Number (1 or 2): ").strip()
            try:
                show_idx = int(show_idx_str) - 1
                if 0 <= show_idx < len(shows):
                    seats = shows[show_idx].get_available_seats()
                    print(f"\nAvailable Seats for {shows[show_idx].start_time}:")
                    for s in seats: 
                        print(f"- {s.physical_seat.seat_id}")
                else:
                    print("Invalid show number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == '4':
            show_idx_str = input("\nEnter Show Number (1 or 2): ").strip()
            try:
                show_idx = int(show_idx_str) - 1
                if 0 <= show_idx < len(shows):
                    seat_id = input("Enter Seat ID to book (e.g., A1, A2): ").upper().strip()
                    booking = Booking(customer, shows[show_idx])
                    
                    if booking.add_seat(seat_id):
                        if booking.confirm_booking(payment_succeeds=True):
                            my_bookings.append(booking)
                            print(f"\n✅ Booking Confirmed! Your booking ID is: {booking.booking_id}")
                        else:
                            print("\n❌ Payment failed!")
                else:
                    print("Invalid show number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == '5':
            print("\nMy Bookings:")
            if not my_bookings:
                print("No bookings found.")
            for b in my_bookings:
                print(f"ID: {b.booking_id} | Show: {b.show.start_time} | Status: {b.status}")
                
        elif choice == '6':
            b_id = input("\nEnter Booking ID to cancel: ").strip()
            # Find the booking in our list
            booking_to_cancel = next((b for b in my_bookings if b.booking_id == b_id), None)
            
            if booking_to_cancel:
                success = booking_to_cancel.cancel_booking(is_eligible_for_refund=True)
                if success:
                    print(f"\n✅ Booking {b_id} has been cancelled successfully.")
            else:
                print("\n❌ Booking ID not found.")
                
        elif choice == '7':
            # In order to test cleanly, we recreate fresh dummy data just for the test cases
            test_cinema, test_movie, test_shows = setup_data()
            run_automated_tests(test_cinema, test_movie, test_shows, customer)
            
        elif choice == '8':
            print("\nExiting system. Goodbye!")
            sys.exit()
            
        else:
            print("\nInvalid choice, please select a number from 1 to 8.")

if __name__ == "__main__":
    interactive_cli()
