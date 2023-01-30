

## Connecting to Kaggle API
- Install kaggle package.
    ```
        pip install kaggle
    ```
- Generate api token and set it up.
    - To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com.
    - Then go to the `Account` tab of your user profile and select `Create API Token`.
        - This will trigger the download of `kaggle.json`, a file containing your API credentials.
    - Execute following commands to move file 
    ```
        mkdir - p ~/.kaggle
        mvl kaggle.json ~/.kaggle/
        ls ~/.kaggle
        chmod 600 ~/.kaggle/kaggle.json
    ```