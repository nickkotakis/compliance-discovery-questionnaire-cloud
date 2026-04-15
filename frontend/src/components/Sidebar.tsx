import React from 'react';
import SideNavigation from '@cloudscape-design/components/side-navigation';

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  controlCount: number;
  completionRate: number;
  activeEngagementName?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ 
  activeView, 
  onViewChange, 
  controlCount, 
  completionRate,
  activeEngagementName,
}) => {
  const engagementLabel = activeEngagementName
    ? `📋 ${activeEngagementName}`
    : '📋 No engagement selected';

  return (
    <SideNavigation
      activeHref={`#${activeView}`}
      header={{ href: '#', text: 'Compliance Discovery' }}
      items={[
        { type: 'section', text: 'Assessment', items: [
          { type: 'link', text: 'Dashboard', href: '#dashboard' },
          { type: 'link', text: 'Questionnaire', href: '#questionnaire' },
        ]},
        { type: 'divider' },
        { type: 'section', text: `Engagement PM`, items: [
          { type: 'link', text: engagementLabel, href: '#engagement-setup' },
          { type: 'link', text: '🤖 AI Assistant', href: '#ai-assistant' },
          { type: 'link', text: 'Engagement Schedule', href: '#schedule' },
          { type: 'link', text: 'Evidence Tracker', href: '#evidence' },
          { type: 'link', text: 'Facilitation Guide', href: '#facilitation' },
        ]},
        { type: 'divider' },
        { type: 'section', text: 'Configuration', items: [
          { type: 'link', text: 'Settings', href: '#settings' },
        ]},
        { type: 'divider' },
        { type: 'section', text: 'Statistics', items: [
          { type: 'link', text: `Controls: ${controlCount}`, href: '#', info: <span>{controlCount} total</span> },
          { type: 'link', text: `Progress: ${completionRate}%`, href: '#', info: <span>{completionRate}% complete</span> },
        ]},
      ]}
      onFollow={(event) => {
        event.preventDefault();
        const view = event.detail.href.replace('#', '');
        if (view && view !== activeView) onViewChange(view);
      }}
    />
  );
};

export default Sidebar;
