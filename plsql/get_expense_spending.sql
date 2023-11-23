create FUNCTION get_expense_spending(username VARCHAR2)
RETURN SYS_REFCURSOR IS
    expense_cursor SYS_REFCURSOR;
BEGIN
    OPEN expense_cursor FOR
    SELECT c.CategoryName, SUM(t.Amount) AS TotalSpending
    FROM Transactions t
    JOIN Categories c ON t.CategoryID = c.CategoryID
    AND t.CategoryID IN (3, 4, 5, 6, 7, 8) -- Expense Categories
    AND EXTRACT(MONTH FROM t.TransactionDate) = EXTRACT(MONTH FROM SYSTIMESTAMP) -- Current Month
    AND t.Username = get_expense_spending.username
    GROUP BY c.CategoryName;

    RETURN expense_cursor;
END get_expense_spending;
/

