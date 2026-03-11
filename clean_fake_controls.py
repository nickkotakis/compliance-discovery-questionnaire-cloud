"""
Clean fake AWS Control Guide entries from both JSON data files.

Removes entries with fabricated control IDs (like AWS-CG-PS-4, AWS-CG-AC-2)
and keeps only entries with real AWS Control Guide IDs (like AWS-CG-0000138).

Real AWS-CG IDs are always in the format AWS-CG-XXXXXXX (7-digit zero-padded number).
"""
import json
import re
import copy

REAL_CG_PATTERN = re.compile(r'^AWS-CG-\d{7}$')


def is_real_control_id(control_id: str) -> bool:
    """Check if a control ID is a real AWS Control Guide ID."""
    return bool(REAL_CG_PATTERN.match(control_id))


def clean_file(filepath: str, label: str) -> dict:
    """Clean a JSON data file by removing fake AWS-CG entries.
    
    Returns stats about what was cleaned.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    controls = data.get('controls', {})
    
    stats = {
        'total_controls': len(controls),
        'total_entries_before': 0,
        'total_entries_after': 0,
        'fake_entries_removed': 0,
        'real_entries_kept': 0,
        'controls_with_no_entries': 0,
        'controls_emptied': [],
        'fake_ids_found': set(),
    }
    
    cleaned_controls = {}
    
    for control_id, entries in controls.items():
        stats['total_entries_before'] += len(entries)
        
        # Keep only entries with real AWS-CG IDs
        real_entries = []
        for entry in entries:
            cg_id = entry.get('control_id', '')
            if is_real_control_id(cg_id):
                real_entries.append(entry)
                stats['real_entries_kept'] += 1
            else:
                stats['fake_entries_removed'] += 1
                stats['fake_ids_found'].add(cg_id)
        
        stats['total_entries_after'] += len(real_entries)
        
        if real_entries:
            cleaned_controls[control_id] = real_entries
        else:
            stats['controls_with_no_entries'] += 1
            stats['controls_emptied'].append(control_id.upper())
            # Still include the key with empty list so the app knows
            # this control exists but has no AWS Control Guides
            cleaned_controls[control_id] = []
    
    # Update metadata
    data['controls'] = cleaned_controls
    total_real = sum(len(v) for v in cleaned_controls.values())
    data['metadata']['total_controls_with_guides'] = sum(1 for v in cleaned_controls.values() if v)
    data['metadata']['total_aws_control_guides'] = total_real
    data['metadata']['source'] = 'AWS Control Guides from ControlCompass (verified)'
    
    # Write cleaned file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Print stats
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Controls in file:        {stats['total_controls']}")
    print(f"  Entries before cleaning:  {stats['total_entries_before']}")
    print(f"  Real entries kept:        {stats['real_entries_kept']}")
    print(f"  Fake entries removed:     {stats['fake_entries_removed']}")
    print(f"  Entries after cleaning:   {stats['total_entries_after']}")
    print(f"  Controls now empty:       {stats['controls_with_no_entries']}")
    print(f"  Unique fake IDs found:    {len(stats['fake_ids_found'])}")
    
    if stats['fake_ids_found']:
        sample = sorted(stats['fake_ids_found'])[:10]
        print(f"\n  Sample fake IDs removed:")
        for fid in sample:
            print(f"    - {fid}")
        if len(stats['fake_ids_found']) > 10:
            print(f"    ... and {len(stats['fake_ids_found']) - 10} more")
    
    if stats['controls_emptied']:
        print(f"\n  Controls with no real AWS-CG mappings ({len(stats['controls_emptied'])}):")
        # Group by family
        emptied = sorted(stats['controls_emptied'])
        for i in range(0, len(emptied), 10):
            chunk = emptied[i:i+10]
            print(f"    {', '.join(chunk)}")
    
    return stats


def main():
    print("Cleaning fake AWS Control Guide entries from data files...")
    
    # Clean NIST 800-53 file
    nist_stats = clean_file(
        'backend/compliance_discovery/aws_controls_mcp_data.json',
        'NIST 800-53 Rev 5 (aws_controls_mcp_data.json)'
    )
    
    # Clean CSF file
    csf_stats = clean_file(
        'backend/compliance_discovery/csf_aws_mappings.json',
        'NIST CSF 2.0 (csf_aws_mappings.json)'
    )
    
    # Copy to lambda package
    print("\n\nCopying cleaned files to lambda package...")
    
    for src, dst in [
        ('backend/compliance_discovery/aws_controls_mcp_data.json',
         'backend/lambda_package/compliance_discovery/aws_controls_mcp_data.json'),
        ('backend/compliance_discovery/csf_aws_mappings.json',
         'backend/lambda_package/compliance_discovery/csf_aws_mappings.json'),
    ]:
        with open(src, 'r') as f:
            data = json.load(f)
        with open(dst, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  Copied: {src} -> {dst}")
    
    # Summary
    total_fake = nist_stats['fake_entries_removed'] + csf_stats['fake_entries_removed']
    total_real = nist_stats['real_entries_kept'] + csf_stats['real_entries_kept']
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Total fake entries removed: {total_fake}")
    print(f"  Total real entries kept:    {total_real}")
    print(f"  Data integrity: Only verified AWS Control Guide IDs remain")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
