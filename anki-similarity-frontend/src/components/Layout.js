import React from "react";
import { Box } from "@mui/material";
import Sidebar from "./Sidebar";
import Header from "./Header";
import { Outlet } from "react-router-dom"; // Import Outlet

const Layout = () => {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      {/* Header */}
      <Header />

      {/* Main Content and Sidebar */}
      <Box sx={{ display: "flex", flexGrow: 1, marginTop: "64px" }}>
        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            marginLeft: "240px", // Adjust margin to match Sidebar width
            padding: "12px", // Add padding for better spacing
            overflowY: "auto", // Allow scrolling for main content
          }}
        >
          <Outlet /> {/* Render child routes here */}
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;
