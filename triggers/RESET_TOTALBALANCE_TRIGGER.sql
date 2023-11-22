create trigger RESET_TOTALBALANCE_TRIGGER
    before insert
    on TRANSACTIONS
    for each row
DECLARE
    v_current_month NUMBER;
    v_current_year NUMBER;
BEGIN
    -- Get the current month and year
    SELECT EXTRACT(MONTH FROM SYSTIMESTAMP), EXTRACT(YEAR FROM SYSTIMESTAMP)
    INTO v_current_month, v_current_year
    FROM dual;

    -- Check if it's a new month
    IF v_current_month <> EXTRACT(MONTH FROM :new.TransactionDate) OR v_current_year <> EXTRACT(YEAR FROM :new.TransactionDate) THEN
        -- Loop through all users and reset totalbalance to 0
        FOR user_row IN (SELECT Username FROM Users) LOOP
            UPDATE Users
            SET total_balance = 0
            WHERE Username = user_row.Username;
        END LOOP;
    END IF;
END;
/

