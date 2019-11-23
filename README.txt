PostgresSQL instructions:
    - In order to import db file, please run from your prompt: psql [existing db] username < dbexport.pgsql
    - The default values for db name, user, password and host were taken from my local environment
      and you can change it by specify them in the cmd (see the parser's help)
    - The table name is files_reader and it has 2 columns:
        1. Type - file\heartbeat.
        2. Name - name of file or the server timestamp.

Client & Server:
    - The json data consists of file's name and if it's corrupted.(e.g "file_44 : not-corrupted").
    - All the requested values (timeout, heartbeat interval...) located in configuration file.
    - The flow parser contains both arguments for the client and the server.
    - It's recommended to see the common help menu by running the scripts with -h\--help.