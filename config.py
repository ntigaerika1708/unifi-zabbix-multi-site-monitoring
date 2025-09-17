"""
Configuration file for UniFi Zabbix Monitoring
Customize these settings for your environment
"""

# UniFi Controller Settings
UNIFI_CONTROLLER = {
    'host': 'https://192.168.1.20:8443',  # Your UniFi Controller URL
    'username': 'zabbix',                   # Monitoring user
    'password': 'zabbix',                   # User password
    'verify_ssl': False,                    # Set to True if using valid SSL cert
    'timeout': 30                           # Request timeout in seconds
}

# Site Configuration
# To find site IDs: UniFi Controller > Settings > System > Advanced > Site ID
SITES = {
    "Default": "default",
    "Branch Office": "abc123def456", 
    "Warehouse": "def456ghi789",
    "Main Campus": "ghi789jkl012",
    "Remote Site": "jkl012mno345"
    # Add your sites here:
    # "Site Name": "site_id_from_controller"
}

# Device Type Mapping (for filtering if needed)
DEVICE_TYPES = {
    'access_points': ['uap'],       # UniFi Access Points
    'switches': ['usw'],            # UniFi Switches  
    'gateways': ['ugw'],            # UniFi Gateways (if monitored)
    'all': ['uap', 'usw', 'ugw']    # All device types
}

# Monitoring Configuration
MONITORING = {
    'included_types': ['uap', 'usw'],       # Device types to monitor
    'exclude_offline_discovery': False,      # Set True to exclude offline devices from discovery
    'name_fallback_order': ['name', 'model', 'mac'],  # Priority for device naming
    'default_uptime': 0,                    # Default uptime for devices without data
}

# Logging (future feature)
LOGGING = {
    'enabled': False,
    'level': 'INFO',
    'file': '/var/log/zabbix/unifi_monitoring.log'
}
