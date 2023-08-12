import React, { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';

export default function Terminal() {
	const dispatch = useDispatch();
	const [navbarHeight, setNavbarHeight] = useState(0);
	const [height, setHeight] = useState(window.innerHeight - navbarHeight);

	// Function to calculate the height of the terminal iframe based on navbarHeight
	const calcHeight = (navbarHeightParam) =>
		window.innerHeight - navbarHeightParam;

	useEffect(() => {
		dispatch({ type: 'currentPage/setCurrentPage', payload: 'Terminal' });

		// Update the navbarHeight state when it becomes available
		const navbarElement = document.getElementById('navbar');
		if (navbarElement) {
			setNavbarHeight(navbarElement.clientHeight);
		}

		// Update the iframe height based on navbarHeight
		setHeight(calcHeight(navbarHeight));

		// Add the resize event listener to update iframe height when window resizes
		const handleResize = () => {
			if (navbarElement) {
				setNavbarHeight(navbarElement.clientHeight);
				setHeight(calcHeight(navbarElement.clientHeight));
			}
		};
		window.addEventListener('resize', handleResize);

		// Cleanup: Remove the resize event listener when the component unmounts
		return () => {
			window.removeEventListener('resize', handleResize);
		};
	}, [navbarHeight]); // Run this effect whenever navbarHeight changes

	return (
		<div style={{ height, padding: 0 }}>
			<iframe
				src="http://localhost:8765"
				title="Terminal"
				style={{ width: '100%', height }}
			/>
		</div>
	);
}
