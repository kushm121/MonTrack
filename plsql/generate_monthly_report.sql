create PROCEDURE generate_monthly_report(username_param IN VARCHAR2) AS
    v_report_id NUMBER;
BEGIN
    SELECT REPORTID_SEQ.NEXTVAL INTO v_report_id FROM dual;
    INSERT INTO Reports (ReportID, Username, ReportType, StartDate, EndDate, IncomeTotal, ExpenseTotal, NetSavings)
    SELECT
        v_report_id,
        username_param,
        'Monthly',
        TRUNC(SYSDATE, 'MM') AS StartDate,
        LAST_DAY(SYSDATE) AS EndDate,
        NVL(SUM(CASE WHEN CategoryID IN (1, 2) THEN Amount ELSE 0 END), 0) AS IncomeTotal,
        NVL(SUM(CASE WHEN CategoryID not IN (1,2) THEN Amount ELSE 0 END), 0) AS ExpenseTotal,
        NVL(SUM(CASE WHEN CategoryID IN (1, 2) THEN Amount ELSE 0 END), 0) - NVL(SUM(CASE WHEN CategoryID not IN (1,2) THEN Amount ELSE 0 END), 0) AS NetSavings
    FROM Transactions
    WHERE TRUNC(TransactionDate, 'MM') = TRUNC(SYSDATE, 'MM')
      AND USERNAME = username_param;
END generate_monthly_report;
/

