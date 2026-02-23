Feature: Modules
    Background:
        Given a temporary data directory
        And a mocked channel
        And a mocked repository

    Scenario: Get modules after initialization
        When the module 'mol-scale' becomes available
        And the client requests /modules
        Then the client receives a response of length 1
        And the client receives a response containing
            {"name": "mol_scale", "version": "0.1"}

    Scenario: Get modules after adding a module
        Given a file at 'modules/test-1.0.0' with content
            {
                "id": "test-1.0.0",
                "name": "test",
                "version": "1.0.0"
            }
        When the channel receives a message on topic 'modules' with content
            {
                "id": "test-1.0.0"
            }
        And the module 'test' becomes available
        And the client requests /modules
        Then the client receives a response containing
            {"name": "test", "version": "1.0.0"}
