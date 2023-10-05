# Crypto Profit Calculator
Flask-based API for calculating crypto trading profits/losses. The application uses Coinbase API for fetching historical price data of 150+ cryptocurrencies. The local K8s cluster development and deployment is configured with Docker, minikube, and Skaffold.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [skaffold](https://skaffold.dev/docs/install/)

## How To Run

1. Clone the repository and navigate to the project directory
   ```$xslt
   $ git clone git@github.com:mDemianchuk/crypto-profit-calculator.git
   $ cd crypto-profit-calculator
   ```
   
2. [Configure](https://minikube.sigs.k8s.io/docs/handbook/config/) and start minikube
    ```$xslt
    $ minikube start
    ```

3. Run skaffold
    
    ```$xslt
    $ skaffold dev
    ```
   \* This command will also port forward K8s service (port 5000) to your local machine (port 5005)

4. Submit your Coinbase Pro statement in the csv format

    ```$xslt
    $ curl -X POST -F "csv=@/path/to/statement.csv" http://127.0.0.1:5005/api/reports
    ```
   \* Your statements or any other metadata are not uploaded or stored anywhere other than your own machine!
