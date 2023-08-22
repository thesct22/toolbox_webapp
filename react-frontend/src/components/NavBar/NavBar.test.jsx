/* global jest, describe, test, expect, beforeEach */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import NavBar from './NavBar';

// Mocking useSelector and useNavigate
jest.mock('react-redux', () => ({
	useSelector: jest.fn(),
}));

jest.mock('react-router-dom', () => ({
	...jest.requireActual('react-router-dom'),
	useNavigate: jest.fn(),
}));

describe('NavBar', () => {
	beforeEach(() => {
		useSelector.mockReturnValue({ currentPage: 'Home' });
		useNavigate.mockReturnValue(jest.fn()); // Mock the navigate function
	});

	test('renders correctly with window width < 1080', () => {
		global.innerWidth = 1079; // Simulate a small window width

		render(<NavBar />);

		// Test if the current page is rendered
		expect(screen.getByText('Home')).toBeInTheDocument();

		// Test if small window width renders the correct buttons
		expect(screen.queryByText('Installer')).not.toBeInTheDocument();
		expect(screen.queryByText('Custom Playbook')).not.toBeInTheDocument();
		expect(screen.queryByText('Configure Target')).not.toBeInTheDocument();
		expect(screen.queryByText('Code Editor')).not.toBeInTheDocument();
		expect(screen.queryByText('Terminal')).not.toBeInTheDocument();
		expect(screen.queryByText('Instructions')).not.toBeInTheDocument();

		// Test if the "Installer" button is rendered as a Button component
		expect(
			screen.getByRole('button', { name: 'Installer' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Custom Playbook' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Configure Target' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Code Editor' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Terminal' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Instructions' })
		).toBeInTheDocument();

		// Test if the "Installer" button is rendered
		expect(screen.getByLabelText('Installer')).toBeInTheDocument();
		expect(screen.getByLabelText('Custom Playbook')).toBeInTheDocument();
		expect(screen.getByLabelText('Configure Target')).toBeInTheDocument();
		expect(screen.getByLabelText('Code Editor')).toBeInTheDocument();
		expect(screen.getByLabelText('Terminal')).toBeInTheDocument();
		expect(screen.getByLabelText('Instructions')).toBeInTheDocument();
	});

	test('renders correctly with window width >= 1080', () => {
		global.innerWidth = 1200; // Simulate a larger window width

		render(<NavBar />);

		// Test if the current page is rendered
		expect(screen.getByText('Home')).toBeInTheDocument();

		// Test if large window width renders the correct buttons
		expect(screen.queryByText('Installer')).toBeInTheDocument();
		expect(screen.queryByText('Custom Playbook')).toBeInTheDocument();
		expect(screen.queryByText('Configure Target')).toBeInTheDocument();
		expect(screen.queryByText('Code Editor')).toBeInTheDocument();
		expect(screen.queryByText('Terminal')).toBeInTheDocument();
		expect(screen.queryByText('Instructions')).toBeInTheDocument();

		// Test if the "Installer" button is rendered as a Button component
		expect(
			screen.getByRole('button', { name: 'Installer' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Custom Playbook' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Configure Target' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Code Editor' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Terminal' })
		).toBeInTheDocument();
		expect(
			screen.getByRole('button', { name: 'Instructions' })
		).toBeInTheDocument();

		// Test if the "Installer" button is rendered
		expect(screen.getByLabelText('Installer')).toBeInTheDocument();
		expect(screen.getByLabelText('Custom Playbook')).toBeInTheDocument();
		expect(screen.getByLabelText('Configure Target')).toBeInTheDocument();
		expect(screen.getByLabelText('Code Editor')).toBeInTheDocument();
		expect(screen.getByLabelText('Terminal')).toBeInTheDocument();
		expect(screen.getByLabelText('Instructions')).toBeInTheDocument();
	});
});
