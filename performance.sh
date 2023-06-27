pipeline {
    agent any
    
    stages {
        stage('Invoke PowerShell Script') {
            steps {
                script {
                    // Path to the PowerShell script
                    def scriptPath = "path/to/script.ps1"
                    
                    // Execute the PowerShell script
                    def powerShellOutput = powershell(returnStdout: true, script: "powershell.exe -ExecutionPolicy Bypass -File ${scriptPath}")
                    
                    // Print the output of the PowerShell script
                    echo "PowerShell script output: ${powerShellOutput}"
                }
            }
        }
    }
}
