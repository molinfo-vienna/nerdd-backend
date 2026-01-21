Feature: Maintenance Mode
    Background:
        Given a temporary data directory
        And a mocked channel
        And a mocked repository

    Scenario: Requesting resources when maintenance mode is inactive
        When the client requests /modules
        Then the status code of the response is 200

    Scenario: Requesting resources when maintenance mode is active
        Given an environment variable MAINTENANCE_MODE is set to true
        When the client requests /modules
        Then the status code of the response is 503
        And the client receives a response with content
            {
                "detail": "Server is under maintenance.", 
                "code": "under_maintenance"
            }
