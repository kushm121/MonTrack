create FUNCTION get_total_balance(username VARCHAR2) RETURN NUMBER IS
    total_income NUMBER := 0;
    total_expense NUMBER := 0;
BEGIN
    SELECT SUM(Amount)
    INTO total_income
    FROM Transactions
    WHERE USERNAME = get_total_balance.username
    AND CategoryID IN (1, 2); -- Income categories

    SELECT SUM(Amount)
    INTO total_expense
    FROM Transactions
    WHERE USERNAME = get_total_balance.username
    AND CategoryID not in (1,2); -- Expense categories

    RETURN NVL(total_income, 0) - NVL(total_expense, 0);
END get_total_balance;
/

