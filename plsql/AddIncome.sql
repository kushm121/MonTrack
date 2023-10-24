SET SERVEROUTPUT ON;
CREATE OR REPLACE PROCEDURE InsertTransactionAndCategory (
    p_Username VARCHAR2,
    p_CategoryID NUMBER,
    p_CategoryName VARCHAR2,
    p_TransactionID NUMBER,
    p_Amount NUMBER,
    p_Description VARCHAR2,
    p_TransactionDate DATE
)
IS
BEGIN
    -- Insert into User_Income_Categories table
    INSERT INTO User_Income_Categories (CategoryID, Username)
    VALUES (p_CategoryID, p_Username);
    
    -- Insert into Transactions table
    INSERT INTO Transactions (TransactionID, Username, CategoryID, Amount, Description, TransactionDate)
    VALUES (p_TransactionID, p_Username, p_CategoryID, p_Amount, p_Description, p_TransactionDate);
EXCEPTION
    WHEN OTHERS THEN
        -- Handle exceptions if necessary
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END InsertTransactionAndCategory;
/
