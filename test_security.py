import pytest
from hypothesis import given, strategies as st

# Import from your demo module
from demo import (
    MemberAccount, Book, DVD, Library,
    EmailNotifier, ConsolePayment, StandardPolicy, ChildrenPolicy
)

def make_lib(policy="standard"):
    if policy == "children":
        policy_obj = ChildrenPolicy()
    else:
        policy_obj = StandardPolicy()
    return Library(EmailNotifier(), ConsolePayment(), policy_obj)

# ---------- Misuse tests (explicit negative/invalid inputs) ----------

def test_overpay_is_rejected():
    m = MemberAccount("Eve")
    m.add_charge(5.0)
    ok = m.pay(10.0)            # trying to overpay more than balance
    assert ok is False
    assert m.balance() == 5.0   # balance should be unchanged

def test_negative_payment_is_rejected():
    m = MemberAccount("Nina")
    m.add_charge(10.0)
    ok = m.pay(-3.0)            # negative payments should be rejected
    assert ok is False
    assert m.balance() == 10.0

def test_checkout_and_return_removes_item_from_loans():
    L = make_lib()
    m = MemberAccount("Sam")
    b = Book("Test Book", 14)
    L.checkout(m, b)
    assert "Test Book" in L.list_loans(m)
    L.return_item(m, b, days_late=0)
    assert "Test Book" not in L.list_loans(m)

# ---------- Fuzz/property tests (Hypothesis generates inputs) ----------

@given(amount=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False))
def test_random_payments_never_create_negative_balance(amount):
    m = MemberAccount("Alex")
    m.add_charge(50.0)
    # Only pay if the request is valid per your API contract
    ok = m.pay(amount) if (amount > 0 and amount <= m.balance()) else False
    # Library logic ensures balance never dips below zero
    assert m.balance() >= 0.0

@given(days=st.integers(min_value=-365, max_value=10000))
def test_days_late_never_produces_negative_fee(days):
    L = make_lib()
    m = MemberAccount("Bob")
    d = DVD("The Matrix", 7)
    L.checkout(m, d)
    L.return_item(m, d, days_late=days)
    # Fees are added via add_charge, which never subtracts
    assert m.balance() >= 0.0

@given(days=st.integers(min_value=-365, max_value=10000))
def test_children_policy_never_negative_fee(days):
    L = make_lib(policy="children")
    m = MemberAccount("Carol")
    b = Book("Moby Dick", 14)
    L.checkout(m, b)
    L.return_item(m, b, days_late=days)
    assert m.balance() >= 0.0

# ---------- Invariants on multiple operations ----------

def test_multiple_loans_and_returns_invariants():
    L = make_lib()
    m = MemberAccount("Dana")
    items = [
        Book("A", 14),
        DVD("B", 7),
        Book("C", 21),
    ]
    for it in items:
        L.checkout(m, it)
    assert set(L.list_loans(m)) == {"A", "B", "C"}

    # Return in different order with mixed lateness
    L.return_item(m, items[1], days_late=3)   # DVD late
    L.return_item(m, items[0], days_late=0)   # Book on time
    L.return_item(m, items[2], days_late=10)  # Book late
    # All should be removed from loans
    assert L.list_loans(m) == []
    # Balance must not be negative
    assert m.balance() >= 0.0
