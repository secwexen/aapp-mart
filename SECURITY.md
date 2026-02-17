# Security Policy

AAPP-MART values responsible disclosure and safe, ethical security research. This document outlines the security policy for reporting vulnerabilities, response expectations, and legal guidance.

---

## Reporting a Vulnerability

If you discover a security vulnerability in AAPP-MART, please report it responsibly.

**Preferred method:**
- Open a **[private GitHub Security Advisory](https://github.com/secwexen/aapp-mart/security/advisories/new)**.

**Important:** Do **not disclose security issues publicly** until a fix or mitigation has been released.

---

## Response Expectations

- **Initial response:** within 72 hours  
- **Fix or mitigation:** as soon as reasonably possible  
- Security issues will be tracked via a **ticket system or CVE** where applicable  
- Coordinated disclosure will be handled in collaboration with the reporter

---

## Supported Versions

Security updates are provided **only for the latest stable release** of AAPP-MART (currently `v0.3.0-alpha`).  
Older versions may not receive security fixes.

---

## Scope

This project **does not provide exploit code**.  

**Valid reports include:**
- Code-level security weaknesses  
- Dependency vulnerabilities  
- Logic flaws affecting security  
- Configuration or deployment misconfigurations  

**Out of scope:**
- Social engineering  
- Denial-of-service via unrealistic traffic  
- Issues requiring physical access

---

## Reporting Guidelines / Example Report Format

When submitting a security report, please include the following:

- **Software version:** The version of AAPP-MART affected  
- **Environment:** OS, Python version, dependencies  
- **Steps to reproduce:** Detailed instructions  
- **Observed behavior:** What happens when the vulnerability occurs  
- **Expected behavior:** What should happen  
- **Supporting evidence:** Logs, screenshots, or proof-of-concept code (**required**)  
- **Additional context:** Any other relevant information such as timing, frequency, or impact assessment

---

## Legal Notice

Unauthorized testing or exploitation may **violate laws**. Ensure you have explicit permission before performing any security testing.

**AAPP-MART, its authors, and contributors assume no responsibility or liability** for any misuse, damage, or legal consequences arising from the use of this software.  
Users are solely responsible for ensuring compliance with all applicable laws, regulations, and organizational policies.

---

## Credits

We appreciate responsible disclosure and will acknowledge reporters when appropriate.
