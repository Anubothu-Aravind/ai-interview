import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

describe('App', () => {
  it('should render the app title', () => {
    render(<App />);
    const titleElement = screen.getByText(/AI Interview System/i);
    expect(titleElement).toBeInTheDocument();
  });

  it('should render system status section', () => {
    render(<App />);
    const statusElement = screen.getByText(/System Status/i);
    expect(statusElement).toBeInTheDocument();
  });

  it('should render how it works section', () => {
    render(<App />);
    const howItWorksElement = screen.getByText(/How It Works/i);
    expect(howItWorksElement).toBeInTheDocument();
  });
});
