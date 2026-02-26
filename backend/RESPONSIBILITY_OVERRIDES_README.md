# AWS Responsibility Override Configuration

## Quick Start

1. Copy the example file:
   ```bash
   cp responsibility_overrides.example.json responsibility_overrides.json
   ```

2. Edit `responsibility_overrides.json` with your overrides:
   ```json
   {
     "ac-1": "shared",
     "pe-17": "customer"
   }
   ```

3. Restart the backend server:
   ```bash
   python3 compliance_discovery/api_server.py
   ```

## File Format

```json
{
  "control-id": "responsibility-value"
}
```

- **Control IDs**: Lowercase NIST control IDs (e.g., `"ac-2"`, `"pe-1"`)
- **Responsibility Values**: `"aws"`, `"shared"`, or `"customer"`

## Examples

### Example 1: Hybrid Cloud Environment
```json
{
  "pe-17": "customer",
  "_comment": "We have on-premises infrastructure with remote workers"
}
```

### Example 2: Policy Controls Using AWS Organizations
```json
{
  "ac-1": "shared",
  "au-1": "shared",
  "cm-1": "shared",
  "cp-1": "shared",
  "ia-1": "shared",
  "ir-1": "shared",
  "ra-1": "shared",
  "sc-1": "shared",
  "si-1": "shared",
  "_comment": "We use AWS Organizations SCPs and Config to enforce these policy controls"
}
```

### Example 3: Extensive Use of AWS Managed Services
```json
{
  "si-1": "shared",
  "si-2": "shared",
  "si-3": "shared",
  "si-4": "shared",
  "_comment": "We use GuardDuty, Inspector, and Security Hub for all system integrity monitoring"
}
```

## Common Override Scenarios

### Scenario 1: Remote Work Policy (PE-17)
**Default**: AWS responsibility (AWS employee work sites)
**Override to Customer**: If you have remote workers accessing your AWS resources
```json
{
  "pe-17": "customer"
}
```

### Scenario 2: Policy Controls (AC-1, AU-1, CM-1, etc.)
**Default**: Customer responsibility (organizational policies)
**Override to Shared**: If you use AWS Organizations, Config, or Control Tower to enforce policies
```json
{
  "ac-1": "shared",
  "au-1": "shared",
  "cm-1": "shared"
}
```

### Scenario 3: On-Premises Maintenance
**Default**: AWS responsibility (AWS hardware maintenance)
**Override to Customer**: If you have on-premises infrastructure
```json
{
  "ma-2": "customer",
  "ma-3": "customer",
  "ma-4": "customer"
}
```

## Validation

The system will:
- ✅ Load overrides at startup
- ✅ Log the number of overrides loaded
- ✅ Log each override when applied to a control
- ✅ Fall back to defaults if override file doesn't exist
- ✅ Handle errors gracefully if JSON is invalid

Check the console output when starting the server:
```
Loaded 5 responsibility overrides from responsibility_overrides.json
Using override for AC-1: shared
Using override for PE-17: customer
```

## Troubleshooting

### Override not working?
1. Check file name is exactly `responsibility_overrides.json`
2. Verify JSON syntax is valid (use a JSON validator)
3. Ensure control IDs are lowercase
4. Restart the backend server
5. Check console for error messages

### Invalid JSON?
```bash
# Validate your JSON
python3 -m json.tool responsibility_overrides.json
```

### Need to reset to defaults?
```bash
# Simply remove or rename the override file
mv responsibility_overrides.json responsibility_overrides.json.backup
```

## Best Practices

1. **Document your rationale**: Use `_comment` fields to explain why you're overriding
2. **Review regularly**: Update overrides when your AWS architecture changes
3. **Coordinate with auditors**: Ensure your overrides align with auditor expectations
4. **Version control**: Keep your override file in version control (but not in public repos)
5. **Test changes**: Review the UI after applying overrides to ensure they appear correctly

## Security Considerations

- The override file is loaded at server startup only
- Changes require a server restart to take effect
- The file should be readable only by the application user
- Do not commit sensitive information in comments
- Consider using environment-specific override files for dev/staging/prod

## Integration with Compliance Assessment

Overrides affect:
- ✅ Responsibility badges in the UI (AWS Only / Shared / Customer Only)
- ✅ Applicability messages in control details
- ✅ Evidence requirements in questionnaires
- ✅ Export formats (PDF, Excel, YAML, JSON)

## Support

For questions or issues:
1. Review the main documentation: `AWS_RESPONSIBILITY_MAPPING.md`
2. Check the example file: `responsibility_overrides.example.json`
3. Examine the source code: `compliance_discovery/aws_control_mapping.py`

---

**Last Updated**: February 26, 2026
