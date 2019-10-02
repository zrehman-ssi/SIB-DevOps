pipeline{
    agent any
    stages{
        stage("Create Virtual Environment"){
            // agent {
            //     docker {
            //         image 'python:latest' 
            //     }
            // }
            steps{
                // sh "python3.7 --version"
                echo "====++++Creating virtual envrionment steps is running++++===="
            }
        }
    }
    post{
        always{
            echo "Piple line completed"
        }
        success{
            echo "Piple line completed successfully"
        }
        failure{
            echo "Pipeline failed to completed"
        }
    }
}