/* global jest, describe, test, expect, beforeEach, afterEach */
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useDispatch, useSelector } from 'react-redux';
import { act } from 'react-dom/test-utils';
import ConfigureTarget from './ConfigureTarget';

jest.mock('react-redux', () => ({
	useDispatch: jest.fn(),
	useSelector: jest.fn(), // Mock useSelector
}));

// Mock the dispatch function
const mockDispatch = jest.fn();

describe('ConfigureTarget component', () => {
	beforeEach(() => {
		// Mock the useDispatch hook to return the mockDispatch function
		useDispatch.mockReturnValue(mockDispatch);
		useSelector.mockReturnValue({ hosts: { hosts: '' } }); // Mock useSelector
	});

	afterEach(() => {
		jest.clearAllMocks();
	});

	test('renders the component', async () => {
		render(<ConfigureTarget />);
		await waitFor(() => {
			// Look for the header text once the component is ready
			const header = screen.getByText('Configure Target');
			expect(header).toBeInTheDocument();
		});
	});

	test('displays loading backdrop when RSA key is not fetched yet', () => {
		render(<ConfigureTarget />);

		const loadingBackdrop = screen.getByTestId('loading-backdrop');
		expect(loadingBackdrop).toBeInTheDocument();
	});

	test('fetches the RSA key, handles input changes and button click', async () => {
		// Mock the fetch function to return the RSA key
		const mockRsaKey =
			'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAspgMUpVAX1MfBUnqG50m\nVdCdzPbf/yauINkSfCkQMLTLw6827FbCj0nTNnscYpoaovlGkt01AuwlRwQgdMee\nr3y2kaSwuJbMPqTOMss0OmRjGioQVgo2TDDATiB8nmhiLiZaO1MIP2NM1+dDbRm2\nCdqyPJ8zHBNR4F5yVrGA8fEbUk1NG9bWEt1fQqMuf3NpC2RZJDFA+ETE41fisz5R\n45mMtmIak1Swz7DQx2cTVUDw785YCKq6tVn8HKh2FC0F7Dfs5d4xLL5UlpQquFkJ\nxA3nP1ml+gPhTjhSzyhbyUuKprmWQb3+9ydBHTvVCnHcsnNFeA9H/9BdRCyXmG2Z\newIDAQAB\n-----END PUBLIC KEY-----\n'; // Replace with the actual RSA key
		const mockFetchResponse = {
			json: jest.fn().mockResolvedValue({ public_key: mockRsaKey }),
		};
		const mockConfigResponse = {
			json: jest
				.fn()
				.mockResolvedValue({ detail: 'Configured target machines' }),
		};
		global.fetch = jest
			.fn()
			.mockResolvedValueOnce(mockFetchResponse)
			.mockResolvedValueOnce(mockConfigResponse);

		render(<ConfigureTarget />);

		await waitFor(() => {
			expect(fetch).toHaveBeenCalledWith(
				`${process.env.REACT_APP_API_URL}/public_key`
			);
			const usernameInput = screen.getByLabelText('Username *');
			const passwordInput = screen.getByLabelText('Password *');
			const hostsInput = screen.getByLabelText('Hosts *');
			const configureButton = screen.getByText('Configure');
			act(() => {
				userEvent.type(usernameInput, 'testUser');
				userEvent.type(passwordInput, 'testPassword');
				userEvent.type(hostsInput, 'host1,host2');

				fireEvent.click(configureButton);
			});
			expect(fetch).toHaveBeenCalledWith(
				`${process.env.REACT_APP_API_URL}/target/configure`,
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
					},
					body: expect.stringMatching(
						/^\{"user":"[A-Za-z0-9+/=]+","password":"[A-Za-z0-9+/=]+","hosts":"[A-Za-z0-9+/=]+"\}$/
					),
				}
			);
			// check if the snackbar is rendered
			const snackbar = screen.getByTestId('snackbar');
			expect(snackbar).toBeInTheDocument();

			// check if the severity is error
			const alert = screen.getByRole('alert');
			expect(alert).toHaveClass('MuiAlert-standardError');

			// check if the snackbar message is correct
			expect(snackbar).toHaveTextContent('Error:');

			// check if the dispatch function was called with the correct action
			expect(mockDispatch).toHaveBeenCalledTimes(1);
		});
	});

	// test('fetches RSA key, encrypts data, and sends the data to the live server', async () => {
	//     render(<ConfigureTarget />);

	//     // Wait for the RSA key to be fetched and set
	//     await waitFor(() => {
	//         expect(fetch).toHaveBeenCalledWith(`${process.env.REACT_APP_API_URL}/public_key`);
	//     });

	//     await waitFor(() => {
	//         const usernameInput = screen.getByLabelText('Username *');
	//         const passwordInput = screen.getByLabelText('Password *');
	//         const hostsInput = screen.getByLabelText('Hosts *');
	//         const configureButton = screen.getByText('Configure');

	//         // Type values into the input fields
	//         userEvent.type(usernameInput, 'testUser');
	//         userEvent.type(passwordInput, 'testPassword');
	//         userEvent.type(hostsInput, 'host1,host2');

	//         // Click the configure button
	//         fireEvent.click(configureButton);
	//     });
	//     // Wait for the loading spinner to disappear
	//     await waitFor(() => {
	//         const loadingBackdrop = screen.queryByTestId('loading-backdrop');
	//         expect(loadingBackdrop).toBeNull();
	//     });

	//     const snackbar = screen.getByTestId('snackbar');
	//     expect(snackbar).toBeInTheDocument();

	//         // check if the severity is error
	//         const alert = screen.getByRole('alert');
	//         expect(alert).toHaveClass('MuiAlert-standardError');

	//         // check if the snackbar message is correct
	//         expect(snackbar).toHaveTextContent('Error:');

	//         // check if the dispatch function was called with the correct action
	//         expect(mockDispatch).toHaveBeenCalledTimes(1);
	// });
});
