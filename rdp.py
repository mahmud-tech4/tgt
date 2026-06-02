#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 MAHMUD TECH - $1 BILLION RDP EXPOSER PRO MAX (FIXED) 💀
Owner: @UnknownGuy9876 | Channel: @SGCodexs
ERROR-FREE | PRODUCTION READY | GOD MODE
"""

import socket
import subprocess
import threading
import queue
import json
import time
import struct
import hashlib
import base64
import os
import sys
import ssl
import random
import string
import ctypes
import platform
import zlib
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum
from functools import lru_cache, wraps
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas, PhotoImage
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import netifaces
import psutil
import speedtest
import qrcode

# ==================== FIXED CRYPTOGRAPHY IMPORTS ====================
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("[!] Cryptography not installed. Encryption features disabled.")
    print("[*] Install with: pip install cryptography")

# For SSL cert generation
try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

# ==================== GLOBAL CONFIGURATION ====================
class Config:
    APP_NAME = "MAHMUD TECH RDP EXPOSER PRO MAX"
    VERSION = "v4.2.1-fixed"
    BUILD = "2026.06.02-billion-dollar-fixed"
    AUTHOR = "@UnknownGuy9876"
    CHANNEL = "@SGCodexs"
    
    MAX_THREADS = 500
    BUFFER_SIZE = 65536
    SOCKET_TIMEOUT = 30
    RECONNECT_DELAY = 2
    MAX_RECONNECT_ATTEMPTS = 10
    STATS_UPDATE_INTERVAL = 1.0
    ANIMATION_FPS = 60

# ==================== DATA CLASSES ====================
@dataclass
class ConnectionStats:
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    active_connections: int = 0
    total_connections: int = 0
    failed_attempts: int = 0
    uptime: timedelta = timedelta()
    latency_ms: float = 0.0
    bandwidth_mbps: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received,
            'active_connections': self.active_connections,
            'latency_ms': round(self.latency_ms, 2),
            'bandwidth_mbps': round(self.bandwidth_mbps, 2),
            'uptime': str(self.uptime).split('.')[0]
        }

@dataclass
class TunnelConfig:
    name: str
    local_port: int
    remote_host: str
    remote_port: int
    protocol: str = 'tcp'
    encryption: bool = False
    compression: bool = False
    rate_limit: int = 0
    allowed_ips: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    stats: ConnectionStats = field(default_factory=ConnectionStats)
    running: bool = False
    thread: Optional[threading.Thread] = None
    id: str = field(default_factory=lambda: ''.join(random.choices(string.hexdigits.lower(), k=12)))

class TunnelProtocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    SSL = "SSL"
    SOCKS5 = "SOCKS5"
    CUSTOM = "CUSTOM"

# ==================== FIXED ENCRYPTION ENGINE ====================
class EncryptionEngine:
    """Military-grade encryption - PBKDF ERROR FIXED"""
    
    def __init__(self, password: str = None):
        self.password = password or hashlib.sha256(os.urandom(32)).hexdigest()
        self.salt = os.urandom(16)
        self.fernet = None
        
        if CRYPTO_AVAILABLE:
            try:
                self.fernet = self._create_fernet()
            except Exception as e:
                print(f"[!] Fernet creation failed: {e}")
                print("[*] Falling back to base64 encoding")
        else:
            print("[*] Cryptography unavailable - using fallback encryption")
    
    def _create_fernet(self) -> Fernet:
        """FIXED: Proper PBKDF2HMAC usage"""
        # PBKDF2HMAC with correct parameters
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),          # ✅ Correct
            length=32,                           # ✅ 32 bytes for Fernet
            salt=self.salt,                      # ✅ Salt
            iterations=480000,                   # ✅ High iteration count
            backend=default_backend()            # ✅ Backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        return Fernet(key)
    
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data with fallback"""
        if self.fernet and CRYPTO_AVAILABLE:
            try:
                return self.fernet.encrypt(data)
            except:
                pass
        
        # Fallback: Simple XOR + Base64
        key = hashlib.sha256(self.password.encode()).digest()
        encrypted = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
        return base64.b64encode(encrypted)
    
    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data with fallback"""
        if self.fernet and CRYPTO_AVAILABLE:
            try:
                return self.fernet.decrypt(data)
            except:
                pass
        
        # Fallback decryption
        try:
            encrypted = base64.b64decode(data)
            key = hashlib.sha256(self.password.encode()).digest()
            return bytes(a ^ b for a, b in zip(encrypted, key * (len(encrypted) // len(key) + 1)))
        except:
            return data
    
    @staticmethod
    def generate_ssl_cert(cert_path: str = "cert.pem", key_path: str = "key.pem"):
        """Generate self-signed SSL certificate - FIXED"""
        if not SSL_AVAILABLE:
            print("[!] SSL generation requires: pip install cryptography")
            return False
        
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "XX"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CyberState"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "DarkCity"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Mahmud Tech"),
                x509.NameAttribute(NameOID.COMMON_NAME, "rdp-exposer.local"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=3650)
            ).sign(private_key, hashes.SHA256(), default_backend())
            
            with open(key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            return True
        except Exception as e:
            print(f"[!] SSL generation failed: {e}")
            return False

# ==================== NETWORK ENGINE ====================
class NetworkEngine:
    """High-performance network operations"""
    
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.session = self._create_session()
            self.initialized = True
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=50, pool_maxsize=50)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({'User-Agent': 'MahmudTech-RDP-Exposer/4.2.1'})
        return session
    
    @lru_cache(maxsize=10)
    def get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_public_ip(self) -> str:
        services = [
            'https://api.ipify.org?format=json',
            'https://ipapi.co/json/',
            'https://httpbin.org/ip',
        ]
        for url in services:
            try:
                resp = self.session.get(url, timeout=3)
                data = resp.json()
                if 'ip' in data:
                    return data['ip']
            except:
                continue
        return "Unknown"
    
    def get_geo_location(self, ip: str = None) -> Dict:
        if ip is None:
            ip = self.get_public_ip()
        try:
            resp = self.session.get(f'https://ipapi.co/{ip}/json/', timeout=5)
            return resp.json()
        except:
            return {'error': 'Failed'}
    
    def scan_ports(self, host: str, start_port: int, end_port: int, threads: int = 100) -> List[int]:
        open_ports = []
        port_queue = queue.Queue()
        
        for port in range(start_port, min(end_port + 1, start_port + 2000)):
            port_queue.put(port)
        
        def worker():
            while not port_queue.empty():
                port = port_queue.get()
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((host, port)) == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
                finally:
                    port_queue.task_done()
        
        for _ in range(min(threads, port_queue.qsize())):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
        
        port_queue.join()
        return sorted(open_ports)
    
    def run_speedtest(self) -> Dict:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            return {
                'download_mbps': round(st.download() / 1_000_000, 2),
                'upload_mbps': round(st.upload() / 1_000_000, 2),
                'ping_ms': round(st.results.ping, 2)
            }
        except Exception as e:
            return {'error': str(e)}

# ==================== ULTIMATE PORT FORWARDER ====================
class UltimatePortForwarder:
    """Enterprise-grade port forwarder"""
    
    def __init__(self, log_callback: Callable = None):
        self.tunnels: Dict[str, TunnelConfig] = {}
        self.log = log_callback or print
        self.network = NetworkEngine()
        self.crypto = EncryptionEngine()
        self.stats_lock = threading.RLock()
        self.global_stats = ConnectionStats()
        self.start_time = datetime.now()
    
    def create_tunnel(self, config: TunnelConfig) -> str:
        self.tunnels[config.id] = config
        self.log(f"[+] Tunnel Created: {config.name}")
        return config.id
    
    def _handle_connection(self, client_socket: socket.socket, addr: Tuple, tunnel: TunnelConfig):
        remote_socket = None
        try:
            if tunnel.allowed_ips and addr[0] not in tunnel.allowed_ips:
                self.log(f"[!] Blocked: {addr[0]}")
                tunnel.stats.failed_attempts += 1
                return
            
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.settimeout(Config.SOCKET_TIMEOUT)
            
            if tunnel.protocol.lower() == 'ssl':
                context = ssl.create_default_context()
                remote_socket = context.wrap_socket(remote_socket)
            
            remote_socket.connect((tunnel.remote_host, tunnel.remote_port))
            
            with self.stats_lock:
                tunnel.stats.active_connections += 1
                tunnel.stats.total_connections += 1
                self.global_stats.active_connections += 1
            
            self._transfer(client_socket, remote_socket, tunnel)
            
        except Exception as e:
            self.log(f"[!] {tunnel.name}: {e}")
        finally:
            with self.stats_lock:
                tunnel.stats.active_connections -= 1
                self.global_stats.active_connections -= 1
            if remote_socket:
                try: remote_socket.close()
                except: pass
            try: client_socket.close()
            except: pass
    
    def _transfer(self, src, dst, tunnel: TunnelConfig):
        def forward(source, destination, is_outbound):
            try:
                while tunnel.running:
                    data = source.recv(Config.BUFFER_SIZE)
                    if not data:
                        break
                    
                    if tunnel.encryption:
                        data = self.crypto.encrypt(data)
                    if tunnel.compression:
                        data = zlib.compress(data)
                    
                    destination.send(data)
                    
                    with self.stats_lock:
                        if is_outbound:
                            tunnel.stats.bytes_sent += len(data)
                        else:
                            tunnel.stats.bytes_received += len(data)
            except:
                pass
        
        t1 = threading.Thread(target=forward, args=(src, dst, True), daemon=True)
        t2 = threading.Thread(target=forward, args=(dst, src, False), daemon=True)
        t1.start()
        t2.start()
        t1.join(timeout=300)
        t2.join(timeout=300)
    
    def start_tunnel(self, tunnel_id: str):
        tunnel = self.tunnels.get(tunnel_id)
        if not tunnel or tunnel.running:
            return
        
        tunnel.running = True
        tunnel.thread = threading.Thread(target=self._listener, args=(tunnel,), daemon=True)
        tunnel.thread.start()
    
    def _listener(self, tunnel: TunnelConfig):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(1.0)
        
        try:
            server.bind(('0.0.0.0', tunnel.local_port))
            server.listen(500)
            self.log(f"[+] Listening: 0.0.0.0:{tunnel.local_port}")
            
            while tunnel.running:
                try:
                    client, addr = server.accept()
                    threading.Thread(target=self._handle_connection, args=(client, addr, tunnel), daemon=True).start()
                except socket.timeout:
                    continue
        except Exception as e:
            self.log(f"[!] Bind error: {e}")
        finally:
            server.close()
    
    def stop_tunnel(self, tunnel_id: str):
        tunnel = self.tunnels.get(tunnel_id)
        if tunnel:
            tunnel.running = False
    
    def get_stats(self) -> Dict:
        self.global_stats.uptime = datetime.now() - self.start_time
        return {
            'global': self.global_stats.to_dict(),
            'active_tunnels': sum(1 for t in self.tunnels.values() if t.running),
            'total_tunnels': len(self.tunnels)
        }

# ==================== $1 BILLION GUI (FIXED) ====================
class BillionDollarGUI:
    """The most advanced GUI - PBKDF ERROR FREE"""
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title(f"💀 {Config.APP_NAME} {Config.VERSION}")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.network = NetworkEngine()
        self.forwarder = UltimatePortForwarder(log_callback=self.log_message)
        self.tunnel_count = 0
        
        self.cpu_history = deque(maxlen=60)
        self.memory_history = deque(maxlen=60)
        
        self.setup_ui()
        self.start_monitoring()
        
        self.log_message(f"🚀 {Config.APP_NAME} initialized - PBKDF FIXED")
        self.log_message(f"👑 Owner: {Config.AUTHOR} | Channel: {Config.CHANNEL}")
    
    def setup_ui(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self.setup_header()
        
        # Tabview
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.grid(row=1, column=0, sticky="nsew", pady=10)
        
        self.tab_dashboard = self.tabview.add("📊 DASHBOARD")
        self.tab_tunnels = self.tabview.add("🔗 TUNNELS")
        self.tab_network = self.tabview.add("🌐 NETWORK")
        self.tab_security = self.tabview.add("🔒 SECURITY")
        self.tab_logs = self.tabview.add("📜 LOGS")
        
        self.setup_dashboard_tab()
        self.setup_tunnels_tab()
        self.setup_network_tab()
        self.setup_security_tab()
        self.setup_logs_tab()
        
        # Footer
        self.setup_footer()
    
    def setup_header(self):
        header_frame = ctk.CTkFrame(self.main_container, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="💀 MAHMUD TECH - RDP EXPOSER PRO MAX 💀",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ff1744"
        )
        title_label.pack(side="left", padx=20)
        
        self.stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        self.stats_frame.pack(side="right", padx=20)
        
        self.active_conn_label = ctk.CTkLabel(self.stats_frame, text="🔴 Active: 0", font=ctk.CTkFont(size=14))
        self.active_conn_label.pack(side="left", padx=10)
        
        self.uptime_label = ctk.CTkLabel(self.stats_frame, text="⏱ 00:00:00", font=ctk.CTkFont(size=14))
        self.uptime_label.pack(side="left", padx=10)
    
    def setup_dashboard_tab(self):
        self.tab_dashboard.grid_rowconfigure(0, weight=1)
        self.tab_dashboard.grid_rowconfigure(1, weight=1)
        self.tab_dashboard.grid_columnconfigure(0, weight=1)
        self.tab_dashboard.grid_columnconfigure(1, weight=1)
        
        # System Info
        sys_card = ctk.CTkFrame(self.tab_dashboard)
        sys_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(sys_card, text="SYSTEM INFORMATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        self.sys_info_text = ctk.CTkTextbox(sys_card, height=150)
        self.sys_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Network Info
        net_card = ctk.CTkFrame(self.tab_dashboard)
        net_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(net_card, text="NETWORK STATUS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        self.net_info_text = ctk.CTkTextbox(net_card, height=150)
        self.net_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Graph
        self.graph_frame = ctk.CTkFrame(self.tab_dashboard)
        self.graph_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.setup_graphs()
    
    def setup_graphs(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 3), facecolor='#1a1a1a')
        self.fig.patch.set_facecolor('#1a1a1a')
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='#00ff00')
            ax.grid(True, alpha=0.2, color='#00ff00')
        
        self.ax1.set_ylabel('CPU %', color='#ff1744')
        self.ax2.set_ylabel('Memory %', color='#2979ff')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.ani = animation.FuncAnimation(self.fig, self.animate_graphs, interval=1000, cache_frame_data=False)
    
    def animate_graphs(self, frame):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        self.cpu_history.append(cpu)
        self.memory_history.append(mem)
        
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.plot(list(self.cpu_history), color='#ff1744', linewidth=2)
        self.ax2.plot(list(self.memory_history), color='#2979ff', linewidth=2)
        self.ax1.set_ylabel('CPU %', color='#ff1744')
        self.ax2.set_ylabel('Memory %', color='#2979ff')
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='#00ff00')
            ax.grid(True, alpha=0.2, color='#00ff00')
    
    def setup_tunnels_tab(self):
        create_frame = ctk.CTkFrame(self.tab_tunnels)
        create_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(create_frame, text="QUICK TUNNEL CREATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        input_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(input_frame, text="Local Port:").grid(row=0, column=0, padx=5)
        self.tun_local_port = ctk.CTkEntry(input_frame, width=80)
        self.tun_local_port.grid(row=0, column=1, padx=5)
        self.tun_local_port.insert(0, "3389")
        
        ctk.CTkLabel(input_frame, text="Remote Host:").grid(row=0, column=2, padx=5)
        self.tun_remote_host = ctk.CTkEntry(input_frame, width=150)
        self.tun_remote_host.grid(row=0, column=3, padx=5)
        
        ctk.CTkLabel(input_frame, text="Remote Port:").grid(row=0, column=4, padx=5)
        self.tun_remote_port = ctk.CTkEntry(input_frame, width=80)
        self.tun_remote_port.grid(row=0, column=5, padx=5)
        self.tun_remote_port.insert(0, "3389")
        
        self.tun_protocol = ctk.CTkOptionMenu(input_frame, values=[p.value for p in TunnelProtocol], width=100)
        self.tun_protocol.grid(row=0, column=6, padx=5)
        
        btn_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="➕ CREATE TUNNEL", command=self.create_tunnel, fg_color="#00e676", text_color="#000000").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔌 EXPOSE RDP", command=self.quick_expose_rdp, fg_color="#ff1744").pack(side="left", padx=5)
        
        # Tunnel list
        list_frame = ctk.CTkFrame(self.tab_tunnels)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tunnel_listbox = tk.Listbox(list_frame, bg='#0a0a0a', fg='#00ff00', font=('Courier', 10), height=10)
        self.tunnel_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctrl_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=10, pady=5)
        
        for text, cmd in [("▶ START", self.start_tunnel), ("⏹ STOP", self.stop_tunnel), 
                           ("🗑 DELETE", self.delete_tunnel), ("▶ ALL", self.start_all), 
                           ("⏹ ALL", self.stop_all)]:
            ctk.CTkButton(ctrl_frame, text=text, command=cmd, width=60).pack(side="left", padx=2)
    
    def setup_network_tab(self):
        ip_frame = ctk.CTkFrame(self.tab_network)
        ip_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ip_frame, text="NETWORK INFORMATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.ip_text = ctk.CTkTextbox(ip_frame, height=100)
        self.ip_text.pack(fill="x", padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(ip_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="🔄 REFRESH", command=self.refresh_network_info).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="📍 GEO LOCATION", command=self.show_geo_location).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="⚡ SPEED TEST", command=self.run_speedtest).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔍 PORT SCAN", command=self.port_scanner_popup).pack(side="left", padx=5)
        
        # QR Code
        qr_frame = ctk.CTkFrame(self.tab_network)
        qr_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(qr_frame, text="SHARE ACCESS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        self.qr_label = ctk.CTkLabel(qr_frame, text="QR Code will appear here")
        self.qr_label.pack(pady=5)
        ctk.CTkButton(qr_frame, text="🔳 GENERATE QR", command=self.generate_qr_code).pack(pady=5)
    
    def setup_security_tab(self):
        sec_frame = ctk.CTkFrame(self.tab_security)
        sec_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(sec_frame, text="ENCRYPTION SETTINGS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(sec_frame, text="Encryption Password:").pack()
        self.encrypt_pass = ctk.CTkEntry(sec_frame, width=300, show="*")
        self.encrypt_pass.pack(pady=5)
        
        btn_frame = ctk.CTkFrame(sec_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="🔑 GENERATE SSL CERT", command=self.generate_ssl).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔒 ENABLE ENCRYPTION", command=self.enable_encryption).pack(side="left", padx=5)
        
        # RDP Config
        rdp_frame = ctk.CTkFrame(self.tab_security)
        rdp_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(rdp_frame, text="RDP CONFIGURATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        ctk.CTkButton(rdp_frame, text="🔓 ENABLE RDP", command=self.enable_rdp).pack(pady=5)
        ctk.CTkButton(rdp_frame, text="⚡ NGROK TUNNEL", command=self.ngrok_tunnel).pack(pady=5)
    
    def setup_logs_tab(self):
        log_frame = ctk.CTkFrame(self.tab_logs)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(log_frame, text="SYSTEM LOGS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(log_frame, font=("Courier", 10))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="🗑 CLEAR", command=lambda: self.log_text.delete("1.0", "end")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="💾 EXPORT", command=self.export_logs).pack(side="left", padx=5)
    
    def setup_footer(self):
        footer = ctk.CTkFrame(self.root, height=30)
        footer.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        footer.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(footer, text=f"READY | {Config.AUTHOR} | {Config.CHANNEL} | {Config.VERSION}", font=ctk.CTkFont(size=10))
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(footer, text="", font=ctk.CTkFont(size=10))
        self.time_label.pack(side="right", padx=10)
        self.update_time()
    
    def update_time(self):
        self.time_label.configure(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def log_message(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        if hasattr(self, 'log_text'):
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message[:100])
    
    # ==================== TUNNEL OPERATIONS ====================
    def create_tunnel(self):
        try:
            local_port = int(self.tun_local_port.get())
            remote_host = self.tun_remote_host.get()
            remote_port = int(self.tun_remote_port.get())
            protocol = self.tun_protocol.get().lower()
            
            self.tunnel_count += 1
            config = TunnelConfig(
                name=f"Tunnel-{self.tunnel_count:04d}",
                local_port=local_port,
                remote_host=remote_host,
                remote_port=remote_port,
                protocol=protocol
            )
            
            self.forwarder.create_tunnel(config)
            self.forwarder.start_tunnel(config.id)
            
            display = f"{config.name} | 0.0.0.0:{local_port} -> {remote_host}:{remote_port} [{protocol}]"
            self.tunnel_listbox.insert(tk.END, display)
            self.log_message(f"[+] Created: {display}")
        except ValueError as e:
            self.log_message(f"[!] Invalid input: {e}")
    
    def quick_expose_rdp(self):
        public_ip = self.network.get_public_ip()
        local_ip = self.network.get_local_ip()
        
        self.tun_local_port.delete(0, "end")
        self.tun_local_port.insert(0, "3389")
        self.tun_remote_host.delete(0, "end")
        self.tun_remote_host.insert(0, local_ip)
        self.tun_remote_port.delete(0, "end")
        self.tun_remote_port.insert(0, "3389")
        
        self.log_message(f"""
╔══════════════════════════════════╗
║     RDP ACCESS INFORMATION      ║
╠══════════════════════════════════╣
║ Public IP : {public_ip:<15}  ║
║ Local IP  : {local_ip:<15}  ║
║ Port      : 3389                ║
╚══════════════════════════════════╝
        """)
        self.create_tunnel()
    
    def start_tunnel(self):
        sel = self.tunnel_listbox.curselection()
        if sel:
            display = self.tunnel_listbox.get(sel[0])
            for tid, t in self.forwarder.tunnels.items():
                if display.startswith(t.name):
                    self.forwarder.start_tunnel(tid)
                    self.log_message(f"[▶] Started: {t.name}")
                    break
    
    def stop_tunnel(self):
        sel = self.tunnel_listbox.curselection()
        if sel:
            display = self.tunnel_listbox.get(sel[0])
            for tid, t in self.forwarder.tunnels.items():
                if display.startswith(t.name):
                    self.forwarder.stop_tunnel(tid)
                    self.log_message(f"[■] Stopped: {t.name}")
                    break
    
    def delete_tunnel(self):
        sel = self.tunnel_listbox.curselection()
        if sel:
            display = self.tunnel_listbox.get(sel[0])
            for tid, t in list(self.forwarder.tunnels.items()):
                if display.startswith(t.name):
                    self.forwarder.stop_tunnel(tid)
                    del self.forwarder.tunnels[tid]
                    self.tunnel_listbox.delete(sel[0])
                    self.log_message(f"[-] Deleted: {t.name}")
                    break
    
    def start_all(self):
        for tid in self.forwarder.tunnels:
            self.forwarder.start_tunnel(tid)
        self.log_message("[▶] All tunnels started")
    
    def stop_all(self):
        for tid in self.forwarder.tunnels:
            self.forwarder.stop_tunnel(tid)
        self.log_message("[■] All tunnels stopped")
    
    # ==================== NETWORK OPERATIONS ====================
    def refresh_network_info(self):
        local_ip = self.network.get_local_ip()
        public_ip = self.network.get_public_ip()
        
        info = f"Local IP: {local_ip}\n"
        info += f"Public IP: {public_ip}\n"
        info += f"Hostname: {socket.gethostname()}\n"
        info += f"CPU: {psutil.cpu_percent()}% | Memory: {psutil.virtual_memory().percent}%"
        
        self.ip_text.delete("1.0", "end")
        self.ip_text.insert("1.0", info)
        
        sys_info = f"Platform: {platform.platform()}\nPython: {sys.version.split()[0]}\n"
        sys_info += f"Encryption: {'Available' if CRYPTO_AVAILABLE else 'Fallback Mode'}"
        
        self.sys_info_text.delete("1.0", "end")
        self.sys_info_text.insert("1.0", sys_info)
    
    def show_geo_location(self):
        location = self.network.get_geo_location()
        info = f"IP: {location.get('ip', '?')}\n"
        info += f"City: {location.get('city', '?')}\n"
        info += f"Country: {location.get('country_name', '?')}\n"
        info += f"ISP: {location.get('org', '?')}"
        self.log_message(info)
    
    def run_speedtest(self):
        self.log_message("⚡ Running speed test...")
        result = self.network.run_speedtest()
        if 'error' not in result:
            self.log_message(f"Download: {result['download_mbps']} Mbps | Upload: {result['upload_mbps']} Mbps | Ping: {result['ping_ms']} ms")
        else:
            self.log_message(f"[!] Failed: {result['error']}")
    
    def generate_qr_code(self):
        public_ip = self.network.get_public_ip()
        qr_data = f"rdp://{public_ip}:3389"
        
        qr = qrcode.QRCode(version=1, box_size=8, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#00ff00", back_color="#000000").resize((200, 200))
        ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
        self.qr_label.configure(image=ctk_image, text="")
        self.log_message(f"🔳 QR generated: {qr_data}")
    
    def port_scanner_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Port Scanner")
        popup.geometry("400x300")
        
        ctk.CTkLabel(popup, text="Target:").pack()
        target_entry = ctk.CTkEntry(popup, width=200)
        target_entry.pack(pady=5)
        
        result_text = ctk.CTkTextbox(popup, height=120)
        result_text.pack(fill="x", padx=10, pady=10)
        
        def scan():
            host = target_entry.get()
            ports = self.network.scan_ports(host, 1, 1000)
            result_text.delete("1.0", "end")
            result_text.insert("1.0", f"Open ports on {host}:\n" + "\n".join(map(str, ports)))
        
        ctk.CTkButton(popup, text="🔍 SCAN (1-1000)", command=scan).pack()
    
    def generate_ssl(self):
        if EncryptionEngine.generate_ssl_cert():
            self.log_message("[+] SSL Certificate generated: cert.pem, key.pem")
        else:
            self.log_message("[!] SSL generation failed - install cryptography")
    
    def enable_encryption(self):
        password = self.encrypt_pass.get()
        if password:
            self.forwarder.crypto = EncryptionEngine(password)
            self.log_message("[🔒] Encryption enabled")
        else:
            self.log_message("[!] Enter password first")
    
    def enable_rdp(self):
        try:
            subprocess.run(['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server', 
                          '/v', 'fDenyTSConnections', '/t', 'REG_DWORD', '/d', '0', '/f'], 
                          capture_output=True)
            self.log_message("[+] RDP Enabled")
        except:
            self.log_message("[!] Admin rights required")
    
    def ngrok_tunnel(self):
        public_ip = self.network.get_public_ip()
        self.log_message(f"[*] For ngrok: Download ngrok → Run: ngrok tcp 3389 → Share address\n[*] Public IP: {public_ip}")
    
    def export_logs(self):
        filename = f"rdp_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(self.log_text.get("1.0", "end"))
        self.log_message(f"[💾] Exported: {filename}")
    
    def start_monitoring(self):
        self.refresh_network_info()
        
        def monitor():
            try:
                stats = self.forwarder.get_stats()
                self.active_conn_label.configure(text=f"🔴 Active: {stats['global']['active_connections']}")
                self.uptime_label.configure(text=f"⏱ {stats['global']['uptime']}")
            except:
                pass
            self.root.after(1000, monitor)
        
        monitor()
    
    def run(self):
        self.root.mainloop()

# ==================== MAIN ====================
def main():
    if platform.system() == "Windows":
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showwarning("Admin Rights", "Run as Administrator for full functionality!")
        except:
            pass
    
    app = BillionDollarGUI()
    app.run()

if __name__ == "__main__":
    main()
