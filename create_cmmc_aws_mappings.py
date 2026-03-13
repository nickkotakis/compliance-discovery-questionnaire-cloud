#!/usr/bin/env python3
"""Create CMMC AWS mappings by leveraging existing NIST 800-53 MCP data.

CMMC Level 2 maps to NIST SP 800-171 Rev 2, which maps to NIST 800-53 controls.
We use the existing aws_controls_mcp_data.json and csf_aws_mappings.json to build
CMMC-specific mappings by mapping 800-171 requirements to their 800-53 equivalents.
"""

import json
import os

# CMMC Practice -> NIST 800-53 control mapping
# Each CMMC practice maps to one or more 800-53 controls
CMMC_TO_800_53 = {
    # Access Control
    "ac.l2-3.1.1": ["ac-2", "ac-3", "ac-17"],
    "ac.l2-3.1.2": ["ac-3", "ac-6"],
    "ac.l2-3.1.3": ["ac-4"],
    "ac.l2-3.1.4": ["ac-5"],
    "ac.l2-3.1.5": ["ac-6", "ac-6(1)", "ac-6(5)"],
    "ac.l2-3.1.6": ["ac-6(2)"],
    "ac.l2-3.1.7": ["ac-6(9)", "ac-6(10)"],
    "ac.l2-3.1.8": ["ac-7"],
    "ac.l2-3.1.9": ["ac-8"],
    "ac.l2-3.1.10": ["ac-11", "ac-11(1)"],
    "ac.l2-3.1.11": ["ac-12"],
    "ac.l2-3.1.12": ["ac-17(1)"],
    "ac.l2-3.1.13": ["ac-17(2)"],
    "ac.l2-3.1.14": ["ac-17(3)"],
    "ac.l2-3.1.15": ["ac-17(4)"],
    "ac.l2-3.1.16": ["ac-18"],
    "ac.l2-3.1.17": ["ac-18(1)"],
    "ac.l2-3.1.18": ["ac-19"],
    "ac.l2-3.1.19": ["ac-19(5)"],
    "ac.l2-3.1.20": ["ac-20", "ac-20(1)"],
    "ac.l2-3.1.21": ["ac-20(2)"],
    "ac.l2-3.1.22": ["ac-22"],
    # Awareness and Training
    "at.l2-3.2.1": ["at-2"],
    "at.l2-3.2.2": ["at-3"],
    "at.l2-3.2.3": ["at-2(2)"],
    # Audit and Accountability
    "au.l2-3.3.1": ["au-2", "au-3", "au-3(1)"],
    "au.l2-3.3.2": ["au-6", "au-6(1)"],
    "au.l2-3.3.3": ["au-2(3)"],
    "au.l2-3.3.4": ["au-5"],
    "au.l2-3.3.5": ["au-6(3)"],
    "au.l2-3.3.6": ["au-7"],
    "au.l2-3.3.7": ["au-8"],
    "au.l2-3.3.8": ["au-9"],
    "au.l2-3.3.9": ["au-9(4)"],
    # Configuration Management
    "cm.l2-3.4.1": ["cm-2", "cm-8"],
    "cm.l2-3.4.2": ["cm-6"],
    "cm.l2-3.4.3": ["cm-3"],
    "cm.l2-3.4.4": ["cm-4"],
    "cm.l2-3.4.5": ["cm-5"],
    "cm.l2-3.4.6": ["cm-7"],
    "cm.l2-3.4.7": ["cm-7(1)", "cm-7(2)"],
    "cm.l2-3.4.8": ["cm-7(4)", "cm-7(5)"],
    "cm.l2-3.4.9": ["cm-11"],
    # Identification and Authentication
    "ia.l2-3.5.1": ["ia-2", "ia-5"],
    "ia.l2-3.5.2": ["ia-2", "ia-5"],
    "ia.l2-3.5.3": ["ia-2(1)", "ia-2(2)"],
    "ia.l2-3.5.4": ["ia-2(8)"],
    "ia.l2-3.5.5": ["ia-4"],
    "ia.l2-3.5.6": ["ia-4(4)"],
    "ia.l2-3.5.7": ["ia-5(1)"],
    "ia.l2-3.5.8": ["ia-5(1)"],
    "ia.l2-3.5.9": ["ia-5(1)"],
    "ia.l2-3.5.10": ["ia-5(1)"],
    "ia.l2-3.5.11": ["ia-6"],
    # Incident Response
    "ir.l2-3.6.1": ["ir-2", "ir-4", "ir-5", "ir-6"],
    "ir.l2-3.6.2": ["ir-6(1)"],
    "ir.l2-3.6.3": ["ir-3", "ir-3(2)"],
    # Maintenance
    "ma.l2-3.7.1": ["ma-2"],
    "ma.l2-3.7.2": ["ma-3", "ma-3(1)", "ma-3(2)"],
    "ma.l2-3.7.3": ["ma-3(3)"],
    "ma.l2-3.7.4": ["ma-3(2)"],
    "ma.l2-3.7.5": ["ma-4"],
    "ma.l2-3.7.6": ["ma-5"],
    # Media Protection
    "mp.l2-3.8.1": ["mp-4"],
    "mp.l2-3.8.2": ["mp-2"],
    "mp.l2-3.8.3": ["mp-6"],
    "mp.l2-3.8.4": ["mp-3"],
    "mp.l2-3.8.5": ["mp-5"],
    "mp.l2-3.8.6": ["mp-5(4)"],
    "mp.l2-3.8.7": ["mp-7"],
    "mp.l2-3.8.8": ["mp-7(1)"],
    "mp.l2-3.8.9": ["cp-9"],
    # Physical Protection
    "pe.l2-3.10.1": ["pe-2", "pe-5"],
    "pe.l2-3.10.2": ["pe-6"],
    "pe.l2-3.10.3": ["pe-3"],
    "pe.l2-3.10.4": ["pe-8"],
    "pe.l2-3.10.5": ["pe-3"],
    "pe.l2-3.10.6": ["pe-17"],
    # Personnel Security
    "ps.l2-3.9.1": ["ps-3"],
    "ps.l2-3.9.2": ["ps-4", "ps-5"],
    # Risk Assessment
    "ra.l2-3.11.1": ["ra-3"],
    "ra.l2-3.11.2": ["ra-5"],
    "ra.l2-3.11.3": ["ra-5(5)"],
    # Security Assessment
    "ca.l2-3.12.1": ["ca-2"],
    "ca.l2-3.12.2": ["ca-5"],
    "ca.l2-3.12.3": ["ca-7"],
    "ca.l2-3.12.4": ["pl-2"],
    # System and Communications Protection
    "sc.l2-3.13.1": ["sc-7"],
    "sc.l2-3.13.2": ["sa-8"],
    "sc.l2-3.13.3": ["sc-2"],
    "sc.l2-3.13.4": ["sc-4"],
    "sc.l2-3.13.5": ["sc-7(5)"],
    "sc.l2-3.13.6": ["sc-7(5)"],
    "sc.l2-3.13.7": ["sc-7(7)"],
    "sc.l2-3.13.8": ["sc-8", "sc-8(1)"],
    "sc.l2-3.13.9": ["sc-10"],
    "sc.l2-3.13.10": ["sc-12"],
    "sc.l2-3.13.11": ["sc-13"],
    "sc.l2-3.13.12": ["sc-15"],
    "sc.l2-3.13.13": ["sc-18"],
    "sc.l2-3.13.14": ["sc-19"],
    "sc.l2-3.13.15": ["sc-23"],
    "sc.l2-3.13.16": ["sc-28"],
    # System and Information Integrity
    "si.l2-3.14.1": ["si-2"],
    "si.l2-3.14.2": ["si-3"],
    "si.l2-3.14.3": ["si-5"],
    "si.l2-3.14.4": ["si-3"],
    "si.l2-3.14.5": ["si-3"],
    "si.l2-3.14.6": ["si-4"],
    "si.l2-3.14.7": ["si-4"],
}


def classify_priority(control_data):
    """Classify control priority based on automation capabilities."""
    config_rules = control_data.get('config_rules', [])
    security_hub = control_data.get('security_hub_controls', [])
    control_tower = control_data.get('control_tower_ids', [])
    frameworks = control_data.get('frameworks', [])

    if config_rules:
        return 'core'
    elif security_hub or control_tower:
        return 'recommended'
    elif len(frameworks) >= 5:
        return 'recommended'
    else:
        return 'enhanced'


def main():
    basedir = os.path.join(os.path.dirname(__file__), 'backend', 'compliance_discovery')

    # Load existing 800-53 MCP data
    mcp_file = os.path.join(basedir, 'aws_controls_mcp_data.json')
    with open(mcp_file, 'r') as f:
        mcp_data = json.load(f)
    mcp_controls = mcp_data.get('controls', {})

    # Load CSF AWS mappings for additional coverage
    csf_file = os.path.join(basedir, 'csf_aws_mappings.json')
    with open(csf_file, 'r') as f:
        csf_data = json.load(f)
    csf_controls = csf_data.get('controls', {})

    cmmc_mappings = {}
    total_controls = 0
    practices_with_controls = 0

    for cmmc_practice, nist_controls in CMMC_TO_800_53.items():
        aws_controls = []
        seen_ids = set()

        for nist_id in nist_controls:
            nist_key = nist_id.lower()
            if nist_key in mcp_controls:
                for ctrl in mcp_controls[nist_key]:
                    ctrl_id = ctrl.get('control_id', '')
                    if ctrl_id not in seen_ids:
                        seen_ids.add(ctrl_id)
                        control_copy = dict(ctrl)
                        control_copy['priority'] = classify_priority(ctrl)
                        aws_controls.append(control_copy)

        # Sort: core first, then recommended, then enhanced
        priority_order = {'core': 0, 'recommended': 1, 'enhanced': 2}
        aws_controls.sort(key=lambda c: priority_order.get(c.get('priority', 'enhanced'), 3))

        if aws_controls:
            cmmc_mappings[cmmc_practice] = aws_controls
            total_controls += len(aws_controls)
            practices_with_controls += 1

    output = {
        "metadata": {
            "source": "AWS Control Guides from ControlCompass (via NIST 800-53 mapping)",
            "description": "AWS implementation guides for CMMC Level 2 practices",
            "total_practices": len(CMMC_TO_800_53),
            "practices_with_controls": practices_with_controls,
            "total_aws_control_guides": total_controls
        },
        "controls": cmmc_mappings
    }

    output_file = os.path.join(basedir, 'cmmc_aws_mappings.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Created CMMC AWS mappings:")
    print(f"  Total practices: {len(CMMC_TO_800_53)}")
    print(f"  Practices with AWS controls: {practices_with_controls}")
    print(f"  Total AWS control guides: {total_controls}")
    print(f"  Output: {output_file}")


if __name__ == '__main__':
    main()
