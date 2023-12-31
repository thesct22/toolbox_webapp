/* eslint-disable default-param-last */
import { configureStore } from '@reduxjs/toolkit';

const store = configureStore({
	reducer: {
		currentPage: (state = { currentPage: 'Home' }, action) => {
			switch (action.type) {
				case 'currentPage/setCurrentPage':
					return { currentPage: action.payload };
				default:
					return state;
			}
		},
		currentPageIcon: (state = { currentPageIcon: 'home' }, action) => {
			switch (action.type) {
				case 'currentPageIcon/setCurrentPageIcon':
					return { currentPageIcon: action.payload };
				default:
					return state;
			}
		},
		tags: (state = { tags: [] }, action) => {
			switch (action.type) {
				case 'tags/setTags':
					return { tags: action.payload };
				default:
					return state;
			}
		},
		selectedTags: (state = { selectedTags: [] }, action) => {
			switch (action.type) {
				case 'selectedTags/setSelectedTags':
					return { selectedTags: action.payload };
				default:
					return state;
			}
		},
		hosts: (state = { hosts: '' }, action) => {
			switch (action.type) {
				case 'hosts/setHosts':
					return { hosts: action.payload };
				default:
					return state;
			}
		},
		os: (state = { os: '' }, action) => {
			switch (action.type) {
				case 'os/setOS':
					return { os: action.payload };
				default:
					return state;
			}
		},
		fileList: (state = { fileList: [] }, action) => {
			switch (action.type) {
				case 'fileList/setFileList':
					return { fileList: action.payload };
				default:
					return state;
			}
		},
		selectedFile: (state = { selectedFile: '' }, action) => {
			switch (action.type) {
				case 'selectedFile/setSelectedFile':
					return { selectedFile: action.payload };
				default:
					return state;
			}
		},
		fileContent: (state = { fileContent: '' }, action) => {
			switch (action.type) {
				case 'fileContent/setFileContent':
					return { fileContent: action.payload };
				default:
					return state;
			}
		},
		language: (state = { language: 'yaml' }, action) => {
			switch (action.type) {
				case 'language/setLanguage':
					return { language: action.payload };
				default:
					return state;
			}
		},
		playbook: (state = { playbook: '' }, action) => {
			switch (action.type) {
				case 'playbook/setPlaybook':
					return { playbook: action.payload };
				default:
					return state;
			}
		},
		inventory: (state = { inventory: '' }, action) => {
			switch (action.type) {
				case 'inventory/setInventory':
					return { inventory: action.payload };
				default:
					return state;
			}
		},
	},
});

export default store;
