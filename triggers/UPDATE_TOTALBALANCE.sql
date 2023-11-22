create trigger UPDATE_TOTALBALANCE
    after insert
    on TRANSACTIONS
    for each row
BEGIN
    IF :NEW.CategoryID IN (1, 2) THEN
        UPDATE Users
        SET total_balance = total_balance + :NEW.Amount
        WHERE Username = :NEW.Username;
    ELSIF :NEW.CategoryID IN (3, 4, 5, 6, 7, 8) THEN
        UPDATE Users
        SET total_balance = total_balance - :NEW.Amount
        WHERE Username = :NEW.Username;
    END IF;
END;
/

