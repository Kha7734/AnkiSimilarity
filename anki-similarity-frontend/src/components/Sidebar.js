import React from "react";
import { List, ListItem, ListItemText } from "@mui/material";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
      <div
          style={{
              width: "240px",
              position: "fixed",
              height: "calc(100vh - 64px)", // Adjust height to account for Header
              backgroundColor: "#f5f5f5",
              zIndex: 1000, // Ensure Sidebar is above other content
          }}
      >
          <List>
              <ListItem button component={Link} to="/dashboard">
                  <ListItemText primary="Dashboard"/>
              </ListItem>
              <ListItem button component={Link} to="/vocabulary">
                  <ListItemText primary="Vocabulary"/>
              </ListItem>
              <ListItem button component={Link} to="/datasets">
                  <ListItemText primary="Datasets"/>
              </ListItem>
              <ListItem button component={Link} to="/progress">
                  <ListItemText primary="Progress"/>
              </ListItem>
              <ListItem button component={Link} to="/settings">
                  <ListItemText primary="Settings"/>
              </ListItem>
          </List>
      </div>
  );
};

export default Sidebar;