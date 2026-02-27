# AWS Cloudscape Design System - Agent Core Instructions

## Overview

AWS Cloudscape is Amazon's official design system for building cloud applications and web experiences. It provides a comprehensive set of React components, design patterns, and guidelines specifically optimized for AWS console interfaces and enterprise cloud applications.

**Official Documentation**: https://cloudscape.design/

## When to Use Cloudscape

Use Cloudscape when building:
- AWS console interfaces and experiences
- Internal AWS tools and dashboards
- Enterprise cloud management applications
- Data-intensive applications requiring tables, forms, and complex layouts
- Applications requiring AWS visual consistency

## Core Design Principles

### 1. Customer-Centric Design
- Prioritize user tasks and workflows
- Minimize cognitive load
- Provide clear feedback and guidance
- Support both novice and expert users

### 2. Consistency
- Use standard Cloudscape components
- Follow established patterns
- Maintain visual and interaction consistency
- Align with AWS brand guidelines

### 3. Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support

### 4. Performance
- Optimized for large datasets
- Efficient rendering and updates
- Progressive loading patterns
- Responsive design

## Installation and Setup

### NPM Installation
```bash
npm install @cloudscape-design/components @cloudscape-design/global-styles
```

### Basic Setup
```typescript
import '@cloudscape-design/global-styles/index.css';
import { Button, Container, Header } from '@cloudscape-design/components';

function App() {
  return (
    <Container header={<Header variant="h1">My Application</Header>}>
      <Button variant="primary">Get Started</Button>
    </Container>
  );
}
```

## Component Categories

### Layout Components
- **AppLayout**: Main application shell with navigation, content, and tools panels
- **Container**: Content grouping with optional headers and footers
- **Grid**: Responsive grid system
- **SpaceBetween**: Consistent spacing between elements
- **ColumnLayout**: Multi-column layouts
- **Box**: Flexible container with spacing utilities

### Navigation Components
- **SideNavigation**: Primary navigation menu
- **BreadcrumbGroup**: Hierarchical navigation
- **Tabs**: Content organization
- **Pagination**: Page navigation for large datasets
- **Link**: Styled hyperlinks

### Data Display Components
- **Table**: Feature-rich data tables with sorting, filtering, pagination
- **Cards**: Grid-based content display
- **KeyValuePairs**: Label-value pair display
- **StatusIndicator**: Visual status representation
- **Badge**: Compact information display
- **ProgressBar**: Progress visualization

### Input Components
- **Input**: Text input fields
- **Textarea**: Multi-line text input
- **Select**: Dropdown selection
- **Multiselect**: Multiple option selection
- **Autosuggest**: Autocomplete input
- **DatePicker**: Date selection
- **TimePicker**: Time selection
- **Checkbox**: Boolean selection
- **RadioGroup**: Single option from multiple choices
- **Toggle**: On/off switch
- **FileUpload**: File selection and upload

### Feedback Components
- **Alert**: Contextual messages
- **Flashbar**: Temporary notifications
- **Modal**: Dialog overlays
- **Popover**: Contextual information
- **HelpPanel**: Contextual help content

### Action Components
- **Button**: Primary actions
- **ButtonDropdown**: Actions with options
- **Icon**: Visual indicators
- **ExpandableSection**: Collapsible content

## Design Patterns

### Pattern 1: Data Tables
```typescript
import { Table, Header, Pagination } from '@cloudscape-design/components';

<Table
  columnDefinitions={[
    {
      id: 'name',
      header: 'Name',
      cell: item => item.name,
      sortingField: 'name'
    },
    {
      id: 'status',
      header: 'Status',
      cell: item => <StatusIndicator type={item.status}>{item.statusText}</StatusIndicator>
    }
  ]}
  items={items}
  loadingText="Loading resources"
  sortingDisabled={false}
  empty={
    <Box textAlign="center" color="inherit">
      <b>No resources</b>
      <Box padding={{ bottom: 's' }} variant="p" color="inherit">
        No resources to display.
      </Box>
    </Box>
  }
  header={
    <Header
      counter={`(${items.length})`}
      actions={
        <Button variant="primary">Create resource</Button>
      }
    >
      Resources
    </Header>
  }
  pagination={<Pagination currentPageIndex={1} pagesCount={10} />}
/>
```

### Pattern 2: Forms
```typescript
import { Form, FormField, Input, SpaceBetween, Button } from '@cloudscape-design/components';

<Form
  actions={
    <SpaceBetween direction="horizontal" size="xs">
      <Button variant="link">Cancel</Button>
      <Button variant="primary">Submit</Button>
    </SpaceBetween>
  }
>
  <SpaceBetween size="l">
    <FormField
      label="Name"
      description="Enter a unique name"
      constraintText="Use only letters, numbers, and hyphens"
    >
      <Input value={name} onChange={({ detail }) => setName(detail.value)} />
    </FormField>
    
    <FormField
      label="Description"
      description="Optional description"
    >
      <Textarea value={description} onChange={({ detail }) => setDescription(detail.value)} />
    </FormField>
  </SpaceBetween>
</Form>
```

### Pattern 3: AppLayout
```typescript
import { AppLayout, SideNavigation, BreadcrumbGroup } from '@cloudscape-design/components';

<AppLayout
  navigation={
    <SideNavigation
      activeHref="/dashboard"
      items={[
        { type: 'link', text: 'Dashboard', href: '/dashboard' },
        { type: 'link', text: 'Resources', href: '/resources' },
        { type: 'divider' },
        { type: 'link', text: 'Settings', href: '/settings' }
      ]}
    />
  }
  breadcrumbs={
    <BreadcrumbGroup
      items={[
        { text: 'Home', href: '/' },
        { text: 'Dashboard', href: '/dashboard' }
      ]}
    />
  }
  content={
    <Container header={<Header variant="h1">Dashboard</Header>}>
      {/* Your content here */}
    </Container>
  }
  tools={
    <HelpPanel header={<h2>Help</h2>}>
      Contextual help content
    </HelpPanel>
  }
/>
```

### Pattern 4: Wizards
```typescript
import { Wizard } from '@cloudscape-design/components';

<Wizard
  steps={[
    {
      title: 'Basic information',
      content: <BasicInfoStep />
    },
    {
      title: 'Configuration',
      content: <ConfigStep />
    },
    {
      title: 'Review',
      content: <ReviewStep />
    }
  ]}
  activeStepIndex={activeStep}
  onNavigate={({ detail }) => setActiveStep(detail.requestedStepIndex)}
  onSubmit={handleSubmit}
/>
```

## Best Practices

### Component Usage
1. **Use semantic HTML**: Cloudscape components render semantic HTML
2. **Leverage built-in features**: Use component props instead of custom implementations
3. **Follow composition patterns**: Nest components as documented
4. **Use TypeScript**: Take advantage of type definitions
5. **Implement error boundaries**: Handle component errors gracefully

### Accessibility
1. **Provide labels**: All form inputs must have labels
2. **Use ARIA attributes**: Leverage built-in ARIA support
3. **Test keyboard navigation**: Ensure all interactions work via keyboard
4. **Support screen readers**: Test with screen reader software
5. **Maintain focus management**: Handle focus appropriately in modals and dynamic content

### Performance
1. **Virtualize large lists**: Use Table's virtualization for large datasets
2. **Implement pagination**: Don't render thousands of items at once
3. **Lazy load content**: Load data as needed
4. **Optimize re-renders**: Use React.memo and useMemo appropriately
5. **Code split**: Lazy load routes and heavy components

### State Management
1. **Controlled components**: Manage form state explicitly
2. **Validation**: Implement client-side validation
3. **Error handling**: Display clear error messages
4. **Loading states**: Show loading indicators during async operations
5. **Optimistic updates**: Update UI before server confirmation when appropriate

## Visual Foundation

### Colors
- Use Cloudscape design tokens for colors
- Support both light and dark modes
- Maintain sufficient contrast ratios
- Use semantic color names (e.g., `colorTextStatusError`)

### Typography
- Use Cloudscape typography scale
- Maintain consistent heading hierarchy
- Use appropriate font weights
- Ensure readable line heights

### Spacing
- Use Cloudscape spacing tokens
- Maintain consistent spacing patterns
- Use SpaceBetween for element spacing
- Follow 8px grid system

## Common Patterns

### Error Handling
```typescript
<Alert
  type="error"
  dismissible
  onDismiss={() => setError(null)}
>
  {error.message}
</Alert>
```

### Confirmation Dialogs
```typescript
<Modal
  visible={showConfirm}
  onDismiss={() => setShowConfirm(false)}
  header="Confirm deletion"
  footer={
    <Box float="right">
      <SpaceBetween direction="horizontal" size="xs">
        <Button variant="link" onClick={() => setShowConfirm(false)}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleDelete}>
          Delete
        </Button>
      </SpaceBetween>
    </Box>
  }
>
  Are you sure you want to delete this resource?
</Modal>
```

### Help Panels
```typescript
<HelpPanel
  header={<h2>Resource details</h2>}
  footer={
    <div>
      <h3>Learn more</h3>
      <ul>
        <li><Link external href="#">Documentation</Link></li>
        <li><Link external href="#">API Reference</Link></li>
      </ul>
    </div>
  }
>
  <p>Detailed help content about the current page or feature.</p>
</HelpPanel>
```

## Testing

### Unit Testing
```typescript
import { render, screen } from '@testing-library/react';
import { Button } from '@cloudscape-design/components';

test('renders button with text', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

### Accessibility Testing
```typescript
import { axe } from 'jest-axe';

test('has no accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Migration Guides

### From Material-UI
- Replace `<Paper>` with `<Container>`
- Replace `<TextField>` with `<FormField>` + `<Input>`
- Replace `<Button>` with Cloudscape `<Button>` (similar API)
- Replace `<Table>` with Cloudscape `<Table>` (more features)
- Replace `<Dialog>` with `<Modal>`

### From Bootstrap
- Replace `.container` with `<Container>`
- Replace `.row` and `.col` with `<Grid>` and `<ColumnLayout>`
- Replace `.btn` with `<Button>`
- Replace `.alert` with `<Alert>`
- Replace `.modal` with `<Modal>`

## Code Generation Guidelines

When generating code with Cloudscape:

1. **Always import from @cloudscape-design/components**
2. **Use TypeScript for type safety**
3. **Include proper error handling**
4. **Implement loading states**
5. **Add accessibility attributes**
6. **Follow AWS naming conventions**
7. **Use semantic component composition**
8. **Implement responsive layouts**
9. **Add help content where appropriate**
10. **Test keyboard navigation**

## Anti-Patterns to Avoid

❌ **Don't**:
- Mix Cloudscape with other design systems
- Override Cloudscape styles extensively
- Ignore accessibility features
- Create custom components when Cloudscape provides them
- Use inline styles instead of design tokens
- Forget to handle loading and error states
- Ignore responsive design
- Skip keyboard navigation testing

✅ **Do**:
- Use Cloudscape components exclusively
- Leverage design tokens for customization
- Implement full accessibility support
- Use built-in component features
- Follow Cloudscape patterns
- Handle all interaction states
- Test on multiple screen sizes
- Ensure keyboard accessibility

## Resources

- **Official Documentation**: https://cloudscape.design/
- **Component Gallery**: https://cloudscape.design/components/
- **Design Guidelines**: https://cloudscape.design/foundation/
- **GitHub Repository**: https://github.com/cloudscape-design/components
- **Figma Design Kit**: Available through AWS internal resources

## Support

For questions and issues:
- Check official documentation first
- Review component examples
- Search GitHub issues
- Consult AWS internal Cloudscape channels
- Review accessibility guidelines

---

**Remember**: Cloudscape is optimized for AWS console experiences. When building AWS-related applications, always prefer Cloudscape over generic design systems for consistency, accessibility, and AWS-specific patterns.
