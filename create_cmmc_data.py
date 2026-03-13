#!/usr/bin/env python3
"""Create CMMC Level 2 data file with all 110 practices organized by domain.

CMMC Level 2 maps directly to NIST SP 800-171 Rev 2.
The 14 domains correspond to the 14 families in 800-171.
"""

import json

cmmc_data = {
    "framework": "CMMC Level 2",
    "version": "2.0",
    "source": "https://dodcio.defense.gov/CMMC/",
    "nist_mapping": "NIST SP 800-171 Rev 2",
    "domains": {
        "AC": {
            "name": "Access Control",
            "description": "Limit information system access to authorized users, processes acting on behalf of authorized users, or devices. Manage access to CUI in accordance with approved authorizations.",
            "practices": {
                "AC.L2-3.1.1": "Limit information system access to authorized users, processes acting on behalf of authorized users, or devices (including other information systems).",
                "AC.L2-3.1.2": "Limit information system access to the types of transactions and functions that authorized users are permitted to execute.",
                "AC.L2-3.1.3": "Control the flow of CUI in accordance with approved authorizations.",
                "AC.L2-3.1.4": "Separate the duties of individuals to reduce the risk of malevolent activity without collusion.",
                "AC.L2-3.1.5": "Employ the principle of least privilege, including for specific security functions and privileged accounts.",
