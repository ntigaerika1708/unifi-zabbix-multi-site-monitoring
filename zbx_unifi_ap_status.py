#!/usr/bin/env python3
"""
UniFi Multi-Site Monitoring Script for Zabbix
Monitors UniFi Access Points and Switches across multiple sites
"""

import requests
import sys
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# UniFi Controller Configuration
UNIFI_HOST = "https://192.168.11.220:8443"  # Change to your controller IP
USERNAME = "zabbix"                         # UniFi username for monitoring
PASSWORD = "zabbix"                        # UniFi password

# Site mapping (Description -> Site ID)
# To get site IDs: Login to UniFi Controller > Settings > System > Advanced > Site ID
SITE_MAP = {
    "Default": "default",                   # Default site
    "Branch Office": "abc123def456",        # Example site IDs  
    "Warehouse": "def456ghi789",           # Replace with your actual site IDs
    "Main Campus": "ghi789jkl012",
    "Remote Site": "jkl012mno345"
}

def get_session():
    """
    Authenticate with UniFi Controller and return session
    """
    session = requests.Session()
    login_data = {"username": USERNAME, "password": PASSWORD}
    
    try:
        response = session.post(f"{UNIFI_HOST}/api/login", json=login_data, verify=False)
        if response.status_code != 200:
            print(json.dumps({"error": f"Authentication failed: HTTP {response.status_code}"}))
            sys.exit(1)
        return session
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Connection error: {str(e)}"}))
        sys.exit(1)

def format_device_data(raw_devices):
    """
    Format device data for Zabbix template consumption
    """
    formatted_devices = []
    
    for device in raw_devices:
        # Determine device name priority: name > model > mac
        device_name = device.get('name') or device.get('model') or device.get('mac', 'Unknown')
        
        # Normalize state (1 for online, 0 for offline)
        state = 1 if device.get('state') == 1 else 0
        
        formatted_device = {
            'mac': device.get('mac', ''),
            'name': device_name,
            'model': device.get('model', 'Unknown'),
            'ip': device.get('ip', 'Unknown'),
            'state': state,
            'uptime': device.get('uptime', 0),
            'version': device.get('version', 'Unknown'),
            'type': device.get('type', 'unknown')
        }
        
        formatted_devices.append(formatted_device)
    
    return formatted_devices

def main():
    """
    Main execution function
    """
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: zbx_unifi_ap_status.py <site_name>"}))
        sys.exit(1)
    
    site_desc = sys.argv[1]
    site_name = SITE_MAP.get(site_desc)
    
    if not site_name:
        available_sites = list(SITE_MAP.keys())
        print(json.dumps({
            "error": f"Site '{site_desc}' not found. Available sites: {', '.join(available_sites)}"
        }))
        sys.exit(1)
    
    try:
        # Get authenticated session
        session = get_session()
        
        # Query device statistics
        url = f"{UNIFI_HOST}/api/s/{site_name}/stat/device"
        response = session.get(url, verify=False)
        
        if response.status_code != 200:
            print(json.dumps({"error": f"Failed to fetch devices: HTTP {response.status_code}"}))
            sys.exit(1)
        
        # Parse response
        raw_data = response.json()
        
        # Extract device data (UniFi API returns {"meta": {}, "data": [...]})
        if 'data' in raw_data:
            devices = raw_data['data']
        else:
            devices = raw_data if isinstance(raw_data, list) else []
        
        # Format devices for Zabbix template
        formatted_devices = format_device_data(devices)
        
        # Return formatted result
        result = {
            "data": formatted_devices
        }
        
        print(json.dumps(result))
        
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Network error: {str(e)}"}))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parsing error: {str(e)}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {str(e)}"}))
        sys.exit(1)
    finally:
        # Logout from controller (cleanup)
        try:
            if 'session' in locals():
                session.post(f"{UNIFI_HOST}/api/logout", verify=False)
        except:
            pass  # Ignore logout errors

if __name__ == "__main__":
    main()
