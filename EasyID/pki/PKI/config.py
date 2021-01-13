import getpass

# Configuration file
class Config:
    # SET ENVIRONMENT VARIABLES
    hostname = "localhost"
    port = 8888
    username = "mateus"
    path_key = f"/home/{getpass.getuser()}/.ssh/id_rsa"

    commands_refresh_OCSP_docker = "docker exec ca /kill.sh"
    command_sign_userdict_docker = "docker exec ca python3 new_main.py"
    profile = "client"
