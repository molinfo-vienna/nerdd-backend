Feature: Jobs
    Background:
        Given a temporary data directory
        And a mocked channel
        And a mocked repository

    Scenario: Create a source
        Given a list of 10 random molecules
        And a file containing the molecules in smiles format

        When the client sends a PUT request to /sources/ with the files

        Then the status code of the response is 200
        # file system
        And the sources folder contains exactly 1 file(s)
        And the source file in the response was created
        # channel
        And the channel sends 0 messages on topic 'jobs'
        # repository
