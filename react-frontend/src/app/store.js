import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: {
    currentPage: (state = { currentPage: "Home" }, action) => {
      switch (action.type) {
        case "currentPage/setCurrentPage":
          return { currentPage: action.payload };
        default:
          return state;
      }
    },
    currentPageIcon: (state = { currentPageIcon: "home" }, action) => {
      switch (action.type) {
        case "currentPageIcon/setCurrentPageIcon":
          return { currentPageIcon: action.payload };
        default:
          return state;
      }
    },
    tags: (state = { tags: [] }, action) => {
      switch (action.type) {
        case "tags/setTags":
          return { tags: action.payload };
        default:
          return state;
      }
    },
  },
});
