# Tata - Test Automation and Troubleshooting Assistant

Tata is a command-line utility designed for checking the configuration of host machines within specified tasks. It provides a simple and efficient way to automate tests related to host settings.

## Supported Tasks

Tata supports the following tasks:

1. **check_hostname:**
   - Verifies that the hostname of the machine matches the specified value.
    ```yaml
    tasks:
      - task: check_hostname
        target_hostname: "test"
    ```

2. **check_ping:**
   - Checks if the specified IP address or domain is reachable via ping.
   ```yaml
    tasks:
      - task: check_ping
        target_ip: "127.0.0.1"
   ```
3. **linux_check_ipv4_forwarding**
   ```yaml
   tasks:
     - task: linux_check_ipv4_forwarding
       enabled: no
   ```
4. **linux_check_ipv6_forwarding**
   ```yaml
   tasks:
     - task: linux_check_ipv6_forwarding
       enabled: no
   ```

## Task Configuration

Tasks are defined in a YAML file with the following format:

```yaml
tasks:
  - task: check_hostname
    target_hostname: "test"

  - task: check_ping
    target_ip: "127.0.0.1"
  - task: check_ping
    target_ip: "ya.ru"

  - task: linux_check_ipv4_forwarding
    enabled: no
  - task: linux_check_ipv6_forwarding
    enabled: no

```

## Installation

### Preferred method: pipx

```bash
pipx install py_tata
pytata ./tasks.yaml
```

### Alternative method: pip

```bash
pip install py_tata
python -m py_tata.cli.app ./tasks.yaml
```

## Supported Python Versions

Tata is compatible with Python versions 3.10 and above.

---

Thank you for using Tata! If you have any questions or encounter any problems, please don't hesitate to reach out.
