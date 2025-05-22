"""
Questions:
 

    1. Complete the `MiniVenmo.create_user()` method to allow our application to create new users.

    2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

    3. Venmo has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this
   

    Bobby paid Carol $5.00 for Coffee
    Carol paid Bobby $15.00 for Lunch

    Implement the `User.retrieve_activity()` and `MiniVenmo.render_feed()` methods so the MiniVenmo application can render the feed.

    4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
    5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.
"""

"""
MiniVenmo! Imagine that your phone and wallet are trying to have a beautiful
baby. In order to make this happen, you must write a social payment app.
Implement a program that will feature users, credit cards, and payment events.
"""

import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass

class DuplicateFriendException(Exception):
    pass

class Payment:
    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
 

class Feed:
    def __init__(self):
        self._events = []
    
    def add_payment_feed(self, payment: Payment):
        feed_data = payment
        feed_text = f"{payment.actor.username} paid {payment.target.username} ${payment.amount:.2f} for {payment.note}"
        self._events.append({"feed_data": feed_data, "feed_text": feed_text})
    
    def add_friend_feed(self, user1, user2):
        feed_text = f"{user1.username} and {user2.username} are now friends"
        self._events.append({"feed_data": None, "feed_text": feed_text})
    
    def get_events(self):
        return self._events


class User:
    def __init__(self, username, balance=0.0, credit_card_number=None):
        self.friends = []
        self.feed = Feed()

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')

        if credit_card_number:
            if self._is_valid_credit_card(credit_card_number):
                self.credit_card_number = credit_card_number
            else:
                raise CreditCardException("Credit Card not valid.")
        
        self.balance = balance


    def retrieve_feed(self):
        return self.feed

    def add_friend(self, new_friend):
        if new_friend in self.friends:
            raise DuplicateFriendException(f"{new_friend.username} is already your friend")
        self.friends.append(new_friend)
        self.feed.add_friend_feed(self, new_friend)
        new_friend.friends.append(self)
        new_friend.feed.add_friend_feed(new_friend, self)

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number
        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        amount = float(amount)
        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')
    
        if self.balance >= amount:
            self.pay_with_balance(amount)
        else:
            self.pay_with_card(target, amount, note)
        
        target.add_to_balance(amount)

        payment = Payment(amount, self, target, note)
        self.feed.add_payment_feed(payment)
        target.feed.add_payment_feed(payment)

    def pay_with_card(self, target, amount, note):
        if self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(target, amount, note)

    def pay_with_balance(self, amount):
        self.balance -= float(amount)

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, target, amount, note):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        # TODO: add code here
        return User(username, balance, credit_card_number)

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        print("Feed:")
        for event in feed.get_events():
            print(event.get("feed_text"))
        print("End of Feed")
    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")

        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        feed = carol.retrieve_feed()
        venmo.render_feed(feed)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()
        

if __name__ == '__main__':
    MiniVenmo.run()
    unittest.main()
