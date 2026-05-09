import subprocess
import time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow CORS so the frontend running on a different port (e.g. 5173) can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def execute_cmd(title, cmd):
    yield f"\n> {title}\n"
    yield f"$ powershell -Command \"{cmd}\"\n"
    try:
        process = subprocess.Popen(
            ["powershell", "-Command", cmd],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Read the output line by line as it is produced
        if process.stdout:
            for line in process.stdout:
                yield line
                
        process.wait()
    except Exception as e:
        yield f"EXCEPTION: {str(e)}\n"
    time.sleep(0.5)

def forge_generator(debloat, optimize, pos):
    yield "[ ENGINE ] Connection established. Executing Payload...\n"
    
    if debloat == "Aggressive":
        cmd = "Get-AppxPackage -AllUsers | Where-Object {$_.Name -notmatch 'Store|Calculator|Photos'} | Remove-AppxPackage"
        yield from execute_cmd("Aggressive Debloat", cmd)
    elif debloat == "Basic":
        cmd = "Get-AppxPackage *xbox* | Remove-AppxPackage; Get-AppxPackage *zune* | Remove-AppxPackage"
        yield from execute_cmd("Basic Debloat", cmd)

    if optimize:
        cmd = "powercfg -change -standby-timeout-ac 0; powercfg -change -monitor-timeout-ac 0; Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot' -Name 'TurnOffWindowsCopilot' -Value 1 -Type DWord -Force"
        yield from execute_cmd("Applying Optimizations", cmd)

    if pos != "None":
        cmd = f"Write-Host 'Simulating silent install for {pos}...'"
        yield from execute_cmd(f"Installing {pos}", cmd)

@app.post("/api/forge")
async def forge_endpoint(request: Request):
    data = await request.json()
    debloat = data.get("debloat_level", "None")
    optimize = data.get("optimize_hardware", False)
    pos = data.get("pos_software", "None")

    return StreamingResponse(forge_generator(debloat, optimize, pos), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
