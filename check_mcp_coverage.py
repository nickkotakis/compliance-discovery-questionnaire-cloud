import json
from collections import defaultdict

with open('backend/compliance_discovery/aws_controls_mcp_data.json') as f:
    data = json.load(f)

controls = data.get('controls', {})
total = len(controls)
has_any_managed = 0
has_config = 0
has_securityhub = 0
has_controltower = 0
empty_managed = []
total_config = 0
total_sh = 0
total_ct = 0

for cid, entries in controls.items():
    ctrl_has_config = False
    ctrl_has_sh = False
    ctrl_has_ct = False
    for e in entries:
        cr = e.get('config_rules', [])
        sh = e.get('security_hub_controls', [])
        ct = e.get('control_tower_ids', [])
        total_config += len(cr)
        total_sh += len(sh)
        total_ct += len(ct)
        if cr:
            ctrl_has_config = True
        if sh:
            ctrl_has_sh = True
        if ct:
            ctrl_has_ct = True
    if ctrl_has_config:
        has_config += 1
    if ctrl_has_sh:
        has_securityhub += 1
    if ctrl_has_ct:
        has_controltower += 1
    if ctrl_has_config or ctrl_has_sh or ctrl_has_ct:
        has_any_managed += 1
    else:
        empty_managed.append(cid.upper())

print(f'Total controls in MCP data: {total}')
print(f'Controls with ANY managed controls: {has_any_managed}/{total} ({has_any_managed*100//total}%)')
print(f'  With Config rules: {has_config} (total rules: {total_config})')
print(f'  With Security Hub: {has_securityhub} (total controls: {total_sh})')
print(f'  With Control Tower: {has_controltower} (total IDs: {total_ct})')
print(f'Controls with NO managed controls: {len(empty_managed)}')

families = defaultdict(list)
for c in sorted(empty_managed):
    fam = c.split('-')[0]
    families[fam].append(c)
for fam in sorted(families):
    print(f'  {fam}: {", ".join(families[fam])}')
