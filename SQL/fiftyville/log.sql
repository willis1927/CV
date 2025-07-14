-- Keep a log of any SQL queries you execute as you solve the mystery.
--find crime scene report from day and location of crime
SELECT description from crime_scene_reports WHERE month = 7 AND day = 28 and street = "Humphrey Street";
---find interview transcripts
SELECT name, transcript FROM interviews WHERE month = 7 AND day = 28 and transcript LIKE ('%bakery%');
-- View bakery security logs around the time of crime, linking to people table to identify car owners
SELECT day, month, hour, minute, activity, bakery_security_logs.license_plate, name from bakery_security_logs
    JOIN people ON bakery_security_logs.license_plate = people.license_plate
    WHERE month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 30
    ORDER BY minute;
-- cross reference suspects from car park security vs atm transactions earlier in the morning
SELECT name, atm_location, transaction_type, amount FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street";
--look for calls < 1min made by suspects
SELECT people.name, caller, duration from phone_calls
    Join people ON phone_calls.caller = people.phone_number
    WHERE month = 7 AND day = 28 AND duration < 60 and people.name IN ('Diana','Luca','Bruce','Iman');
--retrieve names of receivers of calls by suspects
SELECT people.name,caller, receiver, duration from phone_calls
    Join people ON phone_calls.receiver = people.phone_number
    WHERE month = 7 AND day = 28 AND duration < 60 and phone_calls.id IN
        (SELECT phone_calls.id from phone_calls
        Join people ON phone_calls.caller = people.phone_number
        WHERE duration < 60 and people.name IN ('Diana','Luca','Bruce','Iman'));
--get fiftyville airport id
Select * from airports WHERE city = "Fiftyville";
--Get passport numbers of suspects
SELECT passport_number FROM people WHERE name IN ('Diana','Bruce','Philip','Robin','Charlotte');
-- check if suspects are on any flights 29th from passenger & passport numbers
SELECT * from flights WHERE day = 29 and month = 7 and id IN (SELECT flight_id FROM passengers WHERE passport_number IN (SELECT passport_number FROM people WHERE name IN ('Diana','Luca','Bruce','Iman','Philip','Robin','Charlotte')))ORDER BY hour,minute;
-- get passenger list for flights 18 & 36 excluding anyone not a suspect
SELECT people.name, passengers.flight_id, passengers.seat  FROM passengers
    JOIN people ON passengers.passport_number = people.passport_number
    WHERE flight_id IN ('18','36') AND people.passport_number IN (SELECT passport_number FROM people WHERE name IN ('Diana','Bruce','Philip','Robin','Charlotte'));
-- get flights from fiftyville and destiantions
SELECT * from  flights
    JOIN airports ON flights.id = airports.id
    WHERE day = 29 AND month = 7 ORDER BY hour, minute;
SELECT full_name, city from airports where id = 4;
