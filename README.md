# Aws Lambda for Archie Scan Clouds Templates

This simple lambda function scans the DynamoDB table to serve pre-filtered items to the front end, thus optimizing its loading process.

# How test the lambda locally

*  Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

* Set the environment variables
    ```bash
    # .env
    TableName=archie-new-templates-sandbox
    ```
* Run the tests
    ```bash
    pytest  --import-mode=append 
    
    ```
