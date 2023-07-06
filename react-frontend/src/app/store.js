import { configureStore } from '@reduxjs/toolkit';

const store = configureStore({
	reducer: {
		currentPage: (action, state = { currentPage: 'Home' }) => {
			switch (action.type) {
				case 'currentPage/setCurrentPage':
					return { currentPage: action.payload };
				default:
					return state;
			}
		},
		currentPageIcon: (action, state = { currentPageIcon: 'home' }) => {
			switch (action.type) {
				case 'currentPageIcon/setCurrentPageIcon':
					return { currentPageIcon: action.payload };
				default:
					return state;
			}
		},
		tags: (action, state = { tags: [] }) => {
			switch (action.type) {
				case 'tags/setTags':
					return { tags: action.payload };
				default:
					return state;
			}
		},
		selectedTags: (action, state = { selectedTags: [] }) => {
			switch (action.type) {
				case 'selectedTags/setSelectedTags':
					return { selectedTags: action.payload };
				default:
					return state;
			}
		},
		hosts: (action, state = { hosts: '' }) => {
			switch (action.type) {
				case 'hosts/setHosts':
					return { hosts: action.payload };
				default:
					return state;
			}
		},
		fileList: (action, state = { fileList: [] }) => {
			switch (action.type) {
				case 'fileList/setFileList':
					return { fileList: action.payload };
				default:
					return state;
			}
		},
		selectedFile: (action, state = { selectedFile: '' }) => {
			switch (action.type) {
				case 'selectedFile/setSelectedFile':
					return { selectedFile: action.payload };
				default:
					return state;
			}
		},
		fileContent: (action, state = { fileContent: '' }) => {
			switch (action.type) {
				case 'fileContent/setFileContent':
					return { fileContent: action.payload };
				default:
					return state;
			}
		},
	},
});

export default store;
