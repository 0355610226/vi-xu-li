import http.server
import socketserver
import os
import webbrowser

# Change to the quiz directory
os.chdir(r'C:\Users\WIN\Desktop\New folder')

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Server running at {url}")
    print(f"Press Ctrl+C to stop the server")
    
    # Open in default browser
    try:
        webbrowser.open(url)
    except:
        pass
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
