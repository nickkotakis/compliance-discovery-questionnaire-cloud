"""Human-friendly control descriptions for NIST 800-53 controls.

These descriptions focus on PURPOSE and IMPLEMENTATION rather than
technical compliance language.
"""

CONTROL_DESCRIPTIONS = {
    # Access Control (AC)
    'ac-1': 'Establish and maintain formal access control policies and procedures. Define who can access what, under what conditions, and document how access decisions are made.',
    'ac-2': 'Manage user accounts throughout their lifecycle - creation, modification, enabling, disabling, and removal. Ensure only authorized individuals have accounts and access is appropriate to their role.',
    'ac-3': 'Enforce approved authorizations for accessing information and system resources. Implement technical controls that prevent unauthorized access even if someone has an account.',
    'ac-4': 'Control the flow of information within systems and between interconnected systems. Prevent unauthorized information transfer and enforce security policies on data movement.',
    'ac-5': 'Implement separation of duties to prevent any single person from having too much control. Divide critical functions among different people to reduce fraud and error risk.',
    'ac-6': 'Apply the principle of least privilege - users and processes should have only the minimum access needed to perform their job. Regularly review and adjust privileges.',
    'ac-7': 'Enforce limits on consecutive failed login attempts. Lock accounts or delay login after repeated failures to prevent password guessing attacks.',
    'ac-8': 'Display system use notifications and consent warnings before granting access. Inform users of monitoring, acceptable use, and legal consequences.',
    'ac-11': 'Automatically lock user sessions after a period of inactivity. Require re-authentication to resume work, protecting against unauthorized access to unattended workstations.',
    'ac-12': 'Automatically terminate user sessions after defined conditions (time limits, inactivity). Prevent indefinite sessions that increase security risk.',
    'ac-14': 'Identify and control actions users can perform without authentication. Minimize unauthenticated access to only what is absolutely necessary.',
    'ac-17': 'Establish usage restrictions, configuration requirements, and implementation guidance for remote access. Secure connections from outside the organization.',
    'ac-18': 'Define usage restrictions and implementation guidance for wireless access. Protect against unauthorized wireless connections and eavesdropping.',
    'ac-19': 'Establish usage restrictions and implementation guidance for mobile devices. Protect organizational data on smartphones, tablets, and laptops.',
    'ac-20': 'Establish terms and conditions for authorized use of external systems. Control access to organizational information from systems you don\'t control.',
    'ac-22': 'Designate individuals authorized to make information publicly accessible. Ensure only approved information is released and review before posting.',
    
    # Awareness and Training (AT)
    'at-1': 'Establish and maintain security awareness and training policies and procedures. Define how the organization educates personnel about security.',
    'at-2': 'Provide basic security awareness training to all users. Ensure everyone understands their security responsibilities and common threats.',
    'at-3': 'Provide role-based security training for personnel with specific security responsibilities. Ensure security staff have appropriate knowledge and skills.',
    'at-4': 'Provide training on recognizing and reporting potential security incidents. Ensure personnel know what to look for and who to contact.',
    
    # Audit and Accountability (AU)
    'au-1': 'Establish and maintain audit and accountability policies and procedures. Define what gets logged, how logs are protected, and who reviews them.',
    'au-2': 'Determine which events must be audited and logged. Identify security-relevant activities that need to be tracked for investigation and compliance.',
    'au-3': 'Ensure audit records contain sufficient information to establish what happened, when, where, who, and the outcome. Enable effective investigation and analysis.',
    'au-4': 'Allocate sufficient audit record storage capacity. Prevent audit failure due to lack of space, which could hide security incidents.',
    'au-5': 'Alert appropriate personnel when audit processing failures occur. Ensure audit system problems are detected and addressed promptly.',
    'au-6': 'Review and analyze audit records regularly for inappropriate or unusual activity. Detect security incidents and policy violations.',
    'au-7': 'Provide audit reduction and report generation capability. Enable security staff to analyze large volumes of audit data effectively.',
    'au-8': 'Use synchronized system clocks to generate timestamps for audit records. Ensure accurate time correlation across systems for investigation.',
    'au-9': 'Protect audit information and tools from unauthorized access, modification, and deletion. Prevent attackers from covering their tracks.',
    'au-11': 'Retain audit records for a defined time period. Support after-the-fact investigations, forensics, and compliance requirements.',
    'au-12': 'Generate audit records for defined auditable events. Implement the technical capability to create logs of security-relevant activities.',
    
    # Assessment, Authorization, and Monitoring (CA)
    'ca-1': 'Establish and maintain assessment, authorization, and monitoring policies and procedures. Define how security controls are tested and systems are authorized.',
    'ca-2': 'Conduct periodic assessments of security controls. Verify controls are implemented correctly and operating as intended.',
    'ca-3': 'Authorize connections between systems and external services. Ensure interconnections meet security requirements before allowing data exchange.',
    'ca-5': 'Develop and maintain a plan of action and milestones for security weaknesses. Track remediation of identified vulnerabilities and deficiencies.',
    'ca-6': 'Provide security authorization for systems to operate. Ensure senior management accepts the risk before systems process organizational data.',
    'ca-7': 'Continuously monitor security controls and system security posture. Detect changes that affect security and respond to emerging threats.',
    'ca-9': 'Authorize internal system connections. Control how system components connect and communicate with each other.',
    
    # Configuration Management (CM)
    'cm-1': 'Establish and maintain configuration management policies and procedures. Define how systems are configured, changed, and documented.',
    'cm-2': 'Develop, document, and maintain baseline configurations for systems. Establish approved settings and track authorized changes.',
    'cm-3': 'Control changes to systems through formal change management. Ensure changes are reviewed, approved, tested, and documented.',
    'cm-4': 'Monitor changes to systems and alert on unauthorized modifications. Detect configuration drift and unapproved changes.',
    'cm-5': 'Define, document, approve, and enforce access restrictions for changing systems. Prevent unauthorized configuration changes.',
    'cm-6': 'Establish and document configuration settings for systems. Define secure settings and ensure they are implemented.',
    'cm-7': 'Restrict, disable, or prevent the use of unnecessary functions, ports, protocols, and services. Reduce attack surface by removing what isn\'t needed.',
    'cm-8': 'Develop and maintain an inventory of system components. Know what hardware and software exists in your environment.',
    'cm-10': 'Restrict, disable, or prevent software installation by users. Control what software runs on organizational systems.',
    'cm-11': 'Employ automated mechanisms to install software updates and patches. Ensure systems are kept current with security fixes.',
    
    # Contingency Planning (CP)
    'cp-1': 'Establish and maintain contingency planning policies and procedures. Define how the organization prepares for and responds to disruptions.',
    'cp-2': 'Develop and maintain contingency plans for systems. Document how to respond to disruptions and restore operations.',
    'cp-3': 'Train personnel on their contingency roles and responsibilities. Ensure staff know what to do during disruptions.',
    'cp-4': 'Test contingency plans regularly to identify weaknesses. Verify plans work and personnel can execute them effectively.',
    'cp-6': 'Establish alternate storage sites for backup information. Ensure data can be recovered if primary site is unavailable.',
    'cp-7': 'Establish alternate processing sites for critical systems. Ensure operations can continue if primary site is unavailable.',
    'cp-9': 'Conduct backups of information, software, and system images. Protect against data loss from failures, attacks, or disasters.',
    'cp-10': 'Provide for recovery and reconstitution of systems to a known state. Ensure systems can be restored after disruptions.',
    
    # Identification and Authentication (IA)
    'ia-1': 'Establish and maintain identification and authentication policies and procedures. Define how users and devices prove their identity.',
    'ia-2': 'Uniquely identify and authenticate users and processes. Ensure you know who or what is accessing your systems.',
    'ia-3': 'Uniquely identify and authenticate devices before establishing connections. Prevent unauthorized devices from accessing the network.',
    'ia-4': 'Manage user identifiers by disabling inactive accounts and preventing reuse. Maintain accurate user identity information.',
    'ia-5': 'Manage authenticators (passwords, tokens, certificates) securely. Protect credentials from compromise and enforce strength requirements.',
    'ia-6': 'Obscure feedback of authentication information during the authentication process. Prevent shoulder surfing and credential exposure.',
    'ia-7': 'Implement cryptographic mechanisms for authentication. Use strong cryptography to verify identity and protect credentials.',
    'ia-8': 'Uniquely identify and authenticate non-organizational users. Control access by external users, contractors, and partners.',
    'ia-11': 'Require re-authentication when changing to privileged functions or roles. Verify identity before granting elevated access.',
    
    # Incident Response (IR)
    'ir-1': 'Establish and maintain incident response policies and procedures. Define how the organization detects, responds to, and recovers from security incidents.',
    'ir-2': 'Provide incident response training to personnel. Ensure staff can recognize and respond appropriately to security incidents.',
    'ir-3': 'Test incident response capability regularly. Verify the organization can effectively handle security incidents.',
    'ir-4': 'Implement incident handling capability for security incidents. Establish processes to detect, analyze, contain, eradicate, and recover from incidents.',
    'ir-5': 'Track and document security incidents. Maintain records for analysis, reporting, and lessons learned.',
    'ir-6': 'Report security incidents to appropriate authorities. Ensure incidents are escalated and reported as required.',
    'ir-7': 'Provide incident response assistance to users. Help personnel report and respond to suspected security incidents.',
    'ir-8': 'Establish an incident response plan. Document roles, procedures, and resources for handling security incidents.',
    
    # Maintenance (MA)
    'ma-1': 'Establish and maintain system maintenance policies and procedures. Define how systems are maintained, serviced, and repaired.',
    'ma-2': 'Schedule, perform, and document system maintenance and repairs. Ensure systems are properly maintained and changes are tracked.',
    'ma-3': 'Approve, control, and monitor maintenance tools. Prevent malicious tools and ensure maintenance doesn\'t introduce vulnerabilities.',
    'ma-4': 'Approve and monitor nonlocal maintenance and diagnostic activities. Control remote maintenance access and protect against unauthorized access.',
    'ma-5': 'Require approval and control of maintenance personnel. Ensure only authorized individuals perform maintenance.',
    'ma-6': 'Obtain maintenance support and spare parts within defined timeframes. Ensure systems can be repaired promptly to maintain availability.',
    
    # Media Protection (MP)
    'mp-1': 'Establish and maintain media protection policies and procedures. Define how physical and digital media are protected, used, and disposed of.',
    'mp-2': 'Restrict access to media containing organizational information. Prevent unauthorized access to removable media and backups.',
    'mp-3': 'Mark media indicating distribution limitations and handling caveats. Ensure media is labeled with appropriate security markings.',
    'mp-4': 'Physically control and securely store media. Protect media from unauthorized access, damage, and theft.',
    'mp-5': 'Protect and control media during transport outside controlled areas. Ensure media is secured during shipping and movement.',
    'mp-6': 'Sanitize or destroy media before disposal or reuse. Prevent data recovery from discarded or repurposed media.',
    'mp-7': 'Prohibit or restrict the use of portable storage devices. Control removable media to prevent data exfiltration and malware introduction.',
    
    # Physical and Environmental Protection (PE)
    'pe-1': 'Establish and maintain physical and environmental protection policies and procedures. Define how facilities and systems are physically secured.',
    'pe-2': 'Develop and maintain physical access authorizations. Control who can physically access facilities and areas.',
    'pe-3': 'Enforce physical access authorizations at entry points. Verify identity and authorization before granting physical access.',
    'pe-4': 'Control physical access to information system distribution and transmission lines. Protect cables and network infrastructure from tampering, damage, and eavesdropping.',
    'pe-5': 'Control physical access to output devices. Prevent unauthorized individuals from accessing printers, displays, and other output.',
    'pe-6': 'Monitor physical access to facilities where systems reside. Detect and respond to physical security incidents.',
    'pe-8': 'Maintain visitor access records to facilities. Track who visits, when, and document their access.',
    'pe-9': 'Protect power equipment and cabling from damage and destruction. Ensure reliable power supply for systems.',
    'pe-10': 'Provide emergency shutoff capability for systems. Enable rapid power-off in emergencies to prevent damage or data loss.',
    'pe-11': 'Provide emergency power for systems. Ensure systems can operate or shut down gracefully during power failures.',
    'pe-12': 'Provide emergency lighting for areas containing systems. Enable safe evacuation and emergency operations during power failures.',
    'pe-13': 'Protect systems from fire damage. Implement fire detection and suppression systems.',
    'pe-14': 'Protect systems from environmental hazards. Control temperature, humidity, and other environmental factors.',
    'pe-15': 'Protect systems from water damage. Prevent damage from leaks, floods, and plumbing failures.',
    'pe-16': 'Control delivery and removal of system components. Prevent unauthorized removal or introduction of equipment.',
    'pe-17': 'Establish security controls for alternate work sites (remote work, home offices). Ensure employees working remotely have appropriate security measures in place.',
    
    # Planning (PL)
    'pl-1': 'Establish and maintain planning policies and procedures. Define how security planning is conducted and documented.',
    'pl-2': 'Develop and maintain security plans for systems. Document security requirements, controls, and responsibilities.',
    'pl-4': 'Establish and maintain rules of behavior for system users. Define acceptable use and security responsibilities.',
    'pl-8': 'Develop and maintain security architectures for systems. Design security into systems from the beginning.',
    
    # Program Management (PM)
    'pm-1': 'Establish and maintain an information security program. Provide organization-wide security governance and oversight.',
    'pm-2': 'Designate a senior information security officer. Ensure executive-level responsibility for security program.',
    'pm-3': 'Establish an information security resources allocation process. Ensure adequate funding and resources for security.',
    'pm-4': 'Establish a plan of action and milestones process. Track and manage security weaknesses organization-wide.',
    'pm-5': 'Establish an inventory of information systems. Maintain awareness of all systems processing organizational information.',
    'pm-6': 'Establish measures for security program effectiveness. Monitor and report on security program performance.',
    'pm-7': 'Establish an enterprise architecture with security considerations. Integrate security into organizational planning and design.',
    'pm-9': 'Establish a risk management strategy. Define how the organization identifies, assesses, and responds to risk.',
    'pm-10': 'Establish a security authorization process. Define how systems are authorized to operate.',
    'pm-11': 'Establish a mission/business process definition. Understand what the organization does to inform security decisions.',
    
    # Personnel Security (PS)
    'ps-1': 'Establish and maintain personnel security policies and procedures. Define security requirements for personnel throughout their lifecycle.',
    'ps-2': 'Assign risk designations to positions. Determine security requirements based on position sensitivity.',
    'ps-3': 'Screen individuals before authorizing access. Conduct background checks appropriate to position risk.',
    'ps-4': 'Terminate or revoke access when employment ends. Ensure former personnel cannot access organizational resources.',
    'ps-5': 'Review and update personnel access authorizations regularly. Ensure access remains appropriate as roles change.',
    'ps-6': 'Establish access agreements for personnel. Document security responsibilities and acceptable use requirements.',
    'ps-7': 'Establish personnel sanctions for security violations. Define consequences for failing to comply with security policies.',
    'ps-8': 'Establish personnel sanctions for security policy violations. Enforce consequences for security non-compliance.',
    
    # Risk Assessment (RA)
    'ra-1': 'Establish and maintain risk assessment policies and procedures. Define how the organization identifies and evaluates security risks.',
    'ra-2': 'Categorize systems based on impact of loss. Determine security requirements based on potential harm.',
    'ra-3': 'Conduct risk assessments regularly. Identify threats, vulnerabilities, likelihood, and impact to inform security decisions.',
    'ra-5': 'Scan for vulnerabilities in systems and applications. Identify security weaknesses that could be exploited.',
    'ra-7': 'Employ threat intelligence to inform security decisions. Stay aware of current threats and attack methods.',
    
    # System and Services Acquisition (SA)
    'sa-1': 'Establish and maintain system and services acquisition policies and procedures. Define security requirements for acquiring systems and services.',
    'sa-2': 'Allocate resources for information security in system development lifecycle. Ensure security is funded and planned.',
    'sa-3': 'Manage systems using a system development lifecycle methodology. Integrate security throughout development.',
    'sa-4': 'Include security requirements in acquisition contracts. Ensure vendors and developers meet security needs.',
    'sa-5': 'Obtain developer security documentation for systems. Ensure adequate information for secure operation and maintenance.',
    'sa-8': 'Employ security engineering principles in system design and development. Build security in from the start.',
    'sa-9': 'Require external service providers to comply with security requirements. Ensure third parties protect organizational information.',
    'sa-10': 'Require developers to configure systems securely. Ensure systems are delivered in a secure state.',
    'sa-11': 'Require developers to test security functionality and identify flaws. Verify security controls work as intended.',
    'sa-15': 'Require developers to follow secure development practices. Ensure code is developed securely.',
    'sa-22': 'Replace unsupported system components. Ensure systems use supported software and hardware.',
    
    # System and Communications Protection (SC)
    'sc-1': 'Establish and maintain system and communications protection policies and procedures. Define how systems and networks are protected.',
    'sc-2': 'Separate user functionality from system management functionality. Reduce risk from user actions affecting system operations.',
    'sc-4': 'Prevent unauthorized information disclosure through shared resources. Protect against information leakage.',
    'sc-5': 'Protect against denial of service attacks. Ensure systems remain available during attacks.',
    'sc-7': 'Monitor and control communications at system boundaries. Implement firewalls and boundary protection.',
    'sc-8': 'Protect the confidentiality and integrity of transmitted information. Encrypt sensitive data in transit.',
    'sc-10': 'Terminate network connections at the end of sessions. Prevent session hijacking and unauthorized reuse.',
    'sc-12': 'Establish and manage cryptographic keys. Ensure encryption keys are generated, distributed, and protected properly.',
    'sc-13': 'Use validated cryptography to protect information. Employ proven encryption algorithms and implementations.',
    'sc-15': 'Prohibit remote activation of collaborative computing devices. Prevent unauthorized audio/video capture.',
    'sc-17': 'Issue public key certificates or obtain them from approved providers. Enable secure communications and authentication.',
    'sc-18': 'Protect mobile code from unauthorized modification. Ensure downloaded code hasn\'t been tampered with.',
    'sc-20': 'Provide authoritative DNS servers that deliver authenticated and integrity-protected responses using DNSSEC. Ensure external clients can trust DNS information your organization publishes.',
    'sc-21': 'Verify authenticity and integrity of DNS responses using DNSSEC. Protect against DNS spoofing, cache poisoning, and man-in-the-middle attacks on name resolution.',
    'sc-22': 'Protect system architecture and design information. Prevent attackers from learning system details.',
    'sc-23': 'Protect session authenticity. Prevent session hijacking and man-in-the-middle attacks.',
    'sc-28': 'Protect the confidentiality and integrity of information at rest. Encrypt sensitive stored data.',
    'sc-39': 'Maintain separate execution domains for processes. Isolate processes to prevent interference and privilege escalation.',
    
    # System and Information Integrity (SI)
    'si-1': 'Establish and maintain system and information integrity policies and procedures. Define how systems and data are protected from corruption.',
    'si-2': 'Identify, report, and correct system flaws. Implement patch management and vulnerability remediation.',
    'si-3': 'Implement malicious code protection. Deploy and maintain antivirus and anti-malware solutions.',
    'si-4': 'Monitor systems to detect attacks and unauthorized activities. Implement intrusion detection and security monitoring.',
    'si-5': 'Receive security alerts and advisories and take action. Stay informed about vulnerabilities and threats.',
    'si-6': 'Verify security functionality of systems. Test that security controls are working correctly.',
    'si-7': 'Employ integrity verification tools. Detect unauthorized changes to software and information.',
    'si-8': 'Protect against spam and malicious content. Filter email and web content for threats.',
    'si-10': 'Check information for validity, completeness, and authenticity. Validate inputs to prevent attacks.',
    'si-11': 'Identify and handle error conditions securely. Prevent errors from revealing sensitive information or creating vulnerabilities.',
    'si-12': 'Handle and retain information within systems. Manage information lifecycle securely.',
    'si-16': 'Protect system memory from unauthorized code execution. Prevent buffer overflow and similar attacks.',
    
    # Supply Chain Risk Management (SR)
    'sr-1': 'Establish and maintain supply chain risk management policies and procedures. Define how supply chain risks are identified and mitigated.',
    'sr-2': 'Conduct supply chain risk assessments. Identify and evaluate risks from suppliers and supply chain.',
    'sr-3': 'Require suppliers to implement security controls. Ensure supply chain partners meet security requirements.',
    'sr-5': 'Require suppliers to notify of security incidents and vulnerabilities. Ensure timely awareness of supply chain issues.',
    'sr-6': 'Test and validate security functionality of system components. Verify components work securely before deployment.',
    'sr-8': 'Require suppliers to notify of counterfeit components. Protect against fake or compromised hardware/software.',
    'sr-11': 'Establish and maintain a component inventory. Track hardware and software components throughout lifecycle.',
}


def get_control_description(control_id: str) -> str:
    """Get human-friendly description for a control.
    
    Args:
        control_id: NIST control ID (e.g., "AC-1" or "ac-1")
        
    Returns:
        Human-friendly description or None if not found
    """
    return CONTROL_DESCRIPTIONS.get(control_id.lower())
