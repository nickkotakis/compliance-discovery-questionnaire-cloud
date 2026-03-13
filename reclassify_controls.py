#!/usr/bin/env python3
"""Reclassify AWS controls with a simpler, more defensible approach.

New logic:
- Core: Controls with AWS Config rules that provide automated validation.
  If a subcategory has any controls with Config rules, the top ones are core.
  Config rules = AWS built automated compliance checking for it.
- Recommended: Controls with Security Hub, Control Tower, or meaningful
  framework coverage but no Config rules. Still important, just not
  automatable via Config.
- Enhanced: Synthetic controls (no Config rules, no Security Hub, no
  Control Tower) or very niche service-specific controls.

Within each tier, controls are sorted by framework count (descending)
as a tiebreaker — more framework coverage = more broadly applicable.

Per-subcategory guarantee: if a subcategory has ANY controls with Config
rules, at least one will be core.
"""

import json


def classify_control(control):
    """Classify a single control."""
    config_rules = control.get('config_rules', [])
    security_hub = control.get('security_hub_controls', [])
    control_tower = control.get('control_tower_ids', [])
    frameworks = control.get('frameworks', [])

    # Synthetic controls (ID >= 785) with no managed controls = enhanced
    cid_num = int(control['control_id'].replace('AWS-CG-', ''))
    is_synthetic = cid_num >= 785

    has_config = len(config_rules) > 0
    has_security_hub = len(security_hub) > 0
    has_control_tower = len(control_tower) > 0
    fw_count = len(frameworks)

    if is_synthetic and not has_config and not has_security_hub:
        return 'enhanced'

    # Core: has Config rules (automated validation available)
    if has_config:
        return 'core'

    # Recommended: has Security Hub or Control Tower (managed controls
    # exist but no Config rule), or has meaningful framework coverage
    if has_security_hub or has_control_tower:
        return 'recommended'

    if fw_count >= 3:
        return 'recommended'

    # Enhanced: everything else
    return 'enhanced'


def main():
    path = 'backend/compliance_discovery/csf_aws_mappings.json'
    with open(path) as f:
        data = json.load(f)

    stats = {'core': 0, 'recommended': 0, 'enhanced': 0}
    subcats_with_core = 0
    subcats_without_core = 0
    total_subcats = 0

    for key in sorted(data['controls'].keys()):
        controls = data['controls'][key]
        if not controls:
            continue

        total_subcats += 1

        # Classify each control
        for c in controls:
            c['priority'] = classify_control(c)
            stats[c['priority']] += 1

        # Sort: core first, then recommended, then enhanced
        # Within each tier, sort by framework count descending
        def sort_key(c):
            tier_order = {'core': 0, 'recommended': 1, 'enhanced': 2}
            return (tier_order[c['priority']], -len(c.get('frameworks', [])))

        data['controls'][key] = sorted(controls, key=sort_key)

        has_core = any(c['priority'] == 'core' for c in controls)
        if has_core:
            subcats_with_core += 1
        else:
            subcats_without_core += 1

    total = sum(stats.values())
    print(f'Classification results ({total} total):')
    print(f'  Core:        {stats["core"]}')
    print(f'  Recommended: {stats["recommended"]}')
    print(f'  Enhanced:    {stats["enhanced"]}')
    print()
    print(f'Subcategories: {total_subcats}')
    print(f'  With core:    {subcats_with_core}')
    print(f'  Without core: {subcats_without_core}')

    # Show subcategories without core
    if subcats_without_core > 0:
        print()
        print('Subcategories without core:')
        for key, controls in sorted(data['controls'].items()):
            if not controls:
                continue
            if not any(c['priority'] == 'core' for c in controls):
                tiers = {}
                for c in controls:
                    tiers[c['priority']] = tiers.get(c['priority'], 0) + 1
                print(f'  {key}: {tiers}')
                for c in controls[:2]:
                    print(f'    {c["control_id"]}: {c["title"][:50]} (rules={c.get("config_rules", [])[:1]})')

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'\nSaved to {path}')


if __name__ == '__main__':
    main()
