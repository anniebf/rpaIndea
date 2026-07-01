from datetime import datetime

data = datetime.now().isoformat(timespec='minutes').replace(":", "_")

def Log(mensagemLog):
    with open(fr"C:\monitorAeroporto\log\log_execucao{data}.txt","a") as log:
        log.write(datetime.now().isoformat(timespec='minutes').replace(":", "_")+": "+mensagemLog+"\n")

if __name__ == "__main__":
    Log('')