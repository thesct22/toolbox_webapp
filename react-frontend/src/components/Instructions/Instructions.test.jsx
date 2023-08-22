/* global jest, describe, test, expect, beforeEach, afterEach */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { useDispatch } from 'react-redux';
import Instructions from './Instructions';

jest.mock('react-redux', () => ({
	useDispatch: jest.fn(),
}));

// Mock the dispatch function
const mockDispatch = jest.fn();

describe('Instructions component', () => {
	beforeEach(() => {
		// Mock the useDispatch hook to return the mockDispatch function
		useDispatch.mockReturnValue(mockDispatch);
	});
	afterEach(() => {
		jest.clearAllMocks();
	});

	test('renders all section headings', () => {
		render(<Instructions />);

		// Check if all section headings are present
		const headings = screen.getAllByRole('heading', { level: 2 });
		const expectedHeadings = [
			/Navigation bar/i,
			/Installer Page/i,
			/Custom Playbook Page/i,
			/Configure Target Page/i,
			/Code Editor Page/i,
			/Terminal page/i,
		];

		expectedHeadings.forEach((headingText, index) => {
			expect(headings[index]).toHaveTextContent(headingText);
		});
	});

	test('renders all images', () => {
		render(<Instructions />);

		// Check if all images are present
		const images = screen.getAllByRole('img');
		expect(images).toHaveLength(6);
	});

	test('renders all list items', () => {
		render(<Instructions />);

		const expectedListItems = [
			/Installer Page .* quick configuration/i,
			/Custom Playbook Page .* construct the commands/i,
			/Configure Target Page .* configure the target machines/i,
			/Code Editor Page .* edit the files/i,
			/Terminal page .* bash shell inside the container/i,
		];

		const listItems = screen.getAllByRole('listitem');

		expectedListItems.forEach((listItemText, index) => {
			expect(listItems[index]).toHaveTextContent(listItemText);
		});
	});

	test('dispatches the correct action on mount', () => {
		render(<Instructions />);

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledWith({
			type: 'currentPage/setCurrentPage',
			payload: 'Instructions',
		});
	});

	test('dispatches the correct action on window resize', () => {
		render(<Instructions />);

		// Resize the window
		global.innerWidth = 1200;
		global.dispatchEvent(new Event('resize'));

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledWith({
			type: 'currentPage/setCurrentPage',
			payload: 'Instructions',
		});
	});

	test('removes the resize event listener on unmount', () => {
		const { unmount } = render(<Instructions />);

		// Resize the window
		global.innerWidth = 1200;
		global.dispatchEvent(new Event('resize'));

		// Check if the dispatch function was called with the correct action
		expect(mockDispatch).toHaveBeenCalledWith({
			type: 'currentPage/setCurrentPage',
			payload: 'Instructions',
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
