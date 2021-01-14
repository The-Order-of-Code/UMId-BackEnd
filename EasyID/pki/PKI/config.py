import getpass

# Configuration file
class Config:
    # SET ENVIRONMENT VARIABLES
    hostname = "35.228.11.197"
    port = 8888
    username = "filipap"
    path_key = f"/Users/filipap/.ssh/google_compute_engine"

    commands_refresh_OCSP_docker = "sudo docker exec ca /kill.sh"
    command_sign_userdict_docker = "sudo docker exec ca python3 new_main.py"
    profile = "client"
