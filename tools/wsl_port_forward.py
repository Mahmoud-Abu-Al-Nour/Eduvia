"""
WSL2 Port Forwarder
Forwards 127.0.0.1:5432 -> WSL2 PostgreSQL:5432
Forwards 127.0.0.1:6333 -> WSL2 Qdrant:6333
Dynamically detects WSL2 IP address.
"""
import asyncio
import subprocess
import sys

def get_wsl_ip() -> str:
    try:
        output = subprocess.check_output(["wsl", "-d", "Ubuntu", "-u", "root", "hostname", "-I"], text=True)
        ips = output.strip().split()
        if ips:
            return ips[0]
    except Exception as e:
        print(f"Error querying WSL IP: {e}", file=sys.stderr)
    return "172.28.238.20"

async def pipe(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        while not reader.at_eof():
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

async def forward(local_port: int, remote_host: str, remote_port: int):
    async def handle_client(client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
        try:
            remote_reader, remote_writer = await asyncio.open_connection(remote_host, remote_port)
        except Exception as e:
            client_writer.close()
            return
        asyncio.create_task(pipe(client_reader, remote_writer))
        asyncio.create_task(pipe(remote_reader, client_writer))

    server = await asyncio.start_server(handle_client, "127.0.0.1", local_port)
    print(f"Forwarding 127.0.0.1:{local_port} -> {remote_host}:{remote_port}", flush=True)
    async with server:
        await server.serve_forever()

async def main():
    wsl_ip = get_wsl_ip()
    print(f"Detected WSL IP: {wsl_ip}", flush=True)
    await asyncio.gather(
        forward(5432, wsl_ip, 5432),
        forward(6333, wsl_ip, 6333)
    )

if __name__ == "__main__":
    asyncio.run(main())
