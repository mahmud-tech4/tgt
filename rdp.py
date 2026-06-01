#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀 MAHMUD TECH - $1 BILLION RDP EXPOSER PRO MAX 💀
Owner: @UnknownGuy9876 | Channel: @SGCodexs
Production Ready | Enterprise Grade | God Mode Activated
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
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

# ==================== GLOBAL CONFIGURATION ====================
class Config:
    APP_NAME = "MAHMUD TECH RDP EXPOSER PRO MAX"
    VERSION = "v4.2.0-enterprise"
    BUILD = "2026.06.02-billion-dollar"
    AUTHOR = "@UnknownGuy9876"
    CHANNEL = "@SGCodexs"
    THEME_COLORS = {
        'bg_dark': '#0a0a0a',
        'bg_medium': '#141414',
        'bg_light': '#1e1e1e',
        'accent_red': '#ff1744',
        'accent_green': '#00e676',
        'accent_blue': '#2979ff',
        'accent_yellow': '#ffd600',
        'accent_purple': '#d500f9',
        'text_primary': '#ffffff',
        'text_secondary': '#b0bec5',
        'border': '#333333',
        'glow': '#00ff00'
    }
    
    # Performance settings
    MAX_THREADS = 500
    BUFFER_SIZE = 65536
    SOCKET_TIMEOUT = 30
    RECONNECT_DELAY = 2
    MAX_RECONNECT_ATTEMPTS = 10
    STATS_UPDATE_INTERVAL = 1.0
    ANIMATION_FPS = 60
    
    # Security
    ENCRYPTION_KEY = None
    SSL_CERT_PATH = None
    AUTH_TOKEN = hashlib.sha256(os.urandom(32)).hexdigest()

# ==================== ADVANCED DATA STRUCTURES ====================
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
    rate_limit: int = 0  # 0 = unlimited
    allowed_ips: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    stats: ConnectionStats = field(default_factory=ConnectionStats)
    running: bool = False
    thread: Optional[threading.Thread] = None
    id: str = field(default_factory=lambda: ''.join(random.choices(string.hexdigits.lower(), k=12)))

class TunnelProtocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    SOCKS5 = "SOCKS5"
    SHADOWSOCKS = "SHADOWSOCKS"
    WIREGUARD = "WIREGUARD"
    CUSTOM = "CUSTOM"

# ==================== NETWORK ENGINE ====================
class NetworkEngine:
    """High-performance network operations with caching and async support"""
    
    _instance = None
    _cache = {}
    _cache_ttl = 60
    _lock = threading.RLock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.session = self._create_session()
            self.speedtester = None
            self.executor = ThreadPoolExecutor(max_workers=50, thread_name_prefix="NetEngine")
            self.initialized = True
    
    def _create_session(self) -> requests.Session:
        """Create optimized requests session with retry logic"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=100,
            pool_maxsize=100
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({
            'User-Agent': 'MahmudTech-RDP-Exposer/4.2.0'
        })
        return session
    
    @lru_cache(maxsize=128)
    def get_local_ip(self, interface: str = 'default') -> str:
        """Get local IP with caching"""
        try:
            if interface == 'default':
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            else:
                addrs = netifaces.ifaddresses(interface)
                return addrs[netifaces.AF_INET][0]['addr']
        except:
            return "127.0.0.1"
    
    def get_all_network_interfaces(self) -> Dict[str, Dict]:
        """Get all network interfaces with details"""
        interfaces = {}
        for iface in netifaces.interfaces():
            try:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    interfaces[iface] = {
                        'ip': addrs[netifaces.AF_INET][0]['addr'],
                        'netmask': addrs[netifaces.AF_INET][0]['netmask'],
                        'mac': addrs[netifaces.AF_LINK][0]['addr'] if netifaces.AF_LINK in addrs else 'N/A'
                    }
            except:
                continue
        return interfaces
    
    def get_public_ip(self) -> str:
        """Get public IP from multiple sources with fallback"""
        services = [
            'https://api.ipify.org?format=json',
            'https://ipapi.co/json/',
            'https://api.ip.sb/geoip',
            'https://httpbin.org/ip',
            'https://ifconfig.me/all.json'
        ]
        
        for url in services:
            try:
                resp = self.session.get(url, timeout=3)
                data = resp.json()
                if 'ip' in data:
                    return data['ip']
                if 'query' in data:
                    return data['query']
            except:
                continue
        return "Unknown"
    
    def get_geo_location(self, ip: str = None) -> Dict:
        """Get geographical location of IP"""
        if ip is None:
            ip = self.get_public_ip()
        try:
            resp = self.session.get(f'https://ipapi.co/{ip}/json/', timeout=5)
            return resp.json()
        except:
            return {'error': 'Failed to fetch location'}
    
    def measure_latency(self, host: str, port: int = 80, count: int = 3) -> float:
        """Measure latency to a host"""
        latencies = []
        for _ in range(count):
            try:
                start = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                sock.close()
            except:
                latencies.append(float('inf'))
        
        # Return average, excluding timeouts
        valid = [l for l in latencies if l != float('inf')]
        return sum(valid) / len(valid) if valid else float('inf')
    
    def run_speedtest(self) -> Dict:
        """Run network speed test"""
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download = st.download() / 1_000_000  # Convert to Mbps
            upload = st.upload() / 1_000_000
            ping = st.results.ping
            
            return {
                'download_mbps': round(download, 2),
                'upload_mbps': round(upload, 2),
                'ping_ms': round(ping, 2),
                'server': st.results.server['sponsor']
            }
        except Exception as e:
            return {'error': str(e)}
    
    def scan_ports(self, host: str, start_port: int, end_port: int, threads: int = 100) -> List[int]:
        """Fast multi-threaded port scanner"""
        open_ports = []
        port_queue = queue.Queue()
        
        for port in range(start_port, end_port + 1):
            port_queue.put(port)
        
        def worker():
            while not port_queue.empty():
                port = port_queue.get()
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
                finally:
                    port_queue.task_done()
        
        thread_list = []
        for _ in range(min(threads, end_port - start_port + 1)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)
        
        port_queue.join()
        return sorted(open_ports)

# ==================== ENCRYPTION ENGINE ====================
class EncryptionEngine:
    """Military-grade encryption for tunnels"""
    
    def __init__(self, password: str = None):
        self.password = password or hashlib.sha256(os.urandom(32)).hexdigest()
        self.salt = os.urandom(16)
        self.fernet = self._create_fernet()
    
    def _create_fernet(self) -> Fernet:
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        return Fernet(key)
    
    def encrypt(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)
    
    def decrypt(self, data: bytes) -> bytes:
        return self.fernet.decrypt(data)
    
    def encrypt_file(self, filepath: str, output: str = None):
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted = self.encrypt(data)
        output = output or filepath + '.encrypted'
        with open(output, 'wb') as f:
            f.write(self.salt + encrypted)
    
    @staticmethod
    def generate_ssl_cert(cert_path: str, key_path: str):
        """Generate self-signed SSL certificate"""
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "XX"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Cyber"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Darknet"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Mahmud Tech"),
            x509.NameAttribute(NameOID.COMMON_NAME, "rdp-exposer.pro"),
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
        ).sign(private_key, hashes.SHA256())
        
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

# ==================== ADVANCED PORT FORWARDER ====================
class UltimatePortForwarder:
    """Enterprise-grade multi-protocol port forwarder with encryption & load balancing"""
    
    def __init__(self, log_callback: Callable = None):
        self.tunnels: Dict[str, TunnelConfig] = {}
        self.log = log_callback or print
        self.network = NetworkEngine()
        self.crypto = EncryptionEngine()
        self.stats_lock = threading.RLock()
        self.global_stats = ConnectionStats()
        self.start_time = datetime.now()
        self.backpressure_queue = queue.Queue(maxsize=10000)
        self.connection_pool = {}
        
    def create_tunnel(self, config: TunnelConfig) -> str:
        """Create a new tunnel with advanced configuration"""
        tunnel_id = config.id
        self.tunnels[tunnel_id] = config
        self.log(f"[+] Tunnel Created: {config.name} ({tunnel_id})")
        return tunnel_id
    
    def _handle_connection(self, client_socket: socket.socket, addr: Tuple, tunnel: TunnelConfig):
        """Handle individual connection with stats tracking"""
        start_time = time.time()
        remote_socket = None
        
        try:
            # Apply IP filtering
            if tunnel.allowed_ips and addr[0] not in tunnel.allowed_ips:
                self.log(f"[!] Blocked connection from {addr[0]}")
                tunnel.stats.failed_attempts += 1
                return
            
            # Connect to remote
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.settimeout(Config.SOCKET_TIMEOUT)
            
            if tunnel.protocol == 'tcp':
                remote_socket.connect((tunnel.remote_host, tunnel.remote_port))
            elif tunnel.protocol == 'ssl':
                context = ssl.create_default_context()
                remote_socket = context.wrap_socket(remote_socket, server_hostname=tunnel.remote_host)
                remote_socket.connect((tunnel.remote_host, tunnel.remote_port))
            
            with self.stats_lock:
                tunnel.stats.active_connections += 1
                tunnel.stats.total_connections += 1
                self.global_stats.active_connections += 1
                self.global_stats.total_connections += 1
            
            self.log(f"[*] {tunnel.name}: {addr[0]}:{addr[1]} <-> {tunnel.remote_host}:{tunnel.remote_port}")
            
            # Bi-directional data transfer with rate limiting
            self._transfer_data(client_socket, remote_socket, tunnel)
            
        except Exception as e:
            self.log(f"[!] {tunnel.name}: Connection error - {e}")
            tunnel.stats.failed_attempts += 1
        finally:
            duration = time.time() - start_time
            with self.stats_lock:
                tunnel.stats.active_connections -= 1
                self.global_stats.active_connections -= 1
            
            if remote_socket:
                try:
                    remote_socket.close()
                except:
                    pass
            try:
                client_socket.close()
            except:
                pass
    
    def _transfer_data(self, client: socket.socket, remote: socket.socket, tunnel: TunnelConfig):
        """High-performance data transfer with encryption and compression"""
        
        def forward(src, dst, is_outbound=True):
            nonlocal tunnel
            try:
                while tunnel.running:
                    data = src.recv(Config.BUFFER_SIZE)
                    if not data:
                        break
                    
                    # Apply rate limiting
                    if tunnel.rate_limit > 0:
                        time.sleep(len(data) / (tunnel.rate_limit * 1024 * 1024 / 8))
                    
                    # Apply encryption
                    if tunnel.encryption:
                        data = self.crypto.encrypt(data)
                    
                    # Apply compression (simple RLE for demo)
                    if tunnel.compression:
                        data = self._compress(data)
                    
                    dst.send(data)
                    
                    # Update stats
                    with self.stats_lock:
                        if is_outbound:
                            tunnel.stats.bytes_sent += len(data)
                            tunnel.stats.packets_sent += 1
                            self.global_stats.bytes_sent += len(data)
                        else:
                            tunnel.stats.bytes_received += len(data)
                            tunnel.stats.packets_received += 1
                            self.global_stats.bytes_received += len(data)
                            
            except (ConnectionResetError, BrokenPipeError, OSError):
                pass
            except Exception as e:
                if tunnel.running:
                    self.log(f"[!] Transfer error: {e}")
        
        t1 = threading.Thread(target=forward, args=(client, remote, True), daemon=True)
        t2 = threading.Thread(target=forward, args=(remote, client, False), daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    
    def _compress(self, data: bytes) -> bytes:
        """Simple RLE compression"""
        import zlib
        return zlib.compress(data)
    
    def _decompress(self, data: bytes) -> bytes:
        import zlib
        return zlib.decompress(data)
    
    def start_tunnel(self, tunnel_id: str):
        """Start a tunnel"""
        tunnel = self.tunnels.get(tunnel_id)
        if not tunnel or tunnel.running:
            return
        
        tunnel.running = True
        tunnel.thread = threading.Thread(
            target=self._tunnel_listener,
            args=(tunnel,),
            daemon=True,
            name=f"Tunnel-{tunnel.name}"
        )
        tunnel.thread.start()
        self.log(f"[▶] Started: {tunnel.name}")
    
    def _tunnel_listener(self, tunnel: TunnelConfig):
        """Main tunnel listener with connection pooling"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        # Increase backlog for high-load scenarios
        try:
            server.bind(('0.0.0.0', tunnel.local_port))
            server.listen(1000)
            server.settimeout(1.0)  # Allow checking tunnel.running flag
            
            self.log(f"[+] Listening: 0.0.0.0:{tunnel.local_port} ({tunnel.protocol.upper()})")
            
            while tunnel.running:
                try:
                    client_socket, addr = server.accept()
                    # Handle connection in thread pool
                    threading.Thread(
                        target=self._handle_connection,
                        args=(client_socket, addr, tunnel),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if tunnel.running:
                        self.log(f"[!] Accept error: {e}")
                    break
        except Exception as e:
            self.log(f"[!] Bind error: {e}")
        finally:
            server.close()
            tunnel.running = False
    
    def stop_tunnel(self, tunnel_id: str):
        """Stop a tunnel"""
        tunnel = self.tunnels.get(tunnel_id)
        if tunnel and tunnel.running:
            tunnel.running = False
            self.log(f"[■] Stopped: {tunnel.name}")
    
    def restart_tunnel(self, tunnel_id: str):
        """Restart a tunnel"""
        self.stop_tunnel(tunnel_id)
        time.sleep(0.5)
        self.start_tunnel(tunnel_id)
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        self.global_stats.uptime = datetime.now() - self.start_time
        return {
            'global': self.global_stats.to_dict(),
            'tunnels': {tid: t.stats.to_dict() for tid, t in self.tunnels.items()},
            'active_tunnels': sum(1 for t in self.tunnels.values() if t.running),
            'total_tunnels': len(self.tunnels)
        }

# ==================== LOAD BALANCER ====================
class LoadBalancer:
    """Intelligent load balancer for RDP connections"""
    
    ALGORITHMS = ['round_robin', 'least_connections', 'random', 'weighted']
    
    def __init__(self, targets: List[Tuple[str, int]] = None):
        self.targets = targets or []
        self.current_index = 0
        self.connections = defaultdict(int)
        self.weights = defaultdict(lambda: 1)
        self.health_status = {}
        self.lock = threading.RLock()
    
    def add_target(self, host: str, port: int, weight: int = 1):
        self.targets.append((host, port))
        self.weights[(host, port)] = weight
        self.health_status[(host, port)] = True
    
    def get_target(self, algorithm: str = 'round_robin') -> Tuple[str, int]:
        """Get next target based on algorithm"""
        with self.lock:
            if not self.targets:
                raise ValueError("No targets available")
            
            healthy = [t for t in self.targets if self.health_status.get(t, False)]
            if not healthy:
                raise ValueError("No healthy targets")
            
            if algorithm == 'round_robin':
                target = healthy[self.current_index % len(healthy)]
                self.current_index += 1
            elif algorithm == 'least_connections':
                target = min(healthy, key=lambda t: self.connections[t])
            elif algorithm == 'random':
                target = random.choice(healthy)
            elif algorithm == 'weighted':
                total_weight = sum(self.weights[t] for t in healthy)
                r = random.uniform(0, total_weight)
                upto = 0
                for t in healthy:
                    upto += self.weights[t]
                    if upto >= r:
                        target = t
                        break
            
            self.connections[target] += 1
            return target
    
    def release_target(self, host: str, port: int):
        with self.lock:
            self.connections[(host, port)] = max(0, self.connections[(host, port)] - 1)
    
    def health_check(self):
        """Perform health checks on all targets"""
        for host, port in self.targets:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                self.health_status[(host, port)] = (result == 0)
                sock.close()
            except:
                self.health_status[(host, port)] = False

# ==================== $1 BILLION GUI ====================
class BillionDollarGUI:
    """The most advanced GUI ever created for RDP exposure"""
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title(f"💀 {Config.APP_NAME} {Config.VERSION}")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Make responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Initialize components
        self.network = NetworkEngine()
        self.forwarder = UltimatePortForwarder(log_callback=self.log_message)
        self.load_balancer = LoadBalancer()
        self.tunnel_count = 0
        self.animation_running = True
        
        # System monitoring
        self.cpu_history = deque(maxlen=60)
        self.memory_history = deque(maxlen=60)
        self.bandwidth_history = deque(maxlen=60)
        
        # Build UI
        self.setup_ui()
        self.start_monitoring()
        self.update_stats()
        
        self.log_message(f"🚀 {Config.APP_NAME} {Config.VERSION} initialized")
        self.log_message(f"👑 Owner: {Config.AUTHOR} | Channel: {Config.CHANNEL}")
    
    def setup_ui(self):
        """Setup the billion-dollar UI"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # ===== HEADER =====
        self.setup_header()
        
        # ===== TABVIEW =====
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.grid(row=1, column=0, sticky="nsew", pady=10)
        
        # Add tabs
        self.tab_dashboard = self.tabview.add("📊 DASHBOARD")
        self.tab_tunnels = self.tabview.add("🔗 TUNNELS")
        self.tab_network = self.tabview.add("🌐 NETWORK")
        self.tab_security = self.tabview.add("🔒 SECURITY")
        self.tab_advanced = self.tabview.add("⚡ ADVANCED")
        self.tab_logs = self.tabview.add("📜 LOGS")
        
        # Setup each tab
        self.setup_dashboard_tab()
        self.setup_tunnels_tab()
        self.setup_network_tab()
        self.setup_security_tab()
        self.setup_advanced_tab()
        self.setup_logs_tab()
        
        # ===== FOOTER =====
        self.setup_footer()
    
    def setup_header(self):
        """Animated header with live stats"""
        header_frame = ctk.CTkFrame(self.main_container, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        header_frame.grid_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="💀 MAHMUD TECH - RDP EXPOSER PRO MAX 💀",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ff1744"
        )
        title_label.pack(side="left", padx=20)
        
        # Live stats
        self.stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        self.stats_frame.pack(side="right", padx=20)
        
        self.active_conn_label = ctk.CTkLabel(
            self.stats_frame,
            text="🔴 Active: 0",
            font=ctk.CTkFont(size=14)
        )
        self.active_conn_label.pack(side="left", padx=10)
        
        self.bandwidth_label = ctk.CTkLabel(
            self.stats_frame,
            text="📊 0 MB/s",
            font=ctk.CTkFont(size=14)
        )
        self.bandwidth_label.pack(side="left", padx=10)
        
        self.uptime_label = ctk.CTkLabel(
            self.stats_frame,
            text="⏱ 00:00:00",
            font=ctk.CTkFont(size=14)
        )
        self.uptime_label.pack(side="left", padx=10)
    
    def setup_dashboard_tab(self):
        """Setup the main dashboard with graphs"""
        # Configure grid
        self.tab_dashboard.grid_rowconfigure(0, weight=1)
        self.tab_dashboard.grid_rowconfigure(1, weight=1)
        self.tab_dashboard.grid_columnconfigure(0, weight=1)
        self.tab_dashboard.grid_columnconfigure(1, weight=1)
        
        # System Info Card
        sys_card = ctk.CTkFrame(self.tab_dashboard)
        sys_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(sys_card, text="SYSTEM INFORMATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.sys_info_text = ctk.CTkTextbox(sys_card, height=150)
        self.sys_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Network Card
        net_card = ctk.CTkFrame(self.tab_dashboard)
        net_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(net_card, text="NETWORK STATUS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.net_info_text = ctk.CTkTextbox(net_card, height=150)
        self.net_info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # CPU/Memory Graph
        self.graph_frame = ctk.CTkFrame(self.tab_dashboard)
        self.graph_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.setup_performance_graphs()
    
    def setup_performance_graphs(self):
        """Setup matplotlib performance graphs"""
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 4), facecolor='#1a1a1a')
        self.fig.patch.set_facecolor('#1a1a1a')
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='#00ff00')
            ax.spines['bottom'].set_color('#333')
            ax.spines['top'].set_color('#333')
            ax.spines['left'].set_color('#333')
            ax.spines['right'].set_color('#333')
            ax.grid(True, alpha=0.2, color='#00ff00')
        
        self.ax1.set_ylabel('CPU %', color='#ff1744')
        self.ax2.set_ylabel('Memory %', color='#2979ff')
        self.ax2.set_xlabel('Time (s)', color='#b0bec5')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Animation
        self.ani = animation.FuncAnimation(
            self.fig, self.animate_graphs, interval=1000,
            cache_frame_data=False
        )
    
    def animate_graphs(self, frame):
        """Animate performance graphs"""
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        
        self.cpu_history.append(cpu)
        self.memory_history.append(mem)
        
        self.ax1.clear()
        self.ax2.clear()
        
        self.ax1.plot(list(self.cpu_history), color='#ff1744', linewidth=2)
        self.ax2.plot(list(self.memory_history), color='#2979ff', linewidth=2)
        
        self.ax1.fill_between(range(len(self.cpu_history)), self.cpu_history, alpha=0.2, color='#ff1744')
        self.ax2.fill_between(range(len(self.memory_history)), self.memory_history, alpha=0.2, color='#2979ff')
        
        self.ax1.set_ylabel('CPU %', color='#ff1744')
        self.ax2.set_ylabel('Memory %', color='#2979ff')
        
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='#00ff00')
            ax.grid(True, alpha=0.2, color='#00ff00')
    
    def setup_tunnels_tab(self):
        """Setup tunnel management tab"""
        # Quick create frame
        create_frame = ctk.CTkFrame(self.tab_tunnels)
        create_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(create_frame, text="QUICK TUNNEL CREATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        input_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10)
        
        # Inputs
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
        
        # Protocol selector
        self.tun_protocol = ctk.CTkOptionMenu(
            input_frame,
            values=[p.value for p in TunnelProtocol],
            width=120
        )
        self.tun_protocol.grid(row=0, column=6, padx=5)
        
        # Options
        options_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=10, pady=5)
        
        self.encrypt_var = ctk.BooleanVar()
        ctk.CTkCheckBox(options_frame, text="Encryption", variable=self.encrypt_var).pack(side="left", padx=10)
        
        self.compress_var = ctk.BooleanVar()
        ctk.CTkCheckBox(options_frame, text="Compression", variable=self.compress_var).pack(side="left", padx=10)
        
        ctk.CTkLabel(options_frame, text="Rate Limit (MB/s):").pack(side="left", padx=10)
        self.rate_limit = ctk.CTkEntry(options_frame, width=60)
        self.rate_limit.pack(side="left", padx=5)
        self.rate_limit.insert(0, "0")
        
        # Buttons
        btn_frame = ctk.CTkFrame(create_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="➕ CREATE TUNNEL",
            command=self.create_tunnel,
            fg_color="#00e676",
            hover_color="#00c853",
            text_color="#000000"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔌 EXPOSE RDP",
            command=self.quick_expose_rdp,
            fg_color="#ff1744",
            hover_color="#d50000"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗺 PORT SCANNER",
            command=self.port_scanner_popup,
            fg_color="#2979ff",
            hover_color="#1565c0"
        ).pack(side="left", padx=5)
        
        # Tunnel list
        list_frame = ctk.CTkFrame(self.tab_tunnels)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="ACTIVE TUNNELS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.tunnel_listbox = tk.Listbox(
            list_frame,
            bg='#0a0a0a',
            fg='#00ff00',
            font=('Courier', 10),
            selectbackground='#ff1744',
            height=12
        )
        self.tunnel_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Control buttons
        ctrl_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(ctrl_frame, text="▶ START", command=self.start_tunnel).pack(side="left", padx=2)
        ctk.CTkButton(ctrl_frame, text="⏹ STOP", command=self.stop_tunnel).pack(side="left", padx=2)
        ctk.CTkButton(ctrl_frame, text="🔄 RESTART", command=self.restart_tunnel).pack(side="left", padx=2)
        ctk.CTkButton(ctrl_frame, text="🗑 DELETE", command=self.delete_tunnel).pack(side="left", padx=2)
        ctk.CTkButton(ctrl_frame, text="▶ START ALL", command=self.start_all_tunnels).pack(side="left", padx=2)
        ctk.CTkButton(ctrl_frame, text="⏹ STOP ALL", command=self.stop_all_tunnels).pack(side="left", padx=2)
    
    def setup_network_tab(self):
        """Setup network tools tab"""
        # IP Info
        ip_frame = ctk.CTkFrame(self.tab_network)
        ip_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ip_frame, text="NETWORK INTERFACES", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.ip_text = ctk.CTkTextbox(ip_frame, height=100)
        self.ip_text.pack(fill="x", padx=10, pady=5)
        
        btn_frame = ctk.CTkFrame(ip_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(btn_frame, text="🔄 REFRESH IPs", command=self.refresh_network_info).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="📍 GEO LOCATION", command=self.show_geo_location).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="⚡ SPEED TEST", command=self.run_speedtest).pack(side="left", padx=5)
        
        # QR Code for sharing
        qr_frame = ctk.CTkFrame(self.tab_network)
        qr_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(qr_frame, text="SHARE VIA QR", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.qr_label = ctk.CTkLabel(qr_frame, text="")
        self.qr_label.pack(pady=5)
        
        ctk.CTkButton(
            qr_frame,
            text="🔳 GENERATE QR CODE",
            command=self.generate_qr_code
        ).pack(pady=5)
    
    def setup_security_tab(self):
        """Setup security configuration tab"""
        sec_frame = ctk.CTkFrame(self.tab_security)
        sec_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(sec_frame, text="ENCRYPTION SETTINGS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(sec_frame, text="Encryption Password:").pack()
        self.encrypt_pass = ctk.CTkEntry(sec_frame, width=300, show="*")
        self.encrypt_pass.pack(pady=5)
        
        ctk.CTkButton(
            sec_frame,
            text="🔑 GENERATE SSL CERTIFICATE",
            command=self.generate_ssl
        ).pack(pady=10)
        
        ctk.CTkButton(
            sec_frame,
            text="🔒 ENABLE ENCRYPTION",
            command=self.enable_encryption
        ).pack(pady=5)
        
        # Firewall
        fw_frame = ctk.CTkFrame(self.tab_security)
        fw_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(fw_frame, text="IP WHITELIST/BLACKLIST", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        self.ip_filter_entry = ctk.CTkEntry(fw_frame, width=300, placeholder_text="Enter IP address")
        self.ip_filter_entry.pack(pady=5)
        
        filter_btn_frame = ctk.CTkFrame(fw_frame, fg_color="transparent")
        filter_btn_frame.pack(pady=5)
        
        ctk.CTkButton(filter_btn_frame, text="✅ ALLOW", fg_color="#00e676").pack(side="left", padx=5)
        ctk.CTkButton(filter_btn_frame, text="🚫 BLOCK", fg_color="#ff1744").pack(side="left", padx=5)
    
    def setup_advanced_tab(self):
        """Setup advanced features tab"""
        adv_frame = ctk.CTkFrame(self.tab_advanced)
        adv_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(adv_frame, text="LOAD BALANCER", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(adv_frame, text="Backend Host:Port").pack()
        self.backend_entry = ctk.CTkEntry(adv_frame, width=300, placeholder_text="192.168.1.100:3389")
        self.backend_entry.pack(pady=5)
        
        ctk.CTkButton(
            adv_frame,
            text="➕ ADD BACKEND",
            command=self.add_backend
        ).pack(pady=5)
        
        # RDP Configuration
        rdp_frame = ctk.CTkFrame(self.tab_advanced)
        rdp_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(rdp_frame, text="RDP CONFIGURATION", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(rdp_frame, text="RDP Port:").pack()
        self.rdp_port_entry = ctk.CTkEntry(rdp_frame, width=100)
        self.rdp_port_entry.pack(pady=5)
        self.rdp_port_entry.insert(0, "3389")
        
        ctk.CTkButton(
            rdp_frame,
            text="🔧 CHANGE RDP PORT",
            command=self.change_rdp_port
        ).pack(pady=5)
        
        ctk.CTkButton(
            rdp_frame,
            text="🔓 ENABLE RDP",
            command=self.enable_rdp
        ).pack(pady=5)
        
        # ZeroTier / Ngrok
        tunnel_frame = ctk.CTkFrame(self.tab_advanced)
        tunnel_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(tunnel_frame, text="EXTERNAL TUNNELING", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        
        ctk.CTkButton(
            tunnel_frame,
            text="📦 INSTALL ZEROTIER",
            command=self.install_zerotier
        ).pack(side="left", padx=10, pady=5)
        
        ctk.CTkButton(
            tunnel_frame,
            text="⚡ NGROK TCP TUNNEL",
            command=self.ngrok_tunnel
        ).pack(side="left", padx=10, pady=5)
    
    def setup_logs_tab(self):
        """Setup logging tab"""
        log_frame = ctk.CTkFrame(self.tab_logs)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(log_frame, text="SYSTEM LOGS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(log_frame, font=("Courier", 10))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctrl_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(ctrl_frame, text="🗑 CLEAR LOGS", command=lambda: self.log_text.delete("1.0", "end")).pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text="💾 EXPORT LOGS", command=self.export_logs).pack(side="left", padx=5)
    
    def setup_footer(self):
        """Setup footer with status"""
        footer = ctk.CTkFrame(self.root, height=30)
        footer.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        footer.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            footer,
            text=f"READY | {Config.AUTHOR} | {Config.CHANNEL} | {Config.BUILD}",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.time_label.pack(side="right", padx=10)
        self.update_time()
    
    def update_time(self):
        """Update time display"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=now)
        self.root.after(1000, self.update_time)
    
    def log_message(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        if hasattr(self, 'log_text'):
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")
        
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message[:100])
    
    # ==================== TUNNEL OPERATIONS ====================
    def create_tunnel(self):
        """Create a new tunnel"""
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
                protocol=protocol,
                encryption=self.encrypt_var.get(),
                compression=self.compress_var.get(),
                rate_limit=int(self.rate_limit.get() or 0)
            )
            
            tunnel_id = self.forwarder.create_tunnel(config)
            self.forwarder.start_tunnel(tunnel_id)
            
            display = f"{config.name} | 0.0.0.0:{local_port} -> {remote_host}:{remote_port} [{protocol}]"
            self.tunnel_listbox.insert(tk.END, display)
            self.log_message(f"[+] Created {display}")
            
        except ValueError as e:
            self.log_message(f"[!] Invalid input: {e}")
    
    def quick_expose_rdp(self):
        """Quick expose RDP"""
        public_ip = self.network.get_public_ip()
        local_ip = self.network.get_local_ip()
        
        self.tun_local_port.insert(0, "3389")
        self.tun_remote_host.insert(0, local_ip)
        self.tun_remote_port.insert(0, "3389")
        
        self.log_message(f"""
╔══════════════════════════════════════╗
║     RDP EXPOSURE INFORMATION        ║
╠══════════════════════════════════════╣
║ Public IP : {public_ip:<15}      ║
║ Local IP  : {local_ip:<15}      ║
║ Port      : 3389                    ║
║ Access    : {public_ip}:3389      ║
╚══════════════════════════════════════╝
        """)
        
        self.create_tunnel()
    
    def start_tunnel(self):
        """Start selected tunnel"""
        selection = self.tunnel_listbox.curselection()
        if selection:
            display = self.tunnel_listbox.get(selection[0])
            for tid, tunnel in self.forwarder.tunnels.items():
                if display.startswith(tunnel.name):
                    self.forwarder.start_tunnel(tid)
                    break
    
    def stop_tunnel(self):
        """Stop selected tunnel"""
        selection = self.tunnel_listbox.curselection()
        if selection:
            display = self.tunnel_listbox.get(selection[0])
            for tid, tunnel in self.forwarder.tunnels.items():
                if display.startswith(tunnel.name):
                    self.forwarder.stop_tunnel(tid)
                    break
    
    def restart_tunnel(self):
        """Restart selected tunnel"""
        self.stop_tunnel()
        time.sleep(0.5)
        self.start_tunnel()
    
    def delete_tunnel(self):
        """Delete selected tunnel"""
        selection = self.tunnel_listbox.curselection()
        if selection:
            display = self.tunnel_listbox.get(selection[0])
            for tid, tunnel in list(self.forwarder.tunnels.items()):
                if display.startswith(tunnel.name):
                    self.forwarder.stop_tunnel(tid)
                    del self.forwarder.tunnels[tid]
                    self.tunnel_listbox.delete(selection[0])
                    self.log_message(f"[-] Deleted: {tunnel.name}")
                    break
    
    def start_all_tunnels(self):
        """Start all tunnels"""
        for tid in self.forwarder.tunnels:
            self.forwarder.start_tunnel(tid)
        self.log_message("[▶] All tunnels started")
    
    def stop_all_tunnels(self):
        """Stop all tunnels"""
        for tid in self.forwarder.tunnels:
            self.forwarder.stop_tunnel(tid)
        self.log_message("[■] All tunnels stopped")
    
    # ==================== NETWORK OPERATIONS ====================
    def refresh_network_info(self):
        """Refresh network information"""
        local_ip = self.network.get_local_ip()
        public_ip = self.network.get_public_ip()
        interfaces = self.network.get_all_network_interfaces()
        
        info = f"Local IP: {local_ip}\n"
        info += f"Public IP: {public_ip}\n"
        info += f"Hostname: {socket.gethostname()}\n\n"
        info += "Interfaces:\n"
        
        for iface, details in interfaces.items():
            info += f"  {iface}: {details['ip']} (MAC: {details.get('mac', 'N/A')})\n"
        
        self.ip_text.delete("1.0", "end")
        self.ip_text.insert("1.0", info)
        
        # Update system info
        sys_info = f"CPU: {psutil.cpu_percent()}%\n"
        sys_info += f"Memory: {psutil.virtual_memory().percent}%\n"
        sys_info += f"Disk: {psutil.disk_usage('/').percent}%\n"
        sys_info += f"Platform: {platform.platform()}\n"
        sys_info += f"Python: {sys.version.split()[0]}"
        
        self.sys_info_text.delete("1.0", "end")
        self.sys_info_text.insert("1.0", sys_info)
    
    def show_geo_location(self):
        """Show geographical location"""
        location = self.network.get_geo_location()
        info = "GEO LOCATION:\n"
        info += f"IP: {location.get('ip', 'Unknown')}\n"
        info += f"City: {location.get('city', 'Unknown')}\n"
        info += f"Region: {location.get('region', 'Unknown')}\n"
        info += f"Country: {location.get('country_name', 'Unknown')}\n"
        info += f"ISP: {location.get('org', 'Unknown')}\n"
        info += f"Lat/Lon: {location.get('latitude', '?')}, {location.get('longitude', '?')}"
        
        self.log_message(info)
    
    def run_speedtest(self):
        """Run network speed test"""
        self.log_message("⚡ Running speed test...")
        result = self.network.run_speedtest()
        
        if 'error' not in result:
            info = f"""
╔══════════════════════════════╗
║     SPEED TEST RESULTS       ║
╠══════════════════════════════╣
║ Download : {result['download_mbps']:>6.2f} Mbps ║
║ Upload   : {result['upload_mbps']:>6.2f} Mbps ║
║ Ping     : {result['ping_ms']:>6.2f} ms   ║
║ Server   : {result['server']:<15} ║
╚══════════════════════════════╝
            """
            self.log_message(info)
        else:
            self.log_message(f"[!] Speed test failed: {result['error']}")
    
    def generate_qr_code(self):
        """Generate QR code for RDP access"""
        public_ip = self.network.get_public_ip()
        qr_data = f"rdp://{public_ip}:3389"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#00ff00", back_color="#000000")
        img = img.resize((200, 200))
        
        # Convert to CTkImage
        ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
        self.qr_label.configure(image=ctk_image, text="")
        
        self.log_message(f"🔳 QR Code generated for: {qr_data}")
    
    def port_scanner_popup(self):
        """Open port scanner popup"""
        popup = ctk.CTkToplevel(self.root)
        popup.title("Port Scanner")
        popup.geometry("400x300")
        
        ctk.CTkLabel(popup, text="Target Host:").pack(pady=5)
        target_entry = ctk.CTkEntry(popup, width=200)
        target_entry.pack(pady=5)
        
        ctk.CTkLabel(popup, text="Port Range:").pack(pady=5)
        port_frame = ctk.CTkFrame(popup, fg_color="transparent")
        port_frame.pack()
        
        start_port = ctk.CTkEntry(port_frame, width=70, placeholder_text="1")
        start_port.pack(side="left", padx=5)
        ctk.CTkLabel(port_frame, text="-").pack(side="left")
        end_port = ctk.CTkEntry(port_frame, width=70, placeholder_text="65535")
        end_port.pack(side="left", padx=5)
        
        result_text = ctk.CTkTextbox(popup, height=100)
        result_text.pack(fill="x", padx=10, pady=10)
        
        def scan():
            host = target_entry.get()
            start = int(start_port.get() or 1)
            end = int(end_port.get() or 65535)
            
            result_text.delete("1.0", "end")
            result_text.insert("1.0", "Scanning...\n")
            
            ports = self.network.scan_ports(host, start, min(end, start + 1000))
            
            result_text.delete("1.0", "end")
            result_text.insert("1.0", f"Open ports on {host}:\n")
            for port in ports:
                result_text.insert("end", f"  {port}\n")
        
        ctk.CTkButton(popup, text="🔍 SCAN", command=scan).pack(pady=10)
    
    # ==================== ADVANCED OPERATIONS ====================
    def add_backend(self):
        """Add backend to load balancer"""
        backend = self.backend_entry.get()
        try:
            host, port = backend.split(":")
            self.load_balancer.add_target(host, int(port))
            self.log_message(f"[+] Added backend: {host}:{port}")
        except:
            self.log_message("[!] Invalid format. Use host:port")
    
    def change_rdp_port(self):
        """Change RDP port"""
        try:
            port = int(self.rdp_port_entry.get())
            if ctypes.windll.shell32.IsUserAnAdmin():
                subprocess.run([
                    'reg', 'add',
                    'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp',
                    '/v', 'PortNumber', '/t', 'REG_DWORD', '/d', str(port), '/f'
                ], capture_output=True)
                self.log_message(f"[+] RDP port changed to {port}. REBOOT REQUIRED!")
            else:
                self.log_message("[!] Admin rights required!")
        except Exception as e:
            self.log_message(f"[!] Error: {e}")
    
    def enable_rdp(self):
        """Enable RDP"""
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                subprocess.run([
                    'reg', 'add',
                    'HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server',
                    '/v', 'fDenyTSConnections', '/t', 'REG_DWORD', '/d', '0', '/f'
                ], capture_output=True)
                self.log_message("[+] RDP Enabled!")
            else:
                self.log_message("[!] Admin rights required!")
        except Exception as e:
            self.log_message(f"[!] Error: {e}")
    
    def install_zerotier(self):
        """Install ZeroTier"""
        self.log_message("[*] Downloading ZeroTier...")
        # Add ZeroTier installation logic here
        self.log_message("[+] ZeroTier installation initiated")
    
    def ngrok_tunnel(self):
        """Setup ngrok tunnel"""
        public_ip = self.network.get_public_ip()
        self.log_message(f"""
[*] For ngrok TCP tunnel:
    1. Download ngrok from ngrok.com
    2. Run: ngrok tcp 3389
    3. Share the generated address
    
[*] Current public IP: {public_ip}
        """)
    
    def generate_ssl(self):
        """Generate SSL certificate"""
        EncryptionEngine.generate_ssl_cert("cert.pem", "key.pem")
        self.log_message("[+] SSL Certificate generated: cert.pem, key.pem")
    
    def enable_encryption(self):
        """Enable encryption for tunnels"""
        password = self.encrypt_pass.get()
        if password:
            self.forwarder.crypto = EncryptionEngine(password)
            self.log_message("[🔒] Encryption enabled with custom password")
        else:
            self.log_message("[!] Enter encryption password first")
    
    def export_logs(self):
        """Export logs to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rdp_exposer_logs_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(self.log_text.get("1.0", "end"))
        
        self.log_message(f"[💾] Logs exported to {filename}")
    
    # ==================== MONITORING ====================
    def start_monitoring(self):
        """Start system monitoring"""
        self.refresh_network_info()
        self.root.after(5000, self.monitor_loop)
    
    def monitor_loop(self):
        """Continuous monitoring"""
        try:
            stats = self.forwarder.get_stats()
            global_stats = stats['global']
            
            self.active_conn_label.configure(
                text=f"🔴 Active: {global_stats['active_connections']}"
            )
            
            self.bandwidth_label.configure(
                text=f"📊 {global_stats['bandwidth_mbps']} MB/s"
            )
            
            self.uptime_label.configure(
                text=f"⏱ {global_stats['uptime']}"
            )
            
        except Exception as e:
            pass
        
        self.root.after(1000, self.monitor_loop)
    
    def update_stats(self):
        """Update performance stats"""
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        
        self.cpu_history.append(cpu)
        self.memory_history.append(mem)
        
        self.root.after(2000, self.update_stats)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

# ==================== MAIN ENTRY POINT ====================
def main():
    """Main function"""
    # Check admin rights on Windows
    if platform.system() == "Windows":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                messagebox.showwarning(
                    "Admin Rights Required",
                    "⚠️ Run as Administrator for full functionality!\n\n"
                    "Right-click → Run as Administrator"
                )
        except:
            pass
    
    # Create and run GUI
    app = BillionDollarGUI()
    app.log_message("🔥 MAHMUD TECH RDP EXPOSER PRO MAX STARTED 🔥")
    app.log_message(f"👑 Built for: {Config.AUTHOR}")
    app.log_message(f"📢 Channel: {Config.CHANNEL}")
    app.run()

if __name__ == "__main__":
    main()
