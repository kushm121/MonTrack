SET SERVEROUTPUT ON;
CREATE OR REPLACE PROCEDURE InsertUser (
    p_Username VARCHAR2,
    p_Password VARCHAR2,
    p_Email VARCHAR2,
    p_Role VARCHAR2,
    p_RegistrationDate DATE
)
IS
BEGIN
    INSERT INTO Users (Username, Password, Email, Role, RegistrationDate)
    VALUES (p_Username, p_Password, p_Email, p_Role, p_RegistrationDate);
EXCEPTION
    WHEN OTHERS THEN
        -- Handle exceptions if necessary
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END InsertUser;
/
