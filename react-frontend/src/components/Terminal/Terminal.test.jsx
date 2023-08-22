/* globals jest, describe, test, expect, beforeEach, afterEach */
// Terminal.test.jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { useDispatch } from 'react-redux';
import Terminal from './Terminal';

// Mock the useDispatch function from react-redux
jest.mock('react-redux', () => ({
	useDispatch: jest.fn(),
}));

// Mock the dispatch function
const mockDispatch = jest.fn();

describe('Terminal component', () => {
	beforeEach(() => {
		// Mock the useDispatch hook to return the mockDispatch function
		useDispatch.mockReturnValue(mockDispatch);
	});

	afterEach(() => {
		jest.clearAllMocks();
	});

	test('renders the iframe with the correct URL', () => {
		render(<Terminal />);

		// Check if the iframe has the correct src attribute
		const iframe = screen.getByTitle('Terminal');
		expect(iframe).toHaveAttribute('src', 'http://localhost:8765');
	});

	test('dispatches the correct action on mount', () => {
		render(<Terminal />);

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledWith({
			type: 'currentPage/setCurrentPage',
			payload: 'Terminal',
		});
	});

	test('dispatches the correct action on window resize', () => {
		render(<Terminal />);

		// Resize the window
		global.innerWidth = 1200;
		global.dispatchEvent(new Event('resize'));

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledWith({
			type: 'currentPage/setCurrentPage',
			payload: 'Terminal',
		});
	});

	test('removes the resize event listener on unmount', () => {
		const { unmount } = render(<Terminal />);

		// Resize the window
		global.innerWidth = 1200;
		global.dispatchEvent(new Event('resize'));

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledWith({
			type: 'currentPage/setCurrentPage',
			payload: 'Terminal',
		});

		// Unmount the component
		unmount();

		// Resize the window again
		global.innerWidth = 1079;
		global.dispatchEvent(new Event('resize'));

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledTimes(1);
	});
});
