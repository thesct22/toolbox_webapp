import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import ConfigureTarget from './ConfigureTarget';

// Mock the fetch function to simulate API calls
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () =>
      Promise.resolve({
        public_key: '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAspgMUpVAX1MfBUnqG50m\nVdCdzPbf/yauINkSfCkQMLTLw6827FbCj0nTNnscYpoaovlGkt01AuwlRwQgdMee\nr3y2kaSwuJbMPqTOMss0OmRjGioQVgo2TDDATiB8nmhiLiZaO1MIP2NM1+dDbRm2\nCdqyPJ8zHBNR4F5yVrGA8fEbUk1NG9bWEt1fQqMuf3NpC2RZJDFA+ETE41fisz5R\n45mMtmIak1Swz7DQx2cTVUDw785YCKq6tVn8HKh2FC0F7Dfs5d4xLL5UlpQquFkJ\nxA3nP1ml+gPhTjhSzyhbyUuKprmWQb3+9ydBHTvVCnHcsnNFeA9H/9BdRCyXmG2Z\newIDAQAB\n-----END PUBLIC KEY-----\n',
      }),
    ok: true,
  })
);

test('renders the ConfigureTarget component', () => {
  const { getByLabelText, getByText } = render(<ConfigureTarget />);
  
  // Check if important elements are rendered
  const usernameInput = getByLabelText('Username');
  const passwordInput = getByLabelText('Password');
  const hostsInput = getByLabelText('Hostnames/IP Addresses');
  const configureButton = getByText('Configure');

  expect(usernameInput).toBeInTheDocument();
  expect(passwordInput).toBeInTheDocument();
  expect(hostsInput).toBeInTheDocument();
  expect(configureButton).toBeInTheDocument();
});

// test('submits form data when Configure button is clicked', async () => {
//   const { getByLabelText, getByText } = render(<ConfigureTarget />);
  
//   const usernameInput = getByLabelText('Username');
//   const passwordInput = getByLabelText('Password');
//   const hostsInput = getByLabelText('Hostnames/IP Addresses');
//   const configureButton = getByText('Configure');

//   // Fill in form fields
//   fireEvent.change(usernameInput, { target: { value: 'testUser' } });
//   fireEvent.change(passwordInput, { target: { value: 'testPassword' } });
//   fireEvent.change(hostsInput, { target: { value: 'host1, host2' } });

//   // Mock the fetch function to simulate a successful API response
//   global.fetch.mockResolvedValueOnce({
//     json: () => Promise.resolve({}),
//     ok: true,
//   });

//   // Trigger the form submission
//   fireEvent.click(configureButton);

//   // Wait for the success message to appear
//   await waitFor(() => {
//     const successMessage = getByText('Target(s) configured successfully');
//     expect(successMessage).toBeInTheDocument();
//   });
// });
