# -*- coding: utf-8 -*-

"""
White-box unit testing examples.
"""
import unittest
from unittest.mock import patch

from white_box.class_exercises import (
    BankAccount,
    BankingSystem,
    VendingMachine,
    divide,
    get_grade,
    is_even,
    is_triangle,
)


class TestIsEven(unittest.TestCase):
    """
    White-box unittest class for the is_even function.
    """

    def test_is_even_with_even_number(self):
        """
        Checks if a number is even.
        """
        self.assertTrue(is_even(0))

    def test_is_even_with_odd_number(self):
        """
        Checks if a number is not even.
        """
        self.assertFalse(is_even(7))


class TestDivide(unittest.TestCase):
    """
    White-box unittest class for the divide function.
    """

    def test_divide_by_non_zero(self):
        """
        Checks the divide function works as expected.
        """
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        """
        Checks the divide function returns 0 when dividing by 0.
        """
        self.assertEqual(divide(10, 0), 0)


class TestGetGrade(unittest.TestCase):
    """
    White-box unittest class for the get_grade function.
    """

    def test_get_grade_a(self):
        """
        Checks A grade.
        """
        self.assertEqual(get_grade(95), "A")

    def test_get_grade_b(self):
        """
        Checks B grade.
        """
        self.assertEqual(get_grade(85), "B")

    def test_get_grade_c(self):
        """
        Checks C grade.
        """
        self.assertEqual(get_grade(75), "C")

    def test_get_grade_f(self):
        """
        Checks F grade.
        """
        self.assertEqual(get_grade(65), "F")


class TestIsTriangle(unittest.TestCase):
    """
    White-box unittest class for the is_triangle function.
    """

    def test_is_triangle_yes(self):
        """
        Checks the three inputs can form a triangle.
        """
        self.assertEqual(is_triangle(3, 4, 5), "Yes, it's a triangle!")

    def test_is_triangle_no_1(self):
        """
        Checks the three inputs can't form a triangle when C is greater or equal than A + B.
        """
        self.assertEqual(is_triangle(3, 4, 7), "No, it's not a triangle.")

    def test_is_triangle_no_2(self):
        """
        Checks the three inputs can't form a triangle when B is greater or equal than A + C.
        """
        self.assertEqual(is_triangle(2, 3, 1), "No, it's not a triangle.")

    def test_is_triangle_no_3(self):
        """
        Checks the three inputs can't form a triangle when A is greater or equal than B + C.
        """
        self.assertEqual(is_triangle(2, 1, 1), "No, it's not a triangle.")


class TestWhiteBoxVendingMachine(unittest.TestCase):
    """
    Vending Machine unit tests.
    """

    # @classmethod
    # def setUpClass(cls):
    #    return

    def setUp(self):
        self.vending_machine = VendingMachine()
        self.assertEqual(self.vending_machine.state, "Ready")

    # def tearDown(self):
    #    return

    # @classmethod
    # def tearDownClass(cls):
    #    return

    def test_vending_machine_insert_coin_error(self):
        """
        Checks the vending machine can accept coins.
        """
        self.vending_machine.state = "Dispensing"

        output = self.vending_machine.insert_coin()

        self.assertEqual(self.vending_machine.state, "Dispensing")
        self.assertEqual(output, "Invalid operation in current state.")

    def test_vending_machine_insert_coin_success(self):
        """
        Checks the vending machine fails to accept coins when it's not ready.
        """
        output = self.vending_machine.insert_coin()

        self.assertEqual(self.vending_machine.state, "Dispensing")
        self.assertEqual(output, "Coin Inserted. Select your drink.")


class TestBankingAccount(unittest.TestCase):
    """
    Banking account unit tests.
    """

    def setUp(self):
        self.account = BankAccount(123, 1000)

    def test_initialize_bank_account(self):
        """
        Checks the BankAccount class initializes correctly.
        """
        self.assertEqual(self.account.account_number, 123)
        self.assertEqual(self.account.balance, 1000)

    @patch("builtins.print")
    def test_view_account(self, mock_print):
        """
        Checks the BankAccount can view account details.
        """
        self.account.view_account()
        mock_print.assert_called_with(
            f"The account {self.account.account_number} has a balance of {self.account.balance}"
        )


class TestBankingSystem(unittest.TestCase):
    """
    Banking system unit tests.
    """

    user = "user123"
    password = "pass123"

    def setUp(self):
        self.banking_system = BankingSystem()

    def test_initialize_banking_system(self):
        """
        Checks the BankingSystem class initializes correctly.
        """
        self.assertEqual(
            self.banking_system.users, {f"{self.user}": f"{self.password}"}
        )
        self.assertEqual(self.banking_system.logged_in_users, set())

    @patch("builtins.print")
    def test_authenticate_user_success(self, mock_print):
        """
        Checks the BankingSystem can authenticate users with correct credentials.
        """
        authenticated = self.banking_system.authenticate(self.user, self.password)
        self.assertTrue(authenticated)
        self.assertIn(self.user, self.banking_system.logged_in_users)
        mock_print.assert_called_with(f"User {self.user} authenticated successfully.")

    @patch("builtins.print")
    def test_authenticate_user_already_authenticated(self, mock_print):
        """
        Checks the BankingSystem fails to authenticate users who are already authenticated.
        """
        self.banking_system.logged_in_users.add(self.user)
        authenticated = self.banking_system.authenticate(self.user, self.password)
        self.assertFalse(authenticated)
        mock_print.assert_called_with("User already logged in.")

    @patch("builtins.print")
    def test_authenticate_user_failure(self, mock_print):
        """
        Checks the BankingSystem fails to authenticate users with incorrect credentials.
        """
        authenticated = self.banking_system.authenticate(self.user, "wrongpass")
        self.assertFalse(authenticated)
        self.assertNotIn(self.user, self.banking_system.logged_in_users)
        mock_print.assert_called_with("Authentication failed.")

    @patch("builtins.print")
    def test_transfer_money_user_not_authenticated(self, mock_print):
        """
        Checks the BankingSystem handles users who are not authenticated.
        """
        receiver = "user456"
        amount = 200
        transaction_type = "regular"
        result = self.banking_system.transfer_money(
            self.user, receiver, amount, transaction_type
        )
        mock_print.assert_called_with("Sender not authenticated.")
        self.assertFalse(result)

    @patch("builtins.print")
    def test_transfer_money_regular(self, mock_print):
        """
        Checks the BankingSystem can transfer money between accounts using the regular transaction
        type, when the user is authenticated and has sufficient funds.
        """
        receiver = "user456"
        amount = 200
        transaction_type = "regular"
        self.banking_system.logged_in_users.add(self.user)
        result = self.banking_system.transfer_money(
            self.user, receiver, amount, transaction_type
        )
        mock_print.assert_called_with(
            f"Money transfer of ${amount} ({transaction_type} transfer)"
            f" from {self.user} to {receiver} processed successfully."
        )
        self.assertTrue(result)

    @patch("builtins.print")
    def test_transfer_money_express(self, mock_print):
        """
        Checks the BankingSystem can transfer money between accounts using the express transaction
        type, when the user is authenticated and has sufficient funds.
        """
        receiver = "user456"
        amount = 200
        transaction_type = "express"
        self.banking_system.logged_in_users.add(self.user)
        result = self.banking_system.transfer_money(
            self.user, receiver, amount, transaction_type
        )
        mock_print.assert_called_with(
            f"Money transfer of ${amount} ({transaction_type} transfer)"
            f" from {self.user} to {receiver} processed successfully."
        )
        self.assertTrue(result)

    @patch("builtins.print")
    def test_transfer_money_scheduled(self, mock_print):
        """
        Checks the BankingSystem can transfer money between accounts using the scheduled transaction
        type, when the user is authenticated and has sufficient funds.
        """
        receiver = "user456"
        amount = 200
        transaction_type = "scheduled"
        self.banking_system.logged_in_users.add(self.user)
        result = self.banking_system.transfer_money(
            self.user, receiver, amount, transaction_type
        )
        mock_print.assert_called_with(
            f"Money transfer of ${amount} ({transaction_type} transfer)"
            f" from {self.user} to {receiver} processed successfully."
        )
        self.assertTrue(result)

    @patch("builtins.print")
    def test_transfer_money_invalid_transaction_type(self, mock_print):
        """
        Checks the BankingSystem handles invalid transaction types correctly.
        """
        receiver = "user456"
        amount = 200
        transaction_type = "invalid_type"
        self.banking_system.logged_in_users.add(self.user)
        result = self.banking_system.transfer_money(
            self.user, receiver, amount, transaction_type
        )
        mock_print.assert_called_with("Invalid transaction type.")
        self.assertFalse(result)

    @patch("builtins.print")
    def test_transfer_money_insufficient_funds(self, mock_print):
        """
        Checks the BankingSystem handles insufficient funds correctly.
        """
        receiver = "user456"
        amount = 1000
        transaction_type = "regular"
        self.banking_system.logged_in_users.add(self.user)
        result = self.banking_system.transfer_money(
            self.user, receiver, amount, transaction_type
        )
        mock_print.assert_called_with("Insufficient funds.")
        self.assertFalse(result)
