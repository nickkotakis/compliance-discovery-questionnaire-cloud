# MCP Data Example: AC-2 (Account Management)

## NIST Control: AC-2 - Account Management

When a consultant clicks on AC-2 in your compliance tool, here's the rich AWS guidance they receive from the MCP:

---

## 🟢 SHARED RESPONSIBILITY
AWS provides the services listed below. You must configure and use them properly in your AWS environment to meet this requirement.

---

## AWS Control Guides for AC-2

### 1. Enable MFA for IAM Users with Console Password
**Control ID**: AWS-CG-0000138

**Description**: Enable MFA for IAM users that have a console password in order to strengthen user authentication.

**AWS Service**: AWS Identity and Access Management

**Managed Controls**:
- **Config Rule**: `MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS`
- **Security Hub**: `IAM.5`
- **Control Tower**: 
  - `AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS`
  - `SH.IAM.5`

**Framework Mappings**:
- NIST-SP-800-53-r5: IA-2(1), IA-2(6), IA-2(2)
- PCI-DSS-v4.0: 8.4.1, 8.4.2, 8.4.3
- SOC 2: CC6.1, CC6.6
- CIS AWS Benchmark v1.4: 1.10
- FedRAMP-r4: IA-2(1), IA-2(2), IA-2(3)

**AWS API Calls for Validation**:
```
iam:ListUsers
iam:GetUser
iam:ListMFADevices
iam:GetLoginProfile
iam:GetAccountSummary
```

---

### 2. Ensure IAM User Groups Contain Users
**Control ID**: AWS-CG-0000183

**Description**: Ensure that all IAM user groups contain users, or remove empty user groups when no longer needed so the groups cannot be used to unintentionally grant access.

**AWS Service**: AWS Identity and Access Management

**Managed Controls**:
- **Config Rule**: `IAM_GROUP_HAS_USERS_CHECK`
- **Control Tower**: `CONFIG.IAM.DT.6`

**Framework Mappings**:
- NIST-SP-800-53-r5: AC-2
- ACSC-ISM-02-Mar-2023

---

### 3. Prevent IAM Inline Policies from Using Wildcard Permissions
**Control ID**: AWS-CG-0000479

**Description**: Restrict IAM inline policies from including 'Effect' 'Allow' with 'Action' '*' over 'Resource' '*' to enforce least privilege access. This validation ensures IAM policies grant only the specific permissions required to perform tasks rather than full administrative privileges, reducing the risk of unauthorized access and resource exposure.

**AWS Service**: AWS Identity and Access Management

**Managed Controls**:
- **Control Tower**: `CT.IAM.PR.1`

**Framework Mappings**:
- NIST-SP-800-53-r5: AC-2, AC-6
- PCI-DSS-v4.0: 7.2.1, 7.2.2
- SOC 2: CC6.1, CC6.3
- CIS AWS Benchmark v1.4: 1.16
- FedRAMP-r4: AC-2, AC-6

---

### 4. Enforce Strong IAM Password Policies
**Control ID**: AWS-CG-0000575

**Description**: Requires IAM user password policies to implement strong configurations, preventing the use of weak passwords and reducing the risk of unauthorized access.

**AWS Service**: AWS Identity and Access Management

**Managed Controls**:
- **Security Hub**: `IAM.7`

**Framework Mappings**:
- NIST-SP-800-53-r5: IA-5(1)
- PCI-DSS-v4.0: 8.3.6
- CIS AWS Benchmark v1.4: 1.8
- FedRAMP-r4: IA-5(1)

---

### 5. Enforce Password Complexity Requirements
**Control IDs**: AWS-CG-0000581, AWS-CG-0000574

**Description**: Enforces that IAM password policies require uppercase and lowercase letters in passwords to strengthen authentication security.

**AWS Service**: AWS Identity and Access Management

**Managed Controls**:
- **Security Hub**: `IAM.11`, `IAM.12`

**Framework Mappings**:
- NIST-SP-800-53-r5: IA-5(1)
- PCI-DSS-v4.0: 8.3.6

---

## Summary for AC-2

### AWS Services to Implement
- ✅ **AWS Identity and Access Management (IAM)**

### Config Rules to Enable
1. `MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS` - Ensures MFA is enabled for console users
2. `IAM_GROUP_HAS_USERS_CHECK` - Prevents empty groups that could grant unintended access

### Security Hub Controls to Monitor
1. `IAM.5` - IAM users should have MFA enabled
2. `IAM.7` - Password policies should meet requirements
3. `IAM.11` - Password policy should require uppercase letters
4. `IAM.12` - Password policy should require lowercase letters

### Control Tower Controls (if using Control Tower)
1. `AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS` - Detect IAM users without MFA
2. `CONFIG.IAM.DT.6` - Detect empty IAM groups
3. `CT.IAM.PR.1` - Prevent wildcard permissions in inline policies
4. `SH.IAM.5` - Ensure MFA for console access

### Evidence Collection
Use these AWS API calls to gather evidence:
```bash
# List all IAM users
aws iam list-users

# Check MFA status for each user
aws iam list-mfa-devices --user-name <username>

# Get password policy
aws iam get-account-password-policy

# List IAM groups
aws iam list-groups

# Check group membership
aws iam get-group --group-name <groupname>
```

---

## How This Helps Your Clients

### Before MCP Integration
"You need to implement account management controls in AWS."

### After MCP Integration
"For AC-2, enable these 4 specific Config rules, monitor these 4 Security Hub controls, and use these exact AWS CLI commands to collect evidence. Here are the Control Tower controls if you're using AWS Control Tower. These map to PCI-DSS 8.4.1-8.4.3 and SOC 2 CC6.1."

**Result**: Your clients get actionable, specific guidance instead of generic advice.

---

## Comparison: Manual vs MCP Data

| Aspect | Manual Mapping | MCP Data |
|--------|---------------|----------|
| **Services** | "IAM" | "AWS Identity and Access Management" |
| **Config Rules** | Generic mention | Exact rule names: `MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS` |
| **Security Hub** | Not specified | Specific control IDs: `IAM.5`, `IAM.7`, `IAM.11`, `IAM.12` |
| **Control Tower** | Not available | 4 specific control IDs with descriptions |
| **Framework Mappings** | Single framework | 14 frameworks with specific control mappings |
| **API Calls** | Not provided | Exact API calls with JSONPath queries |
| **Evidence** | Generic guidance | Specific CLI commands |

---

## Real-World Usage Scenario

**Consultant**: "Let's look at AC-2 for your AWS environment."

**Client**: "What do we need to do?"

**Consultant** (using MCP data): 
1. "First, enable the Config rule `MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS` to continuously monitor MFA usage."
2. "Second, check Security Hub control IAM.5 - it will show you which users don't have MFA."
3. "Third, if you're using Control Tower, enable `AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS` for automated enforcement."
4. "Here's the exact AWS CLI command to collect evidence for auditors..."

**Client**: "That's exactly what we needed! Much clearer than our last assessment."

---

This is the power of MCP integration - transforming generic compliance advice into specific, actionable AWS implementation guidance.
