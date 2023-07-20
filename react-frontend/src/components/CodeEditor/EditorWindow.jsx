import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Editor from '@monaco-editor/react'; // used by vscode, microsoft and github

export default function EditorWindow() {
	const dispatch = useDispatch();
	const fileContent = useSelector((state) => state.fileContent.fileContent);
	const language = useSelector((state) => state.language.language);

	return (
		<Editor
			height="80vh"
			defaultLanguage="yaml"
			language={language}
			value={fileContent}
			theme="vs-dark"
			options={{
				readOnly: false,
				minimap: {
					enabled: true,
				},
			}}
			onChange={(value) => {
				dispatch({
					type: 'fileContent/setFileContent',
					payload: value,
				});
			}}
		/>
	);
}
