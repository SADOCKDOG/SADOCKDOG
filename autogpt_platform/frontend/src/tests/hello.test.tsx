import { render, screen } from '@testing-library/react';
import React from 'react';

describe('Hello Vitest', () => {
  it('renders hello world', () => {
    render(<div>Hello world</div>);
    expect(screen.getByText('Hello world')).toBeInTheDocument();
  });
});
