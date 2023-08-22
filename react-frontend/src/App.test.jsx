/* global test, expect, jest */
import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import store from './app/store';
import App from './App';

// Mock react-router-dom
jest.mock('react-router-dom');

test('renders learn react link', () => {
	const { getByText } = render(
		<Provider store={store}>
			<App />
		</Provider>
	);

	// Your test assertions here
	expect(getByText(/Home/i)).toBeInTheDocument();
});
