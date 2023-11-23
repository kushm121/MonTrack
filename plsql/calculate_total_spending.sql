create FUNCTION calculate_total_spending(username VARCHAR2, today DATE)
RETURN FLOAT
IS
    total_spending FLOAT := 0.0;
BEGIN
    SELECT NVL(SUM(Amount),0) INTO total_spending
    FROM Transactions
    WHERE Username = calculate_total_spending.username
    AND TRUNC(TransactionDate) = calculate_total_spending.today
    AND categoryid IN(3,4,5,6,7,8);

    RETURN total_spending;
END calculate_total_spending;
/

