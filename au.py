#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 MAHMUD TECH - NGROK AUTO RDP EXPOSER 💀
Owner: @UnknownGuy9876 | Channel: @SGCodexs
AUTO NGROK TOKEN | REAL-TIME PORT FORWARDING
"""

import socket
import subprocess
import threading
import time
import json
import os
import sys
import re
import requests
import zipfile
import tempfile
import shutil
import ctypes
import platform
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk

# ==================== NGROK MANAGER ====================
class NgrokManager:
    """Complete Ngrok Manager - Download, Auth, Tunnel"""
    
    NGROK_PATHS = [
        os.path.join(os.environ.get('APPDATA', ''), 'ngrok', 'ngrok.exe'),
        os.path.join(os.getcwd(), 'ngrok.exe'),
        os.path.join(os.environ.get('ProgramFiles', ''), 'ngrok', 'ngrok.exe'),
        'ngrok.exe'  # Fallback to PATH
    ]
    
    def __init__(self, log_callback=None):
        self.log = log_callback or print
        self.ngrok_path = None
        self.process = None
        self.public_url = None
        self.tunnel_type = None
        self.local_port = None
        self.auth_token = None
        
        # Find or download ngrok
        self._find_ngrok()
    
    def _find_ngrok(self):
        """Find ngrok binary"""
        for path in self.NGROK_PATHS:
            if os.path.exists(path):
                self.ngrok_path = path
                self.log(f"[+] Ngrok found: {path}")
                return
        
        self.log("[!] Ngrok not found. Will auto-download.")
    
    def download_ngrok(self, force=False):
        """Download latest ngrok for Windows"""
        if self.ngrok_path and not force:
            return True
        
        try:
            self.log("[*] Downloading ngrok...")
            
            # Get latest download URL
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
            
            # Download
            temp_dir = tempfile.gettempdir()
            zip_path = os.path.join(temp_dir, "ngrok.zip")
            
            resp = requests.get(url, stream=True, timeout=30)
            with open(zip_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract
            extract_dir = os.path.join(os.environ.get('APPDATA', os.getcwd()), 'ngrok')
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Clean up
            os.remove(zip_path)
            
            self.ngrok_path = os.path.join(extract_dir, 'ngrok.exe')
            self.log(f"[+] Ngrok downloaded to: {self.ngrok_path}")
            return True
            
        except Exception as e:
            self.log(f"[!] Download failed: {e}")
            return False
    
    def set_auth_token(self, token: str):
        """Set ngrok auth token"""
        if not self.ngrok_path:
            self.download_ngrok()
        
        if not self.ngrok_path:
            return False
        
        try:
            result = subprocess.run(
                [self.ngrok_path, 'config', 'add-authtoken', token],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.auth_token = token
            self.log(f"[+] Auth token set: {token[:10]}...{token[-5:]}")
            return True
        except Exception as e:
            self.log(f"[!] Auth failed: {e}")
            return False
    
    def check_auth(self):
        """Check if ngrok is authenticated"""
        if not self.ngrok_path:
            return False
        
        try:
            result = subprocess.run(
                [self.ngrok_path, 'config', 'check'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'Valid configuration' in result.stdout
        except:
            return False
    
    def start_tcp_tunnel(self, local_port: int, region: str = 'ap') -> dict:
        """Start TCP tunnel for RDP"""
        if not self.ngrok_path:
            self.download_ngrok()
        
        if not self.ngrok_path:
            return {'error': 'Ngrok not available'}
        
        # Stop existing tunnel
        self.stop_tunnel()
        
        self.local_port = local_port
        self.tunnel_type = 'tcp'
        
        try:
            # Start ngrok
            cmd = [self.ngrok_path, 'tcp', str(local_port), '--log=stdout', '--log-format=json']
            
            if region:
                cmd.extend(['--region', region])
            
            self.log(f"[*] Starting ngrok TCP tunnel on port {local_port}...")
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Parse output for public URL
            self.public_url = None
            start_time = time.time()
            
            def read_output():
                for line in self.process.stdout:
                    try:
                        data = json.loads(line.strip())
                        if 'url' in data:
                            self.public_url = data['url']
                            self.log(f"[+] Public URL: {self.public_url}")
                            self.log(f"[+] Connect to: {self.public_url}")
                            break
                    except:
                        # Non-JSON output
                        match = re.search(r'url=([^\s]+)', line)
                        if match:
                            self.public_url = match.group(1)
                            self.log(f"[+] Public URL: {self.public_url}")
                            break
            
            # Read output in background
            output_thread = threading.Thread(target=read_output, daemon=True)
            output_thread.start()
            
            # Wait for URL (max 15 seconds)
            while not self.public_url and (time.time() - start_time) < 15:
                time.sleep(0.5)
            
            if not self.public_url:
                self.log("[!] Failed to get public URL. Check ngrok auth token.")
                return {'error': 'Failed to establish tunnel'}
            
            # Parse the URL
            # Format: tcp://0.tcp.ap.ngrok.io:12345
            parsed = self._parse_ngrok_url(self.public_url)
            
            return {
                'success': True,
                'public_url': self.public_url,
                'host': parsed['host'],
                'port': parsed['port'],
                'local_port': local_port,
                'full_address': f"{parsed['host']}:{parsed['port']}"
            }
            
        except Exception as e:
            self.log(f"[!] Tunnel error: {e}")
            return {'error': str(e)}
    
    def _parse_ngrok_url(self, url: str) -> dict:
        """Parse ngrok URL to extract host and port"""
        # tcp://0.tcp.ap.ngrok.io:12345
        url = url.replace('tcp://', '')
        if ':' in url:
            host, port = url.rsplit(':', 1)
            return {'host': host, 'port': int(port)}
        return {'host': url, 'port': 0}
    
    def get_tunnel_info(self):
        """Get active tunnel information"""
        if not self.public_url or not self.process:
            return None
        
        try:
            # Use ngrok API to get tunnel info
            resp = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=2)
            data = resp.json()
            
            tunnels = data.get('tunnels', [])
            if tunnels:
                tunnel = tunnels[0]
                public_url = tunnel['public_url']
                parsed = self._parse_ngrok_url(public_url)
                
                return {
                    'public_url': public_url,
                    'host': parsed['host'],
                    'port': parsed['port'],
                    'local_port': self.local_port,
                    'full_address': f"{parsed['host']}:{parsed['port']}",
                    'connections': tunnel.get('metrics', {}).get('conns', {}).get('count', 0),
                    'rate': tunnel.get('metrics', {}).get('rate', {})
                }
        except:
            pass
        
        # Fallback to stored URL
        if self.public_url:
            parsed = self._parse_ngrok_url(self.public_url)
            return {
                'public_url': self.public_url,
                'host': parsed['host'],
                'port': parsed['port'],
                'local_port': self.local_port,
                'full_address': f"{parsed['host']}:{parsed['port']}"
            }
        
        return None
    
    def stop_tunnel(self):
        """Stop active tunnel"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                except:
                    pass
            self.process = None
            self.public_url = None
            self.log("[■] Ngrok tunnel stopped")
    
    def is_running(self):
        """Check if tunnel is running"""
        return self.process is not None and self.process.poll() is None

# ==================== PORT FORWARDER ====================
class PortForwarder:
    """Simple TCP Port Forwarder as backup"""
    
    def __init__(self, log_callback=None):
        self.log = log_callback or print
        self.rules = []
        self.running = False
    
    def add_forward(self, local_port: int, remote_host: str, remote_port: int):
        """Add port forwarding rule"""
        self.rules.append({
            'local_port': local_port,
            'remote_host': remote_host,
            'remote_port': remote_port,
            'thread': None
        })
    
    def start_forwarding(self, local_port: int, remote_host: str, remote_port: int):
        """Start forwarding traffic"""
        def forward():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                server.bind(('0.0.0.0', local_port))
                server.listen(50)
                self.log(f"[+] Forwarding: 0.0.0.0:{local_port} -> {remote_host}:{remote_port}")
                
                server.settimeout(1.0)
                
                while self.running:
                    try:
                        client, addr = server.accept()
                        threading.Thread(
                            target=self._handle_connection,
                            args=(client, addr, remote_host, remote_port),
                            daemon=True
                        ).start()
                    except socket.timeout:
                        continue
                    except:
                        break
            except Exception as e:
                self.log(f"[!] Forward error: {e}")
            finally:
                server.close()
        
        self.running = True
        thread = threading.Thread(target=forward, daemon=True)
        thread.start()
        self.log(f"[+] Forward started: :{local_port} -> {remote_host}:{remote_port}")
        return thread
    
    def _handle_connection(self, client, addr, remote_host, remote_port):
        """Handle individual connection"""
        remote = None
        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((remote_host, remote_port))
            
            def pipe(src, dst):
                try:
                    while True:
                        data = src.recv(8192)
                        if not data:
                            break
                        dst.send(data)
                except:
                    pass
            
            t1 = threading.Thread(target=pipe, args=(client, remote), daemon=True)
            t2 = threading.Thread(target=pipe, args=(remote, client), daemon=True)
            t1.start()
            t2.start()
            t1.join(timeout=300)
            t2.join(timeout=300)
            
        except Exception as e:
            self.log(f"[!] Connection error: {e}")
        finally:
            if remote:
                try: remote.close()
                except: pass
            try: client.close()
            except: pass
    
    def stop_all(self):
        """Stop all forwarding"""
        self.running = False

# ==================== MAIN GUI ====================
class NgrokRDPExposer:
    """Main GUI for Ngrok RDP Exposure"""
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("💀 NGROK RDP EXPOSER PRO")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Initialize managers
        self.ngrok = NgrokManager(log_callback=self.log)
        self.forwarder = PortForwarder(log_callback=self.log)
        
        # State
        self.tunnel_active = False
        self.tunnel_info = None
        
        # Setup UI
        self.setup_ui()
        
        # Load saved token
        self.load_saved_token()
        
        self.log("🚀 Ngrok RDP Exposer Pro Ready!")
        self.log(f"👑 Owner: @UnknownGuy9876 | Channel: @SGCodexs")
    
    def setup_ui(self):
        """Setup the complete UI"""
        # Header
        header = ctk.CTkFrame(self.root, height=60)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header,
            text="💀 NGROK RDP AUTO EXPOSER 💀",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ff1744"
        ).pack(pady=10)
        
        # Main content
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # ===== AUTH TOKEN SECTION =====
        token_frame = ctk.CTkFrame(main_frame)
        token_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            token_frame,
            text="🔑 NGROK AUTH TOKEN",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            token_frame,
            text="Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken",
            font=ctk.CTkFont(size=10),
            text_color="#888"
        ).pack()
        
        token_input_frame = ctk.CTkFrame(token_frame, fg_color="transparent")
        token_input_frame.pack(fill="x", padx=10, pady=5)
        
        self.token_entry = ctk.CTkEntry(
            token_input_frame,
            placeholder_text="Paste your ngrok authtoken here...",
            width=500,
            show="•"
        )
        self.token_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(
            token_input_frame,
            text="💾 SAVE TOKEN",
            command=self.save_token,
            fg_color="#2979ff",
            hover_color="#1565c0",
            width=120
        ).pack(side="right", padx=5)
        
        self.token_status = ctk.CTkLabel(
            token_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#ffaa00"
        )
        self.token_status.pack(pady=2)
        
        # ===== RDP CONFIG SECTION =====
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="⚙️ RDP CONFIGURATION",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        # Local port
        port_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        port_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(port_frame, text="Local RDP Port:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=5)
        self.local_port_entry = ctk.CTkEntry(port_frame, width=100)
        self.local_port_entry.grid(row=0, column=1, padx=5)
        self.local_port_entry.insert(0, "3389")
        
        ctk.CTkLabel(port_frame, text="Remote Host:", font=ctk.CTkFont(size=12)).grid(row=0, column=2, padx=5)
        self.remote_host_entry = ctk.CTkEntry(port_frame, width=200)
        self.remote_host_entry.grid(row=0, column=3, padx=5)
        self.remote_host_entry.insert(0, "localhost")
        
        ctk.CTkLabel(port_frame, text="Remote Port:", font=ctk.CTkFont(size=12)).grid(row=0, column=4, padx=5)
        self.remote_port_entry = ctk.CTkEntry(port_frame, width=80)
        self.remote_port_entry.grid(row=0, column=5, padx=5)
        self.remote_port_entry.insert(0, "3389")
        
        # Region selector
        region_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        region_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(region_frame, text="Ngrok Region:", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        
        self.region_var = ctk.StringVar(value="ap")
        regions = ['ap', 'us', 'eu', 'au', 'sa', 'jp', 'in']
        self.region_menu = ctk.CTkOptionMenu(
            region_frame,
            values=regions,
            variable=self.region_var,
            width=100
        )
        self.region_menu.pack(side="left", padx=5)
        
        ctk.CTkLabel(region_frame, text="ap=Asia | us=US | eu=Europe | in=India", 
                    font=ctk.CTkFont(size=10), text_color="#888").pack(side="left", padx=10)
        
        # ===== CONTROL BUTTONS =====
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="🚀 START NGROK TUNNEL",
            command=self.start_ngrok_tunnel,
            fg_color="#00e676",
            hover_color="#00c853",
            text_color="#000000",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹ STOP TUNNEL",
            command=self.stop_ngrok_tunnel,
            fg_color="#ff1744",
            hover_color="#d50000",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        self.copy_btn = ctk.CTkButton(
            btn_frame,
            text="📋 COPY ADDRESS",
            command=self.copy_address,
            fg_color="#ffaa00",
            hover_color="#ff8f00",
            text_color="#000000",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=5, expand=True, fill="x")
        
        # ===== STATUS / CONNECTION INFO =====
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            status_frame,
            text="📡 CONNECTION STATUS",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        self.status_text = ctk.CTkTextbox(
            status_frame,
            height=80,
            font=("Courier", 12),
            fg_color="#0a0a0a",
            text_color="#00ff00"
        )
        self.status_text.pack(fill="x", padx=10, pady=5)
        self.status_text.insert("1.0", "Waiting fo
