#!/usr/bin/env python3
"""Generate CSF 2.0 to AWS control mappings for csf_aws_mappings.json.

Maps NIST CSF 2.0 subcategories to AWS controls by cross-referencing
the well-known CSF-to-800-53 crosswalk with existing AWS control data.
"""

import json
import os

# CSF 2.0 subcategory -> relevant NIST 800-53 control families crosswalk
# Based on NIST's official CSF 2.0 to SP 800-53 Rev 5 mapping
CSF_TO_800_53 = {
    # === GOVERN (GV) ===
    'gv.oc-01': ['pm-7', 'pm-9', 'pm-11'],
    'gv.oc-02': ['pm-1', 'pm-2', 'pm-7'],
    'gv.oc-03': ['pm-1', 'pl-1', 'pl-4'],
    'gv.oc-04': ['pm-7', 'pm-11', 'cp-2'],
    'gv.oc-05': ['pm-7', 'pm-11', 'sa-9'],
    'gv.rm-01': ['pm-9', 'pm-3', 'ra-1'],
    'gv.rm-02': ['pm-9', 'ra-1', 'ra-3'],
    'gv.rm-03': ['pm-9', 'pm-4', 'ra-3'],
    'gv.rm-04': ['pm-9', 'ra-3', 'pm-4'],
    'gv.rm-05': ['pm-9', 'pm-15', 'pm-16'],
    'gv.rm-06': ['ra-1', 'ra-3', 'ra-5'],
    'gv.rm-07': ['pm-9', 'pm-4'],
    'gv.rr-01': ['pm-1', 'pm-2', 'pm-9'],
    'gv.rr-02': ['pm-1', 'pm-2', 'ps-1', 'ps-7'],
    'gv.rr-03': ['pm-3', 'pm-1', 'sa-2'],
    'gv.rr-04': ['ps-1', 'ps-2', 'ps-3', 'ps-4', 'ps-5', 'ps-6', 'ps-7', 'ps-8', 'ps-9'],
    'gv.po-01': ['pm-1', 'pl-1', 'ac-1', 'at-1', 'au-1', 'cm-1', 'cp-1', 'ia-1', 'ir-1', 'sc-1', 'si-1'],
    'gv.po-02': ['pm-1', 'pl-1', 'ac-1', 'si-1'],
    'gv.sc-01': ['sr-1', 'sr-2', 'sr-3'],
    'gv.sc-02': ['sr-1', 'sr-2', 'ps-7'],
    'gv.sc-03': ['sr-1', 'sr-3', 'ra-3'],
    'gv.sc-04': ['sr-2', 'sr-5', 'sr-6'],
    'gv.sc-05': ['sr-1', 'sr-2', 'sr-3', 'sa-4'],
    'gv.sc-06': ['sr-5', 'sr-6', 'sa-9'],
    'gv.sc-07': ['sr-5', 'sr-6', 'sr-8'],
    'gv.sc-08': ['sr-1', 'ir-1', 'ir-4'],
    'gv.sc-09': ['sr-1', 'sr-10', 'sr-11', 'sr-12'],
    'gv.sc-10': ['sr-1', 'sr-2'],

    # === IDENTIFY (ID) ===
    'id.am-01': ['cm-8', 'cm-12', 'pm-5'],
    'id.am-02': ['cm-8', 'cm-7', 'cm-10', 'cm-11'],
    'id.am-03': ['ac-4', 'sc-7', 'ca-3'],
    'id.am-04': ['sa-9', 'sr-2', 'pm-5'],
    'id.am-05': ['ra-2', 'ra-9', 'cm-8', 'sc-7'],
    'id.am-07': ['cm-8', 'cm-12', 'mp-1', 'mp-4'],
    'id.am-08': ['cm-8', 'sa-22', 'cm-2', 'cm-3'],
    'id.ra-01': ['ra-5', 'si-2', 'si-5'],
    'id.ra-02': ['pm-15', 'pm-16', 'si-5'],
    'id.ra-03': ['ra-3', 'pm-12', 'pm-16'],
    'id.ra-04': ['ra-3', 'ra-5', 'pm-12'],
    'id.ra-05': ['ra-3', 'ra-7', 'pm-4'],
    'id.ra-06': ['ra-3', 'ra-7', 'pm-4'],
    'id.ra-07': ['cm-3', 'cm-4', 'ca-7'],
    'id.ra-08': ['ra-5', 'si-2', 'si-5'],
    'id.ra-09': ['sa-10', 'sa-11', 'sr-3', 'sr-5'],
    'id.ra-10': ['sr-5', 'sr-6', 'sa-9'],
    'id.im-01': ['ca-2', 'ca-5', 'ca-7', 'pm-4'],
    'id.im-02': ['ca-2', 'ca-7', 'ca-9'],
    'id.im-03': ['ca-2', 'ca-7', 'pm-4'],
    'id.im-04': ['ir-1', 'ir-8', 'cp-2'],

    # === PROTECT (PR) ===
    'pr.aa-01': ['ac-2', 'ia-2', 'ia-4', 'ia-5', 'ia-12'],
    'pr.aa-02': ['ia-12', 'ia-2', 'ia-5'],
    'pr.aa-03': ['ia-2', 'ia-8', 'ia-11'],
    'pr.aa-04': ['ia-2', 'ia-5', 'ia-6', 'ia-7'],
    'pr.aa-05': ['ac-2', 'ac-3', 'ac-5', 'ac-6', 'ac-17'],
    'pr.aa-06': ['mp-2', 'mp-4', 'mp-5'],
    'pr.at-01': ['at-2', 'at-3', 'at-4'],
    'pr.at-02': ['at-3', 'at-4'],
    'pr.ds-01': ['sc-28', 'sc-12', 'sc-13', 'mp-4', 'mp-5'],
    'pr.ds-02': ['sc-8', 'sc-13', 'sc-23'],
    'pr.ds-10': ['sc-4', 'sc-28', 'sc-39'],
    'pr.ds-11': ['cp-9', 'cp-6', 'cp-10'],
    'pr.ps-01': ['cm-2', 'cm-6', 'cm-8', 'cm-3'],
    'pr.ps-02': ['si-2', 'cm-3', 'cm-4', 'sa-22'],
    'pr.ps-03': ['cm-8', 'sa-22'],
    'pr.ps-04': ['au-2', 'au-3', 'au-6', 'au-12'],
    'pr.ps-05': ['cm-7', 'cm-10', 'cm-11'],
    'pr.ps-06': ['sa-3', 'sa-8', 'sa-10', 'sa-11', 'sa-15'],
    'pr.ir-01': ['ac-4', 'sc-7', 'sc-2'],
    'pr.ir-02': ['cp-2', 'cp-8'],
    'pr.ir-03': ['cp-2', 'cp-7', 'cp-9', 'cp-10'],
    'pr.ir-04': ['cp-2', 'sc-5', 'au-4'],

    # === DETECT (DE) ===
    'de.cm-01': ['si-4', 'sc-7', 'ac-4'],
    'de.cm-02': ['si-4'],
    'de.cm-03': ['au-6', 'au-12', 'ac-2'],
    'de.cm-06': ['sa-9', 'si-4', 'ca-7'],
    'de.cm-09': ['si-3', 'si-4', 'si-7', 'cm-7'],
    'de.ae-02': ['au-6', 'si-4', 'ir-4'],
    'de.ae-03': ['au-6', 'si-4', 'ir-4'],
    'de.ae-04': ['si-4', 'ir-4', 'ir-5'],
    'de.ae-06': ['ir-4', 'ir-5', 'ir-6'],
    'de.ae-07': ['si-4', 'au-6', 'ir-4'],
    'de.ae-08': ['ir-4', 'ir-5'],

    # === RESPOND (RS) ===
    'rs.ma-01': ['ir-1', 'ir-4', 'ir-8'],
    'rs.ma-02': ['ir-4', 'ir-5', 'ir-6'],
    'rs.ma-03': ['ir-4', 'ir-6', 'ir-7'],
    'rs.ma-04': ['ir-4', 'ir-6', 'ir-8'],
    'rs.an-03': ['ir-4', 'au-6', 'au-7'],
    'rs.an-06': ['au-9', 'au-11', 'ir-4'],
    'rs.an-07': ['au-6', 'au-7', 'ir-4'],
    'rs.an-08': ['ir-4', 'ir-5', 'ir-6'],
    'rs.co-02': ['ir-6', 'ir-7'],
    'rs.co-03': ['ir-6', 'si-5'],
    'rs.mi-01': ['ir-4', 'sc-7', 'si-4'],
    'rs.mi-02': ['ir-4', 'si-2', 'cm-3'],
    'rs.ma-05': ['ir-4', 'ir-8', 'cp-2'],

    # === RECOVER (RC) ===
    'rc.rp-01': ['cp-2', 'cp-10', 'ir-4'],
    'rc.rp-02': ['cp-2', 'cp-10', 'cp-9'],
    'rc.rp-03': ['cp-9', 'cp-6'],
    'rc.rp-04': ['cp-2', 'cp-4', 'ir-4'],
    'rc.rp-05': ['cp-2', 'cp-7', 'cp-10'],
    'rc.rp-06': ['cp-2', 'cp-4'],
    'rc.co-01': ['cp-2', 'ir-6'],
    'rc.co-02': ['cp-2', 'ir-6'],
    'rc.co-03': ['cp-2', 'ir-6', 'pm-1'],
    'rc.co-04': ['cp-2', 'ir-4', 'pm-4'],
}


def main():
    # Load existing AWS controls data
    with open('backend/compliance_discovery/aws_controls_mcp_data.json') as f:
        mcp_data = json.load(f)
    controls_by_family = mcp_data.get('controls', {})

    # Build CSF mappings
    csf_mappings = {}
    stats = {'mapped': 0, 'empty': 0}

    for csf_id, nist_families in sorted(CSF_TO_800_53.items()):
        # Collect unique AWS controls from all mapped 800-53 families
        seen_control_ids = set()
        aws_controls = []

        for family in nist_families:
            family_controls = controls_by_family.get(family, [])
            for ctrl in family_controls:
                cid = ctrl.get('control_id', '')
                if cid not in seen_control_ids:
                    seen_control_ids.add(cid)
                    aws_controls.append(ctrl)

        if aws_controls:
            csf_mappings[csf_id] = aws_controls
            stats['mapped'] += 1
        else:
            stats['empty'] += 1

    # Write output
    output = {
        "metadata": {
            "source": "NIST CSF 2.0 to SP 800-53 Rev 5 crosswalk mapped to AWS Control Guides",
            "description": "AWS implementation guides for NIST CSF 2.0 subcategories",
            "total_subcategories": len(csf_mappings),
            "total_controls": sum(len(v) for v in csf_mappings.values())
        },
        "controls": csf_mappings
    }

    with open('backend/compliance_discovery/csf_aws_mappings.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"CSF AWS mappings generated:")
    print(f"  Subcategories with AWS controls: {stats['mapped']}")
    print(f"  Subcategories without controls: {stats['empty']}")
    print(f"  Total AWS control entries: {sum(len(v) for v in csf_mappings.values())}")

    # Show sample
    for csf_id in ['pr.aa-01', 'pr.ds-01', 'de.cm-01']:
        if csf_id in csf_mappings:
            print(f"\n  {csf_id}: {len(csf_mappings[csf_id])} controls")
            for c in csf_mappings[csf_id][:3]:
                print(f"    - {c['control_id']}: {c['title'][:60]}...")


if __name__ == '__main__':
    main()
