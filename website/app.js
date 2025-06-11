const { useState } = React;
const { ReactFlow, MiniMap, Controls, Background } = window.ReactFlow;

function Flow() {
  const nodes = [
    { id: '1', position: { x: 0, y: 50 }, data: { label: 'User' }, type: 'input' },
    { id: '2', position: { x: 250, y: 50 }, data: { label: 'Fremen Agent' } },
  ];
  const edges = [{ id: 'e1-2', source: '1', target: '2', animated: true }];
  return React.createElement(ReactFlow, { nodes, edges, fitView: true, style: { height: 150, background: '#ECEADF' } },
    React.createElement(MiniMap, null),
    React.createElement(Controls, null),
    React.createElement(Background, null)
  );
}

function App() {
  return React.createElement('div', { className: 'container' },
    React.createElement('section', { id: 'main' },
      React.createElement('h1', null, 'Fremen.AI'),
      React.createElement('p', null, 'The Smartest Desktop, Web and Mobile Agent on the Market'),
      React.createElement('p', null, 'Local first, enterprise ready.'),
      React.createElement('p', null, 'See. Learn. Automate. All on your machine'),
      React.createElement('p', null, 'The most reliable desktop and web AI Agent.'),
      React.createElement('p', null, 'Fremen is revolutionizing the way businesses operate by harnessing powerful desktop and web agents to eliminate repetitive tasks. With no coding required, our agent automation solutions empower users to streamline workflows, effortlessly handle browsers, and execute complex online and desktop interactions.'),
      React.createElement('p', null, 'By using the latest AI techniques and models Fremen delivers unparalleled efficiency and reliability. Our robust platform provides comprehensive automation capabilities, including visual understanding, precise HTML extraction, and self-correcting actions to ensure consistent and accurate task execution.'),
      React.createElement('p', null, 'Whether you need to extract data, perform research, or manage complex processes, Fremen\u2019s agent makes automation accessible and straightforward. Enjoy unmatched performance and security, supported by powerful bot protection, mobile proxies, and a fully hosted infrastructure.'),
      React.createElement('p', null, 'Trusted by leading enterprises, Fremen combines cutting-edge AI with human-in-the-loop oversight, ensuring automation that\u2019s not only powerful but also reliable and secure. Join the automation revolution today and transform your workflow with Fremen.'),
      React.createElement('button', null, 'Let us automate your processes')
    ),
    React.createElement('section', { id: 'customer' },
      React.createElement('h2', null, 'Become a customer'),
      React.createElement('button', null, 'Become a customer'),
      React.createElement('div', { className: 'demo-box' },
        React.createElement('form', null,
          React.createElement('label', null, 'Request a demo: '),
          React.createElement('input', { type: 'email', placeholder: 'your email', required: true }),
          React.createElement('input', { type: 'submit', value: 'Submit' })
        )
      )
    ),
    React.createElement('section', { id: 'tech' },
      React.createElement('h2', null, 'Technologies'),
      React.createElement('p', null, 'We use the latest technologies n8n, langchain and langflow in addition to the latest reinforcement learning techniques like GRPO to automate your work.'),
      React.createElement(Flow, null)
    )
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
