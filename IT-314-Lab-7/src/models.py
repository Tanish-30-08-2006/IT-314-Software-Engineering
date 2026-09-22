# models.py
# Extremely simple, human-readable classes for our Movie Ticket Booking System!
import uuid
from typing import List

class Movie:
    """Represents the film being played (like Avengers)."""
    def __init__(self, title: str, duration: int, language: str, genre: str, certificate: str):
        self.title = title
        self.duration = duration # in minutes
        self.language = language
        self.genre = genre
        self.certificate = certificate

class Seat:
    """A physical chair in a cinema room. Just tells us 'Row A, Seat 1'."""
    def __init__(self, row: str, number: int):
        self.row = row
        self.number = number
        self.seat_id = f"{row}{number}" # e.g. "A1"

class Screen:
    """A single room in a cinema. It holds a list of physical chairs."""
    def __init__(self, name: str):
        self.name = name
        self.seats: List[Seat] = [] # All the physical chairs inside this room

    def add_seat(self, seat: Seat):
        self.seats.append(seat)

class Cinema:
    """The actual building that holds the screens."""
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.screens: List[Screen] = []

    def add_screen(self, screen: Screen):
        self.screens.append(screen)

class ShowSeat:
    """
    CRUCIAL FOR VIVA: This links a physical chair to a specific time (Show).
    This answers Part C! If someone books 'A1' at 6PM, it is only booked for THIS ShowSeat.
    The physical 'Seat' itself remains untouched for the 9PM show.
    """
    def __init__(self, physical_seat: Seat):
        self.physical_seat = physical_seat
        self.is_booked = False # Initially, the seat is empty for this show!

    def book(self):
        self.is_booked = True
        
    def release(self):
        self.is_booked = False

class Show:
    """A specific movie playing at a specific time, in a specific room."""
    def __init__(self, movie: Movie, screen: Screen, start_time: str):
        self.movie = movie
        self.screen = screen
        self.start_time = start_time
        
        # When a show is created, we create a 'ShowSeat' for every physical chair in the room.
        self.show_seats: List[ShowSeat] = [ShowSeat(seat) for seat in screen.seats]

    def get_available_seats(self) -> List[ShowSeat]:
        return [ss for ss in self.show_seats if not ss.is_booked]

    def get_show_seat(self, seat_id: str) -> ShowSeat:
        """Finds a specific seat for this show using its ID (like 'A1')."""
        for ss in self.show_seats:
            if ss.physical_seat.seat_id == seat_id:
                return ss
        return None

class Customer:
    """The person buying the tickets."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Ticket:
    """The actual pass generated after payment."""
    def __init__(self, show: Show, seat_id: str):
        self.ticket_id = str(uuid.uuid4())[:8] # Random unique 8-character ID
        self.show = show
        self.seat_id = seat_id

class Payment:
    """Handles the money! Very simple simulation."""
    def __init__(self, amount: float):
        self.amount = amount
        self.is_successful = False

    def process_payment(self, succeed: bool = True):
        # In a real app, this talks to a bank. Here, we just set a flag.
        self.is_successful = succeed
        return self.is_successful

class Refund:
    """If a booking is cancelled, we process a refund."""
    def __init__(self, amount: float):
        self.amount = amount
        self.is_processed = False

    def process_refund(self):
        self.is_processed = True
        return True

class Booking:
    """
    The main shopping cart! 
    It holds the customer, the show they want, the seats they picked, and handles payment.
    """
    def __init__(self, customer: Customer, show: Show):
        self.booking_id = str(uuid.uuid4())[:8]
        self.customer = customer
        self.show = show
        self.selected_show_seats: List[ShowSeat] = []
        self.status = "PENDING" # Can be PENDING, CONFIRMED, or CANCELLED
        self.tickets: List[Ticket] = []
        self.payment: Payment = None

    def add_seat(self, seat_id: str) -> bool:
        """Tries to add a seat to this booking."""
        show_seat = self.show.get_show_seat(seat_id)
        
        # TEST CASE 07: Invalid seat
        if not show_seat:
            print(f"Error: Seat {seat_id} doesn't exist on this screen!")
            return False
            
        # TEST CASE 02: Duplicate seat rejection
        if show_seat.is_booked:
            print(f"Error: Seat {seat_id} is already booked by someone else!")
            return False
            
        self.selected_show_seats.append(show_seat)
        return True

    def confirm_booking(self, payment_succeeds: bool = True):
        """Processes payment and generates tickets if successful."""
        # Calculate a fake price (e.g., $10 per seat)
        total_amount = len(self.selected_show_seats) * 10.0
        self.payment = Payment(total_amount)
        
        # Try to pay!
        if self.payment.process_payment(succeed=payment_succeeds):
            self.status = "CONFIRMED"
            # Actually mark the seats as taken in the system
            for ss in self.selected_show_seats:
                ss.book()
                # Generate a ticket for each seat
                self.tickets.append(Ticket(self.show, ss.physical_seat.seat_id))
            return True
        else:
            # TEST CASE 03: Payment failure
            self.status = "FAILED"
            return False

    def cancel_booking(self, is_eligible_for_refund: bool = True):
        """Cancels a confirmed booking and frees up the seats."""
        if self.status != "CONFIRMED":
            print("Can only cancel confirmed bookings.")
            return False

        if is_eligible_for_refund:
            # TEST CASE 04: Cancellation with refund
            refund = Refund(self.payment.amount)
            refund.process_refund()
            self.status = "CANCELLED"
            
            # Free up the seats so others can buy them!
            for ss in self.selected_show_seats:
                ss.release()
            return True
        else:
            # TEST CASE 05: Cancellation not allowed (e.g., past the deadline)
            print("Cancellation policy denies this cancellation. No refund.")
            return False
